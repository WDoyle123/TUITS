# TUITS - Terminal User Interface Time Sheet

TUITS is a simple, command-line based tool designed to help you log your work hours with ease. Using simple commands, you can log tasks, view completed tasks over different time periods, and manage your workday start and end times.TUITS also utilise gpt3.5-turbo for ai generated summarys of different time frames. TUITS stores your logs in an SQLite database for easy tracking and management.

## Setup

To get started with TUITS, you'll need to have Python 3 installed on your system. Once you have Python 3, follow these steps to set up TUITS:

1. **Clone TUITS**: 
```
git clone https://github.com/wdoyle123/tuits.git
```

2. **Install TUITS**:
```
cd tuits 
python3 setup.py install
```

## Usage
Here is a list of available command in TUITS and how to use them:

### Commands
- `log`
- `start`
- `finish`
- `show`
- `backup`
- `summary`
- 'remove'

### Start Your Day
To start logging your workday, simply run:

```
tuits start
```

### Logging Tasks 
To log a task use `log` command with a job and optional message:

```
tuits log 'ExampleJob' -m 'Example message describing the task complete'
```

### Finish Your Day
To log the end of your workday:

```
tuits Finish
```

### Viewing Logged Tasks 
You can view tasks you have completed within different time frames:

```
tuits show <time_frame>
```
`<time_frame>` - `day`, `week`, `month`, `year`.

Here is an example of the output:

```

| Job    | Message                                        | Time  |
|--------|------------------------------------------------|-------|
| Finish | ##########                                     | 16:30 |
| Job3   | Meeting with Company                           | 16:30 |
| Job2   | Back to finding the answer here!               | 15:30 |
| Lunch  | ##########                                     | 13:30 |
| Job1   | Figure this stuff out                          | 12:30 |
| Start  | ##########                                     | 09:00 |

```

You can also use the `-i` flag for adding a column for the ids of the job.

### Backing Up the Database
To backup or load the database use:

```
tuits backup <operation>
```

with `save` or `load`.

### AI Generated Summary
You can use TUITS to generate an ai generated summary of the selected time frame:

```
tuits summary month --api_key <api_key>
```

Upon entering the api once, this `api_key` will be stored in a config file. Allowing you to run this command again without the flag.

### Removing a Log 
To remove a log from the tuits.db:

```
tuits remove
```

You will then be prompted for the id of the job. See tuits show to find that!
