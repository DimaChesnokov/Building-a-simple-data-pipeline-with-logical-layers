import pandas as pd
from pathlib import Path
from datetime import datetime

def get_season(month: int):
    if month in [12,1,2]:
        return "Зима"
    if month in [3,4,5]:
        return "Весна"
    if month in [6,7,8]:
        return "Лето"
    return "Осень"

def calculate_comfort(temp, wind):
    score = 100

    if temp < -10 or temp > 35:
        score -= 40
    elif temp < 0 or temp > 30:
        score -= 20

    if wind and wind > 12:
        score -= 20

    return max(score, 0)

def recommend_activity(temp, precip):
    if precip and precip > 10:
        return "Домашний отдых"
    if temp < 0:
        return "Музеи(скучноо)"
    if temp > 20:
        return "Прогулки"
    return "Экскурсии"

def enrich():
    cleaned_path = Path("data/cleaned/weather_cleaned.csv")
    ref_path = Path("data/enriched/cities_reference.csv")
    out_path = Path("data/enriched/weather_enriched.csv")

    df = pd.read_csv(cleaned_path)
    ref = pd.read_csv(ref_path)

    df = df.merge(ref, on="city_name", how="left")

    # сезон
    df["month"] = pd.to_datetime(df["date"]).dt.month
    df["season"] = df["month"].apply(get_season)

    # комфорт
    df["comfort_index"] = df.apply(
        lambda row: calculate_comfort(row["temperature_max"], row["wind_speed_max"]),
        axis=1
    )

    # активность
    df["recommended_activity"] = df.apply(
        lambda row: recommend_activity(row["temperature_max"], row["precipitation_sum"]),
        axis=1
    )

    # совпадает ли сезон туризма
    df["tourist_season_match"] = df.apply(
        lambda row: "Да" if row["tourism_season"] == "Круглый год"
        or row["season"] in str(row["tourism_season"])
        else "Нет",
        axis=1
    )

    df.to_csv(out_path)

    print("ENRICHED создан:", out_path)
