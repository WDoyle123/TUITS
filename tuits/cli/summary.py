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
            print("No API key found. Please provide an API key.")
            return

    client = OpenAI(api_key=api_key)

    tasks_text = get_tasks_text_for_time_frame(args.time_frame)

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"Summarize the following tasks so that I can let the team know what I have done in this {args.time_frame} in the daily meeting: {tasks_text}"}
    ])

    print("Summary for", args.time_frame, ":\n", response.choices[0].message.content)
