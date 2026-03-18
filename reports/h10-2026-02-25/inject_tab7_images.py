"""Inject Tab 7 — Image Strategy Brief into index.html."""
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

# ── Load competitor image references ─────────────────────────────────────────
with open('listing_comm_data.json', 'r', encoding='utf-8') as f:
    lcd = json.load(f)

def get_main_img(asin):
    """Get best MAIN image URL for an ASIN (prefer medium size ~500px)."""
    imgs = lcd['products'].get(asin, {}).get('images', [])
    for img in imgs:
        if img['variant'] == 'MAIN' and 400 <= img.get('width', 0) <= 600:
            return img['url']
    for img in imgs:
        if img['variant'] == 'MAIN':
            return img['url']
    return ''

comp_imgs = {
    'B01MRHXM0I': get_main_img('B01MRHXM0I'),
    'B0BX4GQF68': get_main_img('B0BX4GQF68'),
    'B07VYPGHFW': get_main_img('B07VYPGHFW'),
    'B0DGWQV8GK': get_main_img('B0DGWQV8GK'),
    'B0D5DJ7V4P': get_main_img('B0D5DJ7V4P'),
}

# ── CSS ──────────────────────────────────────────────────────────────────────
CSS = """
/* Tab 7: Image Strategy */
.is-slot-card{background:#fff;border-radius:10px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,.08);margin-bottom:18px;border-left:5px solid #2563eb;position:relative;overflow:hidden}
.is-slot-num{position:absolute;top:14px;right:18px;font-size:2.2rem;font-weight:900;color:#e2e8f0;line-height:1}
.is-slot-title{font-size:1rem;font-weight:700;color:#0f2942;margin-bottom:2px}
.is-slot-purpose{font-size:.78rem;color:#64748b;margin-bottom:14px;line-height:1.4}
.is-section{margin-bottom:12px}
.is-section-label{font-size:.68rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}
.is-bullets{list-style:none;padding:0;margin:0}
.is-bullets li{font-size:.78rem;color:#1e293b;padding:3px 0 3px 16px;position:relative;line-height:1.5}
.is-bullets li::before{content:'\\2022';position:absolute;left:0;color:#2563eb;font-weight:700}
.is-copy-box{background:#eff6ff;border-radius:6px;padding:10px 14px;font-size:.8rem;color:#1e40af;font-style:italic;line-height:1.5;margin-top:4px}
.is-palette{display:flex;gap:6px;flex-wrap:wrap;margin-top:4px}
.is-swatch{width:28px;height:28px;border-radius:4px;border:1px solid #e2e8f0;display:inline-block}
.is-swatch-label{font-size:.62rem;color:#94a3b8;text-align:center;margin-top:2px}
.is-do-dont{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:6px}
.is-do{background:#f0fdf4;border-radius:6px;padding:10px 12px;border-left:3px solid #16a34a}
.is-dont{background:#fef2f2;border-radius:6px;padding:10px 12px;border-left:3px solid #dc2626}
.is-do h5,.is-dont h5{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.4px;margin-bottom:4px}
.is-do h5{color:#16a34a}.is-dont h5{color:#dc2626}
.is-do li,.is-dont li{font-size:.72rem;line-height:1.5}
.is-ref-imgs{display:flex;gap:8px;flex-wrap:wrap;margin-top:6px}
.is-ref-img{width:64px;height:64px;object-fit:contain;border-radius:4px;border:1px solid #e2e8f0;background:#f8fafc}
.is-data-tag{display:inline-block;font-size:.62rem;font-weight:600;padding:2px 7px;border-radius:10px;margin:2px;white-space:nowrap}
.is-compliance-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.is-compliance-card{background:#fff;border-radius:8px;padding:14px;box-shadow:0 1px 3px rgba(0,0,0,.07)}
.is-compliance-card h4{font-size:.82rem;font-weight:700;color:#1e293b;margin-bottom:8px}
.is-insights-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-bottom:18px}
.is-insight-card{background:#fff;border-radius:8px;padding:14px;box-shadow:0 1px 3px rgba(0,0,0,.07);border-top:3px solid #2563eb}
.is-insight-card .is-pct{font-size:1.4rem;font-weight:800;color:#0f2942;line-height:1}
.is-insight-card .is-label{font-size:.7rem;color:#64748b;margin-top:4px;line-height:1.3}
"""

