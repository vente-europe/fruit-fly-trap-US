"""Inject Tab 7 v2 — Strategia Zdjęć (PL, bezosobowy, bez kolorów/tagów/referencji)."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

def slot_card(num, title, purpose, objective, show_items, copy_text, dos, donts, priority_color='#2563eb'):
    show_html = ''.join(f'<li>{i}</li>' for i in show_items)
    dos_html = ''.join(f'<li>{d}</li>' for d in dos)
    donts_html = ''.join(f'<li>{d}</li>' for d in donts)
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
  <div class="is-do-dont">
    <div class="is-do"><h5>&#10003; Tak</h5><ul class="is-bullets">{dos_html}</ul></div>
    <div class="is-dont"><h5>&#10007; Nie</h5><ul class="is-bullets">{donts_html}</ul></div>
  </div>
</div>'''

slots = []

# SLOT 1: Hero
slots.append(slot_card(1,
    'Zdj\u0119cie g\u0142\u00f3wne (CTR Driver)',
    'Miniaturka widoczna w wynikach wyszukiwania. Musi maksymalizowa\u0107 CTR.',
    'Produkt powinien zajmowa\u0107 85%+ kadru na czystym bia\u0142ym tle. Opakowanie widoczne z wydrukowanymi claimami \u2014 jedyny zgodny spos\u00f3b na tekst.',
    [
        'Produkt pod k\u0105tem 45\u00b0 \u2014 widoczna etykieta frontowa + profil boczny',
        'Opakowanie z fizycznie wydrukowanymi claimami (nie cyfrowymi)',
        'Je\u015bli pu\u0142apka jest prze\u017aroczysta \u2014 warto doda\u0107 delikatn\u0105 sugestie kolorowego p\u0142ynu wabi\u0105cego',
        'Wszystkie elementy zestawu powinny by\u0107 widoczne (np. 4 pu\u0142apki u\u0142o\u017cone)',
        'Czyste, ostre cienie dla g\u0142\u0119bi \u2014 bez ostrego o\u015bwietlenia'
    ],
    'Brak cyfrowych nak\u0142adek tekstowych. Ca\u0142y przekaz musi by\u0107 fizycznie wydrukowany na produkcie/opakowaniu: brand name, "Non-Toxic", "Fast-Acting", pack count.',
    [
        'Wype\u0142ni\u0107 85%+ powierzchni zdj\u0119cia produktem',
        'U\u017cy\u0107 prawdziwego opakowania z wydrukowanymi claimami',
        'Pokaza\u0107 zawarto\u015b\u0107 ca\u0142ego zestawu',
        'Rozdzielczo\u015b\u0107 2000\u20133000px JPEG',
        'Przetestowa\u0107 vs miniaturki 3 najlepszych konkurent\u00f3w (PickFu)'
    ],
    [
        'Cyfrowe nak\u0142adki tekstowe (AI Amazona blokuje w ci\u0105gu 1h)',
        'Badge\u2019e, wst\u0105\u017cki, grafiki promocyjne',
        'Rekwizyty niedo\u0142\u0105czone do zakupu',
        'Znaki wodne',
        'Luka w opakowaniu jest martwa od 2025 \u2014 nie nale\u017cy dodawa\u0107 tekstu cyfrowo'
    ],
    '#dc2626'
))

# SLOT 2: Benefit Infographic
slots.append(slot_card(2,
    'Infografika korzy\u015bci ("The Hook")',
    'Pierwsze zdj\u0119cie dodatkowe. Powinno przekaza\u0107 3 g\u0142\u00f3wne korzy\u015bci w poni\u017cej 3 sekund (skanowalne na telefonie).',
    'Nale\u017cy pokaza\u0107 REZULTAT, nie cechy: czysta, wolna od owad\u00f3w kuchnia z dyskretnie dzia\u0142aj\u0105c\u0105 pu\u0142apk\u0105. Na\u0142o\u017cy\u0107 3\u20135 kluczowych korzy\u015bci z ikonami.',
    [
        'Centralny obraz produktu (~40% kadru) w czystej kuchni',
        'Korzy\u015b\u0107 #1: "Works in 24 Hours" \u2014 ikona zegara (21.6% pozytywnych recenzji)',
        'Korzy\u015b\u0107 #2: "Non-Toxic &amp; Pet-Safe" \u2014 ikona li\u015bcia (17.3% motywacja kupuj\u0105cych)',
        'Korzy\u015b\u0107 #3: "180-Day Lure Supply" \u2014 ikona kalendarza (28.4% oczekuje d\u0142u\u017cszej trwa\u0142o\u015bci)',
        'Opcjonalnie #4: "Discreet Countertop Design" \u2014 ikona oka (10.8% pozytywnych)',
        'Opcjonalnie #5: "Just Open &amp; Place" \u2014 ikona bez monta\u017cu (16.2% pozytywnych)'
    ],
    '"Works in 24 Hours" &bull; "Non-Toxic &amp; Pet-Safe" &bull; "180-Day Lure Supply" &bull; "Discreet Countertop Design" &bull; "Just Open &amp; Place"',
    [
        'Maksymalnie 5 korzy\u015bci \u2014 mniej = lepiej',
        'Czcionka min. 32px nag\u0142\u00f3wki, 16px podtekst (czytelno\u015b\u0107 na telefonie)',
        'Ikony uniwersalne (ptaszek, li\u015b\u0107, zegar)',
        'Skupi\u0107 si\u0119 na KORZY\u015aCIACH nie cechach ("pest-free kitchen" nie "contains lure")'
    ],
    [
        'Wymienianie sk\u0142adnik\u00f3w (nudne, nieskanowalne)',
        'Wi\u0119cej ni\u017c 25 s\u0142\u00f3w \u0142\u0105cznie',
        'Zat\u0142aczanie \u2014 klient musi z\u0142apa\u0107 warto\u015b\u0107 w 3 sekundy',
        'Niebieski jako dominuj\u0105cy kolor (przyci\u0105ga muchy \u2014 z\u0142e skojarzenie pod\u015bwiadome)'
    ],
    '#2563eb'
))

# SLOT 3: Us vs. Them
slots.append(slot_card(3,
    'My vs. Oni \u2014 Por\u00f3wnanie',
    'Odpowied\u017a na negatywny temat #3: 13.7% klient\u00f3w twierdzi, \u017ce pu\u0142apki DIY z octu dzia\u0142aj\u0105 lepiej.',
    'Por\u00f3wnanie obok siebie pokazuj\u0105ce dlaczego profesjonalna pu\u0142apka jest lepsza od DIY. Nale\u017cy odnie\u015b\u0107 si\u0119 do problem\u00f3w z recenzji konkurencji (wycieki, brzydki wygl\u0105d, ba\u0142agan).',
    [
        'LEWA strona: ba\u0142agan DIY z octem \u2014 plastikowy s\u0142oik, folia, rozlany p\u0142yn, muchy wok\u00f3\u0142 ale niez\u0142apane',
        'PRAWA strona: elegancka pu\u0142apka \u2014 czysty design, muchy z\u0142apane wewn\u0105trz, bez ba\u0142aganu',
        'Wiersze por\u00f3wnania: Design \u2713/\u2717, Effectiveness \u2713/\u2717, Convenience \u2713/\u2717, Safety \u2713/\u2717',
        'Opcjonalnie: por\u00f3wnanie kosztu dziennego (DIY wymaga codziennego mieszania vs. 45-day lure)'
    ],
    '"Stop making DIY vinegar traps. Our scientifically formulated lure catches 3x more flies than homemade solutions \u2014 without the mess."',
    [
        'Kontrast powinien by\u0107 DRAMATYCZNY \u2014 ba\u0142agan vs. czysto\u015b\u0107',
        'U\u017cy\u0107 prawdziwego s\u0142oika DIY (folia, gumka, wyka\u0142aczka)',
        'Pokaza\u0107 z\u0142apane muchy w produkcie (dow\u00f3d skuteczno\u015bci)',
        'Do\u0142\u0105czy\u0107 prost\u0105 metryk\u0119: "Catches 3x more" lub "Lasts 45 days vs. daily mixing"'
    ],
    [
        'Podawanie nazw konkurencyjnych marek (naruszenie TOS Amazon)',
        'Pokazywanie identycznego produktu konkurenta (nale\u017cy u\u017cy\u0107 generycznego "DIY")',
        'Zbyt z\u0142o\u017cone por\u00f3wnanie \u2014 maks. 4 wiersze',
        'Claim\u2019y, kt\u00f3rych nie mo\u017cna potwierdzi\u0107 (np. "100% effective")'
    ],
    '#f97316'
))

# SLOT 4: Size & Scale
slots.append(slot_card(4,
    'Rozmiar i skala',
    'Zapobieganie zwrotom z powodu nieporozumie\u0144 co do rozmiaru. 4.8% klient\u00f3w oczekuje jasnych instrukcji u\u017cycia.',
    'Nale\u017cy umie\u015bci\u0107 pu\u0142apk\u0119 obok typowych obiekt\u00f3w kuchennych, aby klient m\u00f3g\u0142 wizualizowa\u0107 dok\u0142adny rozmiar na swoim blacie.',
    [
        'Pu\u0142apka obok cytryny, kubka kawy lub jab\u0142ka (referencja rozmiaru)',
        'Wymiary z opisem: szeroko\u015b\u0107, wysoko\u015b\u0107, g\u0142\u0119boko\u015b\u0107 w calach/cm',
        'Pu\u0142apka na prawdziwej kraw\u0119dzi blatu dla kontekstu przestrzennego',
        'Przy multi-packu: wszystkie elementy roz\u0142o\u017cone z odst\u0119pami'
    ],
    '"Compact enough for any countertop \u2014 sits discreetly next to your fruit bowl. 3.5\u201d x 3.5\u201d x 1.5\u201d."',
    [
        'U\u017cy\u0107 powszechnie znanych obiekt\u00f3w (cytryna, moneta, d\u0142o\u0144)',
        'Poda\u0107 dok\u0142adne wymiary ze strza\u0142kami',
        'Pokaza\u0107 pu\u0142apk\u0119 w kontek\u015bcie (na blacie, nie "wisz\u0105c\u0105")',
        'Czysta kompozycja \u2014 tylko pu\u0142apka + 1\u20132 obiekty referencyjne'
    ],
    [
        'Obiekty o zmiennym rozmiarze (r\u00f3\u017cne odmiany jab\u0142ek)',
        'Przet\u0142aczanie kadru wieloma przedmiotami',
        'Tylko d\u0142o\u0144 jako referencja (zbyt zmienna)',
        'Pomijanie wymiar\u00f3w \u2014 konkretne miary zapobiegaj\u0105 zwrotom'
    ],
    '#3b82f6'
))

# SLOT 5: Lifestyle
slots.append(slot_card(5,
    'Lifestyle i grupa docelowa',
    'Produkt w g\u0142\u00f3wnym \u015brodowisku u\u017cycia. 29.2% klient\u00f3w u\u017cywa go do kontroli muszek owoc\u00f3wek w kuchni.',
    'Realistyczna scena kuchenna z pu\u0142apk\u0105 przy misce z owocami. Model powinien odzwierciedla\u0107 grup\u0119 docelow\u0105 (w\u0142a\u015bciciel domu, 30\u201350 lat, nowoczesna kuchnia).',
    [
        'Nowoczesna, jasna kuchnia \u2014 granitowy lub marmurowy blat, naturalne \u015bwiat\u0142o',
        'Miska z owocami: banany, jab\u0142ka, winogrona (wyzwalacz zakupu)',
        'Pu\u0142apka umieszczona dyskretnie 15\u201330 cm od miski z owocami',
        'Opcjonalnie: osoba (w\u0142a\u015bciciel domu) w tle, zrelaksowana',
        'Drugie umiejscowienie: przy koszu na \u015bmieci lub kompostowniku (13.8% scenariusz)'
    ],
    '"Place near fruit bowls, trash cans, or compost areas \u2014 wherever fruit flies breed. Discreet design blends with any kitchen decor."',
    [
        'U\u017cy\u0107 modela odzwierciedlaj\u0105cego grup\u0119 docelow\u0105 (w\u0142a\u015bciciel domu, kuchnia rodzinna)',
        'Pokaza\u0107 pu\u0142apk\u0119 "in action" \u2014 w realistycznym miejscu',
        'Naturalne o\u015bwietlenie \u2014 nale\u017cy unika\u0107 studyjnego odczucia',
        'Do\u0142\u0105czy\u0107 misk\u0119 z owocami w pobli\u017cu (wizualny wyzwalacz)'
    ],
    [
        'Zbli\u017cenia martwych owad\u00f3w (odrzucaj\u0105ce dla kupuj\u0105cych)',
        'Pu\u0142apka jako centrum uwagi (powinna si\u0119 wtapia\u0107)',
        'Zimne/kliniczne o\u015bwietlenie (powinno by\u0107 ciep\u0142e, domowe)',
        'Sam produkt bez kontekstu \u2014 KONTEKST jest przekazem'
    ],
    '#16a34a'
))

# SLOT 6: Before/After
slots.append(slot_card(6,
    'Dow\u00f3d skuteczno\u015bci \u2014 Before/After',
    'Odpowied\u017a na temat negatywny #1: 30.9% twierdzi "no effect." Wizualny dow\u00f3d skuteczno\u015bci jest kluczowy.',
    'Podzia\u0142 ekranu: muchy lataj\u0105 (before) \u2192 pu\u0142apka postawiona, muchy z\u0142apane, kuchnia czysta (after). Nale\u017cy uwzgl\u0119dni\u0107 o\u015b czasow\u0105 24h.',
    [
        'BEFORE (lewo/g\u00f3ra): miska z owocami otoczona muchami. Lekko ciep\u0142e, zamglone o\u015bwietlenie.',
        'AFTER (prawo/d\u00f3\u0142): ten sam k\u0105t \u2014 pu\u0142apka przy owocach, muchy widocznie z\u0142apane. Czyste, jasne \u015bwiat\u0142o.',
        'Nak\u0142adka osi czasu: "Day 0 \u2192 Day 1" lub "Before \u2192 After 24 Hours"',
        'Wstawka zbli\u017ceniowa: prze\u017aroczyste okienko pu\u0142apki z widocznymi z\u0142apanymi muchami',
        'Opcjonalnie: przekr\u00f3j 3D pu\u0142apki pokazuj\u0105cy jak wab przyci\u0105ga muchy'
    ],
    '"See results within 24 hours. Our lure attracts fruit flies from up to 3 feet away \u2014 once inside, they can\'t escape."',
    [
        'Ten sam k\u0105t kamery i kadrowanie dla obu uj\u0119\u0107',
        'Konkretny przedzia\u0142 czasowy (24h, 48h \u2014 nie og\u00f3lnikowo)',
        'Pokaza\u0107 z\u0142apane muchy w prze\u017aroczystym okienku (dow\u00f3d)',
        'Transformacja wizualnie dramatyczna (zmiana o\u015bwietlenia mi\u0119dzy before/after)'
    ],
    [
        'Obrzydliwe zbli\u017cenia martwych owad\u00f3w',
        'Twierdzenie "100% elimination" (fa\u0142szywe oczekiwania)',
        'Before/after wygl\u0105daj\u0105ce na photoshopa \u2014 musi by\u0107 autentyczne',
        'R\u00f3\u017cne k\u0105ty kamery mi\u0119dzy before i after'
    ],
    '#7c3aed'
))

# SLOT 7: Pack Value
slots.append(slot_card(7,
    'Wszystko w zestawie / Warto\u015b\u0107',
    'Odpowied\u017a na obawy o warto\u015b\u0107: 15.6% cytuje "runs out quickly", 28.4% oczekuje d\u0142u\u017cszej trwa\u0142o\u015bci, 7.4% uwa\u017ca za przep\u0142acone.',
    'Flat lay z ca\u0142\u0105 zawarto\u015bci\u0105 opakowania i osi\u0105 czasu zapasu. Zwi\u0119kszenie postrzeganej warto\u015bci przez pokazanie wszystkiego, co klient dostaje.',
    [
        'Flat lay: wszystkie pu\u0142apki + wszystkie wk\u0142ady wabiowe roz\u0142o\u017cone starannie',
        'Ka\u017cdy element podpisany: "Trap #1", "Lure #1" itd.',
        'O\u015b czasu zapasu: "45 days per lure \u00d7 4 = 180 days of protection"',
        'Rozk\u0142ad kosztu: "Less than $2.50/month of protection" (przeramowanie warto\u015bci)',
        'Bonus: mapa rozmieszczenia pu\u0142apek (schemat kuchni z 4 optymalnymi miejscami)'
    ],
    '"Everything you need for 180 days of protection. 4 traps + 4 lure pods = 6 months of pest-free living. That\'s less than $2.50/month."',
    [
        'Roz\u0142o\u017cy\u0107 WSZYSTKIE elementy \u2014 postrzegana warto\u015b\u0107 ro\u015bnie gdy widoczne',
        'Do\u0142\u0105czy\u0107 o\u015b czasu lub grafik\u0119 kalendarza',
        'Obliczy\u0107 i pokaza\u0107 koszt za miesi\u0105c (przeramowanie warto\u015bci)',
        'Podpisa\u0107 ka\u017cdy sk\u0142adnik wyra\u017anie'
    ],
    [
        'Elementy u\u0142o\u017cone w stos (zmniejsza postrzegan\u0105 ilo\u015b\u0107)',
        'Pomijanie osi czasu (claim o trwa\u0142o\u015bci wymaga wizualnego wsparcia)',
        'Elementy lifestyle (tu chodzi o WARTO\u015a\u0106, nie kontekst)',
        'Pomini\u0119cie instrukcji je\u015bli jest w zestawie'
    ],
    '#d97706'
))

slots_html = '\n'.join(slots)

PANEL = f'''<!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 TAB IS \u2014 Strategia Zdj\u0119\u0107 \u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->
<div id="tis" class="panel">
<h2>Strategia Zdj\u0119\u0107 &mdash; Brief dla Listingu</h2>

<div class="insight" style="background:#eff6ff;border-left-color:#2563eb;color:#1e40af">
  <strong>Brief oparty na danych.</strong> Strategia oparta na analizie 5 722 recenzji (Tab 4), audycie listing\u00f3w 5 konkurent\u00f3w (Tab 5), badaniu zgodno\u015bci z Amazon 2025\u20132026 oraz frameworku &ldquo;Conversion-First&rdquo; 7-Image Stack. Wszystkie procenty odnosz\u0105 si\u0119 do rzeczywistych danych z recenzji klient\u00f3w.
</div>

<div class="is-insights-grid">
  <div class="is-insight-card" style="border-top-color:#dc2626">
    <div class="is-pct" style="color:#dc2626">30.9%</div>
    <div class="is-label">&ldquo;No effect / zero catch&rdquo;<br>Najwi\u0119ksze wyzwanie wizualne</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#f97316">
    <div class="is-pct" style="color:#f97316">13.7%</div>
    <div class="is-label">&ldquo;DIY vinegar works better&rdquo;<br>Percepcja do wizualnego obalenia</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#16a34a">
    <div class="is-pct" style="color:#16a34a">17.3%</div>
    <div class="is-label">Motywacja bezpiecze\u0144stwem (dzieci/zwierz\u0119ta)<br>Niewykorzystana szansa komunikacyjna</div>
  </div>
  <div class="is-insight-card" style="border-top-color:#d97706">
    <div class="is-pct" style="color:#d97706">38.4%</div>
    <div class="is-label">Oczekiwanie niezawodnej skuteczno\u015bci<br>Konieczno\u015b\u0107 udowodnienia wizualnie</div>
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

<h2 style="margin-top:28px">Stack 7 Zdj\u0119\u0107 &mdash; Briefy slot\u00f3w</h2>
<p style="font-size:.78rem;color:#64748b;margin-bottom:18px;line-height:1.5">Ka\u017cdy slot opisany jest jako kompletny brief fotograficzny: cel, co pokaza\u0107, sugerowany copy, zalecenia i antyrekomendacje. Kolejno\u015b\u0107 slot\u00f3w odpowiada frameworkowi &ldquo;Conversion-First&rdquo; (hero &rarr; korzy\u015bci &rarr; por\u00f3wnanie &rarr; skala &rarr; lifestyle &rarr; dow\u00f3d &rarr; warto\u015b\u0107).</p>

{slots_html}

<!-- ZGODNO\u015a\u0106 TECHNICZNA -->
<h2 style="margin-top:28px">Zgodno\u015b\u0107 techniczna z Amazon (2025&ndash;2026)</h2>
<div class="is-compliance-grid">
  <div class="is-compliance-card" style="border-left:4px solid #dc2626">
    <h4>Zasady zdj\u0119cia g\u0142\u00f3wnego</h4>
    <ul class="is-bullets">
      <li>Czyste bia\u0142e t\u0142o: <strong>RGB 255, 255, 255</strong></li>
      <li>Produkt zajmuje <strong>85%+</strong> kadru</li>
      <li>Brak cyfrowych nak\u0142adek tekstowych (AI blokuje w ci\u0105gu 1h)</li>
      <li>Brak badge\u2019\u00f3w, wst\u0105\u017cek, grafik promocyjnych</li>
      <li>Brak rekwizyt\u00f3w niedo\u0142\u0105czonych do zakupu</li>
      <li>Brak znak\u00f3w wodnych ani cyfrowo dodanych logo</li>
      <li><strong>Luka w opakowaniu jest martwa</strong> &mdash; AI Amazona wykrywa cyfrowe dodatki vs. druk</li>
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
      <li>Nale\u017cy zawsze sprawdzi\u0107 na <strong>telefonie</strong> przed wgraniem</li>
    </ul>
  </div>
  <div class="is-compliance-card" style="border-left:4px solid #16a34a">
    <h4>Testy A/B (Manage Your Experiments)</h4>
    <ul class="is-bullets">
      <li>Najpierw testowa\u0107 zdj\u0119cie g\u0142\u00f3wne (najwi\u0119kszy wp\u0142yw na CTR)</li>
      <li>Prowadzi\u0107 testy 6\u20138 tygodni dla istotno\u015bci statystycznej</li>
      <li>Wersje musz\u0105 si\u0119 <strong>istotnie r\u00f3\u017cni\u0107</strong> (nie tylko zmiana k\u0105ta)</li>
      <li>Nie testowa\u0107 podczas Prime Day / Black Friday</li>
      <li>Jeden element naraz (tylko zdj\u0119cie, nie zdj\u0119cie + tytu\u0142)</li>
      <li>Przypadek: jedna zmiana zdj\u0119cia = <strong>32% wzrost konwersji</strong></li>
    </ul>
  </div>
  <div class="is-compliance-card" style="border-left:4px solid #d97706">
    <h4>Optymalizacja mobilna</h4>
    <ul class="is-bullets">
      <li>Czcionki czytelne <strong>bez powi\u0119kszania</strong></li>
      <li>Kluczowe detale wyeksponowane bez zat\u0142oczenia</li>
      <li>Uk\u0142ad pionowy preferowany dla before/after (nie obok siebie)</li>
      <li>Testowa\u0107 na ekranie 5\u2033 przed wgraniem</li>
      <li>AI Amazona &ldquo;czyta&rdquo; zawarto\u015b\u0107 zdj\u0119\u0107 &mdash; metadane musz\u0105 pasowa\u0107 do wizuali</li>
    </ul>
  </div>
</div>

<div class="note" style="margin-top:22px">
  <strong>Metodologia:</strong> Strategia oparta na danych z: (1) 5 722 recenzji klient\u00f3w Amazon (Tab 4 &mdash; Reviews VOC), (2) audytu listing\u00f3w 5 konkurent\u00f3w (Tab 5 &mdash; Listing Communication) z danymi z Amazon SP-API, (3) analizy luk komunikacyjnych (VoC vs. Listing Gap Analysis), (4) best practices Amazon 2025&ndash;2026, (5) frameworku &ldquo;Conversion-First&rdquo; 7-Image Stack. Wszystkie procenty odnosz\u0105 si\u0119 do rzeczywistych danych z recenzji. J\u0119zyk bezosobowy stosowany zgodnie z konwencj\u0105 brief\u00f3w kreatywnych.
</div>

</div><!-- END TAB IS -->
'''

# ── Inject ───────────────────────────────────────────────────────────────────
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

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
print('\n\u2713 Tab 7 v2 \u2014 Strategia Zdj\u0119\u0107 (PL, bezosobowy) injected.')
