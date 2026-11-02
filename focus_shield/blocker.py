"""Hosts-file website blocker. Needs admin/root to run."""
import platform
import sys
from pathlib import Path

MARK_START = "# >>> FOCUS_SHIELD START"
MARK_END = "# <<< FOCUS_SHIELD END"
ROOT = Path(__file__).resolve().parent.parent


def hosts_path():
    if platform.system() == "Windows":
        return Path(r"C:\Windows\System32\drivers\etc\hosts")
    return Path("/etc/hosts")


def load_domains():
    domains = set()
    for name in ("blocklist_distractions.txt", "blocklist_adult.txt"):
        f = ROOT / name
        if f.exists():
            for line in f.read_text().splitlines():
                line = line.strip().lower()
                if line and not line.startswith("#"):
                    domains.add(line)
    return sorted(domains)


def _strip(text):
    out, skip = [], False
    for line in text.splitlines():
        if line.strip() == MARK_START:
            skip = True
            continue
        if line.strip() == MARK_END:
            skip = False
            continue
        if not skip:
            out.append(line)
    return "\n".join(out).rstrip() + "\n"


def block(include_distractions=True):
    path = hosts_path()
    domains = load_domains()
    text = _strip(path.read_text())
    lines = [MARK_START]
    for d in domains:
        lines.append(f"127.0.0.1 {d}")
        if not d.startswith("www."):
            lines.append(f"127.0.0.1 www.{d}")
    lines.append(MARK_END)
    path.write_text(text + "\n".join(lines) + "\n")
    return len(domains)


def unblock():
    path = hosts_path()
    path.write_text(_strip(path.read_text()))


def permission_error():
    print("Permission denied. Run as Administrator (Windows) or with sudo (Linux/Mac).")
    sys.exit(1)