# ── Helper: build image slot card HTML ───────────────────────────────────────
def slot_card(num, title, purpose, objective, show_items, copy_text, colors, angles, background,
              data_tags, dos, donts, ref_asins, priority_color='#2563eb'):
    show_html = ''.join(f'<li>{item}</li>' for item in show_items)
    dos_html = ''.join(f'<li>{d}</li>' for d in dos)
    donts_html = ''.join(f'<li>{d}</li>' for d in donts)
    tags_html = ''.join(f'<span class="is-data-tag" style="background:{t[1]}22;color:{t[1]};border:1px solid {t[1]}44">{t[0]}</span>' for t in data_tags)
    colors_html = ''.join(f'<div style="text-align:center"><div class="is-swatch" style="background:{c[1]}"></div><div class="is-swatch-label">{c[0]}</div></div>' for c in colors)
    refs_html = ''.join(f'<img class="is-ref-img" src="{comp_imgs.get(a,"")}" alt="{a}" title="{a}" loading="lazy">' for a in ref_asins if comp_imgs.get(a))

    return f'''<div class="is-slot-card" style="border-left-color:{priority_color}">
  <div class="is-slot-num">#{num}</div>
  <div class="is-slot-title">{title}</div>
  <div class="is-slot-purpose">{purpose}</div>

  <div class="is-section">
    <div class="is-section-label">Objective</div>
    <p style="font-size:.78rem;color:#1e293b;line-height:1.5;margin:0">{objective}</p>
  </div>

  <div class="is-section">
    <div class="is-section-label">What to show</div>
    <ul class="is-bullets">{show_html}</ul>
  </div>

  <div class="is-section">
    <div class="is-section-label">Key message / copy</div>
    <div class="is-copy-box">{copy_text}</div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px">
    <div class="is-section">
      <div class="is-section-label">Colors &amp; mood</div>
      <div class="is-palette">{colors_html}</div>
    </div>
    <div class="is-section">
      <div class="is-section-label">Angles &amp; composition</div>
      <p style="font-size:.75rem;color:#475569;margin:0;line-height:1.5">{angles}</p>
    </div>
    <div class="is-section">
      <div class="is-section-label">Background</div>
      <p style="font-size:.75rem;color:#475569;margin:0;line-height:1.5">{background}</p>
    </div>
  </div>

  <div class="is-section">
    <div class="is-section-label">Data backing</div>
    <div>{tags_html}</div>
  </div>

  <div class="is-do-dont">
    <div class="is-do"><h5>&#10003; Do</h5><ul class="is-bullets">{dos_html}</ul></div>
    <div class="is-dont"><h5>&#10007; Don\'t</h5><ul class="is-bullets">{donts_html}</ul></div>
  </div>

  <div class="is-section" style="margin-top:10px">
    <div class="is-section-label">Competitor reference</div>
    <div class="is-ref-imgs">{refs_html}</div>
  </div>
</div>'''


# ── Build all 7 slot cards ──────────────────────────────────────────────────
slots = []

