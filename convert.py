"""Convert weekly Excel reports (sheet 'Cells') into small JSON files for the dashboard.
Usage:  python scripts/convert.py            -> converts every .xlsx inside /reports, then deletes them
        python scripts/convert.py file.xlsx  -> converts only that file (keeps it)"""
import re, os, sys, json, math, glob, datetime
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data"); WEEKS = os.path.join(DATA, "weeks")
os.makedirs(WEEKS, exist_ok=True)

def nan(v): return v is None or (isinstance(v, float) and math.isnan(v))
def num(v, d=2):
    if isinstance(v, bool) or nan(v): return None
    try: return round(float(v), d)
    except Exception: return None
def txt(v): return None if nan(v) else v
def bw(v):
    m = re.search(r"(?:(\d+)\s*\*\s*)?L\d+\s+([\d.]+)\s*M", "" if nan(v) else str(v))
    return int(m.group(1) or 1) * float(m.group(2)) if m else 0
def key_of(name, hdr):
    m = re.search(r"(20\d\d)\D{0,6}W(\d{1,2})", name, re.I)
    if m: return f"{m.group(1)}-W{int(m.group(2)):02d}"
    h = re.search(r"(\d+)", str(hdr or ""))
    return f"{datetime.date.today().year}-W{int(h.group(1)):02d}" if h else None

def convert(path):
    df = pd.read_excel(path, sheet_name="Cells", header=None)
    if df.iloc[3, 156] != "District":
        raise SystemExit(f"{path}: unexpected 'Cells' layout (District column not at column FA)")
    key = key_of(os.path.basename(path), df.iloc[3, 22])
    if not key: raise SystemExit(f"{path}: cannot detect the week - put the year and week in the file name, e.g. ..._2026_W41.xlsx")
    rows, master = [], []
    for r in df.iloc[4:].itertuples(index=False):
        if nan(r[1]): continue
        rows.append([r[1], txt(r[3]), txt(r[156]), num(r[21], 1) or 0, num(r[22]), num(r[27]), num(r[32]),
                     num(r[154], 4) or 0, txt(r[8]), bw(r[5]), bw(r[6]), bw(r[7])])
        master.append([r[1], txt(r[2]), txt(r[137]), txt(r[10]), txt(r[20])])
    return key, rows, master

def main():
    args = sys.argv[1:]
    auto = not args
    files = args or sorted(glob.glob(os.path.join(ROOT, "reports", "*.xlsx")))
    mpath = os.path.join(DATA, "manifest.json")
    man = json.load(open(mpath)) if os.path.exists(mpath) else {"weeks": []}
    names = {w["k"]: w for w in man["weeks"]}
    for f in files:
        print("Converting", f)
        key, rows, master = convert(f)
        json.dump(rows, open(os.path.join(WEEKS, key + ".json"), "w"), separators=(",", ":"), allow_nan=False)
        names[key] = {"k": key, "file": os.path.basename(f), "rows": len(rows)}
        if key >= max(names):   # newest week also provides sector names / vendor / owner
            json.dump(master, open(os.path.join(DATA, "master.json"), "w"), separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        print("  ->", key, len(rows), "sectors")
        if auto: os.remove(f)
    weeks = [names[k] for k in sorted(names) if os.path.exists(os.path.join(WEEKS, k + ".json"))]
    json.dump({"updated": int(datetime.datetime.now().timestamp() * 1000), "weeks": weeks}, open(mpath, "w"), indent=1)
    print("Done:", len(weeks), "week(s) in data/")
main()
