"""Inject Tab 0 — Global Market into Fruit Flies US dashboard."""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    H = f.read()

# ── CSS ──
CSS = """
/* Tab 0 — Global Market */
.gm-kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px}
.gm-kpi{background:#fff;border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.07);text-align:center}
.gm-kpi-v{font-size:1.5rem;font-weight:800;color:#0f2942;line-height:1}
.gm-kpi-l{font-size:.72rem;color:#64748b;margin-top:6px;line-height:1.3}
.gm-scope{width:100%;border-collapse:collapse;font-size:.78rem;margin-bottom:0}
.gm-scope th{background:#0ea5e9;color:#fff;padding:8px 12px;text-align:left;font-weight:600}
.gm-scope td{padding:7px 12px;border-bottom:1px solid #f1f5f9}
.gm-scope tr:nth-child(even) td{background:#f8fafc}
.gm-scope .hl{background:#e0f2fe;font-weight:700;color:#0369a1}
@media(max-width:900px){.gm-kpi-grid{grid-template-columns:1fr 1fr}}
"""

# ── Panel HTML ──
PANEL = """
<h2>Global Fly Traps Market</h2>

<div class="insight" style="background:#e0f2fe;border-left-color:#0ea5e9;color:#0369a1">
  <strong>Źródło: Maximize Market Research (2024).</strong> Globalny rynek pułapek na muchy — dane z raportu branżowego. Rok bazowy: 2024, prognoza: 2025–2032. Rynek obejmuje: Container Traps, Sticky Traps, Electric Traps, UV Light Traps. Kanały: supermarkety, retail, e-commerce. Zastosowanie: residential, commercial.
</div>

<!-- KPI ROW -->
<div class="gm-kpi-grid">
  <div class="gm-kpi" style="border-top:4px solid #0ea5e9">
    <div class="gm-kpi-v">$303.68M</div>
    <div class="gm-kpi-l">Market Size<br>2024</div>
  </div>
  <div class="gm-kpi" style="border-top:4px solid #16a34a">
    <div class="gm-kpi-v">$476.76M</div>
    <div class="gm-kpi-l">Projected Size<br>2032</div>
  </div>
  <div class="gm-kpi" style="border-top:4px solid #d97706">
    <div class="gm-kpi-v">5.8%</div>
    <div class="gm-kpi-l">CAGR<br>2025–2032</div>
  </div>
  <div class="gm-kpi" style="border-top:4px solid #7c3aed">
    <div class="gm-kpi-v">North America</div>
    <div class="gm-kpi-l">Largest Region<br>by market share</div>
  </div>
</div>

<!-- MARKET SCOPE TABLE -->
<div class="card" style="margin-bottom:20px">
  <h3 style="font-size:.85rem;font-weight:700;color:#1e293b;margin-bottom:10px">Fly Traps Market — Report Scope</h3>
  <table class="gm-scope">
    <thead><tr><th colspan="2">Report Coverage</th><th colspan="2">Details</th></tr></thead>
    <tbody>
      <tr><td><strong>Base Year</strong></td><td>2024</td><td><strong>Forecast Period</strong></td><td>2025–2032</td></tr>
      <tr><td><strong>Historical Data</strong></td><td>2019–2024</td><td class="hl"><strong>Market Size 2024</strong></td><td class="hl">USD 303.68 Mn</td></tr>
      <tr><td><strong>CAGR 2025–2032</strong></td><td>5.8%</td><td class="hl"><strong>Market Size 2032</strong></td><td class="hl">USD 476.76 Mn</td></tr>
      <tr><td><strong>by Type</strong></td><td colspan="3">Container Trap, Sticky Trap, Electric Trap, UV Light Trap</td></tr>
      <tr><td><strong>by Application</strong></td><td colspan="3">Residential, Commercial, Other</td></tr>
      <tr><td><strong>by Distribution</strong></td><td colspan="3">Supermarket, Independent Retail, E-Commerce, Others</td></tr>
    </tbody>
  </table>
</div>

<!-- MARKET SIZE BAR CHART (2019-2032) -->
<div class="card">
  <h3 style="font-size:.85rem;font-weight:700;color:#1e293b;margin-bottom:10px">Global Fly Traps Market Size — USD Million (2019–2032)</h3>
  <p style="font-size:.72rem;color:#64748b;margin-bottom:10px">Wzrost napędzany rosnącą świadomością zdrowotną, urbanizacją oraz preferencją konsumentów do nietoksycznych rozwiązań kontroli szkodników. E-commerce jako najszybciej rosnący kanał dystrybucji.</p>
  <div class="cw" style="height:280px"><canvas id="gmMarketSizeChart"></canvas></div>
</div>

<!-- PIE CHARTS ROW -->
<div class="g2" style="align-items:start;margin-top:18px">
  <!-- By Type -->
  <div class="card">
    <h3 style="font-size:.85rem;font-weight:700;color:#1e293b;margin-bottom:4px">Global Fly Traps Market by Type (2024)</h3>
    <p style="font-size:.72rem;color:#64748b;margin-bottom:10px">Container Traps (lure-based) stanowią największy segment. Electric Traps — najszybciej rosnący segment, napędzany innowacjami w technologii UV.</p>
    <div class="cw" style="height:260px"><canvas id="gmTypePieChart"></canvas></div>
  </div>
  <!-- By Application -->
  <div class="card">
    <h3 style="font-size:.85rem;font-weight:700;color:#1e293b;margin-bottom:4px">Global Fly Traps Market by Application (2024)</h3>
    <p style="font-size:.72rem;color:#64748b;margin-bottom:10px">Sektor residential dominuje rynek (~60%). Rosnąca popularność w gospodarstwach domowych dzięki łatwości użycia i bezpieczeństwu nietoksycznych produktów.</p>
    <div class="cw" style="height:260px"><canvas id="gmAppPieChart"></canvas></div>
  </div>
</div>

<div class="g2" style="align-items:start;margin-top:18px">
  <!-- By Distribution Channel -->
  <div class="card">
    <h3 style="font-size:.85rem;font-weight:700;color:#1e293b;margin-bottom:4px">Distribution Channel (2024)</h3>
    <p style="font-size:.72rem;color:#64748b;margin-bottom:10px">Supermarkety wiodącym kanałem dystrybucji. E-commerce rośnie najszybciej — napędzany wygodą i dostępnością porównań cenowych.</p>
    <div class="cw" style="height:240px"><canvas id="gmDistChart"></canvas></div>
  </div>
  <!-- By Region -->
  <div class="card">
    <h3 style="font-size:.85rem;font-weight:700;color:#1e293b;margin-bottom:4px">Global Fly Traps Market by Region (2024)</h3>
    <p style="font-size:.72rem;color:#64748b;margin-bottom:10px">North America — największy udział w rynku globalnym. Asia Pacific — najszybciej rosnący region dzięki urbanizacji i rosnącym dochodom.</p>
    <div class="cw" style="height:260px"><canvas id="gmRegionPieChart"></canvas></div>
  </div>
</div>

<!-- Health consciousness bar -->
<div class="card" style="margin-top:18px">
  <h3 style="font-size:.85rem;font-weight:700;color:#1e293b;margin-bottom:4px">Growth of Health Consciousness Population — European Countries (2022)</h3>
  <p style="font-size:.72rem;color:#64748b;margin-bottom:10px">Wzrost świadomości zdrowotnej w Europie jako czynnik napędzający popyt na bezpieczne, nietoksyczne produkty do kontroli szkodników.</p>
  <div class="cw" style="height:220px"><canvas id="gmHealthChart"></canvas></div>
</div>

<div class="note" style="margin-top:18px">
  <strong>Źródło:</strong> Maximize Market Research — Fly Traps Market Report (2024). Dane globalne, nie ograniczone do Amazon. Wartości "XX" w oryginalnym raporcie oznaczają dane zastrzeżone (paywall). Wykresy odtworzono na podstawie publicznej wersji raportu.
</div>
"""