# SLOT 1: Hero Image
slots.append(slot_card(
    num=1,
    title='Hero Image (CTR Driver)',
    purpose='Primary thumbnail seen in search results. Must maximize click-through rate.',
    objective='Product fills 85%+ of frame on pure white background. Packaging visible with key claims ("Non-Toxic", "Fast-Acting") printed on label — the only compliant way to include text.',
    show_items=[
        'Product at 45° angle showing front label + side profile',
        'Packaging clearly visible with printed claims (non-digital text)',
        'If trap is transparent — add subtle hint of colored lure liquid inside',
        'All items included in pack visible (e.g., 4 traps arranged)',
        'Clean, sharp shadows for depth — no harsh lighting'
    ],
    copy_text='No digital text overlays allowed. All messaging must be physically printed on product/packaging: brand name, "Non-Toxic", "Fast-Acting", pack count.',
    colors=[('Pure white', '#FFFFFF'), ('Product color', '#E8B634'), ('Label green', '#22C55E')],
    angles='45° front-angle view. Product slightly tilted to show both front label and side depth. Camera at eye level.',
    background='Pure white (RGB 255, 255, 255). No gradients, no shadows from props, no lifestyle elements.',
    data_tags=[('Amazon compliance', '#dc2626'), ('CTR driver', '#2563eb'), ('85% frame fill', '#7c3aed')],
    dos=[
        'Fill 85%+ of image area with product',
        'Use actual product packaging with printed claims',
        'Show full pack contents if multi-pack',
        'Resolution 2000-3000px JPEG',
        'Test against top 3 competitor thumbnails via PickFu'
    ],
    donts=[
        'No digital text overlays (suppressed by Amazon AI within 1 hour)',
        'No badges, ribbons, or promotional graphics',
        'No lifestyle background or props not included in purchase',
        'No watermarks or brand logos added digitally',
        'Packaging loophole is dead since 2025 — don\'t add text to packaging digitally'
    ],
    ref_asins=['B01MRHXM0I', 'B0BX4GQF68', 'B07VYPGHFW', 'B0DGWQV8GK', 'B0D5DJ7V4P'],
    priority_color='#dc2626'
))

# SLOT 2: Benefit-Led Infographic
slots.append(slot_card(
    num=2,
    title='Benefit-Led Infographic ("The Hook")',
    purpose='First secondary image. Must communicate top 3 benefits in &lt;3 seconds (scannable on mobile).',
    objective='Show the RESULT, not the features: a clean, pest-free kitchen with the trap working discreetly. Overlay 3-5 key benefits with icons.',
    show_items=[
        'Central product image (smaller, ~40% of frame) in a clean kitchen context',
        'Benefit callout #1: "Works in 24 Hours" — clock icon (21.6% of positive reviews)',
        'Benefit callout #2: "Non-Toxic &amp; Safe" — leaf icon (17.3% buyer motivation)',
        'Benefit callout #3: "180-Day Supply" — calendar icon (28.4% expect longer lasting)',
        'Optional #4: "Discreet Design" — eye icon (10.8% positive)',
        'Optional #5: "Ready to Use" — no-assembly icon (16.2% positive)'
    ],
    copy_text='"Works in 24 Hours" &bull; "Non-Toxic &amp; Pet-Safe" &bull; "180-Day Lure Supply" &bull; "Discreet Countertop Design" &bull; "Just Open &amp; Place"',
    colors=[('Soft cream BG', '#FFF8F0'), ('Trust green', '#16A34A'), ('Action orange', '#F97316'), ('Safe blue', '#2563EB')],
    angles='Product centered, icons radiating outward in circular or grid layout. Clean whitespace between elements.',
    background='Soft cream or very light warm gray. Not pure white (differentiate from hero). Subtle kitchen silhouette if needed.',
    data_tags=[('25.7% effectiveness+', '#16a34a'), ('21.6% fast results+', '#2563eb'), ('16.2% easy to use+', '#7c3aed'), ('17.3% safety motivation', '#d97706')],
    dos=[
        'Maximum 5 benefit callouts — fewer is better',
        'Font minimum 32px for headlines, 16px for sub-text (mobile-readable)',
        'Use universally recognized icons (checkmark, leaf, clock)',
        'Focus on BENEFITS not features ("pest-free kitchen" not "contains lure")'
    ],
    donts=[
        'Don\'t list ingredients (boring, not scannable)',
        'Don\'t use more than 25 words total',
        'Don\'t clutter — customer must grasp value in 3 seconds',
        'Don\'t use blue as dominant color (attracts flies — bad subconscious association)'
    ],
    ref_asins=['B01MRHXM0I', 'B0D5DJ7V4P'],
    priority_color='#2563eb'
))

