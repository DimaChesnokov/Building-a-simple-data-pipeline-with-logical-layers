from datetime import date, datetime, timedelta
from pathlib import Path
import json

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def daterange(d1: date, d2: date):
    cur = d1
    while cur <= d2:
        yield cur
        cur += timedelta(days=1)

def now_iso():
    return datetime.now().isoformat(timespec="seconds")

def write_json(path: Path, obj: dict):
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def append_line(path: Path, line: str):
    ensure_dir(path.parent)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")
