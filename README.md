# Focus Shield

A small Python CLI to protect your focus: a Pomodoro-style timer, a hosts-file website blocker, and a streak tracker.

## Usage
```
python main.py start -m 25 -t "Uninet auth bug"   # focus session
sudo python main.py block                          # block sites (Windows: run terminal as Administrator)
sudo python main.py unblock
python main.py stats                               # focus time + clean streak
python main.py relapse                             # log a slip, reset streak, get back to work
```

Edit `blocklist_distractions.txt` and `blocklist_adult.txt` to change what gets blocked.
No external dependencies, Python 3.8+.

Note: the hosts-file block is easy to undo, so pair it with a router/DNS filter (e.g. CleanBrowsing) for stronger protection.