# SLOT 3: Us vs. Them Comparison
slots.append(slot_card(
    num=3,
    title='Us vs. Them Comparison',
    purpose='Address the #3 negative review theme: 13.7% of customers say DIY vinegar traps work better. Counter this directly.',
    objective='Side-by-side comparison showing why a professional trap beats DIY. Address sticking points from competitor reviews (leaks, ugly, messy).',
    show_items=[
        'LEFT side: messy DIY vinegar jar — plastic wrap, toothpick, spilled liquid, flies around but not caught',
        'RIGHT side: elegant fruit fly trap — clean design, flies trapped inside, no mess',
        'Checkmark/X comparison rows: Design &#10003;/&#10007;, Effectiveness &#10003;/&#10007;, Convenience &#10003;/&#10007;, Safety &#10003;/&#10007;',
        'Optional: add cost-per-day comparison (DIY requires daily mixing vs. 45-day lure)'
    ],
    copy_text='"Stop making DIY vinegar traps. Our scientifically formulated lure catches 3x more flies than homemade solutions — without the mess."',
    colors=[('Split layout', '#F1F5F9'), ('Win green', '#16A34A'), ('Lose red', '#DC2626'), ('Neutral', '#64748B')],
    angles='Flat lay or straight-on comparison. Equal frame split (50/50). DIY side slightly darker/messier lighting.',
    background='Left: slightly messy/warm tone. Right: clean, bright, modern. Clear visual hierarchy — right side "wins."',
    data_tags=[('13.7% DIY comparison', '#dc2626'), ('20.6% question mechanism', '#d97706'), ('30.9% effectiveness concern', '#dc2626')],
    dos=[
        'Make the visual contrast DRAMATIC — messy vs. clean',
        'Use a real DIY vinegar jar (plastic wrap, rubber band, toothpick)',
        'Show actual trapped flies in the product (proof of effectiveness)',
        'Include a simple metric: "Catches 3x more" or "Lasts 45 days vs. daily mixing"'
    ],
    donts=[
        'Don\'t name competitor brands (Amazon TOS violation)',
        'Don\'t show identical competitor product (use generic "DIY" solution)',
        'Don\'t make the comparison too complex — max 4 rows',
        'Don\'t use claim you can\'t substantiate (no "100% effective")'
    ],
    ref_asins=['B07VYPGHFW', 'B0D5DJ7V4P'],
    priority_color='#f97316'
))

# SLOT 4: Size & Scale Reference
slots.append(slot_card(
    num=4,
    title='Size &amp; Scale Reference',
    purpose='Prevent returns caused by size misunderstandings. 4.8% of customers want clear usage instructions.',
    objective='Place the trap next to common kitchen objects so customers can visualize exact size on their counter.',
    show_items=[
        'Trap next to a lemon, coffee mug, or standard apple (size reference)',
        'Dimension callouts: width, height, depth in inches/cm',
        'Show trap on a real countertop edge for spatial context',
        'If multi-pack: show all pieces spread out with spacing reference'
    ],
    copy_text='"Compact enough for any countertop — sits discreetly next to your fruit bowl. 3.5" x 3.5" x 1.5"."',
    colors=[('Clean white', '#FFFFFF'), ('Dimension blue', '#3B82F6'), ('Countertop warm', '#D4C5B0')],
    angles='Top-down or 30° angle. Product centered with reference object beside it. Ruler or measurement overlay optional.',
    background='Light countertop surface (marble, wood, or clean white). Natural, warm lighting.',
    data_tags=[('4.8% want clear instructions', '#7c3aed'), ('2.0% "too small"', '#d97706'), ('Return prevention', '#2563eb')],
    dos=[
        'Use universally known objects as references (lemon, coin, hand)',
        'Include exact dimensions with arrows',
        'Show trap in context (on countertop, not floating)',
        'Keep composition clean — only trap + 1-2 reference objects'
    ],
    donts=[
        'Don\'t use objects that vary in size (different apple varieties)',
        'Don\'t overcrowd the frame with too many reference items',
        'Don\'t use human hand as only reference (varies too much)',
        'Don\'t skip dimensions — actual measurements prevent returns'
    ],
    ref_asins=['B01MRHXM0I', 'B0BX4GQF68'],
    priority_color='#3b82f6'
))

