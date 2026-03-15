from pathlib import Path
import pandas as pd
from openpyxl.utils import get_column_letter

def csv_to_pretty_xlsx(csv_path: Path, xlsx_path: Path):
    df = pd.read_csv(csv_path)

   
    if "date" in df.columns:
        try:
            df["date"] = pd.to_datetime(df["date"]).dt.date
        except:
            pass

    
    if "comfort_index" in df.columns:
        try:
            df["comfort_index"] = pd.to_numeric(df["comfort_index"], errors="coerce").round(2)
        except:
            pass

    xlsx_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        sheet = "data"
        df.to_excel(writer, index=False, sheet_name=sheet)
        ws = writer.sheets[sheet]

     
        ws.freeze_panes = "A2"

        
        ws.auto_filter.ref = ws.dimensions

        
        for i, col in enumerate(df.columns, start=1):
            try:
                max_len = max(len(str(col)), int(df[col].astype(str).map(len).max()))
            except:
                max_len = len(str(col))
            ws.column_dimensions[get_column_letter(i)].width = min(max_len + 2, 45)

def main():
    data_dir = Path("data")
    targets = [
        data_dir / "cleaned",
        data_dir / "enriched",
        data_dir / "aggregated",
    ]

    total = 0
    for folder in targets:
        if not folder.exists():
            continue

        for csv_path in folder.glob("*.csv"):
            xlsx_path = csv_path.with_suffix(".xlsx")
            csv_to_pretty_xlsx(csv_path, xlsx_path)
            print("OK:", csv_path, "->", xlsx_path)
            total += 1

    print("ааа:", total)

if __name__ == "__main__":
    main()
