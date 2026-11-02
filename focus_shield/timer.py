import time
from datetime import datetime


def run_timer(minutes, label="Deep work"):
    total = int(minutes * 60)
    start = datetime.now()
    try:
        for remaining in range(total, 0, -1):
            m, s = divmod(remaining, 60)
            print(f"\r{label}: {m:02d}:{s:02d} remaining  (Ctrl+C = quit)", end="", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        done = (datetime.now() - start).total_seconds() / 60
        print(f"\nStopped early after {done:.1f} min.")
        return False, round(done, 1)
    print("\nSession complete. Take a short break.")
    return True, float(minutes)
