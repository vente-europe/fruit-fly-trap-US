"""Insert 'Unmet Customer Needs' blocks after bullet points in each competitor card."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Unmet needs per competitor, mapped from Claim Theme Coverage (○ = missing)
# + cross-referenced with review data for customer impact
UNMET = {
    'B01MRHXM0I': {  # Terro 4-pack
        'missing': [
            ('Safety / Non-toxic', '#378ADD', '14.1% klientów ceni eko/naturalny skład — brak wzmianki w listingu. Okazja: „non-toxic, plant-based formula."'),
            ('Mechanism / Tech', '#D4537E', '20.6% recenzji kwestionuje działanie wabia lub porównuje z DIY octem. Brak wyjaśnienia jak działa atraktor.'),
        ],
        'strong': [
            ('Effectiveness', '#1D9E75', 'Dobrze komunikowane — ale 30.9% klientów twierdzi „nie działa." Potrzeba konkretnych dowodów (czas, testy).'),
            ('Value / Longevity', '#BA7517', '180 dni supply — mocny claim, potwierdzony przez klientów. Ale 15.6% narzeka na krótką żywotność.'),
            ('Design / Aesthetics', '#7F77DD', 'Apple-shaped design doceniany w recenzjach (10.8%).'),
        ]
    },
    'B0BX4GQF68': {  # Terro 6-pack
        'missing': [
            ('Safety / Non-toxic', '#378ADD', '14.1% klientów ceni eko/naturalny skład — listing nie porusza tego tematu.'),
            ('Mechanism / Tech', '#D4537E', 'Brak wyjaśnienia mechanizmu działania. 13.7% klientów uważa że DIY ocet działa lepiej.'),
        ],
        'strong': [
            ('Effectiveness', '#1D9E75', 'Komunikowane, ale potrzeba wiarygodnych dowodów wobec 30.9% negatywnych opinii.'),
            ('Value / Longevity', '#BA7517', '12-miesięczny zapas — najsilniejszy value claim w kategorii.'),
        ]
    },
    'B07VYPGHFW': {  # Aunt Fannie's
        'missing': [
            ('Design / Aesthetics', '#7F77DD', '10.8% klientów docenia dyskretny design — Aunt Fannie\'s nie komunikuje wyglądu produktu.'),
            ('Mechanism / Tech', '#D4537E', 'Brak wyjaśnienia jak działa atraktor. Okazja: wyróżnić „plant-based formula" technicznie.'),
        ],
        'strong': [
            ('Safety / Non-toxic', '#378ADD', 'Jedyny listing z wyraźnym „non-toxic" — trafia w 14.1% klientów szukających eko rozwiązań.'),
            ('Effectiveness', '#1D9E75', 'Komunikowane i potwierdzone w recenzjach.'),
        ]
    },
    'B0DGWQV8GK': {  # HOT SHOT
        'missing': [
            ('Safety / Non-toxic', '#378ADD', '14.1% klientów ceni naturalność — HOT SHOT (marka chemiczna) nie adresuje obaw o toksyczność.'),
            ('Value / Longevity', '#BA7517', '23% recenzji narzeka na cenę lub trwałość. Listing nie komunikuje wartości ani żywotności.'),
            ('Placement / Targeting', '#639922', '2.9% kupuje na złe owady. Brak info o typie owadów (Drosophila vs. muchy domowe).'),
        ],
        'strong': [
            ('Mechanism / Tech', '#D4537E', 'Jedyny listing wyjaśniający technologię (discreet, hassle-free trap mechanism).'),
            ('Design / Aesthetics', '#7F77DD', 'Komunikowany dyskretny design.'),
        ]
    },
    'B0D5DJ7V4P': {  # Super Ninja
        'missing': [
            ('Design / Aesthetics', '#7F77DD', '10.8% docenia design — Super Ninja nie komunikuje wyglądu mimo atrakcyjnego produktu.'),
            ('Ease of use', '#D85A30', '16.2% klientów ceni prostotę użycia — listing nie podkreśla łatwości setup\'u.'),
        ],
        'strong': [
            ('Safety / Non-toxic', '#378ADD', 'Non-toxic komunikowane — trafia w 14.1% klientów.'),
            ('Mechanism / Tech', '#D4537E', 'Wyjaśnia działanie atraktora — adresuje 20.6% recenzji o DIY/wabie.'),
        ]
    }
}

ASINS = ['B01MRHXM0I', 'B0BX4GQF68', 'B07VYPGHFW', 'B0DGWQV8GK', 'B0D5DJ7V4P']

for asin in ASINS:
    data = UNMET[asin]

    # Build the HTML block
    block = '\n  <div style="margin-bottom:14px;margin-top:14px">\n'
    block += '    <p style="font-size:.68rem;font-weight:600;color:#dc2626;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px">\xe2\x9a\xa0 Unmet Customer Needs \u2014 tematy nieobecne w listingu</p>\n'

    for theme, color, insight in data['missing']:
        block += f'    <div style="display:flex;gap:8px;align-items:flex-start;padding:6px 10px;background:#fef2f2;border-radius:6px;margin-bottom:4px;border-left:3px solid {color}">\n'
        block += f'      <span style="font-size:.72rem;font-weight:700;color:{color};white-space:nowrap;min-width:130px">{theme}</span>\n'
        block += f'      <span style="font-size:.72rem;color:#64748b;line-height:1.4">{insight}</span>\n'
        block += '    </div>\n'

    block += '    <p style="font-size:.68rem;font-weight:600;color:#16a34a;text-transform:uppercase;letter-spacing:.5px;margin-top:10px;margin-bottom:6px">\xe2\x9c\x93 Dobrze komunikowane \u2014 potwierdzone przez klient\u00f3w</p>\n'

    for theme, color, insight in data['strong']:
        block += f'    <div style="display:flex;gap:8px;align-items:flex-start;padding:6px 10px;background:#f0fdf4;border-radius:6px;margin-bottom:4px;border-left:3px solid {color}">\n'
        block += f'      <span style="font-size:.72rem;font-weight:700;color:{color};white-space:nowrap;min-width:130px">{theme}</span>\n'
        block += f'      <span style="font-size:.72rem;color:#64748b;line-height:1.4">{insight}</span>\n'
        block += '    </div>\n'

    block += '  </div>'

    # Find the bullet points section for this ASIN and insert after it
    marker = f'id="comp_body_{asin}"'
    pos = h.find(marker)
    if pos == -1:
        print(f'  WARNING: {asin} not found')
        continue

    # Find "Bullet points" after this marker
    bp_label = '>Bullet points</p>'
    bp_pos = h.find(bp_label, pos)
    if bp_pos == -1:
        print(f'  WARNING: Bullet points not found for {asin}')
        continue

    # Find the closing </div> of the bullet points section
    # Pattern: bullet content...</div>\n  <div> (image gallery)
    close_div = '</div>\n  <div>'
    close_pos = h.find(close_div, bp_pos)
    if close_pos == -1:
        print(f'  WARNING: closing div not found for {asin}')
        continue

    insert_at = close_pos + len('</div>')
    h = h[:insert_at] + block + h[insert_at:]
    print(f'  \u2713 {asin} — {len(data["missing"])} missing, {len(data["strong"])} strong')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print('\nDone — Unmet Customer Needs injected into all 5 competitor cards')
