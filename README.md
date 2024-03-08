## What is TUITS?

TUITS is a Terminal User Interface Time Sheet. 

With simple commands such as:
```
tuits log 'Shell Meeting' -m 'We discussed the new oil reports'
```

You can log you hours.

This works by at the start of the working day you do:
```
tuits start
```

And tuits creates a new record for the day

then you can log your first job of the day

This will give you a duration and a timestamp for each event.

The logs are stored in an sqlite database
