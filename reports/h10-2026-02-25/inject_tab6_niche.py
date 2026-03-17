"""
Inject Tab 6 — Niche Analysis (Competitor Details + Master Keyword List)
Reads competitors CSV and keywords CSV, builds HTML, injects into index.html.
"""
import csv, sys, re, html as html_mod, json
sys.stdout.reconfigure(encoding='utf-8')

BASE = '../../Data/DD/'
COMP_FILE = BASE + 'niche-NbkRzdCvUi-competitors.csv'
KW_FILE = BASE + 'niche-NbkRzdCvUi-keywords.csv'
HTML_FILE = 'index.html'

esc = html_mod.escape

# ── Parse competitors CSV ─────────────────────────────────────────────────────
with open(COMP_FILE, 'r', encoding='utf-8') as f:
    reader = list(csv.reader(f))

# Row structure: [empty, metric_name, empty, niche_median, empty, empty, ASIN1, ASIN2, ...]
asins = reader[0][6:]  # 13 ASINs
brands = reader[1][6:]
n_comp = len(asins)

# Build competitor data
competitors = []
for i in range(n_comp):
    comp = {
        'asin': asins[i].strip(),
        'brand': brands[i].strip(),
    }
    # Parse each metric row
    for row in reader[2:]:
        metric = row[1].strip() if len(row) > 1 else ''
        val = row[6 + i].strip() if len(row) > 6 + i else ''
        if metric == 'Price': comp['price'] = val
        elif metric == 'Rating': comp['rating'] = val
        elif metric == 'Review Count': comp['reviews'] = val
        elif metric == '30d Sales': comp['sales_30d'] = val
        elif metric == '30d Revenue': comp['rev_30d'] = val
        elif metric == 'Listing Age': comp['age'] = val
        elif metric == 'Strength': comp['strength'] = val
        elif metric == 'KWs on P1': comp['kw_p1'] = val
        elif metric == 'KWs on P1 Percentage': comp['kw_p1_pct'] = val
        elif metric == 'SV on P1 (Share of Voice)': comp['sov'] = val
        elif metric == 'SV on P1 Percentage': comp['sov_pct'] = val
        elif metric == 'Variations': comp['variations'] = val
        elif metric == 'Fulfillment': comp['fulfillment'] = val
        elif metric == 'Seller\'s Country': comp['seller'] = val
    competitors.append(comp)

# Sort by 30d sales descending
def parse_sales(s):
    try: return int(s.replace(',', ''))
    except: return 0
competitors.sort(key=lambda c: parse_sales(c.get('sales_30d', '0')), reverse=True)

# Niche median row
niche_median = {}
for row in reader[2:]:
    metric = row[1].strip() if len(row) > 1 else ''
    val = row[3].strip() if len(row) > 3 else ''
    if metric == 'Price': niche_median['price'] = val
    elif metric == 'Rating': niche_median['rating'] = val
    elif metric == 'Review Count': niche_median['reviews'] = val
    elif metric == '30d Sales': niche_median['sales_30d'] = val
    elif metric == '30d Revenue': niche_median['rev_30d'] = val

# ── Parse keywords CSV ────────────────────────────────────────────────────────
with open(KW_FILE, 'r', encoding='utf-8') as f:
    kw_reader = list(csv.reader(f))

kw_header = kw_reader[0]
kw_asins = kw_header[6:]  # same 13 ASINs

keywords = []
for row in kw_reader[1:]:
    if len(row) < 7: continue
    term = row[1].strip()
    sv_raw = row[2].strip().replace(',', '')
    try: sv = int(sv_raw)
    except: sv = 0
    relevance = row[3].strip()

    # Parse rank for each ASIN
    ranks = {}
    for j, asin in enumerate(kw_asins):
        r = row[6 + j].strip() if len(row) > 6 + j else ''
        try: ranks[asin.strip()] = int(r)
        except: ranks[asin.strip()] = None

    keywords.append({
        'term': term,
        'sv': sv,
        'relevance': relevance,
        'ranks': ranks
    })

print(f'Parsed {len(competitors)} competitors, {len(keywords)} keywords')

# ── Strength badge colors ─────────────────────────────────────────────────────
STRENGTH_COLORS = {
    'Very Strong': ('#166534', '#f0fdf4', '#dcfce7'),
    'Strong': ('#166534', '#f0fdf4', '#dcfce7'),
    'Weak': ('#9a3412', '#fff7ed', '#fed7aa'),
    'Very Weak': ('#991b1b', '#fef2f2', '#fecaca'),
}

