import pandas as pd
from openpyxl.utils import get_column_letter

src = "data/cleaned/weather_cleaned.csv"
out = "data/cleaned/weather_cleaned.xlsx"

df = pd.read_csv(src)

# (опционально) нормализуем город
df["city_name"] = df["city_name"].astype(str).str.strip().str.title()

# (опционально) сортировка для красоты
df = df.sort_values(["city_name", "date"])

with pd.ExcelWriter(out, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="cleaned")

    ws = writer.sheets["cleaned"]

    # заморозить первую строку
    ws.freeze_panes = "A2"

    # включить автофильтр
    ws.auto_filter.ref = ws.dimensions

    # чуть расширить колонки
    for i, col in enumerate(df.columns, start=1):
        max_len = max(len(str(col)), int(df[col].astype(str).map(len).max()))
        ws.column_dimensions[get_column_letter(i)].width = min(max_len + 2, 40)

print("Готово:", out)
