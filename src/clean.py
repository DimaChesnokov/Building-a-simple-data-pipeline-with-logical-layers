from pathlib import Path
import json
import pandas as pd

from config import TEMP_MIN, TEMP_MAX
from src.utils import ensure_dir, append_line, now_iso

def build_cleaned():
    raw_base = Path("data/raw/open_meteo")
    out_dir = Path("data/cleaned")
    log = Path("data/cleaned/logs/cleaning_log.txt")
    ensure_dir(out_dir)
    ensure_dir(log.parent)

    files = list(raw_base.glob("**/*.json"))
    append_line(log, f"[{now_iso()}] START files={len(files)}")

    rows = []
    bad = 0

    for fp in files:
        try:
            obj = json.loads(fp.read_text(encoding="utf-8"))
        except Exception as e:
            bad += 1
            append_line(log, f"[{now_iso()}] bad_json {fp} err={e}")
            continue

        meta = obj.get("metadata", {})
        data = obj.get("data", {})
        daily = data.get("daily", {})


        times = daily.get("time", [])
        tmax = daily.get("temperature_2m_max", [])
        tmin = daily.get("temperature_2m_min", [])
        precip = daily.get("precipitation_sum", [])
        wind = daily.get("wind_speed_10m_max", [])

        n = min(len(times), len(tmax), len(tmin))
        for i in range(n):
            try:
                mx = int(round(float(tmax[i])))
                mn = int(round(float(tmin[i])))
            except:
                continue

            
            if not (TEMP_MIN <= mx <= TEMP_MAX):
                continue
            if not (TEMP_MIN <= mn <= TEMP_MAX):
                continue

            rows.append({
                "city_name": meta.get("city_ru") or meta.get("city"),
                "date": times[i],
                "temperature_max": mx,
                "temperature_min": mn,
                "precipitation_sum": precip[i] if i < len(precip) else None,
                "wind_speed_max": wind[i] if i < len(wind) else None,
                "collection_time": meta.get("collection_time"),
            })

    df = pd.DataFrame(rows)
    out_csv = out_dir / "weather_cleaned.csv"
    df.to_csv(out_csv, index=False, encoding="utf-8")

    append_line(log, f"[{now_iso()}] END rows={len(df)} bad_json={bad} csv={out_csv.name}")
    return str(out_csv), str(log)
