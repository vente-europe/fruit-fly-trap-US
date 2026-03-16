"""
Inject Reviews VOC tab into the dashboard as Tab 4.
Reads the template, fills it with analysis data, and inserts into index.html.
"""
import json, os, sys, re, html as html_mod

sys.stdout.reconfigure(encoding='utf-8')
DIR = os.path.dirname(__file__)
TEMPLATE = os.path.join(DIR, '..', '..', '..', '..', '_templates', 'tabs', 'reviews-voc.html')
DATA_FILE = os.path.join(DIR, 'reviews_voc_data.json')
HTML_FILE = os.path.join(DIR, 'index.html')

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    D = json.load(f)

# ── Helper ────────────────────────────────────────────────────────────────────
def esc(s):
    return html_mod.escape(s).replace("'", "&#39;").replace("`", "&#96;")

def pct_bar(pct, color='#93c5fd', max_pct=60):
    w = min(pct / max_pct * 100, 100)
    return f'<span class="us-bar-wrap"><span class="us-bar" style="width:{w:.0f}%;background:{color}"></span></span><span>{pct:.1f}%</span>'

# ── Build CSS (only new classes not already in dashboard) ─────────────────────
VOC_CSS = """
/* Tab 4 VOC Reviews */
.voc-sub-tabs{display:flex;background:#fff;border-bottom:2px solid #e2e8f0;padding:0;gap:2px;margin-bottom:16px}
.voc-sub-tab{padding:10px 18px;cursor:pointer;font-size:.8rem;font-weight:600;color:#64748b;border-bottom:3px solid transparent;margin-bottom:-2px;white-space:nowrap}
.voc-sub-tab:hover{color:#1e3a5f}.voc-sub-tab.active{color:#1e3a5f;border-bottom-color:#2563eb}
.voc-sp{display:none}.voc-sp.active{display:block}
.anchor-nav{display:flex;gap:6px;padding:10px 0;margin-bottom:14px;flex-wrap:wrap}
.anchor-nav a{padding:7px 16px;border-radius:20px;font-size:.75rem;font-weight:600;color:#475569;background:#f1f5f9;text-decoration:none;border:1.5px solid #e2e8f0;transition:all .15s}
.anchor-nav a:hover,.anchor-nav a.active{color:#1e3a5f;background:#dbeafe;border-color:#93c5fd}
.sec-header{display:flex;align-items:center;gap:10px;margin-bottom:6px;padding-top:8px}
.sec-title{font-size:1rem;font-weight:700;color:#1e293b}
.sec-summary{font-size:.78rem;color:#64748b;line-height:1.55;margin-bottom:20px;max-width:900px}
.cp-charts{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:10px}
.cp-chart-box{background:#fff;border-radius:8px;padding:14px 14px 10px;box-shadow:0 1px 3px rgba(0,0,0,.07)}
.cp-chart-box h4{font-size:.82rem;font-weight:700;color:#1e293b;margin-bottom:8px}
.cp-chart-wrap{position:relative;height:230px}
.cs-neg-zone{background:#fef2f2;border-radius:10px;padding:18px;margin-bottom:22px}
.nf-row{cursor:pointer;transition:background .15s}
.nf-row:hover td{background:#fff5f5!important}
.nf-arrow{display:inline-block;font-size:.65rem;margin-right:6px;transition:transform .2s;color:#94a3b8}
.nf-row.open .nf-arrow{transform:rotate(90deg)}
.nf-detail{display:none}.nf-detail.open{display:table-row}
.nf-body{padding:8px 16px 12px;background:#fff9f9;border-left:3px solid #fca5a5}
.nf-body ul{margin:0 0 8px 16px;font-size:.75rem;color:#334155;line-height:1.55}
.nf-quotes p{font-size:.72rem;color:#9a3412;font-style:italic;line-height:1.45;margin-bottom:3px}
.cs-pos-zone{background:#f0fdf4;border-radius:10px;padding:18px;margin-bottom:22px}
.pf-row{cursor:pointer;transition:background .15s}
.pf-row:hover td{background:#f0fdf4!important}
.pf-arrow{display:inline-block;font-size:.65rem;margin-right:6px;transition:transform .2s;color:#94a3b8}
.pf-row.open .pf-arrow{transform:rotate(90deg)}
.pf-detail{display:none}.pf-detail.open{display:table-row}
.pf-body{padding:8px 16px 12px;background:#f7fef9;border-left:3px solid #86efac}
.pf-body ul{margin:0 0 8px 16px;font-size:.75rem;color:#334155;line-height:1.55}
.pf-quotes p{font-size:.72rem;color:#166534;font-style:italic;line-height:1.45;margin-bottom:3px}
.si-table{width:100%;border-collapse:collapse;font-size:.78rem}
.si-table th{background:#f8fafc;text-align:left;padding:10px 14px;font-weight:600;color:#475569;border-bottom:2px solid #e2e8f0}
.si-table td{padding:10px 14px;border-bottom:1px solid #f1f5f9;vertical-align:top;line-height:1.55}
.si-badge{display:inline-block;padding:3px 10px;border-radius:12px;font-size:.7rem;font-weight:600}
.us-table{width:100%;border-collapse:collapse;font-size:.78rem}
.us-table th{background:#f8fafc;text-align:left;padding:10px 16px;font-weight:600;color:#475569;border-bottom:2px solid #e2e8f0}
.us-table td{padding:10px 16px;border-bottom:1px solid #f1f5f9;vertical-align:middle}
.us-table tr:hover td{background:#f8fafc}
.us-label{font-weight:600;color:#1e293b;white-space:nowrap}
.us-reason{color:#64748b;line-height:1.5}
.us-pct{text-align:right;white-space:nowrap;color:#1e293b;font-weight:600}
.us-bar-wrap{display:inline-block;width:50px;height:12px;background:#e2e8f0;border-radius:3px;overflow:hidden;vertical-align:middle;margin-right:8px}
.us-bar{height:100%;background:#93c5fd;border-radius:3px}
.pill{display:inline-block;padding:2px 7px;border-radius:4px;font-size:.68rem;font-weight:600;margin:1px 2px}
.pill-red{background:#fef2f2;color:#dc2626}.pill-orange{background:#fff7ed;color:#ea580c}
.pill-amber{background:#fffbeb;color:#d97706}.pill-blue{background:#eff6ff;color:#2563eb}.pill-purple{background:#faf5ff;color:#7c3aed}
.voc-s1{display:inline-block;padding:2px 6px;border-radius:4px;background:#fef2f2;color:#dc2626;font-weight:700;font-size:.75rem}
.voc-s2{display:inline-block;padding:2px 6px;border-radius:4px;background:#fff7ed;color:#ea580c;font-weight:700;font-size:.75rem}
.voc-s3{display:inline-block;padding:2px 6px;border-radius:4px;background:#fffbeb;color:#d97706;font-weight:700;font-size:.75rem}
.voc-s4{display:inline-block;padding:2px 6px;border-radius:4px;background:#f0fdf4;color:#22c55e;font-weight:700;font-size:.75rem}
.voc-s5{display:inline-block;padding:2px 6px;border-radius:4px;background:#f0fdf4;color:#16a34a;font-weight:700;font-size:.75rem}
.review-text{font-size:.78rem;color:#334155;line-height:1.55}
@media(max-width:900px){.cp-charts{grid-template-columns:1fr 1fr}}
"""

