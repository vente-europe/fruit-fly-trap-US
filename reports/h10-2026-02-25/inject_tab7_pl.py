"""Inject Tab 7 — Image Strategy Brief (POLISH) into index.html."""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('listing_comm_data.json', 'r', encoding='utf-8') as f:
    lcd = json.load(f)

def get_main_img(asin):
    imgs = lcd['products'].get(asin, {}).get('images', [])
    for img in imgs:
        if img['variant'] == 'MAIN' and 400 <= img.get('width', 0) <= 600:
            return img['url']
    for img in imgs:
        if img['variant'] == 'MAIN':
            return img['url']
    return ''

comp_imgs = {a: get_main_img(a) for a in ['B01MRHXM0I','B0BX4GQF68','B07VYPGHFW','B0DGWQV8GK','B0D5DJ7V4P']}

def slot_card(num, title, purpose, objective, show_items, copy_text, colors, angles, background,
              data_tags, dos, donts, ref_asins, priority_color='#2563eb'):
    show_html = ''.join(f'<li>{i}</li>' for i in show_items)
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
    <div class="is-section-label">Cel</div>
    <p style="font-size:.78rem;color:#1e293b;line-height:1.5;margin:0">{objective}</p>
  </div>
  <div class="is-section">
    <div class="is-section-label">Co pokaza\u0107</div>
    <ul class="is-bullets">{show_html}</ul>
  </div>
  <div class="is-section">
    <div class="is-section-label">Sugerowany tekst / copy</div>
    <div class="is-copy-box">{copy_text}</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px">
    <div class="is-section">
      <div class="is-section-label">Kolory i nastr\u00f3j</div>
      <div class="is-palette">{colors_html}</div>
    </div>
    <div class="is-section">
      <div class="is-section-label">K\u0105ty i kompozycja</div>
      <p style="font-size:.75rem;color:#475569;margin:0;line-height:1.5">{angles}</p>
    </div>
    <div class="is-section">
      <div class="is-section-label">T\u0142o</div>
      <p style="font-size:.75rem;color:#475569;margin:0;line-height:1.5">{background}</p>
    </div>
  </div>
  <div class="is-section">
    <div class="is-section-label">Dane \u017ar\u00f3d\u0142owe</div>
    <div>{tags_html}</div>
  </div>
  <div class="is-do-dont">
    <div class="is-do"><h5>&#10003; Tak</h5><ul class="is-bullets">{dos_html}</ul></div>
    <div class="is-dont"><h5>&#10007; Nie</h5><ul class="is-bullets">{donts_html}</ul></div>
  </div>
  <div class="is-section" style="margin-top:10px">
    <div class="is-section-label">Referencje konkurencji</div>
    <div class="is-ref-imgs">{refs_html}</div>
  </div>
