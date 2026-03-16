"""Apply all manual fixes to index.html after script injections."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

fixes = 0

# 1. Sticky header
old = 'header{background:#0f2942;color:#fff;padding:18px 32px;display:flex;justify-content:space-between;align-items:center}'
new = 'header{background:#0f2942;color:#fff;padding:18px 32px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:100}'
if old in h: h = h.replace(old, new); fixes += 1

# 2. Sticky tabs
old = '.tabs{display:flex;background:#fff;border-bottom:2px solid #e2e8f0;padding:0 32px;gap:2px}'
new = '.tabs{display:flex;background:#fff;border-bottom:2px solid #e2e8f0;padding:0 32px;gap:2px;position:sticky;top:73px;z-index:99;box-shadow:0 2px 4px rgba(0,0,0,.06)}'
if old in h: h = h.replace(old, new); fixes += 1

# 3. Renumber tabs
old = """  <div class="tab" onclick="show('tc',this)">4 \u2014 Listing Communication</div>\n</div>"""
new = """  <div class="tab" onclick="show('tv',this)">4 \u2014 Reviews (new)</div>\n  <div class="tab" onclick="show('tc',this)">5 \u2014 Listing Communication</div>\n</div>"""
if old in h: h = h.replace(old, new); fixes += 1

# 4. Remove YoY variables from segInit
import re
h, n = re.subn(
    r'  const totalRevP2.*?const pl = SHARE_DATA\.period_labels;',
    '  const pl = SHARE_DATA.period_labels;',
    h, flags=re.DOTALL, count=1
)
if n: fixes += 1

# 5. Remove growth from KPI blocks (first occurrence)
old_grow = """    const grow = k.growth_pct !== null
      ? (k.growth_pct >= 0 ? '+'+k.growth_pct+'%' : k.growth_pct+'%') : '\u2014';
    const gc = k.growth_pct !== null ? (k.growth_pct >= 0 ? 'delta-pos' : 'delta-neg') : 'delta-neu';
    return `"""
new_grow = "    return `"
while old_grow in h:
    h = h.replace(old_grow, new_grow, 1)
    fixes += 1

# 6. Update insight text
old = """Segment-level view only.</strong> All metrics are aggregated to segment before calculation. Individual ASINs are not shown. 12-month window: Mar 2025 \u2013 Feb 2026. Growth = avg(last 3M) vs avg(previous 3M)."""
new = """Segment-level view only.</strong> All metrics are aggregated to segment before calculation. Individual ASINs are not shown. 12-month estimates based on 30-day X-Ray data (Feb 2026) extrapolated using seasonality index. 207 ASINs across 4 segments."""
if old in h: h = h.replace(old, new); fixes += 1

# 7. Add Units total to Total Category KPI
old_kpi = """const fmtUnits = v => v >= 1e6 ? (v/1e6).toFixed(2)+'M' : (v/1e3).toFixed(0)+'K';
  document.getElementById('seg_total_kpi').innerHTML = `
    <div class="card" style="border-left:4px solid #1e293b;padding:14px 20px;display:flex;align-items:center;gap:28px;flex-wrap:wrap">
      <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#64748b;min-width:120px">Total Category</div>
      <div>
        <div style="font-size:1.6rem;font-weight:700;color:#1e293b;line-height:1">$${(totalRev12m/1e6).toFixed(1)}M</div>
        <div style="font-size:.75rem;color:#64748b;margin-top:3px">Revenue \u00b7 Last 12M (Mar 2025 \u2013 Feb 2026)</div>
      </div>
    </div>`;"""
new_kpi = """const fmtUnits = v => v >= 1e6 ? (v/1e6).toFixed(2)+'M' : (v/1e3).toFixed(0)+'K';
  document.getElementById('seg_total_kpi').innerHTML = `
    <div class="card" style="border-left:4px solid #1e293b;padding:14px 20px">
      <div style="display:flex;align-items:center;gap:28px;flex-wrap:wrap">
        <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#64748b;min-width:120px">Total Category</div>
        <div>
          <div style="font-size:1.6rem;font-weight:700;color:#1e293b;line-height:1">$${(totalRev12m/1e6).toFixed(1)}M</div>
          <div style="font-size:.75rem;color:#64748b;margin-top:3px">Revenue \u00b7 Last 12M (Mar 2025 \u2013 Feb 2026)</div>
        </div>
        <div>
          <div style="font-size:1.6rem;font-weight:700;color:#1e293b;line-height:1">${fmtUnits(totalUnits12m)}</div>
          <div style="font-size:.75rem;color:#64748b;margin-top:3px">Units Sold \u00b7 Last 12M (Mar 2025 \u2013 Feb 2026)</div>
        </div>
      </div>
      <div style="font-size:.68rem;color:#94a3b8;margin-top:10px;border-top:1px solid #f1f5f9;padding-top:8px">
        Totals across all 4 segments: Lure, Sticky Traps, Electric, Passive Attractor. 12M estimates based on 30-day X-Ray data \u00d7 seasonality index.
      </div>
    </div>`;"""
if old_kpi in h: h = h.replace(old_kpi, new_kpi); fixes += 1

# 8. Tab 2 KPIs
replacements = [
    ('44.1%</div><div class="kpi-l">Top 1 ASIN Revenue Share', '43.1%</div><div class="kpi-l">Top 1 ASIN Revenue Share'),
    ('69.5%</div><div class="kpi-l">Top 3 ASINs Share', '67.9%</div><div class="kpi-l">Top 3 ASINs Share'),
    ('78.7%</div><div class="kpi-l">Top 5 ASINs Share', '76.9%</div><div class="kpi-l">Top 5 ASINs Share'),
    ('89.5%</div><div class="kpi-l">Top 10 ASINs Share', '87.5%</div><div class="kpi-l">Top 10 ASINs Share'),
    ('61.9%</div><div class="kpi-l">Top Brand Share (Terro)', '60.5%</div><div class="kpi-l">Top Brand Share (Terro)'),
    ('$21.2M</div><div class="kpi-l">Total Lure Rev (12M)', '$21.7M</div><div class="kpi-l">Total Lure Rev (12M)'),
]
for old, new in replacements:
    if old in h: h = h.replace(old, new); fixes += 1

