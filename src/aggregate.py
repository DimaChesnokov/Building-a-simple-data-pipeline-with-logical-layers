import pandas as pd
from pathlib import Path

def city_rating():
    df = pd.read_csv("data/enriched/weather_enriched.csv")

    result = df.groupby("city_name").agg({
        "comfort_index": "mean",
        "population": "first",
        "federal_district": "first"
    }).reset_index()

    result = result.sort_values("comfort_index", ascending=False)

    out = Path("data/aggregated/city_tourism_rating.csv")
    out.parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(out, index=False)
    print("city_tourism_rating создан ураа")



def federal_summary():
    df = pd.read_csv("data/enriched/weather_enriched.csv")

    result = df.groupby("federal_district").agg({
        "temperature_max": "mean",
        "comfort_index": "mean"
    }).reset_index()

    result = result.sort_values("comfort_index", ascending=False)

    out = Path("data/aggregated/federal_districts_summary.csv")
    result.to_csv(out, index=False, encoding="utf-8")

    print("federal_districts_summary создан, наконец-то")






def make_special_advice(temp_max, precip, wind):
    tips = []

    
    try: temp_max = float(temp_max)
    except: temp_max = None
    try: precip = float(precip)
    except: precip = None
    try: wind = float(wind)
    except: wind = None

    if precip and precip >= 8:
        tips.append("взять зонт/дождевик")

    if temp_max is not None and temp_max <= 0:
        tips.append("тёплая одежда, перчатки")

    if temp_max is not None and temp_max >= 28:
        tips.append("вода + головной убор")

    if wind and wind >= 12:
        tips.append("ветровка")

    return "; ".join(tips) if tips else "обычная погода, без спец. советов"


def is_stay_home(temp_max, precip, wind):
    try: temp_max = float(temp_max)
    except: temp_max = None
    try: precip = float(precip)
    except: precip = None
    try: wind = float(wind)
    except: wind = None

    if precip and precip >= 15:
        return "Да"
    if wind and wind >= 18:
        return "Да"
    if temp_max is not None and temp_max <= -15:
        return "Да"
    return "Нет"


def travel_recommendations():
    df = pd.read_csv("data/enriched/weather_enriched.csv").drop(columns=["Unnamed: 0"], errors="ignore")

    
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["city_name", "date"])
    last_per_city = df.groupby("city_name").tail(1).copy()

  
    last_per_city["special_advice"] = last_per_city.apply(
        lambda r: make_special_advice(r["temperature_max"], r["precipitation_sum"], r["wind_speed_max"]),
        axis=1
    )
    last_per_city["stay_home"] = last_per_city.apply(
        lambda r: is_stay_home(r["temperature_max"], r["precipitation_sum"], r["wind_speed_max"]),
        axis=1
    )

   
    last_per_city["status"] = last_per_city["stay_home"].apply(lambda x: "Лучше дома" if x == "Да" else "Ехать")

    
    go_df = last_per_city[last_per_city["stay_home"] == "Нет"].sort_values("comfort_index", ascending=False)
    home_df = last_per_city[last_per_city["stay_home"] == "Да"].sort_values("comfort_index", ascending=False)

    top3 = pd.concat([go_df.head(3), home_df.head(max(0, 3 - len(go_df.head(3))))], ignore_index=True)

    out = Path("data/aggregated/travel_recommendations.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    top3.to_csv(out, index=False, encoding="utf-8")
    print("travel_recommendations создан:", out)

  
    out_home = Path("data/aggregated/stay_home_cities.csv")
    home_df.to_csv(out_home, index=False)
    print("stay_home_cities создан:", out_home)