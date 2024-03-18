from openai import OpenAI
from tuits.cli.show_tasks import get_tasks_text_for_time_frame
import os

def save_api_key(api_key):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    key_file_path = os.path.join(base_dir, 'config', 'openai_key.txt')
    os.makedirs(os.path.dirname(key_file_path), exist_ok=True)
    with open(key_file_path, 'w') as key_file:
        key_file.write(api_key)

def load_api_key():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    key_file_path = os.path.join(base_dir, 'config', 'openai_key.txt')
    if os.path.exists(key_file_path):
        with open(key_file_path, 'r') as key_file:
            api_key = key_file.read().strip()
            return api_key
    return None

def generate_summary(args):
    # Check if the API key is provided; if so, save it. Otherwise, attempt to load it.
    if args.api_key:
        save_api_key(args.api_key)
        api_key = args.api_key
    else:
        api_key = load_api_key()
        if not api_key:
            print("No API key found. Please provide an API key. e.g., tuits summary day --api_key <api_key>")
            return

    # Initialize the OpenAI client with the API key.
    client = OpenAI(api_key=api_key)

    # Retrieve the tasks text for the specified time frame.
    tasks_text = get_tasks_text_for_time_frame(args.time_frame)

    prompt = (
        f"Using the tasks listed below, create a compelling and concise summary suitable for a {args.time_frame} type meeting. "
        "The summary should: \n"
        "- Highlight key accomplishments and progress made. \n"
        "- Identify any blockers or challenges faced. \n"
        "- Outline the next steps or tasks to focus on. \n"
        "- Be in first person and not use 'We' but only use 'I' \n"
        "- You SHOULD EXCLUDE jobs that are: 'Start' 'Finish' and 'Break' from the summary \n"
        "Please group related tasks together to provide a coherent narrative. \n\n"
        "Tasks: \n"
        f"{tasks_text}"
    )

    # Generate the summary by sending the prompt to the model.
    response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ])

    # Print the generated summary.
    print("Summary for", args.time_frame, ":\n", response.choices[0].message.content)