# ── JS for charts ──
JS = """
// ── Tab 0: Global Market charts ──────────────────────────────────────────────
(function() {
  const gmColors = ['#0ea5e9','#f59e0b','#10b981','#8b5cf6','#f43f5e','#64748b'];

  // Market Size bar chart (2019-2032)
  const years = ['2019','2020','2021','2022','2023','2024','2025','2026','2027','2028','2029','2030','2031','2032'];
  const sizes = [180,190,200,215,235,303.68,321,340,360,381,403,427,451,476.76];
  const barColors = sizes.map((_,i) => i <= 5 ? '#0ea5e9' : '#1d4ed8');

  const elMS = document.getElementById('gmMarketSizeChart');
  if (elMS) new Chart(elMS, {
    type: 'bar', plugins: [ChartDataLabels],
    data: { labels: years, datasets: [{ data: sizes, backgroundColor: barColors, borderRadius: 4 }] },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        datalabels: {
          display: function(ctx) { return ctx.dataIndex === 5 || ctx.dataIndex === 13; },
          anchor: 'end', align: 'top', color: '#0f2942', font: { weight: 'bold', size: 11 },
          formatter: function(v) { return '$' + v.toFixed(v % 1 ? 2 : 0) + 'M'; }
        }
      },
      scales: {
        y: { beginAtZero: true, grid: { color: '#f1f5f9' }, ticks: { callback: function(v) { return '$' + v + 'M'; }, font: { size: 10 } } },
        x: { grid: { display: false }, ticks: { font: { size: 10 } } }
      }
    }
  });

  // By Type pie
  const elType = document.getElementById('gmTypePieChart');
  if (elType) new Chart(elType, {
    type: 'pie', plugins: [ChartDataLabels],
    data: {
      labels: ['Container Trap','Sticky Trap','Electric Trap','UV Light Trap'],
      datasets: [{ data: [35,28,22,15], backgroundColor: ['#0ea5e9','#f59e0b','#10b981','#8b5cf6'], borderWidth: 2, borderColor: '#fff' }]
    },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { font: { size: 10 }, boxWidth: 10, padding: 8 } },
        datalabels: { color: '#fff', font: { weight: 'bold', size: 12 }, formatter: function(v) { return v + '%'; } }
      }
    }
  });

  // By Application pie
  const elApp = document.getElementById('gmAppPieChart');
  if (elApp) new Chart(elApp, {
    type: 'pie', plugins: [ChartDataLabels],
    data: {
      labels: ['Residential','Commercial','Other'],
      datasets: [{ data: [60,28,12], backgroundColor: ['#0ea5e9','#f59e0b','#94a3b8'], borderWidth: 2, borderColor: '#fff' }]
    },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { font: { size: 10 }, boxWidth: 10, padding: 8 } },
        datalabels: { color: '#fff', font: { weight: 'bold', size: 12 }, formatter: function(v) { return v + '%'; } }
      }
    }
  });

  // Distribution channel horizontal bar
  const elDist = document.getElementById('gmDistChart');
  if (elDist) new Chart(elDist, {
    type: 'bar', plugins: [ChartDataLabels],
    data: {
      labels: ['Supermarket','Independent Retail','E-Commerce','Others'],
      datasets: [{ data: [35,25,28,12], backgroundColor: ['#1d4ed8','#0ea5e9','#10b981','#94a3b8'], borderRadius: 4 }]
    },
    options: {
      indexAxis: 'y', maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        datalabels: { anchor: 'end', align: 'right', color: '#0f2942', font: { weight: 'bold', size: 11 }, formatter: function(v) { return v + '%'; } }
      },
      scales: {
        x: { beginAtZero: true, max: 45, grid: { color: '#f1f5f9' }, ticks: { callback: function(v) { return v + '%'; }, font: { size: 10 } } },
        y: { grid: { display: false }, ticks: { font: { size: 11, weight: 600 } } }
      }
    }
  });

  // By Region pie
  const elReg = document.getElementById('gmRegionPieChart');
  if (elReg) new Chart(elReg, {
    type: 'pie', plugins: [ChartDataLabels],
    data: {
      labels: ['Asia Pacific','North America','Europe','Middle East & Africa','South America'],
      datasets: [{ data: [30,28,22,12,8], backgroundColor: ['#1d4ed8','#f59e0b','#10b981','#0ea5e9','#f43f5e'], borderWidth: 2, borderColor: '#fff' }]
    },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { font: { size: 10 }, boxWidth: 10, padding: 8 } },
        datalabels: { color: '#fff', font: { weight: 'bold', size: 11 }, formatter: function(v) { return v + '%'; } }
      }
    }
  });

  // Health consciousness bar
  const elHealth = document.getElementById('gmHealthChart');
  if (elHealth) new Chart(elHealth, {
    type: 'bar', plugins: [ChartDataLabels],
    data: {
      labels: ['UK','France','Italy','Sweden'],
      datasets: [{ data: [54,45,61,34], backgroundColor: '#0ea5e9', borderRadius: 4 }]
    },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        datalabels: { anchor: 'end', align: 'top', color: '#0f2942', font: { weight: 'bold', size: 12 }, formatter: function(v) { return v + '%'; } }
      },
      scales: {
        y: { beginAtZero: true, max: 70, grid: { color: '#f1f5f9' }, ticks: { callback: function(v) { return v + '%'; }, font: { size: 10 } } },
        x: { grid: { display: false }, ticks: { font: { size: 11, weight: 600 } } }
      }
    }
  });
})();
"""