</div>'''

slots = []

# SLOT 1
slots.append(slot_card(1,
    'Zdj\u0119cie g\u0142\u00f3wne (CTR Driver)',
    'Miniaturka widoczna w wynikach wyszukiwania. Musi maksymalizowa\u0107 CTR (wsp\u00f3\u0142czynnik klikalnosci).',
    'Produkt zajmuje 85%+ kadru na czystym bia\u0142ym tle. Opakowanie widoczne z wydrukowanymi claimami ("Non-Toxic", "Fast-Acting") \u2014 jedyny zgodny spos\u00f3b na tekst.',
    [
        'Produkt pod k\u0105tem 45\u00b0 \u2014 widoczna etykieta frontowa + profil boczny',
        'Opakowanie z fizycznie wydrukowanymi claimami (nie cyfrowymi)',
        'Je\u015bli pu\u0142apka jest prze\u017aroczysta \u2014 delikatna sugestia kolorowego p\u0142ynu wabiącego wewn\u0105trz',
        'Wszystkie elementy zestawu widoczne (np. 4 pu\u0142apki u\u0142o\u017cone)',
        'Czyste, ostre cienie dla g\u0142\u0119bi \u2014 bez ostrego o\u015bwietlenia'
    ],
    'Brak cyfrowych nak\u0142adek tekstowych. Ca\u0142y przekaz musi by\u0107 fizycznie wydrukowany na produkcie/opakowaniu: nazwa marki, "Non-Toxic", "Fast-Acting", ilo\u015b\u0107 w opakowaniu.',
    [('Czysty bia\u0142y','#FFFFFF'),('Kolor produktu','#E8B634'),('Zielony etykiety','#22C55E')],
    'Widok pod 45\u00b0 z przodu. Produkt lekko odchylony pokazuj\u0105c etykiet\u0119 i bok. Kamera na wysoko\u015bci oczu.',
    'Czysty bia\u0142y (RGB 255, 255, 255). Bez gradient\u00f3w, bez cieni od rekwizyt\u00f3w.',
    [('Zgodno\u015b\u0107 z Amazon','#dc2626'),('CTR driver','#2563eb'),('85% wype\u0142nienia kadru','#7c3aed')],
    ['Wype\u0142nij 85%+ powierzchni zdj\u0119cia produktem','U\u017cyj prawdziwego opakowania z wydrukowanymi claimami','Poka\u017c zawarto\u015b\u0107 ca\u0142ego zestawu','Rozdzielczo\u015b\u0107 2000-3000px JPEG','Testuj vs miniaturki 3 najlepszych konkurent\u00f3w (PickFu)'],
    ['Brak cyfrowych nak\u0142adek tekstowych (AI Amazona blokuje w ci\u0105gu 1h)','Brak badge\u2019\u00f3w, wst\u0105\u017cek, grafik promocyjnych','Brak rekwizyt\u00f3w niedo\u0142\u0105czonych do zakupu','Brak znak\u00f3w wodnych','Luka w opakowaniu jest MARTWA od 2025 \u2014 nie dodawaj tekstu cyfrowo'],
    ['B01MRHXM0I','B0BX4GQF68','B07VYPGHFW','B0DGWQV8GK','B0D5DJ7V4P'],
    '#dc2626'
))

# SLOT 2
slots.append(slot_card(2,
    'Infografika korzy\u015bci ("Haczyk")',
    'Pierwsze zdj\u0119cie dodatkowe. Musi przekaza\u0107 3 g\u0142\u00f3wne korzy\u015bci w <3 sekundy (skanowalne na telefonie).',
    'Poka\u017c REZULTAT, nie cechy: czysta, wolna od owad\u00f3w kuchnia z dyskretnie dzia\u0142aj\u0105c\u0105 pu\u0142apk\u0105. Na\u0142\u00f3\u017c 3-5 kluczowych korzy\u015bci z ikonami.',
    [
        'Centralny obraz produktu (~40% kadru) w czystej kuchni',
        'Korzy\u015b\u0107 #1: "Dzia\u0142a w 24 godziny" \u2014 ikona zegara (21.6% pozytywnych recenzji)',
        'Korzy\u015b\u0107 #2: "Nietoksyczny i bezpieczny" \u2014 ikona li\u015bcia (17.3% motywacja kupuj\u0105cych)',
        'Korzy\u015b\u0107 #3: "Zapas na 180 dni" \u2014 ikona kalendarza (28.4% oczekuje d\u0142u\u017cszej trwa\u0142o\u015bci)',
        'Opcjonalnie #4: "Dyskretny design" \u2014 ikona oka (10.8% pozytywnych)',
        'Opcjonalnie #5: "Gotowy do u\u017cycia" \u2014 ikona bez monta\u017cu (16.2% pozytywnych)'
    ],
    '"Dzia\u0142a w 24 godziny" \u2022 "Nietoksyczny, bezpieczny dla dzieci i zwierz\u0105t" \u2022 "Zapas wabia na 180 dni" \u2022 "Dyskretny design na blat" \u2022 "Po prostu otw\u00f3rz i postaw"',
    [('Kremowe t\u0142o','#FFF8F0'),('Zielony zaufania','#16A34A'),('Pomara\u0144czowy akcji','#F97316'),('Niebieski bezpiecze\u0144stwa','#2563EB')],
    'Produkt na \u015brodku, ikony promieniuj\u0105 na zewn\u0105trz. Czysta przestrze\u0144 mi\u0119dzy elementami.',
    'Delikatne kremowe lub bardzo jasne ciep\u0142e szare. Nie czyste bia\u0142e (r\u00f3\u017cnica od hero).',
    [('25.7% skuteczno\u015b\u0107+','#16a34a'),('21.6% szybkie wyniki+','#2563eb'),('16.2% \u0142atwo\u015b\u0107 u\u017cycia+','#7c3aed'),('17.3% motywacja bezpiecze\u0144stwem','#d97706')],
    ['Maks. 5 korzy\u015bci \u2014 mniej = lepiej','Czcionka min. 32px nag\u0142\u00f3wki, 16px podtekst (czytelne na telefonie)','Ikony uniwersalne (ptaszek, li\u015b\u0107, zegar)','Skup si\u0119 na KORZY\u015aCIACH nie cechach ("kuchnia bez owad\u00f3w" nie "zawiera wab")'],
    ['Nie wymieniaj sk\u0142adnik\u00f3w (nudne, nieskanowalne)','Nie wi\u0119cej ni\u017c 25 s\u0142\u00f3w \u0142\u0105cznie','Nie zagranicaj \u2014 klient musi z\u0142apa\u0107 warto\u015b\u0107 w 3 sekundy','Nie u\u017cywaj niebieskiego jako dominuj\u0105cego koloru (przyci\u0105ga muchy)'],
    ['B01MRHXM0I','B0D5DJ7V4P'],
    '#2563eb'
))

# SLOT 3
slots.append(slot_card(3,
    'My vs. Oni \u2014 Por\u00f3wnanie',
    'Odpowied\u017a na negatywny temat #3: 13.7% klient\u00f3w twierdzi, \u017ce pu\u0142apki DIY z octu dzia\u0142aj\u0105 lepiej. Trzeba to bezpo\u015brednio skonfrontowa\u0107.',
    'Por\u00f3wnanie obok siebie: dlaczego profesjonalna pu\u0142apka jest lepsza od DIY. Nale\u017cy odnie\u015b\u0107 si\u0119 do problem\u00f3w z recenzji konkurencji (wycieki, brzydki wygl\u0105d, ba\u0142agan).',
    [
        'LEWA strona: ba\u0142agan DIY z octem \u2014 plastikowy s\u0142oik, folia, rozlany p\u0142yn, muchy wok\u00f3\u0142 ale niez\u0142apane',
        'PRAWA strona: elegancka pu\u0142apka \u2014 czysty design, muchy z\u0142apane wewn\u0105trz, bez ba\u0142aganu',
        'Wiersze por\u00f3wnania: Design \u2713/\u2717, Skuteczno\u015b\u0107 \u2713/\u2717, Wygoda \u2713/\u2717, Bezpiecze\u0144stwo \u2713/\u2717',
        'Opcjonalnie: por\u00f3wnanie kosztu dziennego (DIY wymaga codziennego mieszania vs. wab na 45 dni)'
    ],
    '"Przesta\u0144 robi\u0107 pu\u0142apki z octu. Nasz naukowo opracowany wab \u0142apie 3x wi\u0119cej much ni\u017c domowe roztwory \u2014 bez ba\u0142aganu."',
    [('Podzia\u0142 uk\u0142adu','#F1F5F9'),('Zielony wygranej','#16A34A'),('Czerwony przegranej','#DC2626'),('Neutralny','#64748B')],
    'P\u0142aski widok lub prosto z przodu. R\u00f3wny podzia\u0142 kadru (50/50). Strona DIY lekko ciemniejsza/bardziej chaotyczna.',
    'Lewa: lekko ba\u0142aganiarskie/ciep\u0142e. Prawa: czyste, jasne, nowoczesne. Prawa strona "wygrywa" wizualnie.',
    [('13.7% por\u00f3wnanie z DIY','#dc2626'),('20.6% kwestionuje mechanizm','#d97706'),('30.9% problem skuteczno\u015bci','#dc2626')],
    ['Kontrast DRAMATYCZNY \u2014 ba\u0142agan vs. czysto\u015b\u0107','U\u017cyj prawdziwego s\u0142oika DIY (folia, gumka, wyka\u0142aczka)','Poka\u017c z\u0142apane muchy w produkcie (dow\u00f3d skuteczno\u015bci)','Do\u0142\u0105cz prost\u0105 metryk\u0119: "\u0141apie 3x wi\u0119cej" lub "Dzia\u0142a 45 dni vs. codzienne mieszanie"'],
    ['Nie podawaj nazw konkurencyjnych marek (naruszenie TOS Amazon)','Nie pokazuj identycznego produktu konkurenta (u\u017cyj generycznego "DIY")','Nie rób por\u00f3wnania zbyt z\u0142o\u017conego \u2014 maks. 4 wiersze','Nie u\u017cywaj claim\u00f3w, kt\u00f3rych nie mo\u017cna potwierdzi\u0107'],
    ['B07VYPGHFW','B0D5DJ7V4P'],
    '#f97316'
))

# SLOT 4
slots.append(slot_card(4,
    'Rozmiar i skala',
    'Zapobieganie zwrotom z powodu nieporozumie\u0144 co do rozmiaru. 4.8% klient\u00f3w chce jasnych instrukcji u\u017cycia.',
    'Umie\u015b\u0107 pu\u0142apk\u0119 obok typowych obiekt\u00f3w kuchennych, aby klient wizualizowa\u0142 dok\u0142adny rozmiar na swoim blacie.',
    [
        'Pu\u0142apka obok cytryny, kubka kawy lub zwyk\u0142ego jab\u0142ka (referencja rozmiaru)',
        'Wymiary z opisem: szeroko\u015b\u0107, wysoko\u015b\u0107, g\u0142\u0119boko\u015b\u0107 w cm/calach',
        'Pu\u0142apka na prawdziwej kraw\u0119dzi blatu dla kontekstu przestrzennego',
        'Przy multi-packu: wszystkie elementy roz\u0142o\u017cone z odst\u0119pami'
    ],
    '"Kompaktowa \u2014 mie\u015bci si\u0119 dyskretnie obok miski z owocami. 9 x 9 x 4 cm."',
    [('Czysty bia\u0142y','#FFFFFF'),('Niebieski wymiar\u00f3w','#3B82F6'),('Ciep\u0142y blat','#D4C5B0')],
    'Z g\u00f3ry lub pod 30\u00b0. Produkt na \u015brodku z obiektem referencyjnym obok. Opcjonalnie linijka/strza\u0142ki wymiar\u00f3w.',
    'Jasna powierzchnia blatu (marmur, drewno, bia\u0142e). Naturalne, ciep\u0142e o\u015bwietlenie.',
    [('4.8% chce jasnych instrukcji','#7c3aed'),('2.0% "za ma\u0142y"','#d97706'),('Zapobieganie zwrotom','#2563eb')],
    ['U\u017cyj powszechnie znanych obiekt\u00f3w (cytryna, moneta, d\u0142o\u0144)','Podaj dok\u0142adne wymiary ze strza\u0142kami','Poka\u017c pu\u0142apk\u0119 w kontek\u015bcie (na blacie, nie "wisz\u0105c\u0105")','Czysta kompozycja \u2014 tylko pu\u0142apka + 1-2 obiekty referencyjne'],
    ['Nie u\u017cywaj obiekt\u00f3w o zmiennym rozmiarze','Nie przet\u0142aczaj kadru wieloma przedmiotami','Nie u\u017cywaj tylko d\u0142oni jako referencji (zbyt zmienna)','Nie pomijaj wymiar\u00f3w \u2014 konkretne miary zapobiegaj\u0105 zwrotom'],
    ['B01MRHXM0I','B0BX4GQF68'],
    '#3b82f6'
))

# SLOT 5
slots.append(slot_card(5,
    'Lifestyle i grupa docelowa',
    'Produkt w g\u0142\u00f3wnym \u015brodowisku u\u017cycia. 29.2% klient\u00f3w u\u017cywa go do kontroli muszek owoc\u00f3wek w kuchni.',
    'Realistyczna scena kuchenna z pu\u0142apk\u0105 przy misce z owocami. Model odzwierciedla grup\u0119 docelow\u0105 (w\u0142a\u015bciciel domu, 30-50 lat, nowoczesna kuchnia).',
    [
        'Nowoczesna, jasna kuchnia \u2014 granitowy lub marmurowy blat, naturalne \u015bwiat\u0142o',
        'Miska z owocami: banany, jab\u0142ka, winogrona (wyzwalacz zakupu)',
        'Pu\u0142apka umieszczona dyskretnie 15-30 cm od miski z owocami',
        'Opcjonalnie: osoba (w\u0142a\u015bciciel domu) w tle, zrelaksowana',
        'Drugie umiejscowienie: przy koszu na \u015bmieci lub kompostowniku (13.8% scenariusz)'
    ],
    '"Postaw przy miskach z owocami, koszach na \u015bmieci lub kompostownikach \u2014 wsz\u0119dzie gdzie muszki si\u0119 rozmna\u017caj\u0105. Dyskretny design pasuje do ka\u017cdej kuchni."',
    [('Ciep\u0142a kuchnia','#F5E6D0'),('Naturalny zielony','#4ADE80'),('Ton drewna','#A0845C'),('Bia\u0142y akcent','#FFFFFF')],
    'Szeroki plan, 30\u00b0 powy\u017cej poziomu oczu. Pu\u0142apka widoczna ale nie dominuje \u2014 kuchnia jest bohaterem, pu\u0142apka jest rozwi\u0105zaniem.',
    'Prawdziwa kuchnia. Nowoczesna, czysta, aspiracyjna ale osi\u0105galna. Naturalne \u015bwiat\u0142o dzienne.',
    [('29.2% u\u017cycie w kuchni','#16a34a'),('13.8% \u015bmieci/kompost','#d97706'),('10.8% dyskretny design+','#2563eb'),('5.7% motywacja dyskrecj\u0105','#7c3aed')],
    ['U\u017cyj modela odzwierciedlaj\u0105cego grup\u0119 docelow\u0105 (w\u0142a\u015bciciel domu, kuchnia rodzinna)','Poka\u017c pu\u0142apk\u0119 "w akcji" \u2014 w realistycznym miejscu','Naturalne o\u015bwietlenie \u2014 unikaj studyjnego odczucia','Do\u0142\u0105cz misk\u0119 z owocami w pobli\u017cu (wizualny wyzwalacz)'],
    ['Nie pokazuj zbli\u017ce\u0144 martwych owad\u00f3w (odrzucaj\u0105ce)','Nie rób pu\u0142apki centrum uwagi (ma si\u0119 wtapia\u0107)','Nie u\u017cywaj zimnego/klinicznego o\u015bwietlenia','Nie pokazuj samego produktu \u2014 KONTEKST jest przekazem'],
    ['B01MRHXM0I','B07VYPGHFW','B0D5DJ7V4P'],
    '#16a34a'
))

# SLOT 6
slots.append(slot_card(6,
    'Dow\u00f3d skuteczno\u015bci \u2014 Przed/Po',
    'Odpowied\u017a na temat negatywny #1: 30.9% twierdzi "brak efektu." Wizualny dow\u00f3d skuteczno\u015bci jest kluczowy.',
    'Podzia\u0142 ekranu: muchy lataj\u0105 (przed) \u2192 pu\u0142apka postawiona, muchy z\u0142apane, kuchnia czysta (po). Uwzgl\u0119dnij osi\u0119 czasow\u0105 24h.',
    [
        'PRZED (lewo/g\u00f3ra): Miska z owocami otoczona muchami. Lekko ciep\u0142e, zamglone o\u015bwietlenie.',
        'PO (prawo/d\u00f3\u0142): Ten sam k\u0105t \u2014 pu\u0142apka przy owocach, muchy widocznie z\u0142apane. Czyste, jasne \u015bwiat\u0142o.',
        'Nak\u0142adka osi czasu: "Dzie\u0144 0 \u2192 Dzie\u0144 1" lub "Przed \u2192 Po 24 godzinach"',
        'Wstawka zbli\u017ceniowa: prze\u017aroczyste okienko pu\u0142apki z widocznymi z\u0142apanymi muchami',
        'Opcjonalnie: przekr\u00f3j 3D pu\u0142apki pokazuj\u0105cy jak wab przyci\u0105ga muchy'
    ],
    '"Zobacz wyniki w ci\u0105gu 24 godzin. Nasz wab przyci\u0105ga muszki owoc\u00f3wki z odleg\u0142o\u015bci do 1 metra \u2014 raz wewn\u0105trz, nie mog\u0105 uciec."',
    [('Przed ciep\u0142e/zamglone','#FEF3C7'),('Po czyste/jasne','#F0FDF4'),('Zielony dowodu','#16A34A'),('Niebieski osi czasu','#2563EB')],
    'TEN SAM k\u0105t kamery dla przed i po (kluczowe dla efektu wizualnego). Prosto z przodu lub lekkie 30\u00b0.',
    'Ta sama scena kuchenna, r\u00f3\u017cne o\u015bwietlenie/nastr\u00f3j. Przed: ciep\u0142e, zamglone. Po: jasne, czyste, \u015bwie\u017ce.',
    [('30.9% "brak efektu"','#dc2626'),('21.6% szybkie wyniki+','#16a34a'),('38.4% oczekuje niezawodno\u015bci','#d97706'),('25.7% "dzia\u0142a \u015bwietnie"+','#16a34a')],
    ['U\u017cyj TEGO SAMEGO k\u0105ta i kadrowania dla obu uj\u0119\u0107','Podaj konkretny przedzia\u0142 czasowy (24h, 48h \u2014 nie og\u00f3lnikowo)','Poka\u017c z\u0142apane muchy w prze\u017aroczystym okienku (dow\u00f3d)','Zr\u00f3b transformacj\u0119 wizualnie dramatyczn\u0105 (zmiana o\u015bwietlenia)'],
    ['Nie pokazuj obrzydliwych zbli\u017ce\u0144 martwych owad\u00f3w','Nie twierd\u017a "100% eliminacja" (fa\u0142szywe oczekiwania)','Nie rób przed/po wygl\u0105daj\u0105cego na photoshopa \u2014 musi by\u0107 autentyczne','Nie u\u017cywaj r\u00f3\u017cnych k\u0105t\u00f3w kamery mi\u0119dzy przed/po'],
    ['B01MRHXM0I','B0DGWQV8GK','B0D5DJ7V4P'],
    '#7c3aed'
))

# SLOT 7
slots.append(slot_card(7,
    'Wszystko w zestawie / Warto\u015b\u0107',
    'Odpowied\u017a na obawy o warto\u015b\u0107: 15.6% cytuje "szybko si\u0119 ko\u0144czy", 28.4% oczekuje d\u0142u\u017cszej trwa\u0142o\u015bci, 7.4% uwa\u017ca za przep\u0142acone.',
    'Flat lay z ca\u0142\u0105 zawarto\u015bci\u0105 opakowania i osi\u0105 czasu zapasu. Zwi\u0119kszenie postrzeganej warto\u015bci przez pokazanie wszystkiego, co klient dostaje.',
    [
        'Flat lay: wszystkie pu\u0142apki + wszystkie wk\u0142ady wabiowe roz\u0142o\u017cone starannie',
        'Ka\u017cdy element podpisany: "Pu\u0142apka #1", "Wab #1" itd.',
        'O\u015b czasu zapasu: "45 dni na wab \u00d7 4 = 180 dni ochrony"',
        'Rozk\u0142ad kosztu: "X,XX z\u0142 za miesi\u0105c ochrony" (przeramowanie warto\u015bci)',
        'Bonus: mapa rozmieszczenia pu\u0142apek (schemat kuchni z 4 optymalnymi miejscami)'
    ],
    '"Wszystko czego potrzebujesz na 180 dni ochrony. 4 pu\u0142apki + 4 wk\u0142ady wabiowe = 6 miesi\u0119cy bez szkodnik\u00f3w. To mniej ni\u017c 10 z\u0142/miesi\u0105c."',
    [('Czyste bia\u0142e t\u0142o','#FFFFFF'),('Z\u0142oty warto\u015bci','#D97706'),('Niebieski kalendarza','#3B82F6'),('Zielony zapasu','#16A34A')],
    'Prawdziwy flat lay (z g\u00f3ry, 90\u00b0). Wszystkie elementy u\u0142o\u017cone symetrycznie z r\u00f3wnym odst\u0119pem.',
    'Czyste bia\u0142e lub bardzo jasne szare. Bez rozpraszaj\u0105cych element\u00f3w \u2014 fokus na zawarto\u015bci opakowania.',
    [('15.6% "szybko si\u0119 ko\u0144czy"','#dc2626'),('28.4% chce d\u0142u\u017cszej trwa\u0142o\u015bci','#d97706'),('7.4% przep\u0142acone','#dc2626'),('6.9% powracaj\u0105cy klienci+','#16a34a')],
    ['Roz\u0142\u00f3\u017c WSZYSTKIE elementy \u2014 postrzegana warto\u015b\u0107 ro\u015bnie gdy widoczne','Do\u0142\u0105cz o\u015b czasu lub grafik\u0119 kalendarza','Oblicz i poka\u017c koszt za miesi\u0105c (przeramowanie warto\u015bci)','Podpisz ka\u017cdy sk\u0142adnik wyra\u017anie'],
    ['Nie pokazuj element\u00f3w u\u0142o\u017conych w stos (zmniejsza postrzegan\u0105 ilo\u015b\u0107)','Nie pomijaj osi czasu (claim o trwa\u0142o\u015bci wymaga wizualnego wsparcia)','Nie u\u017cywaj element\u00f3w lifestyle (tu chodzi o WARTO\u015a\u0106, nie kontekst)','Nie zapomnij instrukcji je\u015bli jest w zestawie'],
    ['B01MRHXM0I','B0BX4GQF68','B0D5DJ7V4P'],
    '#d97706'
))

slots_html = '\n'.join(slots)

PANEL = f'''<!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 TAB IS \u2014 Image Strategy \u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->
<div id="tis" class="panel">
<h2>Strategia Zdj\u0119\u0107 &mdash; Brief dla Listingu Pu\u0142apek na Muszki</h2>

