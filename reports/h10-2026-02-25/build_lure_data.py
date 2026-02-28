import os, json, csv, sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR   = r'c:\AI Workspaces\Claude Code Workspace - Tom\data-feed\H10-data'
XRAY_FILE  = os.path.join(DATA_DIR, 'X-Ray-full', 'Fruit-flies-traps-24-02.csv')
SALES_DIR  = os.path.join(DATA_DIR, 'H10-xray-popup-sales-units')
OUT_FILE   = r'c:\AI Workspaces\Claude Code Workspace - Tom\outputs\amazon-pipeline\reports\h10-2026-02-25\lure_data.json'

WINDOW_START = datetime(2025, 3, 1)
WINDOW_END   = datetime(2026, 2, 28)

# ── Step 1-3: Load X-Ray, filter Lure, map ASIN → Lure Type / Size / Price ──
lure_asins = {}
with open(XRAY_FILE, encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        if row['Type'].strip() != 'Lure':
            continue
        asin = row['ASIN'].strip()
        if asin in lure_asins:
            continue  # deduplicate
        lure_asins[asin] = {
            'lure_type': row['Lure Type'].strip(),
            'size':      row['Size'].strip(),
            'price':     float(row['Price  US$']) if row['Price  US$'].strip() else 0.0,
        }

print(f"Lure ASINs loaded: {len(lure_asins)}")

# ── Steps 4-8: Load sales, aggregate 12M totals ──────────────────────────────
subseg_units = {'Trap': 0.0, 'Refill': 0.0}
subseg_rev   = {'Trap': 0.0, 'Refill': 0.0}
pack_units   = {}  # size_str -> float
pack_rev     = {}  # size_str -> float
missing      = []

for asin, info in lure_asins.items():
    sales_file = os.path.join(SALES_DIR, f'{asin}-sales-3y.csv')
    if not os.path.exists(sales_file):
        missing.append(asin)
        continue

    total_units = 0.0
    with open(sales_file, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            try:
                date = datetime.strptime(row['Time'].strip()[:10], '%Y-%m-%d')
            except Exception:
                continue
            if WINDOW_START <= date <= WINDOW_END:
                try:
                    total_units += float(row['Sales'])
                except Exception:
                    pass

    revenue    = total_units * info['price']
    lure_type  = info['lure_type']
    subseg_units[lure_type] = subseg_units.get(lure_type, 0.0) + total_units
    subseg_rev[lure_type]   = subseg_rev.get(lure_type, 0.0)   + revenue

    # Pack size deep dive — Trap only
    if lure_type == 'Trap' and info['size']:
        sz = info['size']
        pack_units[sz] = pack_units.get(sz, 0.0) + total_units
        pack_rev[sz]   = pack_rev.get(sz, 0.0)   + revenue

if missing:
    print(f"Missing sales files: {missing}")

# ── Sort pack sizes ascending ─────────────────────────────────────────────────
sorted_sizes = sorted(pack_units.keys(), key=lambda x: int(x) if x.isdigit() else 999)

# ── Build output ──────────────────────────────────────────────────────────────
result = {
    'subseg_units': {k: round(v) for k, v in subseg_units.items()},
    'subseg_rev':   {k: round(v, 2) for k, v in subseg_rev.items()},
    'pack_sizes':   sorted_sizes,
    'pack_units':   {s: round(pack_units[s]) for s in sorted_sizes},
    'pack_rev':     {s: round(pack_rev[s], 2) for s in sorted_sizes},
}

print("\n── Results ──────────────────────────────────────────")
print(json.dumps(result, indent=2))

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)
print(f"\nSaved to {OUT_FILE}")
