import argparse
from tuits.cli.log_task import log_task
from tuits.cli.show_tasks import show_tasks
from tuits.cli.start import start_day
from tuits.cli.finish import finish_day
from tuits.cli.backup import backup_tasks
from tuits.cli.summary import generate_summary
from tuits.cli.remove import remove_tasks
from tuits.cli.edit import edit_task
from tuits.cli.last import show_last
from tuits.cli.undo import undo_last

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
    log_parser.add_argument('job', nargs='?', help='Job name or identifer')
    log_parser.add_argument('-m', '--message', required=False, default=None, help='Message for the log entry')
    log_parser.add_argument('--at', required=False, help='Timestamp for the log (HH:MM or YYYY-MM-DD HH:MM)')
    log_parser.add_argument('--mins', required=False, type=int, help='Offset minutes from now (e.g. -15)')
    log_parser.set_defaults(func=log_task)

    # Show commands
    show_parser = subparsers.add_parser('show', help='Show logged tasks')
    show_parser.add_argument('show', nargs='?', default='day', help='day, week, month, year')
    show_parser.add_argument('-i', '--identifier', required=False, action='store_true', help='Show ids for the logs')
    show_parser.set_defaults(func=show_tasks)

    # Backup commands
    backup_parser = subparsers.add_parser('backup', help="Backup the database")
    backup_parser.add_argument('job', choices=['save', 'load'], help="Operation to perform: save or load the database")
    backup_parser.set_defaults(func=backup_tasks)

    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Generate a summary for a specified time frame')
    summary_parser.add_argument('time_frame', choices=['day', 'week', 'month', 'year'], help="Time frame to summarize")
    summary_parser.add_argument('--api_key', required=False, help='OpenAI API key')
    summary_parser.set_defaults(func=generate_summary)

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a log from the tuits.db')
    remove_parser.add_argument('--limit', type=int, default=10, help='Number of recent logs to display')
    remove_parser.add_argument('--ids', required=False, help='Comma-separated IDs to remove')
    remove_parser.add_argument('--yes', action='store_true', help='Skip confirmation prompt')
    remove_parser.set_defaults(func=remove_tasks)

    # Edit command
    edit_parser = subparsers.add_parser('edit', help='Edit a recent log entry')
    edit_parser.add_argument('--limit', type=int, default=10, help='Number of recent logs to display')
    edit_parser.add_argument('--id', type=int, required=False, help='ID of the log to edit')
    edit_parser.set_defaults(func=edit_task)

    # Last command
    last_parser = subparsers.add_parser('last', help='Show the most recent log entry')
    last_parser.set_defaults(func=show_last)

    # Undo command
    undo_parser = subparsers.add_parser('undo', help='Remove the most recent log entry')
    undo_parser.add_argument('--yes', action='store_true', help='Skip confirmation prompt')
    undo_parser.set_defaults(func=undo_last)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