<div class="insight" style="background:#eff6ff;border-left-color:#2563eb;color:#1e40af">
  <strong>Brief oparty na danych.</strong> Strategia oparta na analizie 5 722 recenzji (Tab 4), audycie listing\u00f3w 5 konkurent\u00f3w (Tab 5), badaniu zgodno\u015bci z Amazon 2025\u20132026 oraz frameworku &ldquo;Conversion-First&rdquo; 7-Image Stack. Wszystkie procenty odnosz\u0105 si\u0119 do rzeczywistych danych z recenzji klient\u00f3w.
</div>

<!-- Przegl\u0105d KPI -->
<div class="is-insights-grid">
  <div class="is-insight-card" style="border-top-color:#dc2626">
    <div class="is-pct" style="color:#dc2626">30.9%</div>
    <div class="is-label">&ldquo;Brak efektu / zero z\u0142apa\u0144&rdquo;<br>Najwi\u0119ksze wyzwanie wizualne</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#f97316">
    <div class="is-pct" style="color:#f97316">13.7%</div>
    <div class="is-label">&ldquo;DIY z octem dzia\u0142a lepiej&rdquo;<br>Percepcja do wizualnego obalenia</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#16a34a">
    <div class="is-pct" style="color:#16a34a">17.3%</div>
    <div class="is-label">Motywacja bezpiecze\u0144stwem (dzieci/zwierz\u0119ta)<br>Niewykorzystana szansa komunikacyjna</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#d97706">
    <div class="is-pct" style="color:#d97706">38.4%</div>
    <div class="is-label">Oczekuje niezawodnej skuteczno\u015bci<br>Musi by\u0107 udowodnione wizualnie</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#2563eb">
    <div class="is-pct" style="color:#2563eb">7&ndash;9</div>
    <div class="is-label">Rekomendowane sloty zdj\u0119\u0107<br>Pe\u0142ny stack = 32% wy\u017cszy CVR</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#7c3aed">
    <div class="is-pct" style="color:#7c3aed">29.2%</div>
    <div class="is-label">Kontrola muszek w kuchni<br>G\u0142\u00f3wny scenariusz u\u017cycia &mdash; kontekst hero</div>
  </div>
