# TUITS - Terminal User Interface Time Sheet

TUITS is a simple, command-line based tool designed to help you log your work hours with ease. Using simple commands, you can log tasks, view completed tasks over different time periods, and manage your workday start and end times. TUITS stores your logs in an SQLite database for easy tracking and management.

## Setup

To get started with TUITS, you'll need to have Python 3 installed on your system. Once you have Python 3, follow these steps to set up TUITS:

1. **Clone TUITS**: 
```
git clone https://github.com/wdoyle123/tuits.git
```

2. **Make the script executable**:
```
cd tuits/tuits
chmod +x tuits.py
```

3. **Make TUITS accessable globally using a symlink**:
```
ln -s tuits.py /usr/local/bin/tuits
```

## Usage

### Start Your Day
To start logging your workday, simply run:
```
tuits start
```

This command creates a new record for the day indicting a start time.

### Logging Tasks 
To log a task use `log` command with a job and message:
```
tuits log 'ExampleJob' -m 'Example message describing the task complete'
```

### Viewing Logged Tasks 
You can view tasks you have completed within different time frames:
```
tuits show day 
```
Replace day with week, month or year to view tasks completed within those time frames.
