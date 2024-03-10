import argparse

from cli.log_task import log_task
from cli.show_tasks import show_tasks

from data.init_db import init_db

def main():
    
    init_db()

    parser = argparse.ArgumentParser(description="Tuits CLI")
    subparsers = parser.add_subparsers(help='commands')
    subparsers.required = True

    # Log commands
    log_parser = subparsers.add_parser('log', help='Log a new task')
    log_parser.add_argument('job', help='Job name or identifer')
    log_parser.add_argument('-m', '--message', required=False, default='', help='Message for the log entry')
    log_parser.set_defaults(func=log_task)

    # Show commands
    show_parser = subparsers.add_parser('show', help='Show logged tasks')
    show_parser.add_argument('show', help='day, week, month, year')
    show_parser.set_defaults(func=show_tasks)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