</div>

<!-- \u2550\u2550\u2550\u2550\u2550 7-IMAGE STACK \u2550\u2550\u2550\u2550\u2550 -->
<h2 style="margin-top:28px">Stack 7 Zdj\u0119\u0107 &mdash; Briefy slot\u00f3w</h2>
<p style="font-size:.78rem;color:#64748b;margin-bottom:18px;line-height:1.5">Ka\u017cdy slot opisany jest jako kompletny brief fotograficzny: cel, co pokaza\u0107, sugerowany copy, kolory, k\u0105ty, t\u0142o, dane \u017ar\u00f3d\u0142owe, zalecenia i antyrekomendacje. Kolejno\u015b\u0107 slot\u00f3w odpowiada frameworkowi &ldquo;Conversion-First&rdquo; (hero &rarr; korzy\u015bci &rarr; por\u00f3wnanie &rarr; skala &rarr; lifestyle &rarr; dow\u00f3d &rarr; warto\u015b\u0107).</p>

{slots_html}

<!-- \u2550\u2550\u2550\u2550\u2550 KOLORY I WYTYCZNE \u2550\u2550\u2550\u2550\u2550 -->
<h2 style="margin-top:28px">Kolory i wytyczne wizualne</h2>
<div class="card">
  <h3 style="font-size:.88rem;margin-bottom:12px">Rekomendowana paleta</h3>
  <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:14px">
    <div style="text-align:center"><div class="is-swatch" style="background:#16A34A;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Zielony zaufania<br>#16A34A</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#F97316;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Pomara\u0144czowy akcji<br>#F97316</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#2563EB;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Niebieski info<br>#2563EB</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#D97706;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Z\u0142oty warto\u015bci<br>#D97706</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#DC2626;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Czerwony alertu<br>#DC2626</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#7C3AED;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Fioletowy premium<br>#7C3AED</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#FFF8F0;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Ciep\u0142y kremowy<br>#FFF8F0</div></div>
    <div style="text-align:center"><div class="is-swatch" style="background:#F1F5F9;width:40px;height:40px"></div><div style="font-size:.68rem;color:#64748b;margin-top:4px">Ch\u0142odny szary<br>#F1F5F9</div></div>
  </div>
  <div class="note">
    <strong>Psychologia kolor\u00f3w (pest control):</strong> Unikaj dominuj\u0105cego niebieskiego &mdash; przyci\u0105ga muchy. Ciep\u0142e odcienie (\u017c\u00f3\u0142\u0107, pomara\u0144cz) odpychaj\u0105 muchy. Biel jest neutralna i wymagana przez Amazon. Zielony buduje zaufanie (bezpiecze\u0144stwo, eko). Pomara\u0144czowy sygnalizuje pilno\u015b\u0107/akcj\u0119.
  </div>
  <div style="margin-top:12px;display:grid;grid-template-columns:1fr 1fr;gap:12px">
    <div>
      <p style="font-size:.72rem;font-weight:700;color:#475569;margin-bottom:6px">Typografia</p>
      <ul class="is-bullets">
        <li>Nag\u0142\u00f3wki: minimum <strong>32px</strong> (czytelne na telefonie)</li>
        <li>Podtekst: minimum <strong>16px</strong></li>
        <li>Czcionka sans-serif (czysta, nowoczesna)</li>
        <li>Maks. 20-25 s\u0142\u00f3w na infografik\u0119</li>
      </ul>
    </div>
    <div>
      <p style="font-size:.72rem;font-weight:700;color:#475569;margin-bottom:6px">Nastr\u00f3j i atmosfera</p>
      <ul class="is-bullets">
        <li>Ciep\u0142y, domowy, przyst\u0119pny</li>
        <li>Naturalne \u015bwiat\u0142o dzienne preferowane</li>
        <li>Czysty ale nie kliniczny</li>
        <li>Aspiracyjna kuchnia &mdash; nowoczesna ale osi\u0105galna</li>
      </ul>
    </div>
  </div>
