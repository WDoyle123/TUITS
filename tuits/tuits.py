import argparse
from tuits.cli.log_task import log_task
from tuits.cli.show_tasks import show_tasks
from tuits.cli.start import start_day
from tuits.cli.finish import finish_day
from tuits.cli.backup import backup_tasks

from tuits.data.init_db import init_db

def main():
    
    init_db()

    parser = argparse.ArgumentParser(description="Tuits CLI")
    subparsers = parser.add_subparsers(help='commands')
    subparsers.required = True

    # Start command
    start_parser = subparsers.add_parser('start', help="Used to log the start of the workday")
    start_parser.set_defaults(func=start_day)

    # Finish command
    finish_parser = subparsers.add_parser('finish', help="Used to log the end of the workday")
    finish_parser.set_defaults(func=finish_day)

    # Log commands
    log_parser = subparsers.add_parser('log', help='Log a new task')
    log_parser.add_argument('job', help='Job name or identifer')
    log_parser.add_argument('-m', '--message', required=False, default='', help='Message for the log entry')
    log_parser.set_defaults(func=log_task)

    # Show commands
    show_parser = subparsers.add_parser('show', help='Show logged tasks')
    show_parser.add_argument('show', help='day, week, month, year')
    show_parser.add_argument('-i', '--identifier', required=False, action='store_true', help='Show ids for the logs')
    show_parser.set_defaults(func=show_tasks)

    # Backup commands
    backup_parser = subparsers.add_parser('backup', help="Backup the database")
    backup_parser.add_argument('job', choices=['save', 'load'], help="Operation to perform: save or load the database")
    backup_parser.set_defaults(func=backup_tasks)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
