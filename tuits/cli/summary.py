import os
import sqlite3
import sys
import warnings
from contextlib import contextmanager
from datetime import datetime, timedelta

import keyring
from openai import OpenAI

from tuits.data.db import get_db_path

SERVICE_NAME = "tuits"
KEY_NAME = "openai_api_key"


def _load_from_keyring():
    return keyring.get_password(SERVICE_NAME, KEY_NAME)


def _save_to_keyring(api_key):
    keyring.set_password(SERVICE_NAME, KEY_NAME, api_key)
    return True

def _load_llama_model():
    try:
        from llama_cpp import Llama  # type: ignore
    except Exception:
        return None, "llama-cpp-python is not installed."

    gguf_path = os.environ.get("TUIT_LLM_GGUF")
    if gguf_path:
        if not os.path.isfile(gguf_path):
            return None, f"GGUF model not found at {gguf_path}."
        return Llama(model_path=gguf_path, verbose=False), None

    repo_id = os.environ.get("TUIT_LLM_REPO", "bartowski/Llama-3.2-1B-Instruct-GGUF")
    gguf_file = os.environ.get(
        "TUIT_LLM_GGUF_FILE",
        "Llama-3.2-1B-Instruct-Q4_K_M.gguf",
    )

    try:
        try:
            from huggingface_hub import hf_hub_download  # type: ignore
            hf_hub_download(repo_id=repo_id, filename=gguf_file, local_files_only=True)
        except Exception:
            print("Downloading local model (first run may take a bit)...", file=sys.stderr)
        os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
        warnings.filterwarnings(
            "ignore",
            message="The `local_dir_use_symlinks` argument is deprecated",
            category=UserWarning,
        )
        with _suppress_stderr():
            return Llama.from_pretrained(repo_id=repo_id, filename=gguf_file, verbose=False), None
    except Exception as exc:
        return None, f"Failed to load model from {repo_id}: {exc}"


@contextmanager
def _suppress_stderr():
    with open(os.devnull, "w") as devnull:
        old_stderr = sys.stderr
        try:
            sys.stderr = devnull
            yield
        finally:
            sys.stderr = old_stderr

def _get_tasks_between(start_dt, end_dt):
    database_path = get_db_path()
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    start_str = start_dt.strftime("%Y-%m-%d %H:%M")
    end_str = end_dt.strftime("%Y-%m-%d %H:%M")
    query = (
        "SELECT job, message FROM tasks "
        "WHERE timestamp >= ? AND timestamp < ? "
        "ORDER BY timestamp DESC"
    )
    cursor.execute(query, (start_str, end_str))
    rows = cursor.fetchall()
    conn.close()

    tasks = []
    for job, message in rows:
        if job in {"Start", "Finish", "Break"}:
            continue
        tasks.append(f"{job}: {message}")
    return tasks