# ── Build neg themes table ────────────────────────────────────────────────────
def build_neg_themes():
    rows = ''
    for i, t in enumerate(D['neg_themes']):
        quotes_html = ''.join(f'<p>"…{esc(q[:180])}…"</p>' for q in t['quotes'][:3])
        findings_html = ''.join(f'<li>{esc(f)}</li>' for f in t['findings'])
        rows += f'''<tr class="nf-row" onclick="toggleNFv(this)">
  <td><span class="nf-arrow">▶</span>{esc(t['label'])}</td>
  <td style="text-align:right;font-weight:600">{t['pct']:.1f}%</td>
</tr>
<tr class="nf-detail"><td colspan="2"><div class="nf-body">
  <ul>{findings_html}</ul>
  <div class="nf-quotes">{quotes_html}</div>
</div></td></tr>
'''
    return rows

def build_pos_themes():
    rows = ''
    for i, t in enumerate(D['pos_themes']):
        quotes_html = ''.join(f'<p>"…{esc(q[:180])}…"</p>' for q in t['quotes'][:3])
        findings_html = ''.join(f'<li>{esc(f)}</li>' for f in t['findings'])
        rows += f'''<tr class="pf-row" onclick="togglePFv(this)">
  <td><span class="pf-arrow">▶</span>{esc(t['label'])}</td>
  <td style="text-align:right;font-weight:600">{t['pct']:.1f}%</td>
</tr>
<tr class="pf-detail"><td colspan="2"><div class="pf-body">
  <ul>{findings_html}</ul>
  <div class="pf-quotes">{quotes_html}</div>
</div></td></tr>
'''
    return rows

