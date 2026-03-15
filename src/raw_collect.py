from datetime import date
from pathlib import Path
import time
import requests

from config import OPEN_METEO_URL, TIMEZONE
from src.utils import write_json, append_line, now_iso, ensure_dir

def collect_raw_10y(cities: list, start: date, end: date):
    base = Path("data/raw/open_meteo")
    log = Path("data/raw/logs/raw_collection_log.txt")
    ensure_dir(base)
    ensure_dir(log.parent)

    append_line(log, f"[{now_iso()}] START (open-meteo) start={start} end={end} cities={len(cities)}")

    ok = 0
    fail = 0

    for c in cities:
        city_dir = base / c["name_en"].lower().replace(" ", "_")
        ensure_dir(city_dir)

        out = city_dir / f"{start.isoformat()}__{end.isoformat()}.json"
        if out.exists():
            append_line(log, f"[{now_iso()}] SKIP exists {c['name_en']} file={out.name}")
            continue

        params = {
            "latitude": c["lat"],
            "longitude": c["lon"],
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
            "timezone": TIMEZONE,
        }


        r = requests.get(OPEN_METEO_URL, params=params, timeout=40)


        if r.status_code != 200:
            fail += 1
            append_line(log, f"[{now_iso()}] FAIL {c['name_en']} http={r.status_code} body={r.text[:160]}")
            time.sleep(1)
            continue

        payload = {
            "metadata": {
                "collection_time": now_iso(),
                "source": "open-meteo.com",
                "city": c["name_en"],
                "city_ru": c["name_ru"],
                "lat": c["lat"],
                "lon": c["lon"],
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
            },
            "data": r.json(),
        }

        write_json(out, payload)
        ok += 1
        append_line(log, f"[{now_iso()}] OK {c['name_en']} file={out.name}")

        time.sleep(0.2)

    append_line(log, f"[{now_iso()}] END ok={ok} fail={fail}")
    return ok, fail, str(log)
