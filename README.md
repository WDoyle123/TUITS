# TUITS - Terminal User Interface Time Sheet

TUITS is a simple, command-line based tool designed to help you log your work hours with ease. Using simple commands, you can log tasks, view completed tasks over different time periods, and manage your workday start and end times.TUITS also utilise gpt3.5-turbo for ai generated summarys of different time frames. TUITS stores your logs in an SQLite database for easy tracking and management.

## Installation (pipx)
TUITS is a CLI tool. Install it with pipx so it is isolated and easy to upgrade.

```
git clone https://github.com/wdoyle123/tuits.git
cd tuits
brew install pipx
pipx install .
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
- `remove`
- `edit`
- `last`
- `undo`

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

For interactive logging (prompts + quick repeat), run without args:

```
tuits log
```

Optional time helpers:

```
tuits log 'ExampleJob' -m 'Late entry' --at 10:15
tuits log 'ExampleJob' -m 'Backdated' --mins -30
```

### Finish Your Day
To log the end of your workday:

```
tuits finish
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
TUITS can generate standup summaries using a local on-demand model (default) or OpenAI (optional).

```
tuits summary month
```

By default it uses a local model via `llama-cpp-python` and downloads the GGUF on first run.  
To use OpenAI instead, set `TUIT_LLM_PROVIDER=openai` and provide an API key with `--api_key` or `OPENAI_API_KEY` (stored in your OS keychain via `keyring`).

### Removing a Log 
To remove a log from the tuits.db:

```
tuits remove
```

You will then be prompted for the entry number or ID. See tuits show to find that!

You can also remove specific IDs directly:

```
tuits remove --ids 12,13
```

### Editing a Log
To edit a recent log entry:

```
tuits edit
```

You can also edit a specific entry by ID:

```
tuits edit --id 12
```

### Show Last or Undo
To show the most recent entry:

```
tuits last
```

To remove the most recent entry:

```
tuits undo
```