# SLOT 5: Lifestyle / Target Audience
slots.append(slot_card(
    num=5,
    title='Lifestyle &amp; Target Audience',
    purpose='Show the product in its primary use environment. 29.2% of customers use it for kitchen fruit fly control.',
    objective='Relatable kitchen scene with the trap placed near a fruit bowl. Model reflects target demographic (homeowner, 30-50, clean modern kitchen).',
    show_items=[
        'Modern, bright kitchen — granite or marble countertop, natural light',
        'Fruit bowl with bananas, apples, grapes (the "trigger" for purchase)',
        'Trap placed discreetly 6-12 inches from fruit bowl',
        'Optional: person (homeowner) in background, relaxed, not focused on trap',
        'Secondary placement: near trash bin or compost area (13.8% use case)'
    ],
    copy_text='"Place near fruit bowls, trash cans, or compost areas — wherever fruit flies breed. Discreet design blends with any kitchen decor."',
    colors=[('Warm kitchen', '#F5E6D0'), ('Natural green', '#4ADE80'), ('Wood tone', '#A0845C'), ('White accent', '#FFFFFF')],
    angles='Wide shot, 30° above eye level. Trap visible but not dominating — the kitchen is the hero, trap is the solution.',
    background='Real kitchen setting. Modern, clean, aspirational but achievable. Natural daylight preferred.',
    data_tags=[('29.2% kitchen use', '#16a34a'), ('13.8% trash/compost', '#d97706'), ('10.8% discreet design+', '#2563eb'), ('5.7% discreet motivation', '#7c3aed')],
    dos=[
        'Use a model that reflects target demographic (homeowner, family kitchen)',
        'Show the trap "in action" — placed in realistic location',
        'Natural lighting — avoid studio feel',
        'Include fruit bowl nearby (the visual trigger that says "I need this")'
    ],
    donts=[
        'Don\'t show close-up of dead flies (gross, turns off buyers)',
        'Don\'t make the trap the center of attention (it should blend in)',
        'Don\'t use cold/clinical lighting (needs to feel warm, home-like)',
        'Don\'t show only the product — the CONTEXT is the message'
    ],
    ref_asins=['B01MRHXM0I', 'B07VYPGHFW', 'B0D5DJ7V4P'],
    priority_color='#16a34a'
))

# SLOT 6: Action Shot / Before-After Proof
slots.append(slot_card(
    num=6,
    title='Action Shot — Before/After Proof',
    purpose='Address the #1 negative theme: 30.9% say "no effect." Visual proof of effectiveness is critical.',
    objective='Side-by-side or split-screen showing: flies swarming (before) → trap placed, flies caught, kitchen clean (after). Include 24h timeline.',
    show_items=[
        'BEFORE (left/top): Fruit bowl surrounded by small flies. Slightly warm, hazy lighting.',
        'AFTER (right/bottom): Same angle — trap placed near fruit, flies visibly trapped inside. Clean, bright lighting.',
        'Timeline overlay: "Day 0 → Day 1" or "Before → After 24 Hours"',
        'Close-up inset: transparent trap window showing trapped flies (proof of mechanism)',
        'Optional: 3D cross-section of trap showing how lure attracts flies'
    ],
    copy_text='"See results within 24 hours. Our lure attracts fruit flies from up to 3 feet away — once inside, they can\'t escape."',
    colors=[('Before warm/hazy', '#FEF3C7'), ('After clean/bright', '#F0FDF4'), ('Proof green', '#16A34A'), ('Timeline blue', '#2563EB')],
    angles='Same camera angle for before and after (critical for visual impact). Straight-on or slight 30° elevation.',
    background='Same kitchen scene, different lighting/mood. Before: warm, slightly hazy. After: bright, clean, fresh.',
    data_tags=[('30.9% "no effect"', '#dc2626'), ('21.6% fast results+', '#16a34a'), ('38.4% expect reliability', '#d97706'), ('25.7% "works great"+', '#16a34a')],
    dos=[
        'Use SAME camera angle and framing for both shots',
        'Include a specific timeframe (24h, 48h — not vague)',
        'Show actual trapped flies in transparent window (the proof)',
        'Make the transformation visually dramatic (lighting shift)'
    ],
    donts=[
        'Don\'t show gross close-ups of dead insects',
        'Don\'t claim "100% elimination" (sets false expectations)',
        'Don\'t make before/after look photoshopped — must feel authentic',
        'Don\'t use different camera angles between before/after'
    ],
    ref_asins=['B01MRHXM0I', 'B0DGWQV8GK', 'B0D5DJ7V4P'],
    priority_color='#7c3aed'
))

