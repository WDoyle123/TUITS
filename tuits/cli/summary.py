from openai import OpenAI
from tuits.cli.show_tasks import get_tasks_text_for_time_frame

def generate_summary(args):

    client = OpenAI(api_key=args.api_key)

    tasks_text = get_tasks_text_for_time_frame(args.time_frame)

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"Summarize the following tasks so that I can let the team know what I have done in this {args.time_frame} in the daily meeting: {tasks_text}"}
    ])

    print("Summary for", args.time_frame, ":\n", response.choices[0].message.content)