def build_si_table(insights, color):
    rows = ''
    for si in insights:
        bg = '#fef2f2' if color == 'red' else '#f0fdf4'
        tc = '#991b1b' if color == 'red' else '#166534'
        rows += f'''<tr>
  <td><span class="si-badge" style="background:{bg};color:{tc}">{esc(si['type'])}</span></td>
  <td>{esc(si['finding'])}</td>
  <td>{esc(si['implication'])}</td>
</tr>'''
    return rows

def build_usage_table(items, bar_color='#93c5fd'):
    rows = ''
    max_pct = max(i['pct'] for i in items) if items else 1
    for it in items:
        w = min(it['pct'] / max_pct * 100, 100)
        rows += f'''<tr>
  <td class="us-label">{esc(it['label'])}</td>
  <td class="us-reason">{esc(it['reason'])}</td>
  <td class="us-pct"><span class="us-bar-wrap"><span class="us-bar" style="width:{w:.0f}%;background:{bar_color}"></span></span><span>{it['pct']:.1f}%</span></td>
</tr>'''
    return rows

# ── Star bar data ─────────────────────────────────────────────────────────────
avg_star = sum(d['star'] * d['count'] for d in D['star_dist']) / D['total_reviews']

# ── Panel HTML ────────────────────────────────────────────────────────────────
PANEL = f'''
<!-- ═══════════════════════════════════════ TAB V ══════════════════════════ -->
<div id="tv" class="panel">
<h2>Reviews — Voice of Customer (VOC)</h2>

<div class="insight">
  <strong>VOC analysis across {D['total_reviews']:,} reviews</strong> from 40+ ASINs in the fruit fly trap category. Reviews scraped from Amazon US (Feb 2026). Sentiment themes and customer profile extracted via keyword analysis. Note: scraping is capped at max 100 reviews per star rating per ASIN — star distribution reflects scraped sample, not full Amazon ratings.
</div>

<!-- KPIs -->
<div class="kpis">
  <div class="kpi"><div class="kpi-v">{D['total_reviews']:,}</div><div class="kpi-l">Total Reviews Analyzed</div></div>
  <div class="kpi"><div class="kpi-v" style="color:#0f2942">{D['sentiment_ratio']}</div><div class="kpi-l">Sentiment Ratio (pos:neg)</div></div>
  <div class="kpi"><div class="kpi-v" style="color:#16a34a">{D['pos_pct']:.1f}%</div><div class="kpi-l">Positive (4★+5★)</div></div>
  <div class="kpi"><div class="kpi-v" style="color:#dc2626">{D['neg_pct']:.1f}%</div><div class="kpi-l">Negative (1★–3★)</div></div>
</div>

<!-- Star Distribution Bar -->
<div class="card" style="padding:12px 16px;margin-bottom:20px">
  <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap">
    <div style="font-size:.78rem;font-weight:600;color:#475569;white-space:nowrap">Star Distribution</div>
    <div style="font-size:1.1rem;font-weight:800;color:#0f2942">{avg_star:.2f} <span style="font-size:.7rem;font-weight:400;color:#64748b">avg</span></div>
    <div id="vocStarBar" style="flex:1;display:flex;height:22px;border-radius:4px;overflow:hidden;min-width:200px"></div>
    <div id="vocStarLegend" style="display:flex;gap:10px;flex-wrap:wrap;font-size:.68rem;color:#475569"></div>
  </div>
</div>

<!-- Sub-tabs -->
<div class="voc-sub-tabs">
  <div class="voc-sub-tab active" onclick="showVocSub('voc_ci',this)">Customer Insights</div>
  <div class="voc-sub-tab" onclick="showVocSub('voc_rb',this)">Review Browser</div>
</div>

<!-- ═══ SUB-PANEL: Customer Insights ═══ -->
<div id="voc_ci" class="voc-sp active">

<!-- Anchor nav -->
<div class="anchor-nav">
  <a href="#" onclick="event.preventDefault();document.getElementById('sec-cp-v').scrollIntoView({{behavior:'smooth'}})">Customer Profile</a>
  <a href="#" onclick="event.preventDefault();document.getElementById('sec-us-v').scrollIntoView({{behavior:'smooth'}})">Usage Scenario</a>
  <a href="#" onclick="event.preventDefault();document.getElementById('sec-cs-v').scrollIntoView({{behavior:'smooth'}})">Customer Sentiment</a>
  <a href="#" onclick="event.preventDefault();document.getElementById('sec-bm-v').scrollIntoView({{behavior:'smooth'}})">Buyers Motivation</a>
  <a href="#" onclick="event.preventDefault();document.getElementById('sec-ce-v').scrollIntoView({{behavior:'smooth'}})">Customer Expectations</a>
</div>

<!-- Section 1: Customer Profile -->
<div id="sec-cp-v">
  <div class="sec-header"><div class="sec-title">👤 Customer Profile</div></div>
  <p class="sec-summary">Who buys fruit fly traps, when, where, and what they care about — based on keyword frequency across {D['total_reviews']:,} reviews (positive 4-5★ in green, negative 1-3★ in red).</p>
  <div class="cp-charts">
    <div class="cp-chart-box"><h4>Who</h4><div class="cp-chart-wrap"><canvas id="vocCpWho"></canvas></div></div>
    <div class="cp-chart-box"><h4>When</h4><div class="cp-chart-wrap"><canvas id="vocCpWhen"></canvas></div></div>
    <div class="cp-chart-box"><h4>Where</h4><div class="cp-chart-wrap"><canvas id="vocCpWhere"></canvas></div></div>
    <div class="cp-chart-box"><h4>What</h4><div class="cp-chart-wrap"><canvas id="vocCpWhat"></canvas></div></div>
  </div>
</div>

<!-- Section 2: Usage Scenario -->
<div id="sec-us-v" style="margin-top:28px">
  <div class="sec-header"><div class="sec-title">🎯 Usage Scenarios</div></div>
  <p class="sec-summary">Top reasons and contexts in which customers use fruit fly traps — percentage of all reviews mentioning each scenario.</p>
  <div class="card">
    <table class="us-table"><thead><tr><th>Usage Scenario</th><th>Reason</th><th style="text-align:right">Percentage</th></tr></thead>
    <tbody>{build_usage_table(D['usage_scenarios'])}</tbody></table>
  </div>
</div>

<!-- Section 3: Customer Sentiment -->
<div id="sec-cs-v" style="margin-top:28px">
  <div class="sec-header"><div class="sec-title">💬 Customer Sentiment</div></div>
  <p class="sec-summary">What customers love and hate — themes extracted from {len(D['neg_themes'])} negative and {len(D['pos_themes'])} positive topic clusters. Click any row to expand details and direct quotes.</p>

  <!-- Negative zone -->
  <div class="cs-neg-zone">
    <h3 style="font-size:.88rem;font-weight:700;color:#991b1b;margin-bottom:12px">❌ Negative Feedback — {D['neg_count']:,} reviews (1-3★)</h3>
    <table class="us-table"><thead><tr><th>Negative Topic</th><th style="text-align:right">% of neg reviews</th></tr></thead>
    <tbody>{build_neg_themes()}</tbody></table>
  </div>

  <!-- Negative strategy insights -->
  <div class="card">
    <h3 style="font-size:.85rem;margin-bottom:10px">Negative Review Insights — CPG Strategy</h3>
    <table class="si-table"><thead><tr><th>Analysis</th><th>Finding</th><th>Strategic Implication</th></tr></thead>
    <tbody>{build_si_table(D['neg_strategic_insights'], 'red')}</tbody></table>
  </div>

  <!-- Positive zone -->
  <div class="cs-pos-zone">
    <h3 style="font-size:.88rem;font-weight:700;color:#166534;margin-bottom:12px">✅ Positive Feedback — {D['pos_count']:,} reviews (4-5★)</h3>
    <table class="us-table"><thead><tr><th>Positive Topic</th><th style="text-align:right">% of pos reviews</th></tr></thead>
    <tbody>{build_pos_themes()}</tbody></table>
  </div>

  <!-- Positive strategy insights -->
  <div class="card">
    <h3 style="font-size:.85rem;margin-bottom:10px">Positive Review Insights — CPG Strategy</h3>
    <table class="si-table"><thead><tr><th>Analysis</th><th>Finding</th><th>Strategic Implication</th></tr></thead>
    <tbody>{build_si_table(D['pos_strategic_insights'], 'green')}</tbody></table>
  </div>
</div>

<!-- Section 4: Buyers Motivation -->
<div id="sec-bm-v" style="margin-top:28px">
  <div class="sec-header"><div class="sec-title">🛒 Buyers Motivation</div></div>
  <p class="sec-summary">Why customers purchase fruit fly traps — top purchase drivers from review analysis.</p>
  <div class="card">
    <table class="us-table"><thead><tr><th>Motivation</th><th>Reason</th><th style="text-align:right">Percentage</th></tr></thead>
    <tbody>{build_usage_table(D['buyer_motivations'], '#a78bfa')}</tbody></table>
  </div>
</div>

<!-- Section 5: Customer Expectations -->
<div id="sec-ce-v" style="margin-top:28px">
  <div class="sec-header"><div class="sec-title">⚡ Customer Expectations (Unmet Needs)</div></div>
  <p class="sec-summary">What customers expected but didn't get — top unmet needs from negative reviews ({D['neg_count']:,} reviews, 1-3★).</p>
  <div class="card">
    <table class="us-table"><thead><tr><th>Unmet Need</th><th>Reason</th><th style="text-align:right">% of neg reviews</th></tr></thead>
    <tbody>{build_usage_table(D['customer_expectations'], '#f87171')}</tbody></table>
  </div>
</div>

</div><!-- end voc_ci -->

<!-- ═══ SUB-PANEL: Review Browser ═══ -->
<div id="voc_rb" class="voc-sp">

<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px;align-items:flex-end">
  <div style="display:flex;flex-direction:column;gap:3px">
    <label style="font-size:.7rem;font-weight:600;color:#475569">Rating</label>
    <select id="vocFilterStar" onchange="vocFilterReviews()" style="border:1.5px solid #cbd5e1;border-radius:5px;padding:5px 8px;font-size:.75rem;background:#fff">
      <option value="0">All stars</option>
      <option value="1">1★</option><option value="2">2★</option><option value="3">3★</option>
      <option value="4">4★</option><option value="5">5★</option>
    </select>
  </div>
  <div style="display:flex;flex-direction:column;gap:3px">
    <label style="font-size:.7rem;font-weight:600;color:#475569">Keyword</label>
    <input id="vocFilterKw" oninput="vocFilterReviews()" placeholder="Search reviews..." style="border:1.5px solid #cbd5e1;border-radius:5px;padding:5px 8px;font-size:.75rem;min-width:200px">
  </div>
  <button onclick="document.getElementById('vocFilterStar').value='0';document.getElementById('vocFilterKw').value='';vocFilterReviews()" style="padding:5px 12px;border:1.5px solid #cbd5e1;border-radius:5px;cursor:pointer;font-size:.75rem;font-weight:600;color:#475569;background:#fff">Clear</button>
  <span id="vocRevCount" style="font-size:.72rem;color:#94a3b8"></span>
</div>

<div class="tbl-wrap" style="max-height:600px">
  <table style="width:100%;border-collapse:collapse;font-size:.75rem">
    <thead><tr><th style="width:50px">★</th><th>Review</th></tr></thead>
    <tbody id="vocReviewBody"></tbody>
  </table>
</div>

</div><!-- end voc_rb -->

</div><!-- END TAB V -->
'''

