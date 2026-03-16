"""
Update dashboard data from new merged X-Ray CSV.
- ASINs with daily sales files in Data/sales-units/ → use actual 12M sum
- ASINs without sales files → extrapolate 30d × seasonality index
Replaces SEGMENT_DATA, SHARE_DATA, brand/pack data in index.html.
"""
import csv, json, os, sys, re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
DIR = os.path.dirname(__file__)

CSV_FILE = os.path.join(DIR, '..', '..', 'Data', 'x-ray', 'Fruit-Flies-US-new-merged-data.csv')
SALES_DIR = os.path.join(DIR, '..', '..', 'Data', 'sales-units')
HTML_FILE = os.path.join(DIR, 'index.html')

WINDOW_START = datetime(2025, 3, 1)
WINDOW_END   = datetime(2026, 2, 28)

# ── Existing seasonality index (from current dashboard, Lure segment) ─────────
# Monthly index: how each month compares to average month (1.0 = average)
# Mar..Feb ordering (same as dashboard month_labels)
# Derived from cat_monthly_units_curr in existing data
# ── Per-segment seasonality from OLD actual monthly data (Mar-Feb) ─────────────
# Each segment has its own seasonality pattern — don't mix them
SEG_MONTHLY_OLD = {
    'Lure':              [34829,50320,98278,158728,202228,182965,172170,263195,195272,103156,48522,31450],
    'Sticky Traps':      [31707,39494,53675,76161,113144,80161,53128,59973,51454,41812,29061,27550],
    'Passive Attractor': [3150,4524,8079,12515,12220,12694,11510,13366,9911,4928,2185,1672],
    'Electric':          [80873,120165,181467,226819,386224,770034,703008,914324,642704,312794,191808,158935],
}

def make_seas_index(monthly):
    avg = sum(monthly) / 12
    return [m / avg for m in monthly]

SEG_SEAS_INDEX = {seg: make_seas_index(m) for seg, m in SEG_MONTHLY_OLD.items()}

# Category-wide index (fallback for unknown segments)
EXISTING_MONTHLY_UNITS = [150559,214503,341499,474223,713815,1045855,939816,1250858,899341,462691,271577,219608]
AVG_MONTHLY = sum(EXISTING_MONTHLY_UNITS) / 12
SEAS_INDEX = [m / AVG_MONTHLY for m in EXISTING_MONTHLY_UNITS]
# Current month is ~Feb/Mar 2026, so 30d data ≈ index for Feb (last element)
CURRENT_MONTH_INDEX = SEAS_INDEX[-1]  # Feb

for seg, idx in SEG_SEAS_INDEX.items():
    feb_idx = idx[-1]  # Feb is last
    print(f'  {seg}: Feb index={feb_idx:.3f}, multiplier={sum(idx)/feb_idx:.1f}x')
print(f'  Category avg: Feb index={CURRENT_MONTH_INDEX:.3f}, multiplier={sum(SEAS_INDEX)/CURRENT_MONTH_INDEX:.1f}x')

# ── Load CSV ──────────────────────────────────────────────────────────────────
def pnum(s):
    """Parse number from CSV (handles commas, N/A, etc.)."""
    if not s or not s.strip():
        return 0.0
    cleaned = s.replace(',', '').strip()
    if cleaned.upper() in ('N/A', '-', ''):
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

