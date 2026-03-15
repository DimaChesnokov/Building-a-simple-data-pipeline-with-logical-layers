from datetime import date

from config import CITIES
from src.raw_collect import collect_raw_10y
from src.clean import build_cleaned
from src.enrich import enrich   
from src.aggregate import city_rating, federal_summary, travel_recommendations

if __name__ == "__main__":
    end = date.today()
    start = date(end.year - 10, end.month, end.day)

   
    ok, fail, raw_log = collect_raw_10y(CITIES, start, end)
    print("RAW ok:", ok, "fail:", fail)

 
    csv_path, clean_log = build_cleaned()
    print("CLEANED:", csv_path)

    enrich()
    city_rating()
    federal_summary()
    travel_recommendations()    

   
