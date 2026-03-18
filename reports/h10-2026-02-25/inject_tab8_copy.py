"""Inject Tab 8 — Listing Copy Brief into index.html."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

PANEL = '''<!-- ═══════════════════════════════════════ TAB CP — Copy Brief ═══════ -->
<div id="tcp" class="panel">
<h2>Listing Copy Brief &mdash; Tytu&#322; i Bullet Points</h2>

<div class="insight" style="background:#eff6ff;border-left-color:#2563eb;color:#1e40af">
  <strong>Brief oparty na danych.</strong> Rekomendacje dotycz&#261;ce tytu&#322;u i bullet points oparte na: analizie tytu&#322;&#243;w 5 konkurent&#243;w (Tab 5), luk komunikacyjnych (Gap Analysis), niezaspokojonych potrzeb klient&#243;w (Reviews VOC) oraz 433 s&#322;&#243;w kluczowych z Helium 10 (Tab 6). S&#322;owa kluczowe oznaczone s&#261; search volume (SV).
</div>

<!-- ═══ TITLE BRIEF ═══ -->
<h2 style="margin-top:22px">Struktura tytu&#322;u</h2>
<p style="font-size:.78rem;color:#64748b;margin-bottom:14px;line-height:1.5">Tytu&#322; powinien mie&#347;ci&#263; si&#281; w 150&ndash;200 znak&#243;w. Poni&#380;sza tabela pokazuje rekomendowane sk&#322;adniki, ich funkcj&#281; oraz sugerowane s&#322;owa kluczowe do wykorzystania. Kolejno&#347;&#263; ma znaczenie &mdash; Amazon indeksuje mocniej pocz&#261;tek tytu&#322;u.</p>

<div class="card">
<table style="width:100%;border-collapse:collapse;font-size:.78rem">
<thead>
<tr style="background:#f8fafc">
  <th style="padding:10px 12px;text-align:left;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700;width:140px">Sk&#322;adnik</th>
  <th style="padding:10px 12px;text-align:left;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700;width:180px">Co powinno zawiera&#263;</th>
  <th style="padding:10px 12px;text-align:left;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700">S&#322;owa kluczowe do u&#380;ycia</th>
  <th style="padding:10px 12px;text-align:left;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700;width:200px">Uzasadnienie</th>
</tr>
</thead>
<tbody>
<tr>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:600;color:#7F77DD">Brand</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">Nazwa marki na pocz&#261;tku</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9"><span style="color:#64748b">[Twoja marka]</span></td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-size:.72rem;color:#64748b">Wszyscy 5 konkurent&#243;w zaczynaj&#261; od brandu. Buduje rozpoznawalno&#347;&#263;.</td>
</tr>
<tr>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:600;color:#1D9E75">Product Type</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">G&#322;&#243;wna kategoria produktu z kluczowym keyword</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <span style="background:#dcfce7;padding:2px 6px;border-radius:4px;font-weight:600">"Fruit Fly Traps for Indoors"</span> <span style="color:#94a3b8;font-size:.68rem">SV 96,624</span><br>
    <span style="background:#dcfce7;padding:2px 6px;border-radius:4px;font-weight:600">"Fruit Fly Trap"</span> <span style="color:#94a3b8;font-size:.68rem">SV 38,092</span>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-size:.72rem;color:#64748b">Najwy&#380;szy SV keyword w kategorii. 4/5 konkurent&#243;w u&#380;ywa dok&#322;adnie tego zwrotu.</td>
</tr>
<tr>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:600;color:#BA7517">Pack Size</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">Ilo&#347;&#263; sztuk + ew. lure supply</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <span style="background:#fef9c3;padding:2px 6px;border-radius:4px;font-weight:600">"(4 Pack)"</span> lub <span style="background:#fef9c3;padding:2px 6px;border-radius:4px;font-weight:600">"(6 Pack)"</span><br>
    + <span style="background:#fef9c3;padding:2px 6px;border-radius:4px;font-weight:600">"+ 180 Days of Lure Supply"</span>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-size:.72rem;color:#64748b">Terro dominuje z "180 Days" claimem. 28.4% klient&#243;w oczekuje d&#322;ugiej trwa&#322;o&#347;ci. Pack size w nawiasie = standard Amazon.</td>
</tr>
<tr>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:600;color:#378ADD">Key Benefit</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">G&#322;&#243;wna korzy&#347;&#263; / USP wyr&#243;&#380;niaj&#261;cy na tle konkurencji</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <span style="background:#dbeafe;padding:2px 6px;border-radius:4px;font-weight:600">"Non-Toxic"</span> <span style="color:#94a3b8;font-size:.68rem">GAP: tylko 2/5 konkurent&#243;w</span><br>
    <span style="background:#dbeafe;padding:2px 6px;border-radius:4px;font-weight:600">"Pet &amp; Kid Safe"</span> <span style="color:#94a3b8;font-size:.68rem">17.3% motywacja kupuj&#261;cych</span><br>
    <span style="background:#dbeafe;padding:2px 6px;border-radius:4px;font-weight:600">"Fast-Acting"</span> <span style="color:#94a3b8;font-size:.68rem">21.6% pozytywnych recenzji</span>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-size:.72rem;color:#64748b"><strong>Safety = biggest gap.</strong> Tylko Aunt Fannie&#8217;s i Super Ninja komunikuj&#261; bezpiecze&#324;stwo. 17.3% kupuj&#261;cych motywowanych bezpiecze&#324;stwem.</td>
</tr>
<tr>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:600;color:#D85A30">Use Case</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">Gdzie / do czego u&#380;ywa&#263;</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <span style="background:#ffedd5;padding:2px 6px;border-radius:4px;font-weight:600">"for Kitchen &amp; Home"</span> <span style="color:#94a3b8;font-size:.68rem">29.2% g&#322;&#243;wny scenariusz</span><br>
    <span style="background:#ffedd5;padding:2px 6px;border-radius:4px;font-weight:600">"Fruit Fly Killer"</span> <span style="color:#94a3b8;font-size:.68rem">SV 15,982</span><br>
    <span style="background:#ffedd5;padding:2px 6px;border-radius:4px;font-weight:600">"Gnat Traps for House Indoor"</span> <span style="color:#94a3b8;font-size:.68rem">SV 74,381</span>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-size:.72rem;color:#64748b">Dodanie "gnat" poszerza zasi&#281;g o 74K SV. 29.2% klient&#243;w u&#380;ywa w kuchni &mdash; potwierdza use case.</td>
</tr>
<tr>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:600;color:#D4537E">Differentiator</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">Co wyr&#243;&#380;nia od konkurencji</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <span style="background:#fce7f3;padding:2px 6px;border-radius:4px;font-weight:600">"Results in 24 Hours"</span> <span style="color:#94a3b8;font-size:.68rem">GAP: tylko Super Ninja twierdzi</span><br>
    <span style="background:#fce7f3;padding:2px 6px;border-radius:4px;font-weight:600">"Plant-Based Formula"</span> <span style="color:#94a3b8;font-size:.68rem">14.1% ceni eko sk&#322;ad</span>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-size:.72rem;color:#64748b"><strong>Speed claim = competitive gap.</strong> Tylko 1/5 podaje konkretny czas. 21.6% recenzji chwali szybko&#347;&#263;.</td>
</tr>
</tbody>
</table>

<div class="note" style="margin-top:14px">
  <strong>Przyk&#322;adowa struktura:</strong> [Brand] Fruit Fly Traps for Indoors (4 Pack) + 180 Days Supply &mdash; Non-Toxic, Pet &amp; Kid Safe &mdash; Fast-Acting Fruit Fly &amp; Gnat Killer for Kitchen &amp; Home &mdash; Results in 24 Hours, Plant-Based Formula<br>
  <strong>Znaki:</strong> ~195 (limit 200). Zawiera: 2 top keywords (SV 96K + 74K), safety gap, speed differentiator, use case.
</div>
</div>

<!-- ═══ BULLET POINTS BRIEF ═══ -->
<h2 style="margin-top:28px">Struktura Bullet Points</h2>
<p style="font-size:.78rem;color:#64748b;margin-bottom:14px;line-height:1.5">Ka&#380;dy bullet point powinien adresowa&#263; konkretny temat z Gap Analysis lub Unmet Customer Needs. Poni&#380;ej rekomendacje co powinno znale&#378;&#263; si&#281; w ka&#380;dym z 5 bullet&#243;w, jakie s&#322;owa kluczowe wykorzysta&#263; i jakie dane z recenzji to uzasadniaj&#261;.</p>

<div class="card">
<table style="width:100%;border-collapse:collapse;font-size:.78rem">
<thead>
<tr style="background:#f8fafc">
  <th style="padding:10px 12px;text-align:left;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700;width:50px">#</th>
  <th style="padding:10px 12px;text-align:left;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700;width:160px">Temat (nag&#322;&#243;wek)</th>
  <th style="padding:10px 12px;text-align:left;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700">Co powinno zawiera&#263;</th>
  <th style="padding:10px 12px;text-align:left;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700;width:180px">S&#322;owa kluczowe</th>
  <th style="padding:10px 12px;text-align:left;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700;width:200px">Uzasadnienie (dane)</th>
</tr>
</thead>
<tbody>

<tr style="border-left:4px solid #1D9E75">
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:800;color:#1D9E75;font-size:.95rem">1</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:700;color:#1D9E75">FAST-ACTING RESULTS</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <ul class="is-bullets" style="margin:0">
      <li>Konkretny czas dzia&#322;ania: "results within 24 hours"</li>
      <li>Mechanizm: jak wab przyci&#261;ga muchy (scientifically formulated lure)</li>
      <li>Zasi&#281;g: "attracts fruit flies from up to 3 feet away"</li>
      <li>Dow&#243;d: "dramatic decrease in fruit fly population"</li>
    </ul>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <span style="background:#dcfce7;padding:2px 6px;border-radius:4px;font-weight:600;font-size:.72rem">"fruit fly killer"</span> <span style="color:#94a3b8;font-size:.65rem">SV 15,982</span><br>
    <span style="background:#dcfce7;padding:2px 6px;border-radius:4px;font-weight:600;font-size:.72rem">"fruit fly bait"</span> <span style="color:#94a3b8;font-size:.65rem">SV 543, rel 0.92</span>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-size:.72rem;color:#64748b">
    <strong style="color:#dc2626">30.9%</strong> recenzji: "no effect" &mdash; bullet #1 musi natychmiast budowa&#263; zaufanie do skuteczno&#347;ci.<br>
    <strong style="color:#16a34a">21.6%</strong> pozytywnych chwali szybko&#347;&#263;.<br>
    <strong>GAP:</strong> Tylko Super Ninja podaje "24h". Okazja do wyr&#243;&#380;nienia.
  </td>
</tr>

<tr style="border-left:4px solid #378ADD">
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:800;color:#378ADD;font-size:.95rem">2</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:700;color:#378ADD">NON-TOXIC &amp; SAFE</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <ul class="is-bullets" style="margin:0">
      <li>Bezpiecze&#324;stwo: "safe for use around food, pets, and children"</li>
      <li>Sk&#322;ad: "plant-based formula, no harsh chemicals"</li>
      <li>Certyfikaty / testy je&#347;li dost&#281;pne</li>
      <li>Umiejscowienie: "safe to place near fruit bowls and kitchen counters"</li>
    </ul>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <span style="background:#dbeafe;padding:2px 6px;border-radius:4px;font-weight:600;font-size:.72rem">"gnat traps for house indoor"</span> <span style="color:#94a3b8;font-size:.65rem">SV 74,381</span><br>
    <span style="background:#dbeafe;padding:2px 6px;border-radius:4px;font-weight:600;font-size:.72rem">"indoor fruit fly traps"</span> <span style="color:#94a3b8;font-size:.65rem">SV 692, rel 0.85</span>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-size:.72rem;color:#64748b">
    <strong style="color:#dc2626">BIGGEST GAP:</strong> Tylko 2/5 konkurent&#243;w porusza bezpiecze&#324;stwo.<br>
    <strong style="color:#16a34a">17.3%</strong> kupuj&#261;cych motywowanych bezpiecze&#324;stwem.<br>
    <strong>14.1%</strong> pozytywnych recenzji ceni eko/naturalny sk&#322;ad.
  </td>
</tr>

<tr style="border-left:4px solid #BA7517">
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:800;color:#BA7517;font-size:.95rem">3</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:700;color:#BA7517">LONG-LASTING VALUE</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <ul class="is-bullets" style="margin:0">
      <li>Trwa&#322;o&#347;&#263;: "each lure lasts up to 45 days" / "180-day total supply"</li>
      <li>Por&#243;wnanie z DIY: "no daily mixing like vinegar traps"</li>
      <li>Koszt: "less than $2.50/month of protection"</li>
      <li>Zawarto&#347;&#263;: "includes X traps + X refill lures"</li>
    </ul>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <span style="background:#fef9c3;padding:2px 6px;border-radius:4px;font-weight:600;font-size:.72rem">"fruit fly lure"</span> <span style="color:#94a3b8;font-size:.65rem">SV 250, rel 0.85</span><br>
    <span style="background:#fef9c3;padding:2px 6px;border-radius:4px;font-weight:600;font-size:.72rem">"fruit fly trap refill"</span> <span style="color:#94a3b8;font-size:.65rem">SV 3,418</span>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-size:.72rem;color:#64748b">
    <strong style="color:#dc2626">15.6%</strong> negatywnych: "runs out quickly".<br>
    <strong style="color:#dc2626">13.7%</strong> por&#243;wnuje z DIY octem (ta&#324;sze).<br>
    <strong style="color:#d97706">28.4%</strong> oczekuje d&#322;u&#380;szej trwa&#322;o&#347;ci.<br>
    Terro dominuje z "180 days" claimem.
  </td>
</tr>

<tr style="border-left:4px solid #7F77DD">
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:800;color:#7F77DD;font-size:.95rem">4</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:700;color:#7F77DD">DISCREET DESIGN &amp; EASY TO USE</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <ul class="is-bullets" style="margin:0">
      <li>Design: "blends seamlessly with kitchen decor"</li>
      <li>Prostota: "ready to use &mdash; just open and place, no assembly"</li>
      <li>Monitoring: "built-in window to check progress"</li>
      <li>Czysto&#347;&#263;: "no mess, no sticky residue, no spills"</li>
    </ul>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <span style="background:#ede9fe;padding:2px 6px;border-radius:4px;font-weight:600;font-size:.72rem">"fly catcher indoor"</span> <span style="color:#94a3b8;font-size:.65rem">SV 6,241</span><br>
    <span style="background:#ede9fe;padding:2px 6px;border-radius:4px;font-weight:600;font-size:.72rem">"fly traps indoor for home"</span> <span style="color:#94a3b8;font-size:.65rem">SV 4,779</span>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-size:.72rem;color:#64748b">
    <strong style="color:#16a34a">16.2%</strong> pozytywnych: "easy to use".<br>
    <strong style="color:#16a34a">10.8%</strong> chwali dyskretny design.<br>
    <strong style="color:#dc2626">20.4%</strong> oczekuje mess-free setup.<br>
    Monitoring window = unmet need z Rufus (kategoria).
  </td>
</tr>

<tr style="border-left:4px solid #639922">
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:800;color:#639922;font-size:.95rem">5</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-weight:700;color:#639922">WHERE TO PLACE &amp; HOW IT WORKS</td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <ul class="is-bullets" style="margin:0">
      <li>Lokalizacje: "near fruit bowls, trash cans, compost areas, kitchen counters"</li>
      <li>Mechanizm: kr&#243;tkie wyja&#347;nienie jak dzia&#322;a (lure attracts &rarr; trapped inside)</li>
      <li>Zasi&#281;g: "for fruit flies (Drosophila) and gnats &mdash; not house flies"</li>
      <li>Obietnica: "covers your entire kitchen with just 2&ndash;4 traps"</li>
    </ul>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9">
    <span style="background:#ecfccb;padding:2px 6px;border-radius:4px;font-weight:600;font-size:.72rem">"fruit flies"</span> <span style="color:#94a3b8;font-size:.65rem">SV 5,435</span><br>
    <span style="background:#ecfccb;padding:2px 6px;border-radius:4px;font-weight:600;font-size:.72rem">"gnat killer indoor"</span> <span style="color:#94a3b8;font-size:.65rem">SV 22,245</span><br>
    <span style="background:#ecfccb;padding:2px 6px;border-radius:4px;font-weight:600;font-size:.72rem">"drain fly killer"</span> <span style="color:#94a3b8;font-size:.65rem">SV 34,515</span>
  </td>
  <td style="padding:10px 12px;border-bottom:1px solid #f1f5f9;font-size:.72rem;color:#64748b">
    <strong style="color:#dc2626">2.9%</strong> negatywnych: "attracts wrong insects" &mdash; konieczne precyzyjne targetowanie.<br>
    <strong style="color:#16a34a">29.2%</strong> u&#380;ywa w kuchni, 13.8% przy &#347;mieciach.<br>
    <strong>GAP:</strong> Mechanism/Tech poruszany tylko przez 2/5 konkurent&#243;w.
  </td>
</tr>

</tbody>
</table>
</div>

<!-- ═══ KEYWORD INTEGRATION MAP ═══ -->
<h2 style="margin-top:28px">Mapa integracji s&#322;&#243;w kluczowych</h2>
<p style="font-size:.78rem;color:#64748b;margin-bottom:14px;line-height:1.5">Najwa&#380;niejsze s&#322;owa kluczowe i rekomendowane miejsce ich umieszczenia. Priorytet: tytu&#322; &gt; bullet points &gt; backend keywords.</p>

<div class="card">
<table style="width:100%;border-collapse:collapse;font-size:.78rem">
<thead>
<tr style="background:#f8fafc">
  <th style="padding:8px 12px;text-align:left;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700">S&#322;owo kluczowe</th>
  <th style="padding:8px 12px;text-align:right;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700;width:80px">SV</th>
  <th style="padding:8px 12px;text-align:center;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700;width:60px">Rel.</th>
  <th style="padding:8px 12px;text-align:center;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700;width:70px">Tytu&#322;</th>
  <th style="padding:8px 12px;text-align:center;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700;width:70px">Bullets</th>
  <th style="padding:8px 12px;text-align:center;border-bottom:2px solid #e2e8f0;color:#475569;font-weight:700;width:70px">Backend</th>
</tr>
</thead>
<tbody>
<tr><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;font-weight:600">fruit fly traps for indoors</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:right;font-weight:700;color:#0f2942">96,624</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center">0.76</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#d4d4d4;font-size:1rem">&#9675;</span></td></tr>
<tr><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;font-weight:600">gnat traps for house indoor</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:right;font-weight:700;color:#0f2942">74,381</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center">0.53</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#d4d4d4;font-size:1rem">&#9675;</span></td></tr>
<tr><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;font-weight:600">fruit fly trap</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:right;font-weight:700;color:#0f2942">38,092</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center">0.76</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#d4d4d4;font-size:1rem">&#9675;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#d4d4d4;font-size:1rem">&#9675;</span></td></tr>
<tr><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;font-weight:600">drain fly killer</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:right;font-weight:700;color:#0f2942">34,515</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center">0.46</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#d4d4d4;font-size:1rem">&#9675;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td></tr>
<tr><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;font-weight:600">gnat killer indoor</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:right;font-weight:700;color:#0f2942">22,245</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center">0.38</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#d4d4d4;font-size:1rem">&#9675;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td></tr>
<tr><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;font-weight:600">fruit fly killer</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:right;font-weight:700;color:#0f2942">15,982</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center">0.53</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#d4d4d4;font-size:1rem">&#9675;</span></td></tr>
<tr><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;font-weight:600">fruit fly bait</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:right">543</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center;font-weight:600;color:#16a34a">0.92</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#d4d4d4;font-size:1rem">&#9675;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td></tr>
<tr><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;font-weight:600">fruit fly trap refill</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:right">3,418</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center">0.38</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#d4d4d4;font-size:1rem">&#9675;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td></tr>
<tr><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;font-weight:600">fly traps indoor for home</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:right">4,779</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center">0.38</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#d4d4d4;font-size:1rem">&#9675;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td></tr>
<tr><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;font-weight:600">fruit fly lure</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:right">250</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center;font-weight:600;color:#16a34a">0.85</td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#d4d4d4;font-size:1rem">&#9675;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td><td style="padding:7px 12px;border-bottom:1px solid #f1f5f9;text-align:center"><span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span></td></tr>
</tbody>
</table>
<div class="note" style="margin-top:12px">
  <strong>Legenda:</strong> <span style="color:#16a34a;font-weight:700;font-size:1rem">&#9679;</span> = nale&#380;y umie&#347;ci&#263; &nbsp;|&nbsp; <span style="color:#d4d4d4;font-size:1rem">&#9675;</span> = nie jest konieczne (pokryte wy&#380;ej lub niska relevancy)<br>
  <strong>Zasada:</strong> Tytu&#322; powinien zawiera&#263; 2&ndash;3 top keywords (SV &gt; 15K). Bullet points powinny naturalnie wplata&#263; secondary keywords. Backend keywords s&#322;u&#380;&#261; do pokrycia long-tail i synonim&#243;w.
</div>
</div>

<div class="note" style="margin-top:22px">
  <strong>Metodologia:</strong> Rekomendacje oparte na: (1) analizie tytu&#322;&#243;w i bullet points 5 konkurent&#243;w z Amazon SP-API (Tab 5), (2) Gap Analysis &mdash; tematy nieporuszane przez konkurencj&#281; (Safety 2/5, Mechanism 2/5), (3) Unmet Customer Needs z 5 722 recenzji (Tab 4), (4) 433 s&#322;&#243;w kluczowych z Helium 10 Niche Analysis (Tab 6) posortowanych wg Search Volume i Relevancy Score. Forma bezosobowa.
</div>

</div><!-- END TAB CP -->
'''

# ── Inject ───────────────────────────────────────────────────────────────────
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add tab button
html = html.replace(
    """<div class="tab" onclick="show('tis',this)">7 \u2014 Strategia Zdj\u0119\u0107</div>\n</div>""",
    """<div class="tab" onclick="show('tis',this)">7 \u2014 Strategia Zdj\u0119\u0107</div>\n  <div class="tab" onclick="show('tcp',this)">8 \u2014 Copy Brief</div>\n</div>"""
)
print('\u2713 Tab button added')

# Insert panel before </div><!-- .content -->
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
print('\n\u2713 Tab 8 \u2014 Copy Brief injected.')