# ── Rank color coding (from screenshot) ───────────────────────────────────────
def rank_color(r):
    """Return (bg, text) color tuple based on rank."""
    if r is None: return ('#f8fafc', '#cbd5e1')  # empty/unranked
    if r <= 5: return ('#166534', '#fff')       # dark green
    if r <= 10: return ('#22c55e', '#fff')      # green
    if r <= 20: return ('#86efac', '#166534')   # light green
    if r <= 50: return ('#fde68a', '#92400e')   # yellow/amber
    if r <= 100: return ('#fdba74', '#9a3412')  # orange
    return ('#fca5a5', '#991b1b')               # red (100+)

def rank_cell(r):
    """Build a colored rank cell."""
    if r is None:
        return '<td style="text-align:center;color:#cbd5e1;font-size:.72rem">—</td>'
    bg, txt = rank_color(r)
    return f'<td style="text-align:center;background:{bg};color:{txt};font-weight:600;font-size:.72rem;padding:4px 2px">{r}</td>'

# ── Build competitor cards HTML ───────────────────────────────────────────────
comp_cards = ''
for i, c in enumerate(competitors):
    strength = c.get('strength', '')
    s_colors = STRENGTH_COLORS.get(strength, ('#64748b', '#f8fafc', '#e2e8f0'))

    comp_cards += f'''<div class="card" style="padding:12px 16px;border-left:4px solid {s_colors[2]}">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
    <div>
      <span style="font-size:.82rem;font-weight:700;color:#1e293b">{esc(c['brand'])}</span>
      <a href="https://www.amazon.com/dp/{c['asin']}" target="_blank" rel="noopener" style="font-size:.68rem;color:#2563eb;margin-left:6px;text-decoration:none;border-bottom:1px dotted #93c5fd">{c['asin']}</a>
    </div>
    <span style="font-size:.62rem;font-weight:700;color:{s_colors[0]};background:{s_colors[1]};border:1px solid {s_colors[2]};border-radius:10px;padding:2px 8px">{esc(strength)}</span>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:6px;font-size:.72rem">
    <div style="background:#f8fafc;padding:6px 8px;border-radius:4px"><div style="font-weight:700;color:#1e293b">{esc(c.get('price',''))}</div><div style="color:#94a3b8;font-size:.65rem">Price</div></div>
    <div style="background:#f8fafc;padding:6px 8px;border-radius:4px"><div style="font-weight:700;color:#1e293b">{esc(c.get('sales_30d',''))}</div><div style="color:#94a3b8;font-size:.65rem">30d Sales</div></div>
    <div style="background:#f8fafc;padding:6px 8px;border-radius:4px"><div style="font-weight:700;color:#1e293b">{esc(c.get('rev_30d',''))}</div><div style="color:#94a3b8;font-size:.65rem">30d Revenue</div></div>
    <div style="background:#f8fafc;padding:6px 8px;border-radius:4px"><div style="font-weight:700;color:#1e293b">⭐ {esc(c.get('rating',''))}</div><div style="color:#94a3b8;font-size:.65rem">Rating ({esc(c.get('reviews',''))} rev)</div></div>
    <div style="background:#f8fafc;padding:6px 8px;border-radius:4px"><div style="font-weight:700;color:#1e293b">{esc(c.get('kw_p1',''))}</div><div style="color:#94a3b8;font-size:.65rem">KWs on P1 ({esc(c.get('kw_p1_pct',''))})</div></div>
    <div style="background:#f8fafc;padding:6px 8px;border-radius:4px"><div style="font-weight:700;color:#1e293b">{esc(c.get('sov_pct',''))}</div><div style="color:#94a3b8;font-size:.65rem">Share of Voice</div></div>
    <div style="background:#f8fafc;padding:6px 8px;border-radius:4px"><div style="font-weight:700;color:#1e293b">{esc(c.get('age',''))}</div><div style="color:#94a3b8;font-size:.65rem">Listing Age</div></div>
    <div style="background:#f8fafc;padding:6px 8px;border-radius:4px"><div style="font-weight:700;color:#1e293b">{esc(c.get('fulfillment',''))}</div><div style="color:#94a3b8;font-size:.65rem">Fulfillment</div></div>
  </div>
</div>
'''

# ── Build keyword table (as JSON for JS sorting) ─────────────────────────────
# Use ALL competitors (sorted by sales)
top_asins = [c['asin'] for c in competitors]
top_brands = [c['brand'] for c in competitors]