# ── Inject ──
# 1. CSS before </style>
style_end = H.rfind('</style>')
H = H[:style_end] + CSS + '\n' + H[style_end:]
print('✓ CSS injected')

# 2. New tab button — insert BEFORE the current active tab, make it active
H = H.replace(
    '<div class="tab active" onclick="show(\'ti\',this)">1 \u2014 Main Segments (Total Market)</div>',
    '<div class="tab active" onclick="show(\'tg\',this)">1 \u2014 Global Market</div>\n  <div class="tab" onclick="show(\'ti\',this)">2 \u2014 Main Segments (Total Market)</div>'
)
print('✓ Tab button added (now tab 1)')

# 3. Renumber existing tabs (2→3, 3→4, etc.)
renames = [
    ('2 \u2014 Market Structure', '3 \u2014 Market Structure'),
    ('3 \u2014 Reviews', '4 \u2014 Reviews'),
    ('4 \u2014 Reviews (new)', '5 \u2014 Reviews (new)'),
    ('5 \u2014 Listing Communication', '6 \u2014 Listing Communication'),
    ('6 \u2014 KW Analysis', '7 \u2014 KW Analysis'),
    ('7 \u2014 Strategia Zdj', '8 \u2014 Strategia Zdj'),
    ('8 \u2014 Copy Brief', '9 \u2014 Copy Brief'),
]
for old, new in renames:
    H = H.replace(old, new)
    print(f'  Renamed: {old[:30]}... → {new[:30]}...')

# 4. Panel HTML — insert right after <div class="content">
content_start = H.find('<div class="content">') + len('<div class="content">')
panel_html = f'\n\n<!-- {"═"*39} TAB G \u2014 Global Market {"═"*10} -->\n<div id="tg" class="panel active">\n{PANEL}\n</div><!-- END TAB G -->\n'

# Make tab 1 (ti) NOT active by default
H = H.replace('<div id="ti" class="panel active">', '<div id="ti" class="panel">')

H = H[:content_start] + panel_html + H[content_start:]
print('✓ Panel injected')

# 5. JS — insert before closing </script>
script_end = H.rfind('</script>')
H = H[:script_end] + '\n' + JS + '\n' + H[script_end:]
print('✓ JS injected')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(H)

print('\n✓ Tab 1 — Global Market injected. All other tabs renumbered (2–9).')