# ── JavaScript ────────────────────────────────────────────────────────────────
star_dist_js = json.dumps(D['star_dist'])
cp_data_js = json.dumps(D['cp_data'])
reviews_js = json.dumps(D['reviews'], ensure_ascii=False)

JS = f'''
// ── Tab V — Reviews VOC ──────────────────────────────────────────────────────
function showVocSub(id, el) {{
  document.querySelectorAll('.voc-sp').forEach(function(p) {{ p.classList.remove('active'); }});
  document.querySelectorAll('.voc-sub-tab').forEach(function(t) {{ t.classList.remove('active'); }});
  document.getElementById(id).classList.add('active');
  el.classList.add('active');
}}
function toggleNFv(row) {{
  row.classList.toggle('open');
  var detail = row.nextElementSibling;
  detail.classList.toggle('open');
}}
function togglePFv(row) {{
  row.classList.toggle('open');
  var detail = row.nextElementSibling;
  detail.classList.toggle('open');
}}

// Star bar
(function() {{
  var dist = {star_dist_js};
  var total = dist.reduce(function(s,d) {{ return s + d.count; }}, 0);
  var bar = document.getElementById('vocStarBar');
  var legend = document.getElementById('vocStarLegend');
  if (!bar) return;
  bar.innerHTML = dist.map(function(d) {{
    var pct = d.count / total * 100;
    return '<div style="width:' + pct.toFixed(1) + '%;background:' + d.color + ';height:100%" title="' + d.star + '★: ' + d.count + ' (' + pct.toFixed(1) + '%)"></div>';
  }}).join('');
  legend.innerHTML = dist.map(function(d) {{
    return '<span style="display:flex;align-items:center;gap:3px"><span style="width:8px;height:8px;border-radius:2px;background:' + d.color + '"></span>' + d.star + '★ ' + d.count + '</span>';
  }}).join('');
}})();

// Customer Profile stacked bar charts
(function() {{
  var cpData = {cp_data_js};
  var charts = [
    ['vocCpWho', cpData.who],
    ['vocCpWhen', cpData.when],
    ['vocCpWhere', cpData.where],
    ['vocCpWhat', cpData.what]
  ];
  charts.forEach(function(cfg) {{
    var el = document.getElementById(cfg[0]);
    if (!el) return;
    var d = cfg[1];
    new Chart(el, {{
      type: 'bar',
      data: {{
        labels: d.labels,
        datasets: [
          {{ label: 'Positive (4-5★)', data: d.pos, backgroundColor: '#22c55e' }},
          {{ label: 'Negative (1-3★)', data: d.neg.map(function(v) {{ return -v; }}), backgroundColor: '#ef4444' }}
        ]
      }},
      options: {{
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        scales: {{
          x: {{ stacked: true, grid: {{ display: false }}, ticks: {{ callback: function(v) {{ return Math.abs(v); }} }} }},
          y: {{ stacked: true, grid: {{ display: false }}, ticks: {{ font: {{ size: 10 }} }} }}
        }},
        plugins: {{
          legend: {{ display: false }},
          datalabels: {{ display: false }},
          tooltip: {{ callbacks: {{ label: function(ctx) {{ return ctx.dataset.label + ': ' + Math.abs(ctx.raw); }} }} }}
        }}
      }}
    }});
  }});
}})();

// Review Browser
var VOC_REVIEWS = {reviews_js};
var VOC_THEMES = {{
  no_effect: /doesn't work|no effect|zero|nothing caught|useless|waste/i,
  packaging: /leak|damage|empty|broken|spill/i,
  too_expensive: /expensive|price|waste|rip.?off|not worth/i,
  weak_lure: /weak|doesn't attract|no interest|ignore/i,
  diy_better: /vinegar|DIY|homemade|apple cider/i,
  slow: /slow|days|week|wait|long time/i,
  smell: /smell|stink|odor/i,
  short_life: /dried|runs out|short|stopped/i
}};
var VOC_THEME_PILLS = {{
  no_effect: '<span class="pill pill-red">no effect</span>',
  packaging: '<span class="pill pill-orange">packaging</span>',
  too_expensive: '<span class="pill pill-amber">price</span>',
  weak_lure: '<span class="pill pill-blue">weak lure</span>',
  diy_better: '<span class="pill pill-purple">DIY better</span>',
  slow: '<span class="pill pill-amber">slow</span>',
  smell: '<span class="pill pill-orange">smell</span>',
  short_life: '<span class="pill pill-red">short life</span>'
}};
var VOC_STAR_BADGES = {{
  1: '<span class="voc-s1">1★</span>',
  2: '<span class="voc-s2">2★</span>',
  3: '<span class="voc-s3">3★</span>',
  4: '<span class="voc-s4">4★</span>',
  5: '<span class="voc-s5">5★</span>'
}};

function vocTagReview(text) {{
  var tags = '';
  for (var k in VOC_THEMES) {{
    if (VOC_THEMES[k].test(text)) tags += VOC_THEME_PILLS[k];
  }}
  return tags;
}}
function vocRenderReviews(list) {{
  var body = document.getElementById('vocReviewBody');
  if (!body) return;
  body.innerHTML = list.map(function(rv) {{
    var escaped = rv.t.replace(/</g,'&lt;').replace(/>/g,'&gt;');
    return '<tr><td>' + (VOC_STAR_BADGES[rv.r] || rv.r + '★') + '</td><td>' + vocTagReview(rv.t) + ' <span class="review-text">' + escaped.substring(0, 400) + (escaped.length > 400 ? '…' : '') + '</span></td></tr>';
  }}).join('');
  document.getElementById('vocRevCount').textContent = list.length + ' reviews shown';
}}
function vocFilterReviews() {{
  var star = parseInt(document.getElementById('vocFilterStar').value) || 0;
  var kw = (document.getElementById('vocFilterKw').value || '').toLowerCase();
  var filtered = VOC_REVIEWS.filter(function(rv) {{
    if (star > 0 && rv.r !== star) return false;
    if (kw && rv.t.toLowerCase().indexOf(kw) === -1) return false;
    return true;
  }});
  vocRenderReviews(filtered);
}}
vocRenderReviews(VOC_REVIEWS);
'''

# ── Inject into HTML ──────────────────────────────────────────────────────────
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CSS
html = html.replace('</style>', VOC_CSS + '</style>', 1)
print('✓ CSS injected')

# 2. Panel — insert before Tab C panel
html = html.replace(
    '<!-- ═══════════════════════════════════════ TAB C',
    PANEL + '\n\n<!-- ═══════════════════════════════════════ TAB C'
)
print('✓ Panel HTML injected')

# 3. JS — insert before the Tab C JS
html = html.replace(
    '// ── Tab C — Listing Communication',
    JS + '\n// ── Tab C — Listing Communication'
)
print('✓ JavaScript injected')

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n✓ Reviews VOC tab injected as Tab 4')
print(f'  Panel: ~{len(PANEL.splitlines())} lines HTML')
print(f'  JS: ~{len(JS.splitlines())} lines')
