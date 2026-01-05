from tuits.cli.utils import fetch_last_task, print_task_table


def show_last(args=None):
    task = fetch_last_task()
    if not task:
        print("No logs found.")
        return

    print_task_table([task], show_index=False)