def _get_time_frame_window(time_frame, now):
    if time_frame == "day":
        start_range = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        end_range = start_range + timedelta(days=2)
    elif time_frame == "week":
        start_range = (now - timedelta(days=now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_range = start_range + timedelta(days=5)
    elif time_frame == "month":
        start_range = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if start_range.month == 12:
            end_range = start_range.replace(year=start_range.year + 1, month=1)
        else:
            end_range = start_range.replace(month=start_range.month + 1)
    else:
        raise ValueError(f"Unsupported time frame: '{time_frame}', Choose from: day, week, month")

    return start_range, end_range


def generate_summary(args):
    provider = os.environ.get("TUIT_LLM_PROVIDER", "llama").strip().lower()
    if provider not in {"llama", "openai"}:
        provider = "llama"

    client = None
    llama = None
    if provider == "llama":
        llama, llama_error = _load_llama_model()
        if llama is None:
            if llama_error:
                print(llama_error, file=sys.stderr)
            print("Set TUIT_LLM_PROVIDER=openai to use the hosted model.", file=sys.stderr)

    if llama is None:
        # Check if the API key is provided; if so, save it. Otherwise, attempt to load it.
        api_key = None
        if args.api_key:
            api_key = args.api_key
            try:
                _save_to_keyring(api_key)
            except Exception as exc:
                print(
                    f"Warning: failed to save API key in keyring ({exc}). "
                    "Set OPENAI_API_KEY to avoid re-entering your key."
                )

        if not api_key:
            api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            try:
                api_key = _load_from_keyring()
            except Exception as exc:
                print(
                    f"Warning: failed to read API key from keyring ({exc}). "
                    "Set OPENAI_API_KEY or provide --api_key <api_key>."
                )

        if not api_key:
            print("No API key found. Please set OPENAI_API_KEY or provide --api_key <api_key>.")
            return

        # Initialize the OpenAI client with the API key.
        client = OpenAI(api_key=api_key)
        model = "gpt-5-nano"

    now = datetime.now()
    start_range, end_range = _get_time_frame_window(args.time_frame, now)
    start_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_today = min(now, end_range)
    end_yesterday = min(start_today, end_range)
    if end_yesterday < start_range:
        end_yesterday = start_range

    yesterday_tasks = _get_tasks_between(start_range, end_yesterday)
    today_tasks = _get_tasks_between(start_today, end_today) if start_today < end_today else []

    yesterday_text = "\n".join(yesterday_tasks) if yesterday_tasks else "No logged tasks."
    today_text = "\n".join(today_tasks) if today_tasks else "No logged tasks."

    if args.time_frame == "day":
        prompt = (
            "Create a standup summary using only the tasks below. "
            "Use a clear two-part format with headings: Yesterday, Today. "
            "Yesterday means the previous calendar day; Today means tasks logged today so far. "
            "Do not infer or propose future work. "
            "Keep it concise, first person, and focused on outcomes and progress. "
            "Group related work into a single bullet where possible. "
            "Do not mention logging meta-items like Start/Finish/Break. \n\n"
            "Yesterday tasks:\n"
            f"{yesterday_text}\n\n"
            "Today tasks:\n"
            f"{today_text}"
        )
    elif args.time_frame == "week":
        week_tasks = _get_tasks_between(start_range, end_range)
        week_text = "\n".join(week_tasks) if week_tasks else "No logged tasks."
        prompt = (
            "Create a standup summary using only the tasks below. "
            "Use a short intro line starting with: \"This week I've been working on:\" "
            "Then provide 3-6 concise bullet points. "
            "Do not infer or propose future work. "
            "Keep it concise, first person, and focused on outcomes and progress. "
            "Group related work into a single bullet where possible. "
            "Do not mention logging meta-items like Start/Finish/Break. \n\n"
            "Week tasks:\n"
            f"{week_text}"
        )
    elif args.time_frame == "month":
        month_tasks = _get_tasks_between(start_range, end_range)
        month_text = "\n".join(month_tasks) if month_tasks else "No logged tasks."
        prompt = (
            "Create a standup summary using only the tasks below. "
            "Use a short intro line starting with: \"This month I've been working on:\" "
            "Then provide 4-8 concise bullet points. "
            "Do not infer or propose future work. "
            "Keep it concise, first person, and focused on outcomes and progress. "
            "Group related work into a single bullet where possible. "
            "Do not mention logging meta-items like Start/Finish/Break. \n\n"
            "Month tasks:\n"
            f"{month_text}"
        )
    else:
        raise ValueError(f"Unsupported time frame: '{args.time_frame}', Choose from: day, week, month")

    # Generate the summary by streaming the response.
    print("Summary for", args.time_frame, ":\n", end="", flush=True)
    if llama is not None:
        with _suppress_stderr():
            stream = llama.create_chat_completion(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                stream=True,
            )
            for event in stream:
                delta = event["choices"][0].get("delta", {})
                content = delta.get("content")
                if content:
                    print(content, end="", flush=True)
    else:
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            stream=True,
        )
        for event in stream:
            if not event.choices:
                continue
            delta = event.choices[0].delta
            content = getattr(delta, "content", None)
            if content:
                print(content, end="", flush=True)
    print()