# SLOT 7: Everything Included / Value
slots.append(slot_card(
    num=7,
    title='Everything Included / Pack Value',
    purpose='Address value concerns: 15.6% cite "runs out quickly", 28.4% expect longer lasting, 7.4% feel overpriced.',
    objective='Flat lay showing all pack contents with supply duration timeline. Increase perceived value by showing everything the customer gets.',
    show_items=[
        'Flat lay: all traps + all lure refills spread out neatly',
        'Each piece labeled: "Trap #1", "Lure #1" etc.',
        'Supply timeline: "45 days per lure × 4 = 180 days of protection"',
        'Cost breakdown: "$X.XX per month of protection" (value reframe)',
        'Bonus: show trap placement map (kitchen diagram with 4 optimal spots)'
    ],
    copy_text='"Everything you need for 180 days of protection. 4 traps + 4 lure pods = 6 months of pest-free living. That\'s less than $2.50/month."',
    colors=[('Clean white BG', '#FFFFFF'), ('Value gold', '#D97706'), ('Calendar blue', '#3B82F6'), ('Supply green', '#16A34A')],
    angles='True flat lay (top-down, 90°). All items arranged symmetrically with equal spacing.',
    background='Pure white or very light gray. No distracting elements — focus entirely on what\'s in the box.',
    data_tags=[('15.6% "runs out"', '#dc2626'), ('28.4% want longer lasting', '#d97706'), ('7.4% overpriced', '#dc2626'), ('6.9% repeat buyers+', '#16a34a')],
    dos=[
        'Spread out ALL contents — perceived value increases when items are visible',
        'Include a timeline or calendar graphic showing supply duration',
        'Calculate and show cost-per-month (value reframe)',
        'Label each component clearly'
    ],
    donts=[
        'Don\'t show items stacked or bundled (reduces perceived quantity)',
        'Don\'t skip the timeline (duration claim needs visual backing)',
        'Don\'t use lifestyle elements (this is about VALUE, not context)',
        'Don\'t forget to show the instruction card/sheet if included'
    ],
    ref_asins=['B01MRHXM0I', 'B0BX4GQF68', 'B0D5DJ7V4P'],
    priority_color='#d97706'
))

# ── Combine all slot HTML ────────────────────────────────────────────────────
slots_html = '\n'.join(slots)

