"""
Inject Tab 4 (Listing Communication) into index.html.
Reads listing_comm_data.json + listing_analysis.json, builds HTML+JS, injects into index.html.
"""
import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')
DIR = os.path.dirname(__file__)

# ── Load data ─────────────────────────────────────────────────────────────────
with open(os.path.join(DIR, 'listing_comm_data.json'), 'r', encoding='utf-8') as f:
    api_data = json.load(f)
with open(os.path.join(DIR, 'listing_analysis.json'), 'r', encoding='utf-8') as f:
    analysis = json.load(f)
with open(os.path.join(DIR, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

# ── Helper: get 500px image URL per variant ───────────────────────────────────
def best_image(images, variant):
    """Pick the ~500px image for a variant (good balance of quality vs load speed)."""
    candidates = [i for i in images if i['variant'] == variant]
    # Prefer 500px, then closest to 500
    candidates.sort(key=lambda i: abs(i['width'] - 500))
    return candidates[0]['url'] if candidates else ''

# ── Build product data for inline JS ─────────────────────────────────────────
ASINS = ['B01MRHXM0I', 'B0BX4GQF68', 'B07VYPGHFW', 'B0DGWQV8GK', 'B0D5DJ7V4P']
products_js = {}
for asin in ASINS:
    api = api_data['products'][asin]
    ana = analysis['products'][asin]
    # Deduplicate images: one URL per variant
    variants = list(dict.fromkeys(i['variant'] for i in api['images']))
    images = []
    for v in variants:
        url = best_image(api['images'], v)
        img_type = ana.get('image_classifications', {}).get(v, 'other')
        images.append({'variant': v, 'url': url, 'type': img_type})
    products_js[asin] = {
        'asin': asin,
        'brand': ana['brand'],
        'short_title': ana['short_title'],
        'title': api['title'],
        'price': ana['price'],
        'bsr': ana['bsr'],
        'rating': ana['rating'],
        'reviews': ana['reviews'],
        'aplus': ana['aplus'],
        'video': ana['video'],
        'main_keyword': ana['main_keyword'],
        'title_structure': ana['title_structure'],
        'hero_message': ana['hero_message'],
        'claim_themes': ana['claim_themes'],
        'key_claims': ana['key_claims'],
        'bullet_points': api['bullet_points'],
        'images': images,
    }

categories = analysis['claim_categories']
benchmark = analysis['benchmark']

# ── 1. CSS ────────────────────────────────────────────────────────────────────
CSS = """
/* Tab 4: Listing Communication */
.lc-subtabs{display:flex;gap:6px;margin-bottom:16px}
.lc-stab{padding:6px 14px;border:1.5px solid #cbd5e1;border-radius:20px;cursor:pointer;font-size:.75rem;font-weight:600;color:#475569;background:#fff;transition:all .15s}
.lc-stab.active{background:#2563eb;color:#fff;border-color:#2563eb}
.lc-sp{display:none}.lc-sp.active{display:block}
.cc{background:#fff;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.07);margin-bottom:12px;overflow:hidden}
.cc-hdr{padding:14px 16px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;border-left:4px solid #2563eb;transition:background .15s}
.cc-hdr:hover{background:#f8fafc}
.cc-body{display:none;padding:0 16px 16px;border-top:1px solid #f1f5f9}
.cc-body.open{display:block}
.ig{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;margin-top:10px}
.ig-slot{position:relative;background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;overflow:hidden;text-align:center}
.ig-slot img{width:100%;aspect-ratio:1;object-fit:contain;display:block}
.ig-badge{position:absolute;top:3px;left:3px;font-size:.58rem;padding:2px 5px;border-radius:3px;font-weight:600;color:#fff;text-transform:uppercase;letter-spacing:.3px}
.ig-var{font-size:.62rem;color:#94a3b8;padding:2px 0;text-align:center}
.tm-table{width:100%;border-collapse:collapse;font-size:.73rem}
.tm-table th,.tm-table td{text-align:center;padding:7px 8px;border-bottom:1px solid #f1f5f9}
.tm-table th{background:#f8fafc;color:#475569;font-weight:600;font-size:.7rem}
.tm-table td:first-child,.tm-table th:first-child{text-align:left}
.tm-chk{font-size:.9rem;font-weight:700}.tm-miss{color:#e2e8f0;font-size:.9rem}
.cl-badge{display:inline-block;font-size:.65rem;font-weight:500;padding:2px 7px;border-radius:10px;margin:2px;white-space:nowrap}
.ts-tag{display:inline-block;font-size:.68rem;padding:2px 6px;border-radius:4px;margin:2px}
.gap-badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:.68rem;font-weight:600}
.gap-high{background:#fee2e2;color:#991b1b}.gap-med{background:#fef3c7;color:#92400e}.gap-low{background:#dcfce7;color:#15803d}
.bench-card{padding:14px;margin-bottom:10px;background:#fff;border:.5px solid #e2e8f0;border-radius:8px}
.bench-card h4{font-size:.82rem;font-weight:600;color:#1e293b;margin:0 0 8px}
.bench-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:.75rem;margin-bottom:8px}
.bench-lbl{font-size:.62rem;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px}
.bench-rec{margin-top:8px;padding:6px 10px;background:#eff6ff;border-radius:6px;font-size:.73rem;color:#1e40af}
"""

# ── 2. Tab button ─────────────────────────────────────────────────────────────
TAB_BUTTON = '  <div class="tab" onclick="show(\'tc\',this)">4 — Listing Communication</div>'

# ── 3. Panel HTML ─────────────────────────────────────────────────────────────
# Build theme matrix HTML
def build_theme_matrix():
    cats = categories
    rows = ''
    for cat in cats:
        cells = f'<td style="color:{cat["color"]};font-weight:500">{cat["label"]}</td>'
        for asin in ASINS:
            p = analysis['products'][asin]
            has = cat['id'] in p['claim_themes']
            cells += f'<td><span class="tm-chk" style="color:{cat["color"]}">●</span></td>' if has else '<td><span class="tm-miss">○</span></td>'
        rows += f'<tr>{cells}</tr>\n'
    header = '<th>Theme</th>' + ''.join(
        f'<th>{analysis["products"][a]["brand"]}<br><span style="font-weight:400;font-size:.62rem;color:#94a3b8">{analysis["products"][a]["short_title"]}</span></th>'
        for a in ASINS
    )
    return f'<table class="tm-table"><thead><tr>{header}</tr></thead><tbody>{rows}</tbody></table>'

# Build image comparison grid
IMG_TYPE_COLORS = {
    'hero':'#378ADD','lifestyle':'#1D9E75','infographic':'#7F77DD','comparison':'#D85A30',
    'scale':'#BA7517','package':'#639922','detail':'#D4537E','value':'#BA7517','other':'#94a3b8'
}
IMG_TYPE_LABELS = {
    'hero':'Hero','lifestyle':'Lifestyle','infographic':'Info','comparison':'Compare',
    'scale':'Scale','package':'Package','detail':'Detail','value':'Value','other':'Other'
}

def build_image_grid():
    types_order = ['hero','lifestyle','infographic','comparison','scale','detail','value','package']
    header = '<th>Image type</th>' + ''.join(
        f'<th>{analysis["products"][a]["brand"]}</th>' for a in ASINS
    )
    rows = ''
    for t in types_order:
        any_has = any(
            t in [img['type'] for img in products_js[a]['images']]
            for a in ASINS
        )
        if not any_has:
            continue
        c = IMG_TYPE_COLORS.get(t, '#94a3b8')
        cells = f'<td style="color:{c};font-weight:500"><span style="display:inline-block;width:6px;height:6px;border-radius:1px;background:{c};margin-right:4px;vertical-align:middle"></span>{IMG_TYPE_LABELS.get(t,t)}</td>'
        for asin in ASINS:
            count = sum(1 for img in products_js[asin]['images'] if img['type'] == t)
            if count > 1:
                cells += f'<td><span style="color:{c};font-weight:600">{count}x</span></td>'
            elif count == 1:
                cells += f'<td><span style="color:{c};font-weight:600">✓</span></td>'
            else:
                cells += '<td><span style="color:#e2e8f0">—</span></td>'
        rows += f'<tr>{cells}</tr>\n'
    # Total row
    cells = '<td style="font-weight:600">Total slots</td>'
    for asin in ASINS:
        n = len(products_js[asin]['images'])
        cells += f'<td style="font-weight:700;font-size:.82rem">{n}</td>'
    rows += f'<tr style="border-top:1.5px solid #e2e8f0">{cells}</tr>'
    return f'<table class="tm-table"><thead><tr>{header}</tr></thead><tbody>{rows}</tbody></table>'

# Build competitor cards
def stars_html(rating):
    full = int(rating)
    half = rating - full >= 0.3
    empty = 5 - full - (1 if half else 0)
    return '<span style="color:#d97706;letter-spacing:1px">' + '★' * full + ('½' if half else '') + '☆' * empty + f' <span style="color:#64748b;font-size:.75rem">{rating}</span></span>'

def bsr_color(bsr):
    if bsr <= 100: return '#16a34a'
    if bsr <= 500: return '#d97706'
    return '#94a3b8'

def build_competitor_cards():
    cards = ''
    for asin in ASINS:
        p = products_js[asin]
        a = analysis['products'][asin]

        # Header
        badges = f'<span style="background:{bsr_color(p["bsr"])};color:#fff;font-size:.65rem;padding:2px 8px;border-radius:10px;font-weight:600">BSR #{p["bsr"]:,}</span>'
        if p['aplus']:
            badges += ' <span style="border:1px solid #7F77DD;color:#7F77DD;font-size:.65rem;padding:1px 6px;border-radius:10px;font-weight:500">A+</span>'
        if p['video']:
            badges += ' <span style="border:1px solid #D4537E;color:#D4537E;font-size:.65rem;padding:1px 6px;border-radius:10px;font-weight:500">Video</span>'

        header = f'''<div class="cc-hdr" onclick="toggleComp('{asin}')" style="border-left-color:{bsr_color(p['bsr'])}">
  <div style="flex:1;min-width:0">
    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px">
      <span style="font-weight:600;font-size:.88rem;color:#0f2942">{p['brand']}</span> {badges}
    </div>
    <p style="font-size:.73rem;color:#64748b;margin:2px 0 4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{p['title']}</p>
    <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap">
      {stars_html(p['rating'])}
      <span style="font-size:.73rem;color:#64748b">{p['reviews']:,} reviews</span>
      <span style="font-size:.88rem;font-weight:600;color:#0f2942">${p['price']}</span>
      <span style="font-size:.68rem;color:#94a3b8">keyword: "{p['main_keyword']}"</span>
    </div>
  </div>
  <span id="comp_arrow_{asin}" style="font-size:.85rem;color:#94a3b8;margin-left:8px;flex-shrink:0">▼</span>
</div>'''

        # Title structure
        ts = a['title_structure']
        ts_colors = {'brand':'#7F77DD','product_type':'#1D9E75','key_benefit':'#378ADD','use_case':'#D85A30','differentiator':'#D4537E','pack_size':'#BA7517'}
        ts_labels = {'brand':'Brand','product_type':'Product type','key_benefit':'Key benefit','use_case':'Use case','differentiator':'Differentiator','pack_size':'Pack size'}
        ts_html = ''
        for key, color in ts_colors.items():
            val = ts.get(key)
            if val:
                ts_html += f'<span class="ts-tag" style="border:1px solid {color}33;background:{color}11"><span style="color:{color};font-weight:500;font-size:.6rem">{ts_labels[key]}:</span> {val}</span> '

        # Key claims
        cat_map = {c['id']: c for c in categories}
        claims_html = ''
        for cl in p['key_claims']:
            cat = cat_map.get(cl['cat'], {'color':'#94a3b8'})
            claims_html += f'<span class="cl-badge" style="border:1px solid {cat["color"]};color:{cat["color"]}">{cl["text"]}</span> '

        # Bullet points
        bullets_html = ''
        for bp in p['bullet_points']:
            # Extract the header part (before colon) and body
            if ':' in bp and bp.index(':') < 40:
                hdr, body = bp.split(':', 1)
                bullets_html += f'<p style="font-size:.73rem;margin:3px 0;line-height:1.4;color:#1e293b"><strong style="color:#0f2942">{hdr}:</strong>{body}</p>'
            else:
                bullets_html += f'<p style="font-size:.73rem;margin:3px 0;line-height:1.4;color:#1e293b">{bp}</p>'

        # Image gallery
        imgs_html = ''
        for img in p['images']:
            tc = IMG_TYPE_COLORS.get(img['type'], '#94a3b8')
            tl = IMG_TYPE_LABELS.get(img['type'], img['type'])
            imgs_html += f'''<div class="ig-slot">
  <span class="ig-badge" style="background:{tc}">{tl}</span>
  <img src="{img['url']}" alt="{img['variant']}" loading="lazy">
  <div class="ig-var">{img['variant']}</div>
</div>'''

        body = f'''<div id="comp_body_{asin}" class="cc-body">
  <div style="margin-top:14px;margin-bottom:14px">
    <p style="font-size:.68rem;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">Title structure</p>
    <div style="display:flex;flex-wrap:wrap;gap:4px">{ts_html}</div>
  </div>
  <div style="margin-bottom:14px">
    <p style="font-size:.68rem;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">Hero message</p>
    <p style="font-size:.82rem;font-style:italic;color:#1e293b;margin:0;padding:8px 12px;background:#f8fafc;border-radius:6px;line-height:1.4">"{p['hero_message']}"</p>
  </div>
  <div style="margin-bottom:14px">
    <p style="font-size:.68rem;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">Key claims</p>
    <div style="display:flex;flex-wrap:wrap;gap:2px">{claims_html}</div>
  </div>
  <div style="margin-bottom:14px">
    <p style="font-size:.68rem;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">Bullet points</p>
    {bullets_html}
  </div>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
      <p style="font-size:.68rem;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin:0">Image gallery ({len(p['images'])} slots)</p>
      <span style="font-size:.62rem;color:#cbd5e1">Source: Amazon SP-API Catalog Items</span>
    </div>
    <div class="ig">{imgs_html}</div>
  </div>
</div>'''

        cards += f'<div class="cc">{header}{body}</div>\n'
    return cards

# Build benchmark section
def build_benchmark():
    dims = benchmark['dimensions']
    html_out = ''
    for d in dims:
        html_out += f'''<div class="bench-card">
  <h4>{d['label']}</h4>
  <div class="bench-row">
    <div><div class="bench-lbl">Leader pattern</div><div style="color:#475569;line-height:1.5">{d['leader_pattern']}</div></div>
    <div><div class="bench-lbl">Recommendation</div><div class="bench-rec">{d['recommendation']}</div></div>
  </div>
</div>'''
    return html_out

def build_gaps():
    gaps = benchmark['gaps']
    rows = ''
    for g in gaps:
        pc = {'high':'gap-high','medium':'gap-med','low':'gap-low'}[g['priority']]
        rows += f'''<div style="display:grid;grid-template-columns:100px 1fr 140px 70px;gap:8px;padding:8px 0;border-bottom:.5px solid #f1f5f9;align-items:center;font-size:.75rem">
  <span style="font-weight:600;color:#475569">{g['area']}</span>
  <span style="color:#1e293b">{g['gap']}</span>
  <span style="color:#94a3b8;font-size:.68rem">{g['who']}</span>
  <span class="gap-badge {pc}">{g['priority']}</span>
</div>'''
    return rows

# KPI row
avg_price = sum(products_js[a]['price'] for a in ASINS) / len(ASINS)
avg_rating = sum(products_js[a]['rating'] for a in ASINS) / len(ASINS)
avg_reviews = sum(products_js[a]['reviews'] for a in ASINS) // len(ASINS)
with_aplus = sum(1 for a in ASINS if products_js[a]['aplus'])
with_video = sum(1 for a in ASINS if products_js[a]['video'])
avg_images = sum(len(products_js[a]['images']) for a in ASINS) // len(ASINS)

PANEL_HTML = f'''
<!-- ═══════════════════════════════════════ TAB C ══════════════════════════ -->
<div id="tc" class="panel">
<h2>Listing Communication Analysis</h2>

<div class="insight" style="background:#eff6ff;border-left-color:#2563eb;color:#1e40af">
  <strong>Competitive listing audit.</strong> Images and attributes pulled from Amazon SP-API Catalog Items API (2026-03-15). Claim themes and image classifications analyzed from bullet points and listing content. 5 lure-segment competitors compared.
</div>

<!-- Sub-tabs -->
<div class="lc-subtabs">
  <div class="lc-stab active" onclick="showLC('tc_listing',this)">Listing Communication</div>
  <div class="lc-stab" onclick="showLC('tc_bench',this)">Competitive Benchmark</div>
</div>

<!-- ── Sub-tab 1: Listing Communication ────────────────────────────────────── -->
<div id="tc_listing" class="lc-sp active">

<!-- KPI row -->
<div class="kpis" style="margin-bottom:18px">
  <div class="kpi"><div class="kpi-v">${avg_price:.2f}</div><div class="kpi-l">Avg price<br>across 5 listings</div></div>
  <div class="kpi"><div class="kpi-v">{avg_rating:.1f} ★</div><div class="kpi-l">Avg rating<br>across 5 listings</div></div>
  <div class="kpi"><div class="kpi-v">{avg_reviews:,}</div><div class="kpi-l">Avg reviews<br>across 5 listings</div></div>
  <div class="kpi"><div class="kpi-v">{with_aplus}/{len(ASINS)}</div><div class="kpi-l">Have A+ Content</div></div>
  <div class="kpi"><div class="kpi-v">{with_video}/{len(ASINS)}</div><div class="kpi-l">Have listing video</div></div>
  <div class="kpi"><div class="kpi-v">{avg_images}</div><div class="kpi-l">Avg image slots<br>per listing</div></div>
</div>

<!-- Claim theme matrix -->
<div class="card">
  <h3>Claim Theme Coverage</h3>
  <p style="font-size:.72rem;color:#64748b;margin-bottom:10px">Which communication themes each competitor addresses in their bullet points and key claims</p>
  {build_theme_matrix()}
  <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:10px">
    {''.join(f'<span style="font-size:.62rem;display:flex;align-items:center;gap:3px"><span style="width:7px;height:7px;border-radius:1px;background:{c["color"]};display:inline-block"></span><span style="color:#94a3b8">{c["label"]}</span></span>' for c in categories)}
  </div>
</div>

<!-- Image slot comparison -->
<div class="card">
  <h3>Image Slot Comparison</h3>
  <p style="font-size:.72rem;color:#64748b;margin-bottom:10px">Image types used across listing slots — source: Amazon SP-API Catalog Items (includedData=images)</p>
  {build_image_grid()}
</div>

<!-- Competitor cards -->
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;margin-top:22px">
  <h3 style="margin:0;font-size:.88rem;font-weight:700;color:#1e293b">Competitor Listing Details</h3>
  <div style="display:flex;gap:6px">
    <button onclick="document.querySelectorAll('.cc-body').forEach(b=>b.classList.add('open'));document.querySelectorAll('[id^=comp_arrow_]').forEach(a=>a.textContent='▲')" style="font-size:.68rem;padding:4px 10px;cursor:pointer;background:#fff;border:1px solid #cbd5e1;border-radius:5px;color:#475569">Expand all</button>
    <button onclick="document.querySelectorAll('.cc-body').forEach(b=>b.classList.remove('open'));document.querySelectorAll('[id^=comp_arrow_]').forEach(a=>a.textContent='▼')" style="font-size:.68rem;padding:4px 10px;cursor:pointer;background:#fff;border:1px solid #cbd5e1;border-radius:5px;color:#475569">Collapse all</button>
  </div>
</div>
{build_competitor_cards()}

</div><!-- end tc_listing -->

<!-- ── Sub-tab 2: Competitive Benchmark ────────────────────────────────────── -->
<div id="tc_bench" class="lc-sp">

<div class="card">
  <h3>How Do These Listings Compare?</h3>
  <p style="font-size:.72rem;color:#64748b;margin-bottom:14px">Analysis across 6 critical listing dimensions — leader patterns vs. actionable recommendations</p>
  {build_benchmark()}
</div>

<div class="card">
  <h3>Key Gaps & Opportunities</h3>
  <p style="font-size:.72rem;color:#64748b;margin-bottom:10px">Identified weaknesses and missed opportunities across competitor listings</p>
  {build_gaps()}
</div>

<div class="note" style="margin-top:18px">
  <strong>Data sources:</strong> Amazon SP-API Catalog Items API (images, titles, bullet points, product types) · Helium 10 X-Ray (BSR, estimated revenue, reviews) · Manual analysis (claim themes, image classification, hero messages).
</div>

</div><!-- end tc_bench -->

</div><!-- END TAB C -->
'''

# ── 4. JS for sub-tab switching and card toggle ───────────────────────────────
JS = """
// ── Tab C — Listing Communication ────────────────────────────────────────────
function showLC(subId, el) {
  document.querySelectorAll('.lc-sp').forEach(function(p) { p.classList.remove('active'); });
  document.querySelectorAll('.lc-stab').forEach(function(t) { t.classList.remove('active'); });
  document.getElementById(subId).classList.add('active');
  el.classList.add('active');
}
function toggleComp(asin) {
  var body = document.getElementById('comp_body_' + asin);
  body.classList.toggle('open');
  var arrow = document.getElementById('comp_arrow_' + asin);
  arrow.textContent = body.classList.contains('open') ? '\\u25B2' : '\\u25BC';
}
"""

# ── Inject into HTML ──────────────────────────────────────────────────────────
# 1. CSS before </style>
html = html.replace('</style>', CSS + '</style>', 1)

# 2. Tab button before </div> of .tabs
html = html.replace(
    '  <div class="tab" onclick="show(\'tl\',this)">3 — Reviews</div>\n</div>',
    '  <div class="tab" onclick="show(\'tl\',this)">3 — Reviews</div>\n' + TAB_BUTTON + '\n</div>'
)

# 3. Panel HTML before </div><!-- .content -->
html = html.replace('</div><!-- .content -->', PANEL_HTML + '\n</div><!-- .content -->')

# 4. JS before the window.addEventListener('load'...)
html = html.replace(
    "// ── Fix: resize all charts after init",
    JS + "\n// ── Fix: resize all charts after init"
)

# ── Write output ──────────────────────────────────────────────────────────────
with open(os.path.join(DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html)

print('✓ Tab 4 injected successfully.')
print(f'  CSS: ~{len(CSS.splitlines())} lines')
print(f'  Panel HTML: ~{len(PANEL_HTML.splitlines())} lines')
print(f'  JS: ~{len(JS.splitlines())} lines')