kw_json = json.dumps([{
    't': k['term'],
    'sv': k['sv'],
    'rl': round(float(k['relevance']), 2) if k['relevance'] else 0,
    'r': [k['ranks'].get(a) for a in top_asins]
} for k in keywords], ensure_ascii=False)

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
/* Tab 6 — Niche Analysis */
.na-comp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:12px;margin-bottom:24px}
.kw-table{width:100%;border-collapse:collapse;font-size:.72rem}
.kw-table thead th{position:sticky;top:0;background:#0f2942;color:#fff;padding:8px 6px;font-size:.68rem;font-weight:600;cursor:pointer;white-space:nowrap;user-select:none}
.kw-table thead th:hover{background:#1e3a5f}
.kw-table thead th .sort-arrow{font-size:.6rem;margin-left:3px;opacity:.5}
.kw-table thead th.sorted .sort-arrow{opacity:1}
.kw-table tbody td{padding:5px 6px;border-bottom:1px solid #f1f5f9}
.kw-table tbody tr:hover td{background:#f8fafc!important}
.kw-sv{font-weight:600;text-align:right;color:#1e293b}
.kw-term{color:#334155;max-width:280px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.kw-legend{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px;font-size:.68rem;color:#64748b}
.kw-legend span{display:inline-flex;align-items:center;gap:4px}
.kw-legend i{display:inline-block;width:16px;height:12px;border-radius:2px}
"""

# ── Panel HTML ────────────────────────────────────────────────────────────────
PANEL = f'''<!-- ═══════════════════════════════════════ TAB N — Niche Analysis ═══════ -->
<div id="tn" class="panel">
<h2>Niche Analysis — Competitor Landscape</h2>

<p class="sec-summary" style="margin-bottom:16px">Competitive intelligence from Helium 10 Niche analysis. {len(competitors)} competitors ranked by 30-day sales. {len(keywords)} tracked keywords with ranking positions.</p>

<!-- Niche Median KPIs -->
<div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:20px">
  <div class="card" style="padding:10px 16px;border-left:4px solid #64748b;flex:1;min-width:140px">
    <div style="font-size:.68rem;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">Niche Median</div>
    <div style="display:flex;gap:20px;flex-wrap:wrap;font-size:.75rem">
      <div><span style="font-weight:700">{esc(niche_median.get('price',''))}</span> <span style="color:#94a3b8">Price</span></div>
      <div><span style="font-weight:700">{esc(niche_median.get('rating',''))}</span> <span style="color:#94a3b8">Rating</span></div>
      <div><span style="font-weight:700">{esc(niche_median.get('reviews',''))}</span> <span style="color:#94a3b8">Reviews</span></div>
      <div><span style="font-weight:700">{esc(niche_median.get('sales_30d',''))}</span> <span style="color:#94a3b8">30d Sales</span></div>
      <div><span style="font-weight:700">{esc(niche_median.get('rev_30d',''))}</span> <span style="color:#94a3b8">30d Revenue</span></div>
    </div>
  </div>
</div>

<!-- Competitor cards -->
<div class="sec-header" style="margin-bottom:12px"><div class="sec-title">Competitor Details</div></div>
<div class="na-comp-grid">
{comp_cards}
</div>

<!-- Keyword Ranking Legend -->
<div class="sec-header" style="margin-bottom:12px"><div class="sec-title">Master Keyword List — {len(keywords)} Keywords</div></div>
<div class="kw-legend">
  <span><i style="background:#166534"></i> 1–5 (Top)</span>
  <span><i style="background:#22c55e"></i> 6–10</span>
  <span><i style="background:#86efac"></i> 11–20</span>
  <span><i style="background:#fde68a"></i> 21–50</span>
  <span><i style="background:#fdba74"></i> 51–100</span>
  <span><i style="background:#fca5a5"></i> 100+</span>
  <span><i style="background:#f8fafc;border:1px solid #e2e8f0"></i> Not ranked</span>
</div>

<!-- Keyword table container -->
<div class="card" style="padding:0;overflow:hidden">
  <div style="max-height:600px;overflow-y:auto">
    <table class="kw-table" id="kwTable">
      <thead>
        <tr>
          <th onclick="sortKW('t')" style="text-align:left;min-width:200px">Keyword <span class="sort-arrow">▼</span></th>
          <th onclick="sortKW('sv')" style="text-align:right;width:80px">Search Vol <span class="sort-arrow">▼</span></th>
          <th onclick="sortKW('rl')" style="text-align:center;width:55px">Relev. <span class="sort-arrow">▼</span></th>
'''

# Add ASIN headers (all competitors)
for j, (a, b) in enumerate(zip(top_asins, top_brands)):
    PANEL += f'          <th style="text-align:center;width:50px;font-size:.58rem;line-height:1.2" title="{a}">{esc(b)}<br><span style="opacity:.6;font-weight:400">{a[-4:]}</span></th>\n'

PANEL += '''        </tr>
      </thead>
      <tbody id="kwBody"></tbody>
    </table>
  </div>
</div>

</div>
'''

# ── JS ────────────────────────────────────────────────────────────────────────
JS = f'''
// ── Tab N — Niche Analysis ─────────────────────────────────────────────────
(function() {{
  const KW_DATA = {kw_json};
  let sortCol = 'sv', sortDir = -1;

  function rankColor(r) {{
    if (r === null || r === undefined) return ['#f8fafc','#cbd5e1'];
    if (r <= 5) return ['#166534','#fff'];
    if (r <= 10) return ['#22c55e','#fff'];
    if (r <= 20) return ['#86efac','#166534'];
    if (r <= 50) return ['#fde68a','#92400e'];
    if (r <= 100) return ['#fdba74','#9a3412'];
    return ['#fca5a5','#991b1b'];
  }}

  function renderKW() {{
    const sorted = [...KW_DATA].sort((a, b) => {{
      let va = a[sortCol], vb = b[sortCol];
      if (sortCol === 't') {{
        va = (va||'').toLowerCase(); vb = (vb||'').toLowerCase();
        return sortDir * va.localeCompare(vb);
      }}
      return sortDir * ((va||0) - (vb||0));
    }});

    const body = document.getElementById('kwBody');
    if (!body) return;
    let html = '';
    for (const k of sorted) {{
      html += '<tr>';
      html += `<td class="kw-term">${{k.t}}</td>`;
      html += `<td class="kw-sv">${{k.sv.toLocaleString()}}</td>`;
      const rlPct = Math.round(k.rl * 100);
      const rlBg = rlPct >= 80 ? '#dcfce7' : rlPct >= 50 ? '#fef9c3' : '#fee2e2';
      const rlTxt = rlPct >= 80 ? '#166534' : rlPct >= 50 ? '#854d0e' : '#991b1b';
      html += `<td style="text-align:center;font-size:.68rem;font-weight:600;background:${{rlBg}};color:${{rlTxt}}">${{rlPct}}%</td>`;
      for (let i = 0; i < k.r.length; i++) {{
        const r = k.r[i];
        if (r === null || r === undefined) {{
          html += '<td style="text-align:center;color:#cbd5e1;font-size:.72rem">—</td>';
        }} else {{
          const [bg, txt] = rankColor(r);
          html += `<td style="text-align:center;background:${{bg}};color:${{txt}};font-weight:600;font-size:.72rem;padding:4px 2px">${{r}}</td>`;
        }}
      }}
      html += '</tr>';
    }}
    body.innerHTML = html;
  }}

  window.sortKW = function(col) {{
    if (sortCol === col) sortDir *= -1;
    else {{ sortCol = col; sortDir = col === 'sv' ? -1 : 1; }}
    renderKW();
  }};

  // Initial render (sorted by SV desc)
  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', renderKW);
  }} else {{
    setTimeout(renderKW, 50);
  }}
}})();
'''

# ── Inject into HTML ──────────────────────────────────────────────────────────
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# 0. Remove existing tn panel if present (idempotent)
html = re.sub(r'<div id="tn" class="panel">.*?(?=</div>\s*<script>)', '', html, flags=re.DOTALL, count=1)
html = re.sub(r'// ── Tab N — Niche Analysis.*?(?=\}\)\(\);.*?// ──|\}\)\(\);\s*$)', '', html, flags=re.DOTALL)

# 1. CSS
if '.na-comp-grid' not in html:
    html = html.replace('</style>', CSS + '</style>', 1)
print('✓ CSS injected')

# 2. Add tab button (before closing </div> of tabs)
if "show('tn'" not in html:
    html = html.replace(
        """</div>\n</div>\n<div class="content">""",
        """  <div class="tab" onclick="show('tn',this)">6 — Niche Analysis</div>\n</div>\n</div>\n<div class="content">"""
    )
    print('✓ Tab button added')

# 3. Panel — insert before closing </div> of content + before <script>
# Handle various patterns of content closing
import re as re2
html = re2.sub(
    r'\n</div><!-- \.content -->\n\n<script>',
    '\n' + PANEL + '\n</div><!-- .content -->\n\n<script>',
    html, count=1
)
if 'id="tn"' not in html:
    # Fallback: try simpler pattern
    html = html.replace('\n</div>\n<script>', '\n' + PANEL + '\n</div>\n<script>', 1)
print('✓ Panel HTML injected')

# 4. JS — insert before closing </script>
html = html.replace(
    '\n</script>\n</body>',
    '\n' + JS + '\n</script>\n</body>'
)
print('✓ JavaScript injected')

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n✓ Tab 6 — Niche Analysis injected')
print(f'  Competitors: {len(competitors)}')
print(f'  Keywords: {len(keywords)}')
print(f'  Top 8 in keyword table: {", ".join(top_brands)}')