rows = []
with open(CSV_FILE, encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        seg = r['Type'].strip()
        # Normalize segment names
        if seg.lower() == 'sticky traps':
            seg = 'Sticky Traps'
        elif seg.lower() == 'passive attractor':
            seg = 'Passive Attractor'
        elif seg.lower() == 'electric traps':
            seg = 'Electric'

        asin = r['ASIN'].strip()
        brand = r['Brand'].strip()
        price = pnum(r['Price  US$'])
        sales_30d = pnum(r['ASIN Sales'])
        rev_30d = pnum(r['ASIN Revenue'])
        bsr = pnum(r['BSR'])
        rating = pnum(r['Ratings'])
        reviews = pnum(r['Review Count'])
        title = r['Product Details'].strip()
        lure_type = r['Lure Type'].strip()
        size = r['Size'].strip()

        # ── 12M calculation: actual sales file first, fallback to seasonality ──
        sales_file = os.path.join(SALES_DIR, f'{asin}-sales-3y.csv')
        units_12m = 0
        data_source = 'extrapolated'

        if os.path.exists(sales_file):
            # Use actual daily sales data
            with open(sales_file, encoding='utf-8-sig') as sf:
                for srow in csv.DictReader(sf):
                    try:
                        date = datetime.strptime(srow['Time'].strip()[:10], '%Y-%m-%d')
                    except Exception:
                        continue
                    if WINDOW_START <= date <= WINDOW_END:
                        try:
                            units_12m += float(srow['Sales'])
                        except Exception:
                            pass
            rev_12m = units_12m * price if price > 0 else 0
            data_source = 'actual'
        elif sales_30d > 0:
            # Fallback: extrapolate 30d Feb × segment-specific seasonality
            seg_idx = SEG_SEAS_INDEX.get(seg, SEAS_INDEX)
            feb_idx = seg_idx[-1]  # Feb is last element
            if feb_idx > 0:
                avg_monthly = sales_30d / feb_idx
                units_12m = avg_monthly * sum(seg_idx)
            else:
                units_12m = sales_30d * 12
            rev_12m = units_12m * price if price > 0 else rev_30d * (units_12m / sales_30d) if sales_30d > 0 else 0
        else:
            units_12m = sales_30d * 12
            rev_12m = rev_30d * 12

        rows.append({
            'asin': asin,
            'brand': brand,
            'segment': seg,
            'price': price,
            'title': title,
            'lure_type': lure_type,
            'size': size,
            'sales_30d': sales_30d,
            'rev_30d': rev_30d,
            'units_12m': units_12m,
            'rev_12m': rev_12m,
            'data_source': data_source,
            'bsr': int(bsr) if bsr else 0,
            'rating': rating,
            'reviews': int(reviews) if reviews else 0,
        })

actual_count = sum(1 for r in rows if r['data_source'] == 'actual')
extrap_count = sum(1 for r in rows if r['data_source'] == 'extrapolated')
print(f'\nLoaded {len(rows)} ASINs ({actual_count} with actual sales data, {extrap_count} extrapolated)')

# ── Segment aggregation ──────────────────────────────────────────────────────
SEGMENTS = ['Lure', 'Sticky Traps', 'Passive Attractor', 'Electric']
seg_data = {}
for seg in SEGMENTS:
    seg_rows = [r for r in rows if r['segment'] == seg]
    units_12m = sum(r['units_12m'] for r in seg_rows)
    rev_12m = sum(r['rev_12m'] for r in seg_rows)
    avg_price = rev_12m / units_12m if units_12m > 0 else 0
    seg_data[seg] = {
        'skus': len(seg_rows),
        'units_12m': round(units_12m),
        'revenue_12m': round(rev_12m),
        'avg_price': round(avg_price, 2),
    }
    print(f'  {seg}: {len(seg_rows)} SKUs, {units_12m:,.0f} units 12M, ${rev_12m:,.0f} rev 12M')

total_units = sum(s['units_12m'] for s in seg_data.values())
total_rev = sum(s['revenue_12m'] for s in seg_data.values())
print(f'\n  TOTAL: {total_units:,.0f} units 12M, ${total_rev:,.0f} rev 12M')

# Compute shares
for seg in SEGMENTS:
    seg_data[seg]['unit_share'] = round(seg_data[seg]['units_12m'] / total_units * 100, 1) if total_units > 0 else 0
    seg_data[seg]['rev_share'] = round(seg_data[seg]['revenue_12m'] / total_rev * 100, 1) if total_rev > 0 else 0

# ── Monthly extrapolation per segment (using SEGMENT-SPECIFIC seasonality) ─────
seg_monthly_units = {}
seg_monthly_rev = {}
for seg in SEGMENTS:
    total_u = seg_data[seg]['units_12m']
    total_r = seg_data[seg]['revenue_12m']
    seg_idx = SEG_SEAS_INDEX.get(seg, SEAS_INDEX)
    idx_sum = sum(seg_idx)
    monthly_u = [round(total_u * idx / idx_sum) for idx in seg_idx]
    monthly_r = [round(total_r * idx / idx_sum) for idx in seg_idx]
    seg_monthly_units[seg] = monthly_u
    seg_monthly_rev[seg] = monthly_r

# ── Lure-specific data for Tab 2 ─────────────────────────────────────────────
lure_rows = [r for r in rows if r['segment'] == 'Lure']
lure_rows.sort(key=lambda r: r['rev_12m'], reverse=True)

# Brand aggregation (Lure only)
brand_agg = {}
for r in lure_rows:
    b = r['brand']
    if b not in brand_agg:
        brand_agg[b] = {'units': 0, 'rev': 0, 'count': 0, 'prices': []}
    brand_agg[b]['units'] += r['units_12m']
    brand_agg[b]['rev'] += r['rev_12m']
    brand_agg[b]['count'] += 1
    if r['price'] > 0:
        brand_agg[b]['prices'].append(r['price'])

# Top brands by units
brand_sorted = sorted(brand_agg.items(), key=lambda x: x[1]['units'], reverse=True)
BRAND_LABELS = [b for b, _ in brand_sorted[:7]]
BRAND_UNITS = [round(v['units']) for _, v in brand_sorted[:7]]
BRAND_REV = [round(v['rev']) for _, v in brand_sorted[:7]]
# Add "Others"
other_units = sum(v['units'] for b, v in brand_sorted[7:])
other_rev = sum(v['rev'] for b, v in brand_sorted[7:])
if other_units > 0:
    BRAND_LABELS.append('Others')
    BRAND_UNITS.append(round(other_units))
    BRAND_REV.append(round(other_rev))

print(f'\nLure brands: {BRAND_LABELS}')
print(f'  Units: {BRAND_UNITS}')
print(f'  Rev: {BRAND_REV}')

# Pack size aggregation (Lure only, from Size column)
pack_agg = {}
for r in lure_rows:
    s = r['size'] if r['size'] else 'Other'
    if s not in pack_agg:
        pack_agg[s] = {'units': 0, 'rev': 0}
    pack_agg[s]['units'] += r['units_12m']
    pack_agg[s]['rev'] += r['rev_12m']

pack_sorted = sorted(pack_agg.items(), key=lambda x: x[1]['units'], reverse=True)
PACK_LABELS = [f'{s}-pack' if s.isdigit() else s for s, _ in pack_sorted]
PACK_UNITS = [round(v['units']) for _, v in pack_sorted]
PACK_REV = [round(v['rev']) for _, v in pack_sorted]

print(f'\nPack sizes: {PACK_LABELS}')
print(f'  Units: {PACK_UNITS}')
print(f'  Rev: {PACK_REV}')

# ── Build SHARE_DATA (all ASINs) ─────────────────────────────────────────────
asin_data = []
for r in rows:
    asin_data.append({
        'asin': r['asin'],
        'brand': r['brand'],
        'segment': r['segment'],
        'price': r['price'] if r['price'] > 0 else None,
        'title': r['title'][:80],
        'p1_units': 0,  # No prev year data
        'p2_units': r['units_12m'],
        'p1_rev': 0,
        'p2_rev': r['rev_12m'],
    })

SHARE_DATA_OBJ = {
    'asin_data': asin_data,
    'period_labels': {'p1': 'Mar 2024 – Feb 2025 (N/A)', 'p2': 'Mar 2025 – Feb 2026 (est.)'}
}

# ── Build SEGMENT_DATA ────────────────────────────────────────────────────────
SEGMENT_DATA_OBJ = {
    'segments': SEGMENTS,
    'month_labels': ['Mar 2025','Apr 2025','May 2025','Jun 2025','Jul 2025','Aug 2025',
                     'Sep 2025','Oct 2025','Nov 2025','Dec 2025','Jan 2026','Feb 2026'],
    'monthly_units': seg_monthly_units,
    'monthly_rev': seg_monthly_rev,
    'kpis': {},
}
for seg in SEGMENTS:
    d = seg_data[seg]
    SEGMENT_DATA_OBJ['kpis'][seg] = {
        'skus': d['skus'],
        'units_12m': d['units_12m'],
        'units_prev12m': 0,
        'revenue_12m': d['revenue_12m'],
        'revenue_prev12m': 0,
        'growth_pct': None,  # No prev year
        'avg_price': d['avg_price'],
        'unit_share': d['unit_share'],
        'rev_share': d['rev_share'],
    }

# Category totals (for seasonality section — keep existing)
cat_monthly_units = [sum(seg_monthly_units[s][i] for s in SEGMENTS) for i in range(12)]
cat_monthly_rev = [sum(seg_monthly_rev[s][i] for s in SEGMENTS) for i in range(12)]

SEGMENT_DATA_OBJ['cat_monthly_units_prev'] = [0]*12  # No prev year
SEGMENT_DATA_OBJ['cat_monthly_units_curr'] = cat_monthly_units
SEGMENT_DATA_OBJ['cat_monthly_rev_prev'] = [0]*12
SEGMENT_DATA_OBJ['cat_monthly_rev_curr'] = cat_monthly_rev

# ── Build Top 20 Lure table HTML ─────────────────────────────────────────────
top20_html = ''
for r in lure_rows[:20]:
    top20_html += f'''    <tr>
      <td><a href="https://amazon.com/dp/{r['asin']}" target="_blank">{r['asin']}</a></td>
      <td>{r['brand']}</td>
      <td><span title="{r['title']}">{r['title'][:55]}{'…' if len(r['title']) > 55 else ''}</span></td>
      <td data-val="{r['price']:.2f}">${r['price']:.2f}</td>
      <td data-val="{round(r['rev_12m'])}">${round(r['rev_12m']):,}</td>
      <td>{r['bsr']:,}</td>
      <td>{r['reviews']:,}</td>
      <td>—</td>
    </tr>
'''

# ── Build Brand Summary table HTML (Lure) ────────────────────────────────────
total_lure_units = sum(v['units'] for v in brand_agg.values())
total_lure_rev = sum(v['rev'] for v in brand_agg.values())
brand_summary_html = ''
for b, v in brand_sorted[:10]:
    avg_p = sum(v['prices']) / len(v['prices']) if v['prices'] else 0
    u_share = v['units'] / total_lure_units * 100 if total_lure_units > 0 else 0
    r_share = v['rev'] / total_lure_rev * 100 if total_lure_rev > 0 else 0
    brand_summary_html += f'''    <tr>
      <td><strong>{b}</strong></td>
      <td>{v['count']}</td>
      <td style="text-align:right">${avg_p:.2f}</td>
      <td style="text-align:right">{round(v['units']):,}</td>
      <td style="text-align:right">{u_share:.1f}%</td>
      <td style="text-align:right">${round(v['rev']):,}</td>
      <td style="text-align:right">{r_share:.1f}%</td>
    </tr>
'''

# ── Inject into HTML ──────────────────────────────────────────────────────────
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace SEGMENT_DATA object
seg_data_js = json.dumps(SEGMENT_DATA_OBJ, ensure_ascii=False)
# Find and replace the SEGMENT_DATA block
pattern_seg = r'const SEGMENT_DATA = \{.*?\};'
new_seg = f'const SEGMENT_DATA = {seg_data_js};'
html = re.sub(pattern_seg, new_seg, html, count=1, flags=re.DOTALL)
print('\n✓ SEGMENT_DATA replaced')

# 2. Replace SHARE_DATA object
# NOTE: Do NOT replace SHARE_DATA or ASIN_DS — they contain the original 57 ASINs
# with real monthly data that drives the seasonality chart and lure share line.
# The index mapping between SHARE_DATA and ASIN_DS must stay aligned.
print('⊘ SHARE_DATA kept as-is (original 57 ASINs with monthly data for seasonality)')

# 3. Replace BRAND_LABELS_12M, BRAND_UNITS_12M, BRAND_REV_12M
bl_js = json.dumps(BRAND_LABELS, ensure_ascii=False)
bu_js = json.dumps(BRAND_UNITS)
br_js = json.dumps(BRAND_REV)
html = re.sub(r'const BRAND_LABELS_12M = \[.*?\];', f'const BRAND_LABELS_12M = {bl_js};', html, count=1)
html = re.sub(r'const BRAND_UNITS_12M  = \[.*?\];', f'const BRAND_UNITS_12M  = {bu_js};', html, count=1)
html = re.sub(r'const BRAND_REV_12M    = \[.*?\];', f'const BRAND_REV_12M    = {br_js};', html, count=1)
print('✓ Brand data replaced')

# 4. Replace PACK_LABELS, PACK_UNITS, PACK_REV
pl_js = json.dumps(PACK_LABELS, ensure_ascii=False)
pu_js = json.dumps(PACK_UNITS)
pr_js = json.dumps(PACK_REV)
html = re.sub(r'const PACK_LABELS = \[.*?\];', f'const PACK_LABELS = {pl_js};', html, count=1)
html = re.sub(r'const PACK_UNITS  = \[.*?\];', f'const PACK_UNITS  = {pu_js};', html, count=1)
html = re.sub(r'const PACK_REV    = \[.*?\];', f'const PACK_REV    = {pr_js};', html, count=1)
print('✓ Pack size data replaced')

# 5. Replace lureTop20Table tbody
pattern_top20 = r'(<table[^>]*id="lureTop20Table"[^>]*>.*?<tbody>)(.*?)(</tbody>)'
def repl_top20(m):
    return m.group(1) + '\n' + top20_html + '    ' + m.group(3)
html = re.sub(pattern_top20, repl_top20, html, count=1, flags=re.DOTALL)
print('✓ Top 20 Lure table replaced')

# 6. Replace Brand Summary table tbody (Tab 2)
# Find the brand summary table — it's the one after "Brand Summary — Lure Segment"
pattern_brand_summary = r'(Brand Summary — Lure Segment.*?<tbody>)(.*?)(</tbody>)'
def repl_brand_summary(m):
    return m.group(1) + '\n' + brand_summary_html + '    ' + m.group(3)
html = re.sub(pattern_brand_summary, repl_brand_summary, html, count=1, flags=re.DOTALL)
print('✓ Brand summary table replaced')

# 7. Update header subtitle with new count
html = re.sub(
    r'57 ASINs',
    f'{len(rows)} ASINs',
    html
)
print(f'✓ ASIN count updated to {len(rows)}')

# 8. Update source file name in header
html = re.sub(
    r'Source: Fruit-flies-traps-24-02\.csv',
    'Source: Fruit-Flies-US-new-merged-data.csv',
    html
)
print('✓ Source filename updated')

# ── Write ─────────────────────────────────────────────────────────────────────
with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n✓ Dashboard updated successfully.')
print(f'  Total ASINs: {len(rows)}')
print(f'  Segments: {len(SEGMENTS)}')
print(f'  Total 12M units (est.): {total_units:,}')
print(f'  Total 12M revenue (est.): ${total_rev:,}')