</div>

<!-- \u2550\u2550\u2550\u2550\u2550 ZGODNO\u015a\u0106 TECHNICZNA \u2550\u2550\u2550\u2550\u2550 -->
<h2 style="margin-top:28px">Zgodno\u015b\u0107 techniczna z Amazon (2025&ndash;2026)</h2>
<div class="is-compliance-grid">
  <div class="is-compliance-card" style="border-left:4px solid #dc2626">
    <h4>Zasady zdj\u0119cia g\u0142\u00f3wnego</h4>
    <ul class="is-bullets">
      <li>Czyste bia\u0142e t\u0142o: <strong>RGB 255, 255, 255</strong></li>
      <li>Produkt zajmuje <strong>85%+</strong> kadru</li>
      <li>Brak cyfrowych nak\u0142adek tekstowych (AI blokuje w ci\u0105gu 1h)</li>
      <li>Brak badge\u2019\u00f3w, wst\u0105\u017cek, grafik promocyjnych</li>
      <li>Brak rekwizyt\u00f3w niedołączonych do zakupu</li>
      <li>Brak znak\u00f3w wodnych ani cyfrowo dodanych logo</li>
      <li><strong>Luka w opakowaniu jest MARTWA</strong> &mdash; AI Amazona wykrywa cyfrowe dodatki vs. druk</li>
    </ul>
  </div>
  <div class="is-compliance-card" style="border-left:4px solid #2563eb">
    <h4>Specyfikacja techniczna</h4>
    <ul class="is-bullets">
      <li>Rozdzielczo\u015b\u0107: <strong>1600&ndash;3000px</strong> (umo\u017cliwia zoom)</li>
      <li>Format: <strong>JPEG</strong> preferowany (szybsze \u0142adowanie)</li>
      <li>Proporcje: <strong>1:1</strong> (kwadrat, 2000\u00d72000 idealnie)</li>
      <li>Rozmiar pliku: poni\u017cej 10MB</li>
      <li>Pierwsze 7 zdj\u0119\u0107 widocznych domy\u015blnie na desktopie</li>
      <li>Zawsze sprawd\u017a na <strong>telefonie</strong> przed wgraniem</li>
    </ul>
  </div>
  <div class="is-compliance-card" style="border-left:4px solid #16a34a">
    <h4>Testy A/B (Manage Your Experiments)</h4>
    <ul class="is-bullets">
      <li>Najpierw testuj zdj\u0119cie g\u0142\u00f3wne (najwi\u0119kszy wp\u0142yw na CTR)</li>
      <li>Prowad\u017a testy 6&ndash;8 tygodni dla istotno\u015bci statystycznej</li>
      <li>Wersje musz\u0105 si\u0119 <strong>istotnie r\u00f3\u017cni\u0107</strong> (nie tylko zmiana k\u0105ta)</li>
      <li>Nie testuj podczas Prime Day / Black Friday</li>
      <li>Jeden element naraz (tylko zdj\u0119cie, nie zdj\u0119cie + tytu\u0142)</li>
      <li>Przypadek: jedna zmiana zdj\u0119cia = <strong>32% wzrost konwersji</strong></li>
    </ul>
  </div>
  <div class="is-compliance-card" style="border-left:4px solid #d97706">
    <h4>Optymalizacja mobilna</h4>
    <ul class="is-bullets">
      <li>Czcionki czytelne <strong>bez powi\u0119kszania</strong></li>
      <li>Kluczowe detale wyeksponowane bez zat\u0142oczenia</li>
      <li>Uk\u0142ad pionowy preferowany dla przed/po (nie obok siebie)</li>
      <li>Testuj na ekranie 5\u2033 przed wgraniem</li>
      <li>AI Amazona &ldquo;czyta&rdquo; zawarto\u015b\u0107 zdj\u0119\u0107 &mdash; metadane musz\u0105 pasowa\u0107 do wizuali</li>
    </ul>
  </div>