# ── Build full panel HTML ────────────────────────────────────────────────────
PANEL = f'''<!-- ═══════════════════════════════════════ TAB IS — Image Strategy ═══════ -->
<div id="tis" class="panel">
<h2>Image Strategy Brief &mdash; Fruit Fly Trap Listing</h2>

<div class="insight" style="background:#eff6ff;border-left-color:#2563eb;color:#1e40af">
  <strong>Data-driven image creation brief.</strong> Strategy based on analysis of 5,722 reviews (Tab 4), 5 competitor listing audits (Tab 5), Amazon 2025-2026 compliance research, and the &ldquo;Conversion-First&rdquo; 7-image framework. All percentages reference actual customer review data.
</div>

<!-- KPI overview -->
<div class="is-insights-grid">
  <div class="is-insight-card" style="border-top-color:#dc2626">
    <div class="is-pct" style="color:#dc2626">30.9%</div>
    <div class="is-label">&ldquo;No effect / zero catch&rdquo;<br>Biggest visual challenge to overcome</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#f97316">
    <div class="is-pct" style="color:#f97316">13.7%</div>
    <div class="is-label">&ldquo;DIY vinegar works better&rdquo;<br>Must visually counter this perception</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#16a34a">
    <div class="is-pct" style="color:#16a34a">17.3%</div>
    <div class="is-label">Motivated by safety (kids/pets)<br>Untapped messaging opportunity</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#d97706">
    <div class="is-pct" style="color:#d97706">38.4%</div>
    <div class="is-label">Expect reliable effectiveness<br>Must-prove with visual evidence</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#2563eb">
    <div class="is-pct" style="color:#2563eb">7&ndash;9</div>
    <div class="is-label">Recommended image slots<br>Full stack = 32% higher CVR</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#7c3aed">
    <div class="is-pct" style="color:#7c3aed">29.2%</div>
    <div class="is-label">Kitchen fruit fly control<br>Primary usage scenario &mdash; hero context</div>
  </div>
</div>

<!-- ═════════ THE 7-IMAGE STACK ═════════ -->
<h2 style="margin-top:28px">The 7-Image Stack &mdash; Slot Briefs</h2>
<p style="font-size:.78rem;color:#64748b;margin-bottom:18px;line-height:1.5">Każdy slot opisany jest jako kompletny brief fotograficzny: cel, co pokazać, sugerowany copy, kolory, kąty, tło, dane źródłowe, zalecenia i antyrekomendacje. Kolejność slotów odpowiada frameworkowi &ldquo;Conversion-First&rdquo; (hero &rarr; benefit &rarr; comparison &rarr; scale &rarr; lifestyle &rarr; proof &rarr; value).</p>

{slots_html}

<!-- ═════════ COLOR & VISUAL GUIDELINES ═════════ -->
<h2 style="margin-top:28px">Color &amp; Visual Guidelines</h2>
<div class="card">
  <h3 style="font-size:.88rem;margin-bottom:12px">Recommended Palette</h3>
  <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:14px">
    <div style="text-align:center"><div class="is-swatch" style="background:#16A34A;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Trust Green<br>#16A34A</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#F97316;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Action Orange<br>#F97316</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#2563EB;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Info Blue<br>#2563EB</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#D97706;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Value Gold<br>#D97706</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#DC2626;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Alert Red<br>#DC2626</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#7C3AED;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Premium Purple<br>#7C3AED</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#FFF8F0;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Warm Cream<br>#FFF8F0</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#F1F5F9;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Cool Gray<br>#F1F5F9</div></div>
  </div>
  <div class="note">
    <strong>Psychologia kolor&oacute;w (pest control):</strong> Unikaj dominującego niebieskiego &mdash; przyciąga muchy. Ciepłe odcienie (żółć, pomarańcz) odpychają muchy. Biel jest neutralna i wymagana przez Amazon. Zielony buduje zaufanie (bezpieczeństwo, eko). Pomarańczowy sygnalizuje pilność/akcję.
  </div>
  <div style="margin-top:12px;display:grid;grid-template-columns:1fr 1fr;gap:12px">
    <div>
      <p style="font-size:.72rem;font-weight:700;color:#475569;margin-bottom:6px">Typography</p>
      <ul class="is-bullets">
        <li>Headlines: minimum <strong>32px</strong> (readable on mobile)</li>
        <li>Sub-text: minimum <strong>16px</strong></li>
        <li>Sans-serif font (clean, modern)</li>
        <li>Max 20-25 words per infographic image</li>
      </ul>
    </div>
    <div>
      <p style="font-size:.72rem;font-weight:700;color:#475569;margin-bottom:6px">Mood &amp; Atmosphere</p>
      <ul class="is-bullets">
        <li>Warm, home-like, approachable</li>
        <li>Natural daylight preferred</li>
        <li>Clean but not clinical</li>
        <li>Aspirational kitchen — modern but achievable</li>
      </ul>
    </div>
  </div>
</div>

<!-- ═════════ TECHNICAL COMPLIANCE ═════════ -->
<h2 style="margin-top:28px">Amazon Technical Compliance (2025&ndash;2026)</h2>
<div class="is-compliance-grid">
  <div class="is-compliance-card" style="border-left:4px solid #dc2626">
    <h4>Main Image Rules</h4>
    <ul class="is-bullets">
      <li>Pure white background: <strong>RGB 255, 255, 255</strong></li>
      <li>Product fills <strong>85%+</strong> of frame</li>
      <li>No digital text overlays (AI suppresses within 1h)</li>
      <li>No badges, ribbons, promotional graphics</li>
      <li>No props not included in purchase</li>
      <li>No watermarks or digitally added logos</li>
      <li><strong>Packaging loophole is DEAD</strong> &mdash; Amazon AI detects digital add-ons vs. printed text</li>
    </ul>
  </div>
  <div class="is-compliance-card" style="border-left:4px solid #2563eb">
    <h4>Technical Specs</h4>
    <ul class="is-bullets">
      <li>Resolution: <strong>1600&ndash;3000px</strong> (enables zoom)</li>
      <li>Format: <strong>JPEG</strong> preferred (faster loading)</li>
      <li>Aspect ratio: <strong>1:1</strong> (square, 2000&times;2000 ideal)</li>
      <li>File size: under 10MB</li>
      <li>First 7 images visible on desktop by default</li>
      <li>Always check on <strong>mobile phone</strong> before uploading</li>
    </ul>
  </div>
  <div class="is-compliance-card" style="border-left:4px solid #16a34a">
    <h4>A/B Testing (Manage Your Experiments)</h4>
    <ul class="is-bullets">
      <li>Test main image first (biggest CTR impact)</li>
      <li>Run 6&ndash;8 weeks for statistical confidence</li>
      <li>Make versions <strong>significantly different</strong> (not just angle tweak)</li>
      <li>Don&rsquo;t test during Prime Day / Black Friday</li>
      <li>One element at a time (image only, not image + title)</li>
      <li>Real case: one image change = <strong>32% conversion lift</strong></li>
    </ul>
  </div>
  <div class="is-compliance-card" style="border-left:4px solid #d97706">
    <h4>Mobile Optimization</h4>
    <ul class="is-bullets">
      <li>Fonts must be readable <strong>without zooming</strong></li>
      <li>Critical details highlighted without clutter</li>
      <li>Vertical stacking preferred for before/after (not side-by-side)</li>
      <li>Test on 5&rdquo; phone screen before uploading</li>
      <li>Amazon AI &ldquo;reads&rdquo; image content &mdash; ensure metadata matches visuals</li>
    </ul>
  </div>
</div>

<!-- ═════════ METHODOLOGY ═════════ -->
<div class="note" style="margin-top:22px">
  <strong>Metodologia:</strong> Strategia oparta na danych z: (1) 5 722 recenzji klient&oacute;w Amazon (Tab 4 &mdash; Reviews VOC) z analizą tematów negatywnych/pozytywnych, scenariuszy użycia, motywacji i oczekiwań, (2) audytu listing&oacute;w 5 konkurent&oacute;w (Tab 5 &mdash; Listing Communication) z danymi z Amazon SP-API, (3) analizy luk komunikacyjnych (VoC vs. Listing Gap Analysis), (4) best practices Amazon 2025&ndash;2026 (compliance, A/B testing, mobile optimization), (5) frameworku &ldquo;Conversion-First&rdquo; 7-Image Stack od ekspert&oacute;w e-commerce. Wszystkie procenty odwołują się do rzeczywistych danych z recenzji.
</div>

</div><!-- END TAB IS -->
'''

