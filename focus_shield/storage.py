import json
from datetime import date
from pathlib import Path

DATA_FILE = Path.home() / ".focus_shield.json"


def load():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"sessions": [], "clean_since": date.today().isoformat(), "relapses": []}


def save(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))
