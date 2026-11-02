import argparse
from datetime import date, datetime

from . import blocker, storage, timer


def cmd_start(args):
    data = storage.load()
    ok, mins = timer.run_timer(args.minutes, args.task)
    data["sessions"].append({
        "date": date.today().isoformat(),
        "task": args.task,
        "minutes": mins,
        "completed": ok,
    })
    storage.save(data)


def cmd_block(args):
    try:
        n = blocker.block()
        print(f"Blocked {n} domains. Restart your browser.")
    except PermissionError:
        blocker.permission_error()


def cmd_unblock(args):
    try:
        blocker.unblock()
        print("Unblocked.")
    except PermissionError:
        blocker.permission_error()


def cmd_stats(args):
    data = storage.load()
    today = date.today().isoformat()
    today_min = sum(s["minutes"] for s in data["sessions"] if s["date"] == today)
    total_min = sum(s["minutes"] for s in data["sessions"])
    streak = (date.today() - datetime.fromisoformat(data["clean_since"]).date()).days
    print(f"Today:        {today_min:.0f} min focused")
    print(f"All time:     {total_min / 60:.1f} hours")
    print(f"Clean streak: {streak} days")
    print(f"Relapses:     {len(data['relapses'])}")


def cmd_relapse(args):
    data = storage.load()
    data["relapses"].append(date.today().isoformat())
    data["clean_since"] = date.today().isoformat()
    storage.save(data)
    print("Logged. Streak reset. Don't dwell on it. Open your editor and work for 25 minutes right now.")


def main():
    p = argparse.ArgumentParser(prog="focus_shield")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("start", help="start a focus session")
    s.add_argument("-m", "--minutes", type=float, default=25)
    s.add_argument("-t", "--task", default="Deep work")
    s.set_defaults(func=cmd_start)

    sub.add_parser("block", help="block distracting sites (admin)").set_defaults(func=cmd_block)
    sub.add_parser("unblock", help="remove blocks (admin)").set_defaults(func=cmd_unblock)
    sub.add_parser("stats", help="show focus stats and streak").set_defaults(func=cmd_stats)
    sub.add_parser("relapse", help="log a slip and reset streak").set_defaults(func=cmd_relapse)

    args = p.parse_args()
    args.func(args)