# 9. Pack labels
for old, new in [('224.8K units', '240.1K units'), ('798.9K units', '796.0K units'), ('266.9K units', '266.2K units'),
                  ('$2.99M</p>', '$3.18M</p>'), ('$10.61M</p>', '$10.57M</p>'), ('$4.64M</p>', '$4.63M</p>')]:
    if old in h: h = h.replace(old, new); fixes += 1

# 10. Pack brand pies (units)
h = h.replace("[165412, 42934, 11228, 5181]", "[164631, 42369, 11228, 10822, 5013, 168]")
h = h.replace("""["Aunt Fannie's", 'Terro', 'Super Ninja', 'Others'],\n    [164631, 42369, 11228, 10822, 5013, 168]""",
              """["Aunt Fannie's", 'Terro', 'Super Ninja', 'Raid', 'Acme Approved', 'ELEGENZO'],\n    [164631, 42369, 11228, 10822, 5013, 168]""")
h = h.replace("[701671, 64191, 33039]", "[698991, 64191, 32863]")
h = h.replace("[158277, 74639, 15561, 12462, 5923]", "[157740, 74602, 15561, 12462, 5882]")
fixes += 4

# 11. Pack brand pies (revenue)
h = h.replace("[2479524, 370396, 112968, 29197]", "[2467814, 365771, 129759, 112968, 25014, 4183]")
h = h.replace("""["Aunt Fannie's", 'Terro', 'Super Ninja', 'Others'],\n    [2467814, 365771, 129759, 112968, 25014, 4183]""",
              """["Aunt Fannie's", 'Terro', 'Raid', 'Super Ninja', 'Acme Approved', 'ELEGENZO'],\n    [2467814, 365771, 129759, 112968, 25014, 4183]""")
h = h.replace("[9381344, 898033, 327606]", "[9345505, 898033, 325857]")
h = h.replace("[2910710, 1056891, 248693, 236653, 186579]", "[2900837, 1056369, 246969, 236653, 186579]")
fixes += 4

# 12. PSC_RAW updates
h = h.replace("units: 165412, revenue: 2479524", "units: 164631, revenue: 2467814")
h = h.replace("units: 42934,  revenue: 370396", "units: 42369,  revenue: 365771")
h = h.replace("{ brand: 'Others',        units: 5181,   revenue: 29197   }",
              "{ brand: 'Raid',          units: 10822,  revenue: 129759  },\n      { brand: 'Acme Approved', units: 5013,   revenue: 25014   },\n      { brand: 'ELEGENZO',      units: 168,    revenue: 4183    }")
h = h.replace("units: 701671, revenue: 9381344", "units: 698991, revenue: 9345505")
h = h.replace("units: 33039,  revenue: 327606", "units: 32863,  revenue: 325857")
h = h.replace("units: 158277, revenue: 2910710", "units: 157740, revenue: 2900837")
h = h.replace("units: 74639,  revenue: 1056891", "units: 74602,  revenue: 1056369")
h = h.replace("units: 5923,   revenue: 248693", "units: 5882,   revenue: 246969")
fixes += 8

# 13. PSC_COLORS new brands
h = h.replace(
    "'Qualirey':      '#0891b2',",
    "'Qualirey':      '#0891b2',\n    'Raid':          '#ea580c',\n    'ELEGENZO':      '#d97706',\n    'Acme Approved': '#64748b',"
)
fixes += 1

# 14. VOC: Negative Review Insights red bg
h = h.replace(
    '  <div class="card">\n    <h3 style="font-size:.85rem;margin-bottom:10px">Negative Review Insights',
    '  <div class="card" style="background:#fef2f2;border-left:4px solid #dc2626">\n    <h3 style="font-size:.85rem;margin-bottom:10px;color:#991b1b">Negative Review Insights'
)
fixes += 1

# 15. VOC: 2-col CP charts
h = h.replace('.cp-charts{display:grid;grid-template-columns:repeat(4,1fr)', '.cp-charts{display:grid;grid-template-columns:repeat(2,1fr)')
h = h.replace('.cp-chart-wrap{position:relative;height:230px}', '.cp-chart-wrap{position:relative;height:280px}')
h = h.replace('@media(max-width:900px){.cp-charts{grid-template-columns:1fr 1fr}}', '@media(max-width:600px){.cp-charts{grid-template-columns:1fr}}')
fixes += 3

# 16. VOC: vertical bars
h = h.replace(
    """indexAxis: 'y',\n        responsive: true,\n        maintainAspectRatio: false,\n        scales: {\n          x: { stacked: true, grid: { display: false }, ticks: { callback: function(v) { return Math.abs(v); } } },\n          y: { stacked: true, grid: { display: false }, ticks: { font: { size: 10 } } }""",
    """responsive: true,\n        maintainAspectRatio: false,\n        scales: {\n          x: { stacked: true, grid: { display: false }, ticks: { font: { size: 9 }, maxRotation: 35, minRotation: 35 } },\n          y: { stacked: true, grid: { display: false }, ticks: { callback: function(v) { return Math.abs(v); } } }"""
)
fixes += 1

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print(f'Done — {fixes} fixes applied')
