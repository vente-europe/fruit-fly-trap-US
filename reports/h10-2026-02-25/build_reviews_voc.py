"""
Build Reviews VOC (Voice of Customer) analysis from review data files.
Processes all reviews, conducts analysis, outputs reviews_voc_data.json.
"""
import json, os, sys, re
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
DIR = os.path.dirname(__file__)
REVIEWS_DIR = os.path.join(DIR, '..', '..', 'Data', 'reviews')

# ── 1. Load and deduplicate all reviews ───────────────────────────────────────
all_reviews = []
seen = set()

# Load raw dataset files
for fname in os.listdir(REVIEWS_DIR):
    if not fname.startswith('dataset_') or not fname.endswith('.json'):
        continue
    if '(1)' in fname:
        continue  # skip duplicate
    fpath = os.path.join(REVIEWS_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for r in data:
        text = (r.get('reviewDescription') or '').strip()
        title = (r.get('reviewTitle') or '').strip()
        stars = r.get('ratingScore', 0)
        asin = r.get('productAsin', '')
        key = f"{asin}_{stars}_{text[:50]}"
        if key not in seen and text:
            seen.add(key)
            all_reviews.append({
                'r': stars,
                't': text,
                'title': title,
                'asin': asin,
                'verified': r.get('isVerified', False),
                'date': r.get('date', ''),
            })

# Also load aggregated files
for fname, star_key, text_key in [
    ('hs_reviews.json', 'stars', 'review'),
    ('terro_reviews.json', 'stars', 'review'),
]:
    fpath = os.path.join(REVIEWS_DIR, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    reviews_list = data.get('reviews', data) if isinstance(data, dict) else data
    for r in reviews_list:
        text = (r.get(text_key) or '').strip()
        stars = r.get(star_key, 0)
        key = f"agg_{stars}_{text[:50]}"
        if key not in seen and text:
            seen.add(key)
            all_reviews.append({
                'r': stars,
                't': text,
                'title': '',
                'asin': '',
                'verified': True,
                'date': '',
            })

print(f'Total unique reviews: {len(all_reviews)}')

# ── 2. Star distribution ─────────────────────────────────────────────────────
star_counts = Counter(r['r'] for r in all_reviews)
total = len(all_reviews)
star_dist = []
star_colors = {1: '#dc2626', 2: '#ea580c', 3: '#f59e0b', 4: '#22c55e', 5: '#16a34a'}
for s in range(1, 6):
    star_dist.append({'star': s, 'count': star_counts.get(s, 0), 'color': star_colors[s]})
    print(f'  {s}★: {star_counts.get(s, 0)} ({star_counts.get(s, 0)/total*100:.1f}%)')

pos_reviews = [r for r in all_reviews if r['r'] >= 4]
neg_reviews = [r for r in all_reviews if r['r'] <= 3]
pos_pct = len(pos_reviews) / total * 100
neg_pct = len(neg_reviews) / total * 100
print(f'\nPositive (4-5★): {len(pos_reviews)} ({pos_pct:.1f}%)')
print(f'Negative (1-3★): {len(neg_reviews)} ({neg_pct:.1f}%)')

# ── 3. Customer Profile (who/when/where/what) ────────────────────────────────
def count_keyword(reviews, patterns):
    """Count reviews matching each pattern, split by pos/neg."""
    results = {}
    for label, pattern in patterns:
        pos = sum(1 for r in reviews if r['r'] >= 4 and re.search(pattern, r['t'], re.I))
        neg = sum(1 for r in reviews if r['r'] <= 3 and re.search(pattern, r['t'], re.I))
        if pos + neg > 0:
            results[label] = {'pos': pos, 'neg': neg}
    return results

who_patterns = [
    ('Family/Kids', r'\b(kid|child|family|baby|toddler)\b'),
    ('Pet owner', r'\b(pet|dog|cat|animal)\b'),
    ('Homeowner', r'\b(home|house|apartment|condo)\b'),
    ('Kitchen user', r'\b(kitchen|cook|chef)\b'),
    ('Gardener', r'\b(garden|plant|compost|outdoor)\b'),
    ('Gift buyer', r'\b(gift|recommend|friend|neighbor)\b'),
]
when_patterns = [
    ('Summer', r'\b(summer|hot|warm|july|august|june)\b'),
    ('Within days', r'\b(within.*(day|hour)|overnight|next day|immediately)\b'),
    ('Within weeks', r'\b(within.*week|couple weeks|few weeks|2 weeks)\b'),
    ('Seasonal', r'\b(season|spring|fall|autumn)\b'),
    ('Year-round', r'\b(year.round|all year|every year|annual)\b'),
]
where_patterns = [
    ('Kitchen', r'\b(kitchen|counter|countertop|sink)\b'),
    ('Near fruit', r'\b(fruit|banana|apple|produce|bowl)\b'),
    ('Trash/compost', r'\b(trash|garbage|compost|bin|waste)\b'),
    ('Bathroom', r'\b(bathroom|bath)\b'),
    ('Window', r'\b(window|windowsill)\b'),
    ('Dining area', r'\b(dining|table|eating)\b'),
    ('Garage/basement', r'\b(garage|basement|laundry)\b'),
]
what_patterns = [
    ('Effectiveness', r'\b(work|effective|catch|caught|trap|kill)\b'),
    ('Speed', r'\b(fast|quick|immediate|overnight|hour)\b'),
    ('Design', r'\b(design|look|attractive|discreet|ugly|cute|apple)\b'),
    ('Value/Price', r'\b(price|expensive|cheap|value|worth|money)\b'),
    ('Safety', r'\b(safe|toxic|chemical|natural|organic|eco)\b'),
    ('Smell/Odor', r'\b(smell|odor|scent|stink|fragrance)\b'),
    ('Ease of use', r'\b(easy|simple|setup|open|plug|hassle)\b'),
    ('Duration', r'\b(last|duration|long|month|week|days|refill|replace)\b'),
    ('DIY comparison', r'\b(vinegar|diy|homemade|apple cider)\b'),
]

who_data = count_keyword(all_reviews, who_patterns)
when_data = count_keyword(all_reviews, when_patterns)
where_data = count_keyword(all_reviews, where_patterns)
what_data = count_keyword(all_reviews, what_patterns)

def format_cp(data):
    sorted_items = sorted(data.items(), key=lambda x: x[1]['pos'] + x[1]['neg'], reverse=True)
    return {
        'labels': [k for k, v in sorted_items],
        'pos': [v['pos'] for k, v in sorted_items],
        'neg': [v['neg'] for k, v in sorted_items],
    }

cp_data = {
    'who': format_cp(who_data),
    'when': format_cp(when_data),
    'where': format_cp(where_data),
    'what': format_cp(what_data),
}

# ── 4. Negative feedback themes ──────────────────────────────────────────────
neg_themes = [
    ('No effect / zero catch', r"(doesn'?t|does not|didn'?t|did not|not).{0,20}(work|catch|trap|effective)|zero|no (flies|bugs|effect|catch)|useless|waste of money|doesn't do anything", []),
    ('DIY / vinegar works better', r'vinegar|diy|homemade|apple cider.*(better|more|same)|made my own', []),
    ('Weak attractant / lure', r'(weak|no|doesn.t).{0,15}(attract|lure)|not attract|flies.*(ignore|avoid|won.t go)', []),
    ('Overpriced / poor value', r'(over.?price|too expensive|waste of money|rip.?off|not worth|better off buying)', []),
    ('Packaging leaks / damage', r'(leak|spill|damage|broken|crack|mess).{0,20}(package|box|seal|bottle|arrive|open)|arrived damaged', []),
    ('Too small / tiny', r'(too small|tiny|smaller than|expected bigger|disappoint.*size)', []),
    ('Short duration / runs out', r'(dried|runs? out|short|only last|stopped working after|week|dry)', []),
    ('Sticky tape issues', r'(sticky|tape|glue|adhesive|stick).{0,20}(not|doesn|didn|fall|poor|weak)', []),
    ('Attracts wrong insects', r'(wrong|other|different).{0,15}(insect|bug|fly|flies)|doesn.t catch fruit flies|house flies|gnats? (only|instead)', []),
    ('Messy / hard to set up', r'(mess|spill|hard to|difficult).{0,15}(set ?up|open|use|assemble)|liquid everywhere', []),
    ('Fake reviews suspected', r'(fake|paid|bot|shill|vine|suspicious).{0,15}(review|rating)', []),
    ('Smell / odor issues', r'(smell|stink|odor|scent).{0,10}(bad|terrible|awful|strong|gross)', []),
]

for i, (label, pattern, quotes) in enumerate(neg_themes):
    matching = [r for r in neg_reviews if re.search(pattern, r['t'], re.I)]
    count = len(matching)
    pct = count / len(neg_reviews) * 100 if neg_reviews else 0
    # Get top quotes
    sample = matching[:5]
    quotes_list = [r['t'][:200] for r in sample]
    neg_themes[i] = (label, pattern, count, pct, quotes_list,
                     [f"Found in {count} of {len(neg_reviews)} negative reviews ({pct:.1f}%)"])

# ── 5. Positive feedback themes ──────────────────────────────────────────────
pos_themes = [
    ('Highly effective / works great', r'(work|effective|catch|caught|trap|kill).{0,20}(great|well|perfect|amazing|excellent|fantastic|awesome)|highly effective|really works', []),
    ('Would recommend / buy again', r'(recommend|buy again|reorder|repurchase|repeat|love this|best|must.have)', []),
    ('Eco-friendly / natural', r'(eco|natural|organic|safe|non.toxic|chemical.free|plant.based|green)', []),
    ('Fast results', r'(fast|quick|immediate|overnight|hour|within.*(day|minute)|right away|instantly)', []),
    ('Easy to use / simple setup', r'(easy|simple|no.?hassle|just (open|set|place|plug)|effortless)', []),
    ('Elegant / discreet design', r'(discreet|elegant|attractive|cute|nice look|blend|sleek|apple.shape|design)', []),
    ('No smell / odorless', r'(no smell|odorless|no odor|doesn.t smell|unscented)', []),
    ('Better than DIY', r'(better than|replace|instead of).{0,15}(vinegar|diy|homemade)', []),
    ('Good value / worth price', r'(good value|worth|great price|fair price|affordable|bargain)', []),
    ('Long lasting', r'(long.last|last.*(month|week|long)|extended|durable)', []),
]

for i, (label, pattern, quotes) in enumerate(pos_themes):
    matching = [r for r in pos_reviews if re.search(pattern, r['t'], re.I)]
    count = len(matching)
    pct = count / len(pos_reviews) * 100 if pos_reviews else 0
    sample = matching[:5]
    quotes_list = [r['t'][:200] for r in sample]
    pos_themes[i] = (label, pattern, count, pct, quotes_list,
                     [f"Found in {count} of {len(pos_reviews)} positive reviews ({pct:.1f}%)"])

# ── 6. Usage scenarios ────────────────────────────────────────────────────────
usage_scenarios = [
    ('Kitchen fruit fly control', 'Customers dealing with fruit flies near kitchen counters, fruit bowls, and produce',
     r'(kitchen|counter|fruit).{0,30}(fly|flies|gnat|trap)'),
    ('Summer infestation response', 'Seasonal spike — customers dealing with sudden increase in flying insects',
     r'(summer|season|hot|warm|spike|infestat|sudden|overwhelm)'),
    ('Eco-friendly alternative', 'Looking for non-toxic, chemical-free solutions safe for food areas',
     r'(eco|natural|organic|non.toxic|safe|chemical.free)'),
    ('Replacing DIY vinegar traps', 'Upgrading from homemade apple cider vinegar traps',
     r'(vinegar|diy|homemade|apple cider|tried everything)'),
    ('Gift or recommendation', 'Bought on recommendation from friends/family or as a gift',
     r'(gift|recommend|friend|neighbor|told me|suggested)'),
    ('Trash / compost area', 'Managing flies near waste bins, compost, and garbage areas',
     r'(trash|garbage|compost|bin|waste|recycle)'),
    ('Repeat / loyal purchase', 'Returning customers who buy regularly',
     r'(again|repurchase|reorder|always buy|stock up|loyal|every (year|summer))'),
    ('Quick overnight solution', 'Need immediate results — expecting to catch flies within hours',
     r'(overnight|immediate|quick|hour|urgent|emergency|desperate)'),
    ('Discreet home pest control', 'Want something that blends in with home decor',
     r'(discreet|blend|decor|attractive|not.*ugly|guest|visible)'),
    ('Multiple room placement', 'Using multiple traps across different rooms',
     r'(multiple|every room|throughout|several|all over|each room)'),
]

usage_results = []
for label, reason, pattern in usage_scenarios:
    matching = [r for r in all_reviews if re.search(pattern, r['t'], re.I)]
    pct = len(matching) / total * 100
    usage_results.append({'label': label, 'reason': reason, 'pct': round(pct, 1)})

usage_results.sort(key=lambda x: x['pct'], reverse=True)

# ── 7. Buyer motivations ─────────────────────────────────────────────────────
motivations = [
    ('Fruit fly problem', 'Active fruit fly infestation driving purchase',
     r'(fruit fl|gnat|flying insect|bug).{0,20}(problem|issue|infest|plague|annoying|everywhere)'),
    ('Kitchen hygiene', 'Keeping kitchen clean and pest-free near food',
     r'(kitchen|food|clean|hygien|sanit)'),
    ('DIY methods failed', 'Previous home remedies didn\'t work',
     r'(tried|diy|vinegar|homemade).{0,20}(fail|didn|not work|gave up)'),
    ('Seasonal urgency', 'Summer/warm weather causing sudden pest increase',
     r'(summer|season|warm|sudden|spike|urgent)'),
    ('Safe for kids/pets', 'Need non-toxic option due to children or animals',
     r'(kid|child|pet|dog|cat|baby|safe|non.toxic|family)'),
    ('Discreet appearance', 'Want traps that don\'t look ugly in the home',
     r'(discreet|look|blend|ugly|attractive|decor|guest)'),
    ('Recommendation', 'Bought based on reviews, word of mouth, or social media',
     r'(recommend|review|friend|tiktok|youtube|viral|suggested|told me)'),
    ('Convenience', 'Looking for ready-to-use, low-effort solution',
     r'(easy|simple|convenient|ready|hassle|effort|just (open|set|place))'),
    ('Price / deal', 'Motivated by price point, deals, or coupons',
     r'(price|deal|coupon|sale|affordable|cheap|value|subscription)'),
]

motivation_results = []
for label, reason, pattern in motivations:
    matching = [r for r in all_reviews if re.search(pattern, r['t'], re.I)]
    pct = len(matching) / total * 100
    motivation_results.append({'label': label, 'reason': reason, 'pct': round(pct, 1)})
motivation_results.sort(key=lambda x: x['pct'], reverse=True)

# ── 8. Customer expectations / unmet needs ────────────────────────────────────
expectations = [
    ('Reliable effectiveness', 'Expects the trap to actually catch and reduce flies',
     r'(doesn.t|not|didn.t|zero|no).{0,20}(work|catch|effective|trap)|useless|waste'),
    ('Longer lasting effect', 'Wants traps to work for more than a few days/weeks',
     r'(last|long|dried|runs? out|short|refill|replace|week|month)'),
    ('Better value for money', 'Perceives current price as too high for results',
     r'(expensive|overpriced|waste of money|not worth|poor value|rip.off)'),
    ('Mess-free setup', 'Expects clean, no-spill experience when opening/using',
     r'(mess|spill|leak|liquid|sticky|drip|pour)'),
    ('Odorless operation', 'Doesn\'t want strong smells near food or living areas',
     r'(smell|odor|stink|scent|fragrance)'),
    ('Works on all flying insects', 'Expects trap to catch gnats, house flies, not just fruit flies',
     r'(gnat|house fl|mosquito|different|other).{0,15}(insect|bug|fl)'),
    ('Discreet appearance', 'Wants traps that are not ugly or noticeable',
     r'(ugly|eyesore|discreet|blend|visible|guest|embarrass)'),
    ('Clear usage instructions', 'Confused about placement, timing, or how the product works',
     r'(instruct|confus|how to|where to|placement|direction)'),
    ('Eco-friendly materials', 'Expects sustainable, recyclable, or biodegradable design',
     r'(eco|recycle|sustainab|biodegradab|plastic|waste|environment)'),
    ('Refillable / reusable design', 'Wants to refill existing trap rather than buy new ones',
     r'(refill|reuse|reusable|replace.*(lure|bait)|cartridge)'),
]

expectation_results = []
for label, reason, pattern in expectations:
    matching = [r for r in neg_reviews if re.search(pattern, r['t'], re.I)]
    pct = len(matching) / len(neg_reviews) * 100 if neg_reviews else 0
    expectation_results.append({'label': label, 'reason': reason, 'pct': round(pct, 1)})
expectation_results.sort(key=lambda x: x['pct'], reverse=True)

# ── 9. Strategic insights ─────────────────────────────────────────────────────
neg_si = [
    {'type': 'Efficacy Crisis', 'finding': 'Majority of negative reviews report zero or near-zero fly catch', 'implication': 'Product effectiveness is the #1 driver of dissatisfaction — any new product must solve this first'},
    {'type': 'DIY Benchmark', 'finding': 'Customers compare commercial traps to vinegar DIY and often find DIY better', 'implication': 'The "just use vinegar" narrative undermines entire category — need clear mechanism differentiation'},
    {'type': 'Price Sensitivity', 'finding': 'Perceived poor value when product doesn\'t work drives strong negative sentiment', 'implication': 'Value proposition must be proven before premium pricing — trial/guarantee could help'},
    {'type': 'Expectation Gap', 'finding': 'Customers expect overnight results but many traps need days to work', 'implication': 'Listing copy should set realistic timeline expectations (24-72h) to reduce disappointment'},
    {'type': 'Packaging Risk', 'finding': 'Liquid traps frequently leak in transit or upon opening', 'implication': 'Packaging engineering is a competitive advantage — leak-proof design is a differentiator'},
    {'type': 'Duration Issue', 'finding': 'Traps that dry out or stop working within 1-2 weeks generate complaints', 'implication': 'Longevity claims must be realistic — "up to 45 days" claims damage trust if product fails at day 10'},
    {'type': 'Wrong Pest', 'finding': 'Some customers expect traps to catch house flies, gnats, or mosquitoes', 'implication': 'Clear targeting in title/bullets: "for fruit flies (Drosophila)" prevents wrong-product reviews'},
    {'type': 'Trust Damage', 'finding': 'Multiple customers note suspicious 5-star reviews and Vine program', 'implication': 'Over-reliance on Vine reviews inflates ratings temporarily but erodes long-term trust'},
]
pos_si = [
    {'type': 'Proven Mechanism', 'finding': 'Apple-shaped lure traps and liquid bait consistently rated highest for effectiveness', 'implication': 'Lure-based mechanism is validated by customers — build on this, don\'t reinvent'},
    {'type': 'Loyalty Driver', 'finding': 'High repurchase intent among satisfied customers — "buy every summer"', 'implication': 'Subscription/auto-reorder opportunity for brands with proven effectiveness'},
    {'type': 'Safety Premium', 'finding': 'Non-toxic/natural positioning resonates strongly with kitchen users', 'implication': 'Safety messaging is a conversion driver — highlight prominently in bullets and images'},
    {'type': 'Speed Wins', 'finding': 'Fast-acting claims validated by happy customers — "caught 20 flies overnight"', 'implication': 'Speed-to-catch is the #1 positive surprise — use in hero messaging and A+ content'},
    {'type': 'Design Matters', 'finding': 'Discreet/attractive design mentioned positively even when effectiveness is average', 'implication': 'Design is a tiebreaker — when two products work equally well, the better-looking one wins'},
    {'type': 'Eco Advantage', 'finding': 'Natural/eco-friendly positioning creates emotional connection beyond pest control', 'implication': 'Sustainability messaging differentiates from chemical-based competitors'},
    {'type': 'DIY Upgrade', 'finding': 'Customers who switched from vinegar traps and found the product better become advocates', 'implication': '"Better than DIY" comparison in images/A+ content converts the skeptical vinegar crowd'},
    {'type': 'Word of Mouth', 'finding': 'High recommendation rate — many 5-star reviews mention telling friends/family', 'implication': 'Referral program or "share with a friend" insert could amplify organic growth'},
]

# ── 10. Build review browser data (sample 300 most recent/diverse) ────────────
# Sort by date descending, take up to 300
review_browser = sorted(all_reviews, key=lambda r: r.get('date', ''), reverse=True)[:300]
review_browser_js = [{'r': r['r'], 't': r['t'][:500]} for r in review_browser]

# ── Output ────────────────────────────────────────────────────────────────────
output = {
    'total_reviews': total,
    'star_dist': star_dist,
    'pos_count': len(pos_reviews),
    'neg_count': len(neg_reviews),
    'pos_pct': round(pos_pct, 1),
    'neg_pct': round(neg_pct, 1),
    'sentiment_ratio': f"{len(pos_reviews)}:{len(neg_reviews)}",
    'cp_data': cp_data,
    'neg_themes': [
        {'label': t[0], 'count': t[2], 'pct': round(t[3], 1), 'quotes': t[4], 'findings': t[5]}
        for t in neg_themes if t[2] > 0
    ],
    'pos_themes': [
        {'label': t[0], 'count': t[2], 'pct': round(t[3], 1), 'quotes': t[4], 'findings': t[5]}
        for t in pos_themes if t[2] > 0
    ],
    'usage_scenarios': usage_results,
    'buyer_motivations': motivation_results,
    'customer_expectations': expectation_results,
    'neg_strategic_insights': neg_si,
    'pos_strategic_insights': pos_si,
    'reviews': review_browser_js,
}

out_file = os.path.join(DIR, 'reviews_voc_data.json')
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f'\n✓ Saved to {out_file}')
print(f'  Star dist: {[d["count"] for d in star_dist]}')
print(f'  Neg themes: {len([t for t in neg_themes if t[2] > 0])}')
print(f'  Pos themes: {len([t for t in pos_themes if t[2] > 0])}')
print(f'  Usage scenarios: {len(usage_results)}')
print(f'  Review browser: {len(review_browser_js)} reviews')
