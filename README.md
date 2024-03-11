# TUITS - Terminal User Interface Time Sheet

TUITS is a simple, command-line based tool designed to help you log your work hours with ease. Using simple commands, you can log tasks, view completed tasks over different time periods, and manage your workday start and end times. TUITS stores your logs in an SQLite database for easy tracking and management.

## Setup

To get started with TUITS, you'll need to have Python 3 installed on your system. Once you have Python 3, follow these steps to set up TUITS:

1. **Clone TUITS**: 
```
git clone https://github.com/wdoyle123/tuits.git ```

2. **Install TUITS**:
```
cd tuits 
python3 setup.py install
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

Here is an example of the output:
```
+--------+------------------------------------------------+--------+
| Job    | Message                                        | Time   |
+========+================================================+========+
| Finish | ##########                                     | 20:36  |
+--------+------------------------------------------------+--------+
| Job1   | Back to finding the answer here!               | 20:36  |
+--------+------------------------------------------------+--------+
| Job2   | Long client meeting but resolved the gas leak! | 20:36  |
+--------+------------------------------------------------+--------+
| Job1   | Figure this stuff out                          | 20:35  |
+--------+------------------------------------------------+--------+
| Start  | ##########                                     | 20:35  |
+--------+------------------------------------------------+--------+
```