# ── Read HTML and inject ─────────────────────────────────────────────────────
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject CSS before </style>
html = html.replace('</style>', CSS + '</style>', 1)
print('✓ CSS injected')

# 2. Add tab button
html = html.replace(
    """<div class="tab" onclick="show('tn',this)">6 \u2014 KW Analysis</div>\n</div>""",
    """<div class="tab" onclick="show('tn',this)">6 \u2014 KW Analysis</div>\n  <div class="tab" onclick="show('tis',this)">7 \u2014 Image Strategy</div>\n</div>"""
)
print('✓ Tab button added')

# 3. Insert panel before the last </div><!-- .content --> or before first <script>
# Find the end of the last panel (TAB N) and insert after it
insert_marker = '</div><!-- END TAB N -->'
if insert_marker not in html:
    # Try finding the niche tab end differently
    tn_end = html.rfind('</div>\n\n<script>')
    if tn_end == -1:
        tn_end = html.rfind('</div>\n<script>')
    html = html[:tn_end] + '\n</div>\n\n' + PANEL + '\n' + html[tn_end + len('</div>\n'):]
else:
    html = html.replace(insert_marker, insert_marker + '\n\n' + PANEL)
print('✓ Panel HTML injected')

# ── Write back ───────────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# ── Sync to root ─────────────────────────────────────────────────────────────
import shutil
shutil.copy('index.html', '../../index.html')
print('✓ Synced to root index.html')

print('\n✓ Tab 7 — Image Strategy Brief injected successfully.')