</div>

<!-- \u2550\u2550\u2550\u2550\u2550 METODOLOGIA \u2550\u2550\u2550\u2550\u2550 -->
<div class="note" style="margin-top:22px">
  <strong>Metodologia:</strong> Strategia oparta na danych z: (1) 5 722 recenzji klient\u00f3w Amazon (Tab 4 &mdash; Reviews VOC) z analiz\u0105 temat\u00f3w negatywnych/pozytywnych, scenariuszy u\u017cycia, motywacji i oczekiwa\u0144, (2) audytu listing\u00f3w 5 konkurent\u00f3w (Tab 5 &mdash; Listing Communication) z danymi z Amazon SP-API, (3) analizy luk komunikacyjnych (VoC vs. Listing Gap Analysis), (4) best practices Amazon 2025&ndash;2026 (compliance, testy A/B, optymalizacja mobilna), (5) frameworku &ldquo;Conversion-First&rdquo; 7-Image Stack od ekspert\u00f3w e-commerce. Wszystkie procenty odnosz\u0105 si\u0119 do rzeczywistych danych z recenzji.
</div>

</div><!-- END TAB IS -->
'''

# ── Read and inject ──────────────────────────────────────────────────────────
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find insertion point — before the first <script> tag
import re
marker = '</div><!-- .content -->'
pos = html.find(marker)
if pos != -1:
    html = html[:pos] + PANEL + '\n\n' + html[pos:]
    print('\u2713 Panel HTML injected')
else:
    print('\u2717 Could not find insertion point')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

import shutil
shutil.copy('index.html', '../../index.html')
print('\u2713 Synced to root index.html')
print('\n\u2713 Tab 7 \u2014 Strategia Zdj\u0119\u0107 (PL) injected successfully.')
