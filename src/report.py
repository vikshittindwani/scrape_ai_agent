import pandas as pd
import xlsxwriter
import pathlib
import datetime as dt

def build_excel(reports: list[pd.DataFrame], parsed_query: dict, fname="report.xlsx"):
    out = pathlib.Path("outputs") / fname
    with pd.ExcelWriter(out, engine="xlsxwriter") as xl:
        for df in reports:
            if df.empty:
                continue

            sheet = df.attrs.get("sheet", "Sheet")[:31]
            df.to_excel(xl, sheet_name=sheet, index=False)
            _add_table_and_filters(xl, sheet, df)

        _add_cover_sheet(xl, parsed_query)

    print(f"✅ Report written: {out}")
    return out

def _add_table_and_filters(xl, sheet, df):
    wb = xl.book
    ws = xl.sheets[sheet]
    n, m = df.shape
    ws.add_table(0, 0, n, m - 1, {"columns": [{"header": h} for h in df.columns]})
    ws.autofilter(0, 0, n, m - 1)

def _add_cover_sheet(xl, parsed):
    wb = xl.book
    ws = wb.add_worksheet("Summary")
    ws.write("A1", "Query parsed as:")
    ws.write("A2", str(parsed))
    ws.write("A4", f"Generated: {dt.datetime.now():%Y-%m-%d %H:%M}")

def save_csv(data: list[dict], filename: str, folder="outputs") -> pd.DataFrame:
    """Saves scraped data into CSV and returns the dataframe."""
    df = pd.DataFrame(data)
    if df.empty:
        print("⚠️ No data to save for", filename)
        return df

    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    path = pathlib.Path(folder) / f"{filename}.csv"
    df.to_csv(path, index=False)
    print(f"✅ CSV saved: {path}")
    return df
