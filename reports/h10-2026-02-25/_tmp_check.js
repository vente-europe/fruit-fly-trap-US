
// ═══════════════ TAB G — SHARE & LEADERS ════════════════════════════════
  let _slView = 'brand';
  let _slSegTab = 'All';
  const _slExclBrands = new Set();
  const _slExclAsins  = new Set();

  function slInit() {
    if (!SHARE_DATA || !SHARE_DATA.asin_data || !SHARE_DATA.asin_data.length) return;
    const pl = SHARE_DATA.period_labels;
    document.getElementById('sl_p1_label').textContent = pl.p1;
    document.getElementById('sl_p2_label').textContent = pl.p2;

    // Populate brand checklist (all ticked by default)
    const brands = [...new Set(SHARE_DATA.asin_data.map(r => r.brand))].sort();
    const bList = document.getElementById('sl_brand_list');
    brands.forEach(b => {
      const lbl = document.createElement('label');
      const cb  = document.createElement('input');
      cb.type = 'checkbox'; cb.value = b; cb.checked = true;
      cb.addEventListener('change', () => { if (!cb.checked) _slExclBrands.add(b); else _slExclBrands.delete(b); slRender(); });
      lbl.appendChild(cb); lbl.appendChild(document.createTextNode(' ' + b));
      bList.appendChild(lbl);
    });

    // Populate ASIN checklist (all ticked by default)
    const asins = [...new Set(SHARE_DATA.asin_data.map(r => r.asin))].sort();
    const aList = document.getElementById('sl_asin_list');
    const asnLookup = Object.fromEntries(SHARE_DATA.asin_data.map(r => [r.asin, r.brand]));
    asins.forEach(a => {
      const lbl = document.createElement('label');
      const cb  = document.createElement('input');
      cb.type = 'checkbox'; cb.value = a; cb.checked = true;
      cb.addEventListener('change', () => { if (!cb.checked) _slExclAsins.add(a); else _slExclAsins.delete(a); slRender(); });
      lbl.appendChild(cb); lbl.appendChild(document.createTextNode(' ' + a + ' — ' + (asnLookup[a] || '')));
      aList.appendChild(lbl);
    });

    document.getElementById('sl_seg_filter').addEventListener('change', slRender);
    slRender();
  }

  function slSetView(v) {
    _slView = v;
    document.getElementById('sl_view_brand').classList.toggle('active', v === 'brand');
    document.getElementById('sl_view_asin').classList.toggle('active', v === 'asin');
    slRender();
  }

  function slSetSegTab(s) {
    _slSegTab = s;
    document.querySelectorAll('.seg-tab-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    slRender();
  }

  function slToggleAll(listId, checked) {
    document.querySelectorAll('#' + listId + ' input[type=checkbox]').forEach(cb => { cb.checked = checked; });
    _slExclBrands.clear(); _slExclAsins.clear();
    document.querySelectorAll('#sl_brand_list input').forEach(cb => { if (!cb.checked) _slExclBrands.add(cb.value); });
    document.querySelectorAll('#sl_asin_list input').forEach(cb =>  { if (!cb.checked) _slExclAsins.add(cb.value); });
    slRender();
  }

  function slClearFilters() {
    _slExclBrands.clear(); _slExclAsins.clear();
    document.querySelectorAll('#sl_brand_list input, #sl_asin_list input').forEach(cb => { cb.checked = true; });
    document.getElementById('sl_seg_filter').value = 'All';
    slRender();
  }

  function slGetFiltered(segOverride) {
    const seg = segOverride !== undefined ? segOverride : document.getElementById('sl_seg_filter').value;
    return SHARE_DATA.asin_data.filter(r => {
      if (_slExclBrands.has(r.brand)) return false;
      if (_slExclAsins.has(r.asin))  return false;
      if (seg !== 'All' && r.segment !== seg) return false;
      return true;
    });
  }

  function slAgg(data, key) {
    // key = 'brand' or 'asin'
    const m = {};
    for (const r of data) {
      const k = r[key];
      if (!m[k]) m[k] = {name: k, brand: r.brand, segment: r.segment, title: r.title || k,
                          u1:0, u2:0, r1:0, r2:0};
      m[k].u1 += r.p1_units || 0;
      m[k].u2 += r.p2_units || 0;
      m[k].r1 += r.p1_rev   || 0;
      m[k].r2 += r.p2_rev   || 0;
    }
    return m;
  }

  function slTotals(agg) {
    let tu1=0,tu2=0,tr1=0,tr2=0;
    for (const v of Object.values(agg)) {
      tu1+=v.u1; tu2+=v.u2; tr1+=v.r1; tr2+=v.r2;
    }
    return {tu1,tu2,tr1,tr2};
  }

  function slEnrich(agg, t) {
    const rows = [];
    for (const [k, v] of Object.entries(agg)) {
      const us1 = t.tu1 ? v.u1/t.tu1*100 : null;
      const us2 = t.tu2 ? v.u2/t.tu2*100 : null;
      const rs1 = t.tr1 ? v.r1/t.tr1*100 : null;
      const rs2 = t.tr2 ? v.r2/t.tr2*100 : null;
      rows.push({...v,
        us1, us2, rs1, rs2,
        u_delta: (us2 !== null && us1 !== null) ? us2 - us1 : null,
        r_delta: (rs2 !== null && rs1 !== null) ? rs2 - rs1 : null,
      });
    }
    return rows;
  }

  function _f$(v,d=1) { return v===null||v===undefined ? '—' : v.toFixed(d); }
  function _fc$(v)    { return v===null||v===undefined ? '—' : '$'+v.toLocaleString('en-US',{maximumFractionDigits:0}); }
  function _fp$(v,d=1){ return v===null||v===undefined ? '—' : _f$(v,d)+'%'; }
  function _delta(v)  {
    if (v===null||v===undefined) return '<span class="delta-neu">—</span>';
    const cls = v>0.05?'delta-pos':v<-0.05?'delta-neg':'delta-neu';
    return `<span class="${cls}">${v>0?'+':''}${v.toFixed(2)}pp</span>`;
  }

  function slRenderKpis(rows, t) {
    const p2=SHARE_DATA.period_labels.p2;
    // Leader by rev share P2
    const sorted_r = [...rows].sort((a,b)=>(b.r2||0)-(a.r2||0));
    const sorted_u = [...rows].sort((a,b)=>(b.u2||0)-(a.u2||0));
    const lrName = sorted_r[0]?.name||'—';
    const lrPct  = sorted_r[0] ? _fp$(sorted_r[0].rs2) : '—';
    const luName = sorted_u[0]?.name||'—';
    const luPct  = sorted_u[0] ? _fp$(sorted_u[0].us2) : '—';
    const kpis = [
      {v: _fc$(t.tr2), l: `Total Revenue (P2)`},
      {v: _f$(t.tu2,0), l: `Total Units (P2)`},
      {v: _fc$(t.tr1), l: `Total Revenue (P1)`},
      {v: _f$(t.tu1,0), l: `Total Units (P1)`},
      {v: lrName, l: `Rev Share Leader (P2) · ${lrPct}`},
      {v: luName, l: `Unit Share Leader (P2) · ${luPct}`},
    ];
    document.getElementById('sl_kpis').innerHTML = kpis.map(k=>
      `<div class="kpi"><div class="kpi-v" style="font-size:.95rem">${k.v}</div><div class="kpi-l">${k.l}</div></div>`
    ).join('');
  }

  function slRenderTable(rows, viewKey) {
    const pl = SHARE_DATA.period_labels;
    const nameLabel = viewKey === 'brand' ? 'Brand' : 'ASIN';
    document.getElementById('sl_table_title').textContent =
      (viewKey==='brand'?'Brand':'ASIN') + ` Market Share — P1 (${pl.p1}) vs P2 (${pl.p2})`;
    const sorted = [...rows].sort((a,b)=>(b.r2||0)-(a.r2||0));
    document.getElementById('sl_share_thead').innerHTML = `<tr>
      <th>${nameLabel}</th>
      <th>Rev P1</th><th>Rev Share P1</th><th>Units P1</th><th>Unit Share P1</th>
      <th>Rev P2</th><th>Rev Share P2</th><th>Units P2</th><th>Unit Share P2</th>
      <th>Rev Share Δ</th><th>Unit Share Δ</th>
    </tr>`;
    document.getElementById('sl_share_tbody').innerHTML = sorted.map(r => `<tr>
      <td><strong>${r.name}</strong>${viewKey==='asin'?`<br><small style='color:#94a3b8'>${r.brand}</small>`:''}</td>
      <td>${_fc$(r.r1)}</td><td>${_fp$(r.rs1)}</td><td>${_f$(r.u1,0)}</td><td>${_fp$(r.us1)}</td>
      <td>${_fc$(r.r2)}</td><td>${_fp$(r.rs2)}</td><td>${_f$(r.u2,0)}</td><td>${_fp$(r.us2)}</td>
      <td>${_delta(r.r_delta)}</td><td>${_delta(r.u_delta)}</td>
    </tr>`).join('');
  }

  function slRenderSegTable(segName) {
    const pl = SHARE_DATA.period_labels;
    const data = slGetFiltered(segName === 'All' ? 'All' : segName);
    const agg  = slAgg(data, _slView);
    const t    = slTotals(agg);
    const rows = slEnrich(agg, t);
    const sorted = [...rows].sort((a,b)=>(b.r2||0)-(a.r2||0));
    const nameLabel = _slView === 'brand' ? 'Brand' : 'ASIN';
    const segLabel = segName === 'All' ? 'All Segments' : segName;
    document.getElementById('sl_seg_thead').innerHTML = `<tr>
      <th>${nameLabel} (${segLabel})</th>
      <th>Rev P1</th><th>Rev Share</th><th>Rev P2</th><th>Rev Share P2</th><th>Rev Δ</th>
      <th>Units P2</th><th>Unit Share P2</th><th>Unit Δ</th>
    </tr>`;
    document.getElementById('sl_seg_tbody').innerHTML = sorted.map(r => `<tr>
      <td><strong>${r.name}</strong></td>
      <td>${_fc$(r.r1)}</td><td>${_fp$(r.rs1)}</td>
      <td>${_fc$(r.r2)}</td><td>${_fp$(r.rs2)}</td><td>${_delta(r.r_delta)}</td>
      <td>${_f$(r.u2,0)}</td><td>${_fp$(r.us2)}</td><td>${_delta(r.u_delta)}</td>
    </tr>`).join('');
  }

  function slRenderLeaders(rows, rowsAsin) {
    const topRevBrand = [...rows].sort((a,b)=>(b.rs2||0)-(a.rs2||0))[0];
    const topUnitBrand = [...rows].sort((a,b)=>(b.us2||0)-(a.us2||0))[0];
    const topRevAsin = rowsAsin ? [...rowsAsin].sort((a,b)=>(b.rs2||0)-(a.rs2||0))[0] : null;
    const topUnitAsin = rowsAsin ? [...rowsAsin].sort((a,b)=>(b.us2||0)-(a.us2||0))[0] : null;

    // Segment leaders
    const segs = ['Lure','Sticky traps','Passive attractor'];
    let segCards = '';
    for (const seg of segs) {
      const sd = slGetFiltered(seg);
      const sagg = slAgg(sd, 'brand');
      const st = slTotals(sagg);
      const sr = slEnrich(sagg, st);
      const topR = [...sr].sort((a,b)=>(b.rs2||0)-(a.rs2||0))[0];
      const topU = [...sr].sort((a,b)=>(b.us2||0)-(a.us2||0))[0];
      segCards += `
        <div class="leader-card">
          <h4>${seg} — Rev Leader</h4>
          <div class="lc-name">${topR?.name||'—'}</div>
          <div class="lc-val">${topR ? _fp$(topR.rs2) : '—'} rev share P2</div>
        </div>
        <div class="leader-card">
          <h4>${seg} — Unit Leader</h4>
          <div class="lc-name">${topU?.name||'—'}</div>
          <div class="lc-val">${topU ? _fp$(topU.us2) : '—'} unit share P2</div>
        </div>`;
    }

    document.getElementById('sl_leaders').innerHTML = `
      <div class="leader-card">
        <h4>Overall — Revenue Share Leader</h4>
        <div class="lc-name">${topRevBrand?.name||'—'}</div>
        <div class="lc-val">${topRevBrand ? _fp$(topRevBrand.rs2) : '—'} of total rev (P2)</div>
      </div>
      <div class="leader-card">
        <h4>Overall — Unit Share Leader</h4>
        <div class="lc-name">${topUnitBrand?.name||'—'}</div>
        <div class="lc-val">${topUnitBrand ? _fp$(topUnitBrand.us2) : '—'} of total units (P2)</div>
      </div>
      ${topRevAsin ? `<div class="leader-card">
        <h4>Top ASIN — Revenue Share</h4>
        <div class="lc-name">${topRevAsin.name}</div>
        <div class="lc-val">${_fp$(topRevAsin.rs2)} rev share P2</div>
      </div>` : ''}
      ${topUnitAsin ? `<div class="leader-card">
        <h4>Top ASIN — Unit Share</h4>
        <div class="lc-name">${topUnitAsin.name}</div>
        <div class="lc-val">${_fp$(topUnitAsin.us2)} unit share P2</div>
      </div>` : ''}
      ${segCards}`;
  }

  function slRenderYoY(rows, type) {
    // type = 'rev' or 'unit'
    const delta_key = type === 'rev' ? 'r_delta' : 'u_delta';
    const share_p1  = type === 'rev' ? 'rs1' : 'us1';
    const share_p2  = type === 'rev' ? 'rs2' : 'us2';
    const valid = rows.filter(r => r[delta_key] !== null);
    const gainers = [...valid].sort((a,b)=>(b[delta_key]||0)-(a[delta_key]||0)).slice(0,10);
    const losers  = [...valid].sort((a,b)=>(a[delta_key]||0)-(b[delta_key]||0)).slice(0,10);

    const mkRow = (r, i) => `<tr>
      <td>${i+1}</td>
      <td><strong>${r.name}</strong></td>
      <td>${_fp$(r[share_p1])}</td>
      <td>${_fp$(r[share_p2])}</td>
      <td>${_delta(r[delta_key])}</td>
    </tr>`;

    document.getElementById(`sl_gainers_${type}_body`).innerHTML = gainers.map(mkRow).join('');
    document.getElementById(`sl_losers_${type}_body`).innerHTML  = losers.map(mkRow).join('');
  }

  function slRender() {
    const data     = slGetFiltered();
    const aggMain  = slAgg(data, _slView);
    const totals   = slTotals(aggMain);
    const rows     = slEnrich(aggMain, totals);

    // For leaders, always compute brand and asin separately
    const aggBrand = slAgg(data, 'brand');
    const tBrand   = slTotals(aggBrand);
    const rowsBrand = slEnrich(aggBrand, tBrand);
    const aggAsin  = slAgg(data, 'asin');
    const tAsin    = slTotals(aggAsin);
    const rowsAsin = slEnrich(aggAsin, tAsin);

    slRenderKpis(rowsBrand, tBrand);
    slRenderTable(rows, _slView);
    slRenderSegTable(_slSegTab);
    slRenderLeaders(rowsBrand, rowsAsin);
    slRenderYoY(rows, 'rev');
    slRenderYoY(rows, 'unit');
  }

  // ═══════════════════════════════════════════════════════════════════════════

// ── Tab switching ────────────────────────────────────────────────────────────
function show(id, el) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  el.classList.add('active');
}

const C10 = ['#2563eb','#16a34a','#dc2626','#d97706','#7c3aed','#0891b2','#be185d','#65a30d','#ea580c','#1d4ed8'];

// ── Scatter helper ─────────────────────────────────────────────────────────
function makeScatter(id, data, xlabel, ylabel, color) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  return new Chart(ctx, {
    type: 'scatter',
    data: { datasets: [{ data: data.map(d => ({x:d.x, y:d.y})), backgroundColor: color+'99', pointRadius: 5 }] },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { display: false },
        tooltip: { callbacks: { label: ctx2 => {
          const d = data[ctx2.dataIndex];
          return d ? `${d.label}: (${d.x?.toLocaleString()}, ${d.y?.toLocaleString()})` : '';
        } } } },
      scales: {
        x: { title: { display: true, text: xlabel, font: { size: 10 } } },
        y: { title: { display: true, text: ylabel, font: { size: 10 } },
              ticks: { callback: v => '$' + (v/1000).toFixed(0) + 'k' } }
      }
    }
  });
}

// ── Tab B — Brand Pie Chart (Lure 12M) ───────────────────────────────────────
const BRAND_SMALL = 0.08; // slices < 8% get leader lines
const brandPieLeaderPlugin = {
  id: 'brandPieLeader',
  afterDraw(chart) {
    const ctx2  = chart.ctx;
    const meta  = chart.getDatasetMeta(0);
    const data  = chart.data.datasets[0].data;
    const lbls  = chart.data.labels;
    const total = data.reduce((a, b) => a + b, 0);
    const slices = [];
    meta.data.forEach((arc, i) => {
      if (data[i] / total >= BRAND_SMALL) return;
      const mid = (arc.startAngle + arc.endAngle) / 2;
      const r   = arc.outerRadius;
      const cos = Math.cos(mid), sin = Math.sin(mid);
      const pct = Math.round(data[i] / total * 100);
      slices.push({ arc, i, r, cos, sin, pct,
        txt: lbls[i] + '  ' + pct + '%', onRight: cos > 0,
        ex: arc.x + cos * (r + 16), ey: arc.y + sin * (r + 16),
      });
    });
    slices.sort((a, b) => a.arc.startAngle - b.arc.startAngle);
    slices.forEach(s => { s.ly = s.ey; });
    const GAP = 14;
    for (let pass = 0; pass < 30; pass++) {
      let moved = false;
      for (let i = 1; i < slices.length; i++) {
        const a = slices[i-1], b = slices[i];
        if (b.ly - a.ly < GAP) {
          const d = (GAP - (b.ly - a.ly)) / 2;
          a.ly -= d; b.ly += d; moved = true;
        }
      }
      if (!moved) break;
    }
    const col = '#1e293b';
    slices.forEach(s => {
      ctx2.save();
      ctx2.strokeStyle = col; ctx2.lineWidth = 1.2;
      ctx2.beginPath();
      ctx2.moveTo(s.arc.x + s.cos * (s.r + 2), s.arc.y + s.sin * (s.r + 2));
      ctx2.lineTo(s.ex, s.ey);
      ctx2.lineTo(s.ex, s.ly);
      ctx2.stroke();
      ctx2.font = 'bold 10px sans-serif';
      ctx2.textAlign    = s.onRight ? 'left' : 'right';
      ctx2.textBaseline = 'middle';
      ctx2.fillStyle    = col;
      ctx2.fillText(s.txt, s.ex + (s.onRight ? 4 : -4), s.ly);
      ctx2.restore();
    });
  }
};
new Chart(document.getElementById('brandPieChart'), {
  type: 'pie',
  plugins: [ChartDataLabels, brandPieLeaderPlugin],
  data: {
    labels: ["Terro", "Aunt Fannie's", "Super Ninja", "HOT SHOT", "Qualirey", "Raid", "STEM", "Fly Away Product", "RESCUE!", "Acme Approved"],
    datasets: [{ data: [13099935, 3791909, 1398257, 1056369, 847920, 696475, 129352, 95730, 30844, 25014], backgroundColor: C10 }]
  },
  options: {
    maintainAspectRatio: false,
    layout: { padding: { top: 90, left: 70, right: 20, bottom: 10 } },
    plugins: {
      legend: { display: false },
      datalabels: {
        formatter: (v, ctx) => {
          const pct = Math.round(v / ctx.chart.data.datasets[0].data.reduce((a,b) => a+b, 0) * 100);
          const lbl = ctx.chart.data.labels[ctx.dataIndex];
          return pct >= 8 ? lbl + '\n' + pct + '%' : null;
        },
        color: '#fff',
        font: { weight: 'bold', size: 11 },
        textAlign: 'center'
      },
      tooltip: {
        callbacks: {
          label: ctx => {
            const pct = (ctx.raw / 21175987 * 100).toFixed(1);
            return ctx.label + ': $' + ctx.raw.toLocaleString() + ' (' + pct + '%)';
          }
        }
      }
    }
  }
});

// ── Tab D — Seasonality ────────────────────────────────────────────────────
  const SHARE_DATA = {"asin_data": [{"asin": "B004FDUHS8", "brand": "Natural Catch", "segment": "Unclassified", "price": 18.51, "title": "Natural Catch Fruit Fly Traps - 2 Traps", "p1_units": 1756.0, "p2_units": 1767.2, "p1_rev": 32504.49, "p2_rev": 32710.87}, {"asin": "B005V6ASZU", "brand": "PIC", "segment": "Sticky traps", "price": 8.99, "title": "PIC FR10B 69060216325 Fly Ribbons Fruit Fly Traps for Indoor", "p1_units": 12814.9, "p2_units": 21885.5, "p1_rev": 115206.22, "p2_rev": 196750.56}, {"asin": "B009D17Z5U", "brand": "Fruit Fly BarPro", "segment": "Passive attractor", "price": 11.49, "title": "Fruit Fly BarPro \u2013 Vapor-Activated Insect Control Strip \u2013 Be", "p1_units": 20526.7, "p2_units": 21749.8, "p1_rev": 235851.44, "p2_rev": 249904.63}, {"asin": "B00E4GADNA", "brand": "Terro", "segment": "Lure", "price": 9.93, "title": "TERRO 2-Pack Fly Trap", "p1_units": 45489.3, "p2_units": 25230.7, "p1_rev": 451708.55, "p2_rev": 250541.15}, {"asin": "B00MP3DZ4I", "brand": "RESCUE!", "segment": "Unclassified", "price": 21.18, "title": "RESCUE! Fruit Fly Trap Bait Refill \u2013 30 Day Supply \u2013 10 Pack", "p1_units": 1136.3, "p2_units": 1460.6, "p1_rev": 24067.68, "p2_rev": 30934.66}, {"asin": "B00WMZMHPW", "brand": "Aunt Fannie's", "segment": "Lure", "price": 7.96, "title": "Aunt Fannie's FlyPunch Fruit Fly Trap for Indoor and Kitchen", "p1_units": 62186.5, "p2_units": 63070.2, "p1_rev": 495004.3, "p2_rev": 502038.55}, {"asin": "B01JIRNEQW", "brand": "Terro", "segment": "Lure", "price": 6.77, "title": "TERRO T2502 Ready-to-Use Indoor Fruit Fly Trap with Built in", "p1_units": 42924.0, "p2_units": 17703.8, "p1_rev": 290595.55, "p2_rev": 119854.66}, {"asin": "B01MRHXM0I", "brand": "Terro", "segment": "Lure", "price": 13.37, "title": "TERRO Fruit Fly Traps for Indoors (4 Pack) + 180 Days of Lur", "p1_units": 478199.2, "p2_units": 701671.2, "p1_rev": 6393523.71, "p2_rev": 9381343.94}, {"asin": "B06X1GN4B7", "brand": "Fruit Fly BarPro", "segment": "Passive attractor", "price": 59.99, "title": "Fruit Fly BarPro \u2013 Vapor-Activated Insect Control Strip \u2013 Be", "p1_units": 6216.1, "p2_units": 7509.6, "p1_rev": 372906.84, "p2_rev": 450500.9}, {"asin": "B071FVCYFW", "brand": "Unknown", "segment": "Unclassified", "price": null, "title": "B071FVCYFW", "p1_units": 0.0, "p2_units": 2078.3, "p1_rev": null, "p2_rev": null}, {"asin": "B07CR9B27M", "brand": "Fruit Fly BarPro", "segment": "Passive attractor", "price": 109.99, "title": "Fruit Fly BarPro \u2013 Vapor-Activated Insect Control Strip \u2013 Be", "p1_units": 4215.8, "p2_units": 4519.6, "p1_rev": 463698.04, "p2_rev": 497115.2}, {"asin": "B07KRRJT5J", "brand": "Kensizer", "segment": "Sticky traps", "price": 8.09, "title": "Kensizer 20-Pack Fruit Fly Trap, Yellow Sticky Gnat Traps Ki", "p1_units": 41626.2, "p2_units": 31825.4, "p1_rev": 336755.72, "p2_rev": 257467.49}, {"asin": "B07MF44XRY", "brand": "Aunt Fannie's", "segment": "Lure", "price": 41.99, "title": "Aunt Fannie's FlyPunch Fruit Fly Trap for Indoor and Kitchen", "p1_units": 7060.5, "p2_units": 5922.7, "p1_rev": 296468.3, "p2_rev": 248692.91}, {"asin": "B07V6HBYHK", "brand": "Catchmaster", "segment": "Sticky traps", "price": 12.99, "title": "Catchmaster Fly Ribbon 20-Pack, Bug & Fruit Fly Traps Outdoo", "p1_units": 59391.1, "p2_units": 83917.2, "p1_rev": 771490.52, "p2_rev": 1090083.78}, {"asin": "B07V7GC46D", "brand": "Terro", "segment": "Lure", "price": 37.89, "title": "Terro Fruit Fly Traps for Indoors (12 Pack) + 540 Days of Lu", "p1_units": 13589.2, "p2_units": 12955.7, "p1_rev": 514895.55, "p2_rev": 490889.96}, {"asin": "B07VYPGHFW", "brand": "Aunt Fannie's", "segment": "Lure", "price": 14.99, "title": "Aunt Fannie's FlyPunch Fruit Fly Trap for Indoor and Kitchen", "p1_units": 162243.7, "p2_units": 165411.9, "p1_rev": 2432032.91, "p2_rev": 2479523.78}, {"asin": "B07W1WLZM7", "brand": "Aunt Fannie's", "segment": "Lure", "price": 21.99, "title": "Aunt Fannie's FlyPunch Fruit Fly Trap for Indoor and Kitchen", "p1_units": 15894.3, "p2_units": 13471.3, "p1_rev": 349515.0, "p2_rev": 296233.45}, {"asin": "B07XLM4FWL", "brand": "Stingmon", "segment": "Sticky traps", "price": 7.99, "title": "36 Pack Fruit Fly Traps for Indoors, Gnat Traps for House In", "p1_units": 32744.0, "p2_units": 51767.0, "p1_rev": 261624.24, "p2_rev": 413618.01}, {"asin": "B083ZGVJ28", "brand": "Catchmaster", "segment": "Sticky traps", "price": 21.85, "title": "Catchmaster Gold Stick Fly Trap 4-Pk, Bug & Fruit Fly Traps ", "p1_units": 4381.1, "p2_units": 5578.6, "p1_rev": 95728.13, "p2_rev": 121891.97}, {"asin": "B08DMY3WWX", "brand": "Trappify", "segment": "Sticky traps", "price": 11.99, "title": "Trappify Hanging Fly Traps Outdoor: Fruit Fly Traps for Indo", "p1_units": 22485.5, "p2_units": 21458.4, "p1_rev": 269601.62, "p2_rev": 257286.58}, {"asin": "B08MZN1K2Y", "brand": "Mosqueda", "segment": "Sticky traps", "price": 5.98, "title": "Fruit Fly Traps Fungus Gnat Traps Yellow Sticky Bug Traps 36", "p1_units": 0.0, "p2_units": 5391.3, "p1_rev": 0.0, "p2_rev": 32239.68}, {"asin": "B099P3VMBM", "brand": "Wondercide", "segment": "Passive attractor", "price": 14.11, "title": "Wondercide - Fruit Fly Trap for Kitchen, Home, and Indoor Ar", "p1_units": 0.0, "p2_units": 6876.4, "p1_rev": 0.0, "p2_rev": 97026.57}, {"asin": "B09GD8T863", "brand": "STEM", "segment": "Lure", "price": 6.82, "title": "STEM Kills Fruit Fly Trap: Fruit Fly Catcher With Botanical ", "p1_units": 1200.0, "p2_units": 19089.7, "p1_rev": 8184.07, "p2_rev": 130191.96}, {"asin": "B09GDHSW99", "brand": "Raid", "segment": "Lure", "price": 6.99, "title": "Raid Essentials Fruit Fly Trap for Indoors, Made with Essent", "p1_units": 89897.7, "p2_units": 100268.2, "p1_rev": 628384.57, "p2_rev": 700875.0}, {"asin": "B09GVVTZ2M", "brand": "LFSYS", "segment": "Sticky traps", "price": 13.99, "title": "50 Pack Window Fly Trap, Fruit Fly Traps for Indoors, Fly Pa", "p1_units": 0.0, "p2_units": 6678.0, "p1_rev": 0.0, "p2_rev": 93424.52}, {"asin": "B09WJLKZP1", "brand": "Wondercide", "segment": "Passive attractor", "price": 21.99, "title": "Wondercide - Fruit Fly Traps for Indoors - Fruit Fly Killer ", "p1_units": 83435.0, "p2_units": 54894.4, "p1_rev": 1834734.99, "p2_rev": 1207128.3}, {"asin": "B0B3RJ9JFM", "brand": "Landisun", "segment": "Sticky traps", "price": 5.79, "title": "Fruit Fly Traps Indoor Fungus Gnat Trap 48PCS for Plants Yel", "p1_units": 389941.8, "p2_units": 164737.3, "p1_rev": 2257762.85, "p2_rev": 953828.85}, {"asin": "B0BWM9BBH5", "brand": "BugBane", "segment": "Sticky traps", "price": 24.99, "title": "Fly Stick Sticky Fly Traps for Indoors Outdoor 4pk. Non-Toxi", "p1_units": 31411.9, "p2_units": 52619.9, "p1_rev": 784984.38, "p2_rev": 1314970.3}, {"asin": "B0BX4GQF68", "brand": "Terro", "segment": "Lure", "price": 18.39, "title": "Terro Fruit Fly Traps for Indoors (6 Pack) + 270 Days of Lur", "p1_units": 79824.0, "p2_units": 158276.8, "p1_rev": 1467963.18, "p2_rev": 2910710.35}, {"asin": "B0C4Z77R1F", "brand": "Aunt Fannie's", "segment": "Lure", "price": 19.99, "title": "Aunt Fannie's FlyPunch Fruit Fly Trap for Indoor and Kitchen", "p1_units": 8327.2, "p2_units": 12137.5, "p1_rev": 166460.93, "p2_rev": 242628.43}, {"asin": "B0CJ3Z5TKN", "brand": "Fly Away Product", "segment": "Lure", "price": 12.14, "title": "Fly Away Fruit Fly Liquid Lure - Trap Fruit Flies Fast. Safe", "p1_units": 5806.0, "p2_units": 7932.3, "p1_rev": 70484.35, "p2_rev": 96298.24}, {"asin": "B0CNGBLV5N", "brand": "Cleanuper", "segment": "Sticky traps", "price": 6.99, "title": "58 Pack Flying Insect Traps for Plants \u2013 Yellow Sticky Traps", "p1_units": 59566.5, "p2_units": 154733.4, "p1_rev": 416369.7, "p2_rev": 1081586.68}, {"asin": "B0CP43WSGB", "brand": "BugBane", "segment": "Sticky traps", "price": 32.99, "title": "Fly Stick Sticky Fly Traps for Indoors Outdoor 6pk. Non-Toxi", "p1_units": 0.0, "p2_units": 62293.2, "p1_rev": 0.0, "p2_rev": 2055053.0}, {"asin": "B0CXXC99TZ", "brand": "Qualirey", "segment": "Lure", "price": 19.99, "title": "Qualirey 12 Pack Fruit Fly Trap Refill Liquid, 0.68oz Per Bo", "p1_units": 0.0, "p2_units": 4576.8, "p1_rev": 0.0, "p2_rev": 91490.43}, {"asin": "B0D4DC2KGV", "brand": "Qualirey", "segment": "Lure", "price": 25.99, "title": "Qualirey 24 Pack Fruit Fly Trap Refill Liquid, 0.68oz Per Bo", "p1_units": 0.0, "p2_units": 2785.1, "p1_rev": 0.0, "p2_rev": 72384.75}, {"asin": "B0D4DY85H3", "brand": "Qualirey", "segment": "Unclassified", "price": 11.99, "title": "Qualirey 6 Pack Fruit Fly Trap Refill Liquid, 0.68oz Per Bot", "p1_units": 0.0, "p2_units": 14679.7, "p1_rev": 0.0, "p2_rev": 176009.12}, {"asin": "B0D5DDC4ZS", "brand": "Super Ninja", "segment": "Lure", "price": 37.99, "title": "Super Ninja Fruit Fly Traps for Indoors - 12 Pack, Highly Ef", "p1_units": 0.0, "p2_units": 2932.3, "p1_rev": 0.0, "p2_rev": 111398.46}, {"asin": "B0D5DJ7V4P", "brand": "Super Ninja", "segment": "Lure", "price": 13.99, "title": "Super Ninja Fruit Fly Traps for Indoors - 4 Pack, Highly Eff", "p1_units": 0.0, "p2_units": 64191.1, "p1_rev": 0.0, "p2_rev": 898033.35}, {"asin": "B0D5DJBVCR", "brand": "Super Ninja", "segment": "Lure", "price": 9.99, "title": "Super Ninja Fruit Fly Traps for Indoors - 2 Pack, Highly Eff", "p1_units": 0.0, "p2_units": 10961.0, "p1_rev": 0.0, "p2_rev": 109500.09}, {"asin": "B0D5DJW9BY", "brand": "Super Ninja", "segment": "Lure", "price": 7.99, "title": "Super Ninja Fruit Fly Traps for Indoors - 1 Pack, Highly Eff", "p1_units": 0.0, "p2_units": 4906.6, "p1_rev": 0.0, "p2_rev": 39203.49}, {"asin": "B0DCNZVXTP", "brand": "Qualirey", "segment": "Lure", "price": 9.99, "title": "Qualirey 4 Pack Fruit Fly Trap Refill Liquid, 0.68oz/ Bottle", "p1_units": 3578.3, "p2_units": 30589.6, "p1_rev": 35747.12, "p2_rev": 305589.8}, {"asin": "B0DCP1K7B6", "brand": "Qualirey", "segment": "Lure", "price": 24.99, "title": "Qualirey 20 Pack Fruit Fly Trap Refill Liquid, 0.68oz/ Bottl", "p1_units": 641.4, "p2_units": 1750.9, "p1_rev": 16029.09, "p2_rev": 43754.99}, {"asin": "B0DCP22M9Y", "brand": "Qualirey", "segment": "Lure", "price": 15.99, "title": "Qualirey 8 Pack Fruit Fly Trap Refill Liquid, 0.68oz/ Bottle", "p1_units": 1223.2, "p2_units": 4001.9, "p1_rev": 19559.61, "p2_rev": 63991.02}, {"asin": "B0DCP2TKL5", "brand": "Qualirey", "segment": "Lure", "price": 17.99, "title": "Qualirey 12 Pack Fruit Fly Trap Refill Liquid, 0.68oz/ Bottl", "p1_units": 1033.5, "p2_units": 2313.3, "p1_rev": 18593.2, "p2_rev": 41616.27}, {"asin": "B0DGWQV8GK", "brand": "HOT SHOT", "segment": "Lure", "price": 14.16, "title": "Hot Shot Flying Insect Trap, Discreet, Hassle-Free Trap Attr", "p1_units": 15.0, "p2_units": 74639.2, "p1_rev": 212.68, "p2_rev": 1056890.65}, {"asin": "B0DHCJ3DL9", "brand": "Acme Approved", "segment": "Lure", "price": 4.99, "title": "UV Fruit Fly Traps for Indoors + Sticky Traps 2pk- Fruit Fly", "p1_units": 0.0, "p2_units": 5012.8, "p1_rev": 0.0, "p2_rev": 25013.92}, {"asin": "B0DX45STK3", "brand": "Super Ninja", "segment": "Lure", "price": 18.99, "title": "Super Ninja Fruit Fly Traps for Indoors - 6 Pack, Highly Eff", "p1_units": 0.0, "p2_units": 12462.0, "p1_rev": 0.0, "p2_rev": 236653.0}, {"asin": "B0DX884Y1W", "brand": "Super Ninja", "segment": "Lure", "price": 12.99, "title": "Super Ninja Fungus Gnat & Fruit Fly Traps - 10 Gnat Sticky T", "p1_units": 0.0, "p2_units": 267.0, "p1_rev": 0.0, "p2_rev": 3468.2}, {"asin": "B0F43FB193", "brand": "Qualirey", "segment": "Lure", "price": 15.99, "title": "Qualirey Fruit Fly Trap for Indoor and Kitchen Use, 0.68 oz ", "p1_units": 0.0, "p2_units": 396.3, "p1_rev": 0.0, "p2_rev": 6336.2}, {"asin": "B0F43FPGBK", "brand": "Qualirey", "segment": "Lure", "price": 11.99, "title": "Qualirey Fruit Fly Trap for Indoor and Kitchen Use, 0.68 oz ", "p1_units": 0.0, "p2_units": 881.6, "p1_rev": 0.0, "p2_rev": 10570.26}, {"asin": "B0F43FXY11", "brand": "Qualirey", "segment": "Lure", "price": 19.99, "title": "Qualirey Fruit Fly Trap for Indoor and Kitchen Use, 0.68 oz ", "p1_units": 0.0, "p2_units": 209.0, "p1_rev": 0.0, "p2_rev": 4177.51}, {"asin": "B0F43GM9C5", "brand": "Qualirey", "segment": "Lure", "price": 15.99, "title": "Qualirey Fruit Fly Trap for Indoor and Kitchen Use, 0.68 oz ", "p1_units": 0.0, "p2_units": 308.1, "p1_rev": 0.0, "p2_rev": 4926.68}, {"asin": "B0F43HFFYM", "brand": "Qualirey", "segment": "Lure", "price": 13.99, "title": "Qualirey Fruit Fly Trap for Indoor and Kitchen Use, 0.68 oz ", "p1_units": 0.0, "p2_units": 553.8, "p1_rev": 0.0, "p2_rev": 7747.8}, {"asin": "B0F43HQK4C", "brand": "Qualirey", "segment": "Lure", "price": 8.99, "title": "Qualirey Fruit Fly Trap for Indoor and Kitchen Use, 0.68 oz ", "p1_units": 0.0, "p2_units": 2449.0, "p1_rev": 0.0, "p2_rev": 22016.24}, {"asin": "B0F4KZFPYQ", "brand": "Aunt Fannie's", "segment": "Lure", "price": 24.99, "title": "Aunt Fannie's FlyPunch Fruit Fly Trap Bundle for Indoor and ", "p1_units": 0.0, "p2_units": 1698.7, "p1_rev": 0.0, "p2_rev": 42451.51}, {"asin": "B0GCCJFZ18", "brand": "ELEGENZO", "segment": "Lure", "price": 24.9, "title": "EPA Establishment No.100240-CHN-1 Fruit Fly Traps for Indoor", "p1_units": 0.0, "p2_units": 168.0, "p1_rev": 0.0, "p2_rev": 4183.45}], "period_labels": {"p1": "Feb 2024 \u2013 Feb 2025", "p2": "Feb 2025 \u2013 Feb 2026"}};
const MONTHS =["2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"];
const TOTAL  = [80.9, 89.8, 188.3, 197.1, 270.4, 266.0, 245.8, 187.6, 201.7, 161.5, 92.4, 51.1, 53.6, 61.1, 85.0, 111.9, 175.6, 225.1, 189.5, 166.1, 205.0, 161.5, 90.1, 46.8, 47.7];
const ASIN_DS = [{"label": "Natural Catch", "data": [2.2, 2.6, 3.7, 4.8, 8.3, 6.8, 9.6, 7.7, 7.3, 3.5, 1.1, 1.0, 1.0, 2.0, 3.4, 4.6, 7.9, 8.2, 8.3, 8.1, 7.5, 3.3, 1.8, 1.6, 1.2], "borderColor": "#2563eb", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "PIC", "data": [null, null, null, null, null, null, 147.5, 94.9, 97.9, 69.8, 45.9, 27.2, 30.5, 35.6, 51.0, 80.5, 72.8, 138.2, 83.4, 91.8, 105.8, 18.3, 10.4, 11.5, 10.3], "borderColor": "#16a34a", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Fruit Fly BarPro", "data": [30.7, 46.4, 47.2, 49.4, 77.8, 79.7, 84.4, 76.2, 76.3, 50.0, 35.7, 24.0, 24.9, 31.2, 42.0, 49.6, 86.9, 87.8, 102.1, 73.7, 89.3, 70.6, 33.1, 21.1, 23.7], "borderColor": "#dc2626", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Terro", "data": [32.8, 43.7, 45.5, 31.3, 74.9, 159.7, 165.2, 293.7, 196.8, 227.4, 130.0, 74.1, 52.6, 48.4, 112.0, 227.7, 182.7, 55.6, 37.9, 21.0, 33.9, 34.4, 26.1, 23.7, 18.5], "borderColor": "#d97706", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "RESCUE!", "data": [1.5, 2.0, 4.0, 3.7, 3.7, 4.7, 4.7, 4.6, 4.1, 1.8, 1.4, 1.3, 1.1, 1.5, 2.4, 4.3, 8.6, 4.8, 4.4, 4.7, 7.5, 5.8, 1.4, 1.3, 1.2], "borderColor": "#7c3aed", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Aunt Fannie's", "data": [85.9, 88.6, 74.1, 158.7, 274.3, 327.8, 244.7, 239.0, 265.5, 176.9, 90.2, 42.3, 45.4, 48.4, 62.1, 108.6, 225.7, 287.7, 281.1, 272.5, 341.3, 264.8, 89.1, 39.4, 42.3], "borderColor": "#0891b2", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Terro", "data": [null, null, 102.2, 68.0, 72.6, 63.0, 99.1, 52.8, 189.8, 367.1, 300.7, 122.4, 72.3, 75.6, 76.5, 83.8, 101.2, 59.7, 28.3, 24.3, 22.4, 30.1, 40.8, 13.8, 16.2], "borderColor": "#be185d", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Terro", "data": [614.0, 522.8, 651.5, 1176.8, 1642.8, 1801.9, 2154.2, 1876.7, 2443.9, 1725.0, 812.0, 396.1, 420.6, 453.3, 463.0, 1064.6, 2456.8, 3462.1, 2767.3, 2980.8, 3572.6, 3180.8, 1463.2, 612.2, 491.3], "borderColor": "#65a30d", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Fruit Fly BarPro", "data": [7.5, 10.1, 15.5, 26.7, 27.8, 28.2, 26.3, 20.8, 25.4, 6.0, 6.6, 4.5, 5.0, 7.4, 13.2, 22.0, 33.9, 32.5, 35.8, 27.9, 30.7, 21.4, 9.9, 5.3, 5.8], "borderColor": "#ea580c", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "B071FVCYFW", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, 1.6, 1.8, 1.8, 7.2, 11.3, 8.2, 11.6, 10.8, 6.7, 3.1, 2.5, 1.9], "borderColor": "#1d4ed8", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Fruit Fly BarPro", "data": [6.0, 6.8, 18.0, 14.0, 18.8, 17.6, 16.9, 11.4, 11.5, 8.9, 4.8, 4.5, 5.0, 6.3, 11.0, 15.2, 20.1, 22.3, 20.3, 12.8, 13.5, 9.7, 5.5, 5.3, 5.9], "borderColor": "#059669", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Kensizer", "data": [65.1, 95.5, 119.7, 164.0, 192.5, 150.8, 129.6, 130.6, 123.5, 102.7, 59.2, 47.0, 46.0, 49.9, 71.0, 102.9, 164.3, 158.0, 109.8, 87.2, 85.5, 79.1, 53.7, 40.2, 39.5], "borderColor": "#9333ea", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Aunt Fannie's", "data": [5.5, 9.6, 13.0, 19.8, 27.4, 26.5, 66.5, 20.0, 12.1, 13.3, 9.8, 6.4, 6.8, 7.0, 11.6, 19.5, 26.1, 22.6, 22.8, 21.3, 23.0, 18.0, 11.4, 5.4, 5.0], "borderColor": "#f59e0b", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Catchmaster", "data": [49.2, 83.4, 103.4, 274.8, 596.8, 267.1, 201.5, 119.6, 108.8, 78.3, 47.5, 31.5, 33.4, 69.0, 122.0, 86.0, 209.7, 869.7, 557.1, 228.3, 344.4, 129.4, 45.7, 33.3, 36.7], "borderColor": "#ef4444", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Terro", "data": [41.6, 44.7, 36.6, 36.1, 61.9, 39.4, 71.8, 63.8, 11.5, 16.8, 27.7, 16.0, 13.7, 20.4, 33.9, 46.0, 59.5, 91.6, 67.3, 37.0, 31.0, 9.2, 9.4, 7.3, 9.8], "borderColor": "#10b981", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Aunt Fannie's", "data": [172.8, 208.3, 246.2, 444.0, 705.4, 775.6, 728.6, 603.5, 622.1, 460.0, 254.0, 128.3, 126.6, 135.5, 218.7, 364.5, 638.2, 704.2, 711.5, 671.0, 850.9, 624.7, 255.2, 115.0, 122.1], "borderColor": "#6366f1", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Aunt Fannie's", "data": [24.9, 36.8, 45.0, 49.1, 83.0, 95.2, 105.1, 37.8, 3.9, 7.4, 24.4, 15.2, 15.5, 15.8, 28.9, 43.1, 48.3, 42.8, 45.3, 43.4, 64.6, 50.9, 29.6, 13.8, 13.8], "borderColor": "#2563eb", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Stingmon", "data": [null, null, null, null, null, null, 274.5, 225.5, 188.0, 174.4, 118.4, 137.8, 156.1, 127.4, 112.6, 126.8, 203.5, 195.7, 171.2, 137.8, 132.1, 144.5, 135.6, 94.4, 103.2], "borderColor": "#16a34a", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Catchmaster", "data": [9.1, 13.8, 20.0, 24.9, 27.1, 18.3, 5.8, 8.1, 8.3, 7.0, 3.1, 2.4, 3.6, 5.0, 13.3, 25.2, 44.8, 38.6, 17.2, 11.0, 10.2, 6.1, 3.6, 3.6, 4.0], "borderColor": "#dc2626", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Trappify", "data": [35.7, 47.7, 67.8, 97.1, 87.8, 73.4, 65.3, 75.4, 74.3, 57.4, 36.3, 26.8, 25.7, 32.1, 46.5, 65.1, 47.0, 36.9, 88.7, 72.5, 117.1, 89.1, 53.6, 26.9, 27.1], "borderColor": "#d97706", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Mosqueda", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 599.0], "borderColor": "#7c3aed", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Wondercide", "data": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.7, 33.0, 63.8, 27.9, 53.4, 26.8, 9.3, 9.1], "borderColor": "#0891b2", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "STEM", "data": [null, null, null, null, null, null, null, null, null, null, 21.3, 19.7, 23.2, 21.8, 35.0, 45.0, 64.9, 97.6, 105.8, 59.9, 56.2, 53.6, 34.4, 24.1, 27.7], "borderColor": "#be185d", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Raid", "data": [41.7, 49.7, 61.8, 149.1, 300.0, 297.5, 351.6, 547.4, 495.1, 247.6, 231.5, 125.4, 102.7, 116.4, 229.4, 293.5, 362.9, 334.2, 350.4, 361.8, 423.7, 402.8, 204.1, 113.7, 87.6], "borderColor": "#65a30d", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "LFSYS", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 111.1, 92.3, 103.1], "borderColor": "#ea580c", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Wondercide", "data": [64.4, 76.6, 157.7, 299.9, 439.6, 487.5, 340.4, 264.8, 180.9, 211.2, 149.0, 68.5, 53.3, 54.8, 81.1, 169.3, 268.3, 238.6, 210.0, 197.3, 262.3, 172.0, 81.9, 27.8, 27.0], "borderColor": "#1d4ed8", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Landisun", "data": [576.8, 757.0, 2894.5, 1777.9, 2109.4, 1631.7, 1056.0, 537.4, 708.1, 651.1, 254.2, 172.2, 173.3, 263.5, 399.8, 460.4, 601.6, 941.4, 526.5, 500.4, 467.9, 508.7, 407.7, 150.7, 149.9], "borderColor": "#059669", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "BugBane", "data": [14.0, 20.9, 60.7, 77.4, 39.6, 288.8, 201.2, 143.6, 103.8, 31.0, 25.1, 16.9, 18.3, 29.9, 60.4, 198.4, 348.8, 408.4, 263.2, 82.3, 64.9, 120.1, 72.1, 39.8, 33.8], "borderColor": "#9333ea", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Terro", "data": [61.5, 100.5, 116.2, 217.9, 239.1, 274.8, 279.2, 381.9, 357.4, 306.9, 193.0, 85.1, 68.6, 92.5, 222.6, 362.3, 382.8, 448.7, 452.6, 590.6, 1221.5, 641.4, 420.7, 186.4, 169.1], "borderColor": "#f59e0b", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Aunt Fannie's", "data": [0.1, 3.3, 5.5, 16.8, 31.0, 36.0, 36.9, 30.1, 34.3, 30.9, 21.8, 15.6, 13.7, 17.4, 21.3, 37.7, 45.2, 38.7, 43.1, 40.9, 46.0, 48.2, 30.0, 14.7, 14.4], "borderColor": "#ef4444", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Fly Away Product", "data": [null, 2.2, 6.9, 5.9, 4.0, 9.4, 28.9, 42.0, 42.3, 26.3, 9.5, 8.0, 7.0, 6.3, 9.4, 0.1, 22.8, 29.8, 41.0, 26.1, 30.8, 29.7, 29.1, 22.6, 12.7], "borderColor": "#10b981", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Cleanuper", "data": [24.6, 44.1, 89.6, 134.1, 155.9, 219.4, 192.1, 155.6, 224.8, 232.2, 162.1, 132.0, 292.7, 337.3, 322.9, 418.9, 482.7, 460.1, 437.6, 347.0, 462.2, 514.0, 470.3, 412.8, 418.5], "borderColor": "#6366f1", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "BugBane", "data": [null, null, null, null, null, null, null, null, null, null, null, null, 43.5, 73.0, 117.0, 167.3, 363.5, 402.9, 331.1, 212.5, 144.6, 105.9, 49.4, 31.9, 37.3], "borderColor": "#2563eb", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 14.7, 19.0, 18.3, 18.1, 20.7, 26.0, 17.7, 9.8, 4.1, 3.2], "borderColor": "#16a34a", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 5.6, 9.5, 9.1, 12.5, 11.1, 15.6, 13.5, 6.1, 4.5, 5.3], "borderColor": "#dc2626", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 45.4, 47.5, 51.3, 75.3, 48.1, 84.2, 66.6, 35.8, 17.0, 16.0], "borderColor": "#d97706", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Super Ninja", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 26.4, 48.2, 22.8, 10.7, 5.9, 7.0], "borderColor": "#7c3aed", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Super Ninja", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 856.8, 739.5, 595.8, 373.4, 181.4, 157.5], "borderColor": "#0891b2", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Super Ninja", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 281.0, 145.1, 87.0, 53.0, 26.6, 23.4], "borderColor": "#be185d", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Super Ninja", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 61.3, 137.5, 13.2, 0.7, 0.7, 1.0], "borderColor": "#65a30d", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, 12.8, 14.5, 22.4, 21.2, 26.1, 29.7, 34.4, 49.2, 51.6, 112.6, 111.2, 138.5, 116.5, 138.5, 119.7, 52.2, 40.3, 39.3], "borderColor": "#ea580c", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, 3.3, 5.2, 4.1, 3.8, 2.8, 2.9, 3.6, 4.6, 5.6, 4.9, 5.9, 8.9, 3.9, 7.4, 5.9, 2.3, 2.1, 2.2], "borderColor": "#1d4ed8", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, 8.9, 10.3, 6.0, 8.6, 4.2, 4.3, 4.7, 6.7, 11.4, 15.0, 15.5, 17.7, 11.5, 17.9, 14.3, 7.8, 4.1, 4.3], "borderColor": "#059669", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, 4.9, 9.2, 6.0, 8.4, 4.2, 2.3, 2.4, 4.4, 10.3, 9.7, 8.1, 10.5, 6.8, 9.4, 5.0, 4.4, 2.4, 2.3], "borderColor": "#9333ea", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "HOT SHOT", "data": [null, null, null, null, null, null, null, null, null, null, 0.1, 0.2, 1.5, 18.0, 85.7, 284.0, 385.6, 572.6, 606.8, 194.7, 137.5, 56.6, 31.8, 39.1, 23.5], "borderColor": "#f59e0b", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Acme Approved", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 31.5, 36.2, 29.0, 23.0, 8.2, 0.3, 20.6, 7.3, 4.7, 4.2], "borderColor": "#ef4444", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Super Ninja", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 119.2, 231.9, 57.8, 60.0, 24.6, 24.3], "borderColor": "#10b981", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Super Ninja", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 0.0, 0.0, 0.0, 3.5, 2.5, 3.6], "borderColor": "#6366f1", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 0.0, 0.7, 1.4, 3.2, 2.6, 1.8, 0.4, 1.1, 1.0, 0.9], "borderColor": "#2563eb", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 0.8, 4.1, 4.7, 5.8, 4.0, 3.2, 0.7, 2.1, 2.0, 1.7], "borderColor": "#16a34a", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 0.0, 0.4, 0.4, 1.6, 1.6, 1.0, 0.2, 0.6, 0.6, 0.6], "borderColor": "#dc2626", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 0.0, 0.2, 0.5, 1.5, 2.5, 2.3, 0.4, 1.1, 1.0, 0.9], "borderColor": "#d97706", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 1.1, 1.2, 2.9, 5.3, 2.2, 1.1, 0.5, 1.4, 1.2, 1.3], "borderColor": "#7c3aed", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Qualirey", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 4.8, 13.3, 8.2, 10.5, 10.6, 11.7, 7.5, 9.4, 2.5, 2.5], "borderColor": "#0891b2", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "Aunt Fannie's", "data": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.8, 5.5, 4.2, 4.1, 4.3, 4.6, 8.3, 8.5, 3.4, 3.6], "borderColor": "#be185d", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}, {"label": "ELEGENZO", "data": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 0.0, 0.0, 7.3], "borderColor": "#65a30d", "backgroundColor": "transparent", "borderWidth": 1.5, "pointRadius": 0, "hidden": true}];

// Seasonality index
new Chart(document.getElementById('seasIdxChart'), {
  type: 'bar',
  data: { labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [{ data: [0.33, 0.41, 0.5, 0.91, 1.03, 1.49, 1.64, 1.45, 1.18, 1.36, 1.08, 0.61], backgroundColor: ["#dc2626", "#dc2626", "#dc2626", "#2563eb", "#2563eb", "#16a34a", "#16a34a", "#16a34a", "#16a34a", "#16a34a", "#2563eb", "#dc2626"], label:'Index' }] },
  options: { maintainAspectRatio: false, plugins: { legend: { display:false } },
    scales: { y: { min:0, ticks: { callback: v => v.toFixed(1)+'x' } } } }
});



// ── Tab F — Customer Reviews ──────────────────────────────────────────────────
(function() {
  const revRatingCtx = document.getElementById('revRatingChart');
  if (revRatingCtx) {
    new Chart(revRatingCtx, {
      type: 'doughnut',
      data: {
        labels: ["1\u2605", "2\u2605", "3\u2605"],
        datasets: [{ data: [2335, 1483, 1220],
          backgroundColor: ['#dc2626','#f97316','#d97706'],
          borderWidth: 2, borderColor: '#fff' }]
      },
      options: {
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { font:{size:11}, boxWidth:14 } },
          tooltip: { callbacks: { label: ctx => ctx.label + ': ' + ctx.raw.toLocaleString() + ' (' + [46.3, 29.4, 24.2][ctx.dataIndex] + '%)' } }
        }
      }
    });
  }

  const complaintsCtx = document.getElementById('complaintsChart');
  if (complaintsCtx) {
    const clbl = ["Doesn't work", "Waste of money / overpriced", "Unpleasant smell", "Poor quality", "Lure doesn't attract", "Leaks / spills", "Too small", "Short lifespan", "Not sticky enough", "False advertising"];
    const cpct = [25.9, 12.9, 7.0, 4.9, 3.6, 3.0, 2.6, 2.4, 0.8, 0.5];
    new Chart(complaintsCtx, {
      type: 'bar',
      data: { labels: clbl, datasets: [{ data: [1303, 649, 354, 248, 182, 153, 131, 123, 40, 26],
        backgroundColor: clbl.map((_,i) => i===0 ? '#dc2626' : i<3 ? '#f97316' : '#94a3b8'),
        label: 'reviews' }] },
      options: {
        maintainAspectRatio: false, indexAxis: 'y',
        layout: { padding: { right: 48 } },
        plugins: {
          legend: { display:false },
          datalabels: { anchor:'end', align:'right',
            formatter: (_,ctx) => cpct[ctx.dataIndex]+'%',
            font:{size:10,weight:'600'}, color:'#475569' }
        },
        scales: { x: { ticks: { callback: v => v.toLocaleString() } } }
      },
      plugins: [ChartDataLabels]
    });
  }

  const needsCtx = document.getElementById('needsChart');
  if (needsCtx) {
    const needsData = [160, 146, 63, 22, 12, 4];
    const needsTotal = needsData.reduce((a, b) => a + b, 0);
    new Chart(needsCtx, {
      type: 'pie',
      plugins: [ChartDataLabels],
      data: {
        labels: ["Reusable / refillable", "Faster action", "Larger trap size", "Odorless", "Safe for kids/pets", "Kitchen safe"],
        datasets: [{ data: needsData, backgroundColor: ['#16a34a','#2563eb','#f97316','#7c3aed','#0891b2','#dc2626'] }]
      },
      options: {
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { font: { size: 11 }, padding: 12, boxWidth: 14 } },
          datalabels: {
            display: ctx => needsData[ctx.dataIndex] / needsTotal >= 0.05,
            formatter: v => Math.round(v / needsTotal * 100) + '%',
            color: '#fff',
            font: { weight: 'bold', size: 13 }
          },
          tooltip: {
            callbacks: {
              label: ctx => ctx.label + ': ' + Math.round(ctx.raw / needsTotal * 100) + '% (' + ctx.raw + ' mentions)'
            }
          }
        }
      }
    });
  }
})();

// ── Tab G — Lure Brand Share Pies ─────────────────────────────────────────────
(function() {
  const LURE_C = {
    'Terro':          '#16a34a',
    "Aunt Fannie's":  '#2563eb',
    'Raid':           '#f97316',
    'Super Ninja':    '#7c3aed',
    'HOT SHOT':       '#dc2626',
    'Qualirey':       '#0891b2',
    'Others':         '#94a3b8'
  };
  function makeLurePie(id, labels, vals) {
    const el = document.getElementById(id);
    if (!el) return;
    const tot = vals.reduce((a, b) => a + b, 0);
    new Chart(el, {
      type: 'pie',
      plugins: [ChartDataLabels],
      data: { labels, datasets: [{ data: vals, backgroundColor: labels.map(l => LURE_C[l] || '#94a3b8') }] },
      options: {
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { font: { size: 10 }, padding: 8, boxWidth: 12 } },
          datalabels: {
            display: ctx => ctx.dataset.data[ctx.dataIndex] / tot >= 0.05,
            formatter: v => Math.round(v / tot * 100) + '%',
            color: '#fff',
            font: { weight: 'bold', size: 12 }
          },
          tooltip: { callbacks: { label: ctx => ctx.label + ': ' + Math.round(ctx.raw / tot * 100) + '%' } }
        }
      }
    });
  }
  // Data: Lure segment only, aggregated by brand (pre-computed from SHARE_DATA)
  // P1 = Feb 2024–Feb 2025 | P2 = Feb 2025–Feb 2026
  // Others P1: STEM + HOT SHOT + Qualirey + Fly Away  (13 497 units | $168 810 rev)
  // Others P2: STEM + Fly Away + Acme Approved + ELEGENZO (32 203 units | $255 688 rev)
  makeLurePie('lureUnitP1Chart',
    ['Terro', "Aunt Fannie's", 'Raid', 'Others'],
    [660026, 255712, 89898, 13497]);
  makeLurePie('lureUnitP2Chart',
    ['Terro', "Aunt Fannie's", 'Raid', 'Super Ninja', 'HOT SHOT', 'Qualirey', 'Others'],
    [915838, 261712, 100268, 95720, 74639, 50815, 32203]);
  makeLurePie('lureRevP1Chart',
    ['Terro', "Aunt Fannie's", 'Raid', 'Others'],
    [9118687, 3739481, 628385, 168810]);
  makeLurePie('lureRevP2Chart',
    ['Terro', "Aunt Fannie's", 'Super Ninja', 'HOT SHOT', 'Raid', 'Qualirey', 'Others'],
    [13153340, 3811569, 1398257, 1056891, 700875, 674602, 255688]);
})();

  // Init Share & Leaders tab
  if (typeof SHARE_DATA !== 'undefined' && SHARE_DATA.asin_data && SHARE_DATA.asin_data.length) {
    slInit();
  }

// ═══════════════ TAB I — SEGMENTS ════════════════════════════════════════════
const SEGMENT_DATA = {
  segments: ['Lure','Sticky Traps','Passive Attractor','Electric'],
  month_labels: ['Mar 2025','Apr 2025','May 2025','Jun 2025','Jul 2025','Aug 2025','Sep 2025','Oct 2025','Nov 2025','Dec 2025','Jan 2026','Feb 2026'],
  monthly_units: {
    'Lure':              [34829,50320,98278,158728,202228,182965,172170,263195,195272,103156,48522,31450],
    'Sticky Traps':      [31707,39494,53675,76161,113144,80161,53128,59973,51454,41812,29061,27550],
    'Passive Attractor': [3150,4524,8079,12515,12220,12694,11510,13366,9911,4928,2185,1672],
    'Electric':          [80873,120165,181467,226819,386224,770034,703008,914324,642704,312794,191808,158935]
  },
  monthly_rev: {
    'Lure':              [459188,675925,1338035,2140305,2770762,2503018,2358867,3718204,2665362,1435138,669893,441290],
    'Sticky Traps':      [315329,429222,653721,1063241,1513752,1094016,632944,655040,536231,392412,282530,249295],
    'Passive Attractor': [84716,130127,228318,338720,337304,334537,279594,330325,232606,117501,59543,46332],
    'Electric':          [1406278,2080842,3246786,4008687,7653643,18013193,15633155,19880314,14015434,6679329,4115165,3422671]
  },
  kpis: {
    'Lure':              {skus:37, units_12m:1541113, revenue_12m:21175987, growth_pct:-71.0, avg_price:13.74, unit_share:22.1, rev_share:16.1},
    'Sticky Traps':      {skus:12, units_12m:657321,  revenue_12m:7817732,  growth_pct:-40.2, avg_price:11.89, unit_share:9.4,  rev_share:5.9},
    'Passive Attractor': {skus:6,  units_12m:96754,   revenue_12m:2519624,  growth_pct:-74.7, avg_price:26.04, unit_share:1.4,  rev_share:1.9},
    'Electric':          {skus:22, units_12m:4689156, revenue_12m:100155498,growth_pct:-70.6, avg_price:21.36, unit_share:67.1, rev_share:76.1}
  }
};

const SEG_COLORS = {
  'Lure':'#2563eb', 'Sticky Traps':'#16a34a',
  'Passive Attractor':'#d97706', 'Electric':'#7c3aed'
};
const SEG_COLORS_LIGHT = {
  'Lure':'#93c5fd', 'Sticky Traps':'#86efac',
  'Passive Attractor':'#fcd34d', 'Electric':'#c4b5fd'
};

let _segUnitPie, _segRevPie, _segUnitLine, _segRevLine, _seg3mChart, _segMomChart;

function segInit() {
  const SD   = SEGMENT_DATA;
  const segs = SD.segments;

  // ── KPI blocks ──────────────────────────────────────────────────────────
  document.getElementById('seg_kpi_section').innerHTML = segs.map(s => {
    const k = SD.kpis[s], c = SEG_COLORS[s];
    const grow = k.growth_pct !== null
      ? (k.growth_pct >= 0 ? '+'+k.growth_pct+'%' : k.growth_pct+'%') : '—';
    const gc = k.growth_pct !== null ? (k.growth_pct >= 0 ? 'delta-pos' : 'delta-neg') : 'delta-neu';
    return `<div class="card" style="border-left:4px solid ${c};padding:14px 16px">
      <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:${c};margin-bottom:10px">${s}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px">
        <div class="kpi" style="box-shadow:none;background:#f8fafc;padding:8px 10px">
          <div class="kpi-v" style="font-size:.95rem">${k.units_12m>=1e6?(k.units_12m/1e6).toFixed(1)+'M':(k.units_12m/1000).toFixed(0)+'K'}</div>
          <div class="kpi-l">Units sold (12M)</div>
        </div>
        <div class="kpi" style="box-shadow:none;background:#f8fafc;padding:8px 10px">
          <div class="kpi-v" style="font-size:.95rem">$${(k.revenue_12m/1e6).toFixed(1)}M</div>
          <div class="kpi-l">Segment Value (12M)</div>
        </div>
        <div class="kpi" style="box-shadow:none;background:#f8fafc;padding:8px 10px">
          <div class="kpi-v ${gc}" style="font-size:.95rem">${grow}</div>
          <div class="kpi-l">Growth (3M vs 3M)</div>
        </div>
        <div class="kpi" style="box-shadow:none;background:#f8fafc;padding:8px 10px">
          <div class="kpi-v" style="font-size:.95rem">$${k.avg_price!==null?k.avg_price.toFixed(2):'—'}</div>
          <div class="kpi-l">Avg Price (unit-wtd)</div>
        </div>
      </div>
    </div>`;
  }).join('');

  // ── Pie charts ───────────────────────────────────────────────────────────
  const colors = segs.map(s => SEG_COLORS[s]);

  // Connector lines plugin for small slices (<10%)
  const pieLinePlugin = {
    id: 'pieLinePlugin',
    afterDatasetsDraw(chart) {
      const total = chart.data.datasets[0].data.reduce((a,b) => a+b, 0);
      const ctx2 = chart.ctx;
      chart.getDatasetMeta(0).data.forEach((arc, i) => {
        const v = chart.data.datasets[0].data[i];
        if (v / total >= 0.10) return;
        const mid = (arc.startAngle + arc.endAngle) / 2;
        const r = arc.outerRadius;
        ctx2.save();
        ctx2.strokeStyle = chart.data.datasets[0].backgroundColor[i];
        ctx2.lineWidth = 1.5;
        ctx2.beginPath();
        ctx2.moveTo(arc.x + Math.cos(mid) * (r + 2), arc.y + Math.sin(mid) * (r + 2));
        ctx2.lineTo(arc.x + Math.cos(mid) * (r + 20), arc.y + Math.sin(mid) * (r + 20));
        ctx2.stroke();
        ctx2.restore();
      });
    }
  };

  const _piePct = (v, ctx) => { const t = ctx.chart.data.datasets[0].data.reduce((a,b) => a+b, 0); return t > 0 ? Math.round(v / t * 100) : 0; };
  const pieFmtUnits = (v, ctx) => {
    const k = SD.kpis[segs[ctx.dataIndex]];
    const units = k.units_12m >= 1e6 ? (k.units_12m / 1e6).toFixed(1) + 'M' : (k.units_12m / 1000).toFixed(0) + 'K';
    return _piePct(v, ctx) + '%\n' + units + ' units';
  };
  const pieFmtRev = (v, ctx) => {
    const k = SD.kpis[segs[ctx.dataIndex]];
    return _piePct(v, ctx) + '%\n$' + (k.revenue_12m / 1e6).toFixed(1) + 'M';
  };
  const pieIsSmall = (ctx) => ctx.dataset.data[ctx.dataIndex] / ctx.dataset.data.reduce((a,b) => a+b, 0) < 0.10;
  const pieOpts = (pos, fmt) => ({
    responsive: true, maintainAspectRatio: false,
    plugins: {
      legend: { position: pos, labels: { font: { size: 11 }, boxWidth: 14 } },
      datalabels: {
        formatter: fmt,
        anchor: (ctx) => pieIsSmall(ctx) ? 'end' : 'center',
        align:  (ctx) => pieIsSmall(ctx) ? 'end' : 'center',
        color:  (ctx) => pieIsSmall(ctx) ? '#1e293b' : '#fff',
        offset: (ctx) => pieIsSmall(ctx) ? 22 : 0,
        font: { weight: 'bold', size: 13 },
        textAlign: 'center'
      }
    }
  });

  if (_segUnitPie) _segUnitPie.destroy();
  _segUnitPie = new Chart(document.getElementById('segUnitPieChart'), {
    type: 'pie', plugins: [ChartDataLabels, pieLinePlugin],
    data: { labels: segs, datasets: [{ data: segs.map(s => SD.kpis[s].units_12m), backgroundColor: colors, borderWidth: 2, borderColor: '#fff' }] },
    options: pieOpts('right', pieFmtUnits)
  });

  if (_segRevPie) _segRevPie.destroy();
  _segRevPie = new Chart(document.getElementById('segRevPieChart'), {
    type: 'pie', plugins: [ChartDataLabels, pieLinePlugin],
    data: { labels: segs, datasets: [{ data: segs.map(s => SD.kpis[s].revenue_12m), backgroundColor: colors, borderWidth: 2, borderColor: '#fff' }] },
    options: pieOpts('right', pieFmtRev)
  });

  // ── Growth charts ────────────────────────────────────────────────────────
  // Indices: Sep=6,Oct=7,Nov=8 (prev 3M)  Dec=9,Jan=10,Feb=11 (last 3M)
  const prev3avg = s => (SD.monthly_units[s][6]+SD.monthly_units[s][7]+SD.monthly_units[s][8])/3;
  const last3avg = s => (SD.monthly_units[s][9]+SD.monthly_units[s][10]+SD.monthly_units[s][11])/3;
  const jan      = s =>  SD.monthly_units[s][10];
  const feb      = s =>  SD.monthly_units[s][11];

  const barDl = {
    display: true,
    anchor: 'end',
    align: 'end',
    offset: 2,
    formatter: v => v >= 1000 ? (v / 1000).toFixed(0) + 'K' : Math.round(v).toString(),
    font: { weight: 'bold', size: 13 },
    color: '#1e293b'
  };

  const barBase = {
    responsive: true, maintainAspectRatio: false,
    layout: { padding: { top: 36 } },
    plugins: { legend: { labels: { font: { size: 11 } } }, datalabels: barDl },
    scales: {
      x: { ticks: { font: { size: 10 } } },
      y: { ticks: { font: { size: 10 }, callback: v => (v/1000).toFixed(0)+'K' },
           title: { display: true, text: 'Units', font: { size: 10 } } }
    }
  };

  if (_seg3mChart) _seg3mChart.destroy();
  _seg3mChart = new Chart(document.getElementById('segGrowth3mChart'), {
    type: 'bar',
    plugins: [ChartDataLabels],
    data: {
      labels: segs,
      datasets: [
        { label: 'Sep–Nov 2025 avg', data: segs.map(prev3avg), backgroundColor: segs.map(s => SEG_COLORS_LIGHT[s]), borderRadius: 3 },
        { label: 'Dec 2025–Feb 2026 avg', data: segs.map(last3avg), backgroundColor: segs.map(s => SEG_COLORS[s]), borderRadius: 3 }
      ]
    },
    options: barBase
  });

  if (_segMomChart) _segMomChart.destroy();
  _segMomChart = new Chart(document.getElementById('segGrowthMomChart'), {
    type: 'bar',
    plugins: [ChartDataLabels],
    data: {
      labels: segs,
      datasets: [
        { label: 'Jan 2026', data: segs.map(jan), backgroundColor: segs.map(s => SEG_COLORS_LIGHT[s]), borderRadius: 3 },
        { label: 'Feb 2026', data: segs.map(feb), backgroundColor: segs.map(s => SEG_COLORS[s]), borderRadius: 3 }
      ]
    },
    options: barBase
  });

  // ── Line charts ──────────────────────────────────────────────────────────
  const mkLine = (seg) => ({
    label: seg, borderColor: SEG_COLORS[seg],
    backgroundColor: SEG_COLORS[seg] + '18',
    borderWidth: 2, pointRadius: 3, fill: false, tension: 0.35
  });

  const lineBase = (ylabel, fmt) => ({
    responsive: true, maintainAspectRatio: false,
    plugins: { legend: { labels: { font: { size: 11 }, boxWidth: 12 } }, datalabels: { display: false } },
    scales: {
      x: { ticks: { font: { size: 10 } } },
      y: { ticks: { font: { size: 10 }, callback: fmt }, title: { display: true, text: ylabel, font: { size: 10 } } }
    }
  });

  if (_segUnitLine) _segUnitLine.destroy();
  _segUnitLine = new Chart(document.getElementById('segUnitLineChart'), {
    type: 'line',
    data: { labels: SD.month_labels, datasets: segs.map(s => ({ ...mkLine(s), data: SD.monthly_units[s] })) },
    options: lineBase('Units', v => (v/1000).toFixed(0)+'K')
  });

  if (_segRevLine) _segRevLine.destroy();
  _segRevLine = new Chart(document.getElementById('segRevLineChart'), {
    type: 'line',
    data: { labels: SD.month_labels, datasets: segs.map(s => ({ ...mkLine(s), data: SD.monthly_rev[s] })) },
    options: lineBase('Revenue', v => '$'+(v/1e6).toFixed(1)+'M')
  });

  // ── Summary table ────────────────────────────────────────────────────────
  document.getElementById('seg_summary_tbody').innerHTML = segs.map(s => {
    const k = SD.kpis[s], c = SEG_COLORS[s];
    const grow = k.growth_pct !== null
      ? (k.growth_pct >= 0 ? '+'+k.growth_pct+'%' : k.growth_pct+'%') : '—';
    const gc = k.growth_pct !== null ? (k.growth_pct >= 0 ? 'delta-pos' : 'delta-neg') : 'delta-neu';
    return `<tr>
      <td><strong style="color:${c}">${s}</strong></td>
      <td>${k.skus}</td>
      <td>${k.units_12m.toLocaleString('en-US',{maximumFractionDigits:0})}</td>
      <td>$${k.revenue_12m.toLocaleString('en-US',{maximumFractionDigits:0})}</td>
      <td>$${k.avg_price!==null?k.avg_price.toFixed(2):'—'}</td>
      <td class="${gc}">${grow}</td>
      <td>${k.unit_share}%</td>
      <td>${k.rev_share}%</td>
    </tr>`;
  }).join('');
}

segInit();

// ═══════════════════════════════════ TAB J — LURE ════════════════════════════
const LURE_DATA = {
  subseg_units: { 'Trap': 1462329, 'Refill': 78784 },
  subseg_rev:   { 'Trap': 20056193.48, 'Refill': 1119793.59 },
  pack_sizes:   ['1','2','3','4','6','12'],
  pack_units:   { '1': 195883, '2': 223408, '3': 13363, '4': 763182, '6': 250686, '12': 15807 },
  pack_rev:     { '1': 1502998.78, '2': 2975751.22, '3': 293856.11, '4': 10243538.07, '6': 4440828.08, '12': 599221.22 }
};

const LURE_COLORS = { 'Trap': '#2563eb', 'Refill': '#d97706' };

let _lureUnitPie, _lureRevPie, _lurePack;

function lureInit() {
  const LD   = LURE_DATA;
  const subs = ['Trap', 'Refill'];
  const totalUnits = subs.reduce((a, s) => a + LD.subseg_units[s], 0);
  const totalRev   = subs.reduce((a, s) => a + LD.subseg_rev[s],   0);

  // ── KPI cards ─────────────────────────────────────────────────────────────
  const kpiItems = [
    { label: 'Total Lure Units sold (12M)', value: (totalUnits/1e6).toFixed(2)+'M' },
    { label: 'Total Lure Revenue (12M)',    value: '$'+(totalRev/1e6).toFixed(1)+'M' },
    { label: 'Trap Share',                  value: Math.round(LD.subseg_units['Trap']/totalUnits*100)+'%' },
    { label: 'Refill Share',                value: Math.round(LD.subseg_units['Refill']/totalUnits*100)+'%' },
  ];
  document.getElementById('lure_kpi_section').innerHTML = kpiItems.map(k =>
    `<div class="kpi"><div class="kpi-v">${k.value}</div><div class="kpi-l">${k.label}</div></div>`
  ).join('');

  // ── Shared pie helpers ────────────────────────────────────────────────────
  // Slices below this threshold: label + leader line drawn manually (never clamped)
  const LURE_SMALL = 0.15;

  // Factory: returns a plugin that draws leader line + label for small slices.
  // valueFn(v) → the second line of text shown next to % (e.g. "78K units" or "$1.1M")
  let _lurePlgIdx = 0;
  const makeLureLeaderPlugin = (valueFn) => ({
    id: 'lureLeader' + (++_lurePlgIdx),
    afterDraw(chart) {
      const ctx2   = chart.ctx;
      const meta   = chart.getDatasetMeta(0);
      const data   = chart.data.datasets[0].data;
      const colors = chart.data.datasets[0].backgroundColor;
      const total  = data.reduce((a,b) => a+b, 0);

      meta.data.forEach((arc, i) => {
        const v = data[i];
        if (v / total >= LURE_SMALL) return; // large slices handled by datalabels

        const mid      = (arc.startAngle + arc.endAngle) / 2;
        const r        = arc.outerRadius;
        const cos      = Math.cos(mid), sin = Math.sin(mid);
        const pct      = Math.round(v / total * 100);
        const valStr   = valueFn(v);
        // Dark burnt orange: legible on white background (slice bg #d97706 is too light)
        const extColor = '#b35900';

        // Leader line: arc edge → 22px out
        ctx2.save();
        ctx2.strokeStyle = extColor;
        ctx2.lineWidth = 1.5;
        ctx2.beginPath();
        ctx2.moveTo(arc.x + cos * (r + 2),  arc.y + sin * (r + 2));
        ctx2.lineTo(arc.x + cos * (r + 12), arc.y + sin * (r + 12));
        ctx2.stroke();

        // Label: centered 44px outside arc edge, no white outline
        const lx  = arc.x + cos * (r + 44);
        const ly  = arc.y + sin * (r + 44) + 20;
        const txt = pct + '% · ' + valStr;
        ctx2.font = 'bold 13px sans-serif';
        ctx2.textAlign = 'center';
        ctx2.textBaseline = 'middle';
        ctx2.fillStyle = extColor;
        ctx2.fillText(txt, lx, ly);
        ctx2.restore();
      });
    }
  });

  const _lureSmall = (ctx) => ctx.dataset.data[ctx.dataIndex] / ctx.dataset.data.reduce((a,b)=>a+b,0) < LURE_SMALL;

  // datalabels only for large (inside) slices; small slices drawn by plugin above
  const lureDlOpts = (fmt) => ({
    display: (ctx) => !_lureSmall(ctx),
    formatter: fmt,
    anchor: 'center', align: 'center', offset: 0,
    color: '#fff',
    font: { weight: 'bold', size: 13 },
    textAlign: 'center'
  });

  const lurePieFmtUnits = (v, ctx) => {
    const t = ctx.chart.data.datasets[0].data.reduce((a,b) => a+b, 0);
    const pct = t > 0 ? Math.round(v/t*100) : 0;
    const u = v >= 1e6 ? (v/1e6).toFixed(1)+'M' : (v/1000).toFixed(0)+'K';
    return pct + '%\n' + u + ' units';
  };
  const lurePieFmtRev = (v, ctx) => {
    const t = ctx.chart.data.datasets[0].data.reduce((a,b) => a+b, 0);
    const pct = t > 0 ? Math.round(v/t*100) : 0;
    return pct + '%\n$' + (v/1e6).toFixed(1) + 'M';
  };

  const lurePieOpts = (fmt) => ({
    responsive: true, maintainAspectRatio: false,
    layout: { padding: 40 },
    plugins: {
      legend: { position: 'right', labels: { font: { size: 11 }, boxWidth: 14 } },
      datalabels: lureDlOpts(fmt)
    }
  });
  const lureColors = subs.map(s => LURE_COLORS[s]);

  if (_lureUnitPie) _lureUnitPie.destroy();
  _lureUnitPie = new Chart(document.getElementById('lureUnitPieChart'), {
    type: 'pie',
    plugins: [ChartDataLabels, makeLureLeaderPlugin(v => {
      const u = v >= 1e6 ? (v/1e6).toFixed(1)+'M' : (v/1000).toFixed(0)+'K';
      return u + ' units';
    })],
    data: { labels: subs, datasets: [{ data: subs.map(s => LD.subseg_units[s]), backgroundColor: lureColors, borderWidth: 2, borderColor: '#fff' }] },
    options: lurePieOpts(lurePieFmtUnits)
  });

  if (_lureRevPie) _lureRevPie.destroy();
  _lureRevPie = new Chart(document.getElementById('lureRevPieChart'), {
    type: 'pie',
    plugins: [ChartDataLabels, makeLureLeaderPlugin(v => '$' + (v/1e6).toFixed(1) + 'M')],
    data: { labels: subs, datasets: [{ data: subs.map(s => LD.subseg_rev[s]), backgroundColor: lureColors, borderWidth: 2, borderColor: '#fff' }] },
    options: lurePieOpts(lurePieFmtRev)
  });

  // ── Dual-axis pack size chart ─────────────────────────────────────────────
  const sizes = LD.pack_sizes;
  const packLabels = sizes.map(s => s+'-pack');

  // Custom plugin: draws revenue labels above bar tops (not above line dots)
  const lureRevLabelPlugin = {
    id: 'lureRevLabel',
    afterDatasetsDraw(chart) {
      const ctx = chart.ctx;
      const barMeta = chart.getDatasetMeta(0); // bars dataset
      const revValues = chart.data.datasets[1].data;
      const MIN_FROM_BOTTOM = 44; // px — small-bar labels stay at least this high

      revValues.forEach((val, i) => {
        const bar = barMeta.data[i];
        const label = '$' + (val / 1e6).toFixed(1) + 'M';

        // Target: 14px above bar top. Clamp so short bars lift label up.
        const desired = bar.y - 14;
        const clamp   = chart.chartArea.bottom - MIN_FROM_BOTTOM;
        const labelY  = Math.min(desired, clamp);

        ctx.save();
        ctx.font = 'bold 13px sans-serif';
        ctx.fillStyle = '#b35900';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'bottom';
        ctx.fillText(label, bar.x, labelY);
        ctx.restore();
      });
    }
  };

  const legendLiftPlugin = {
    id: 'legendLift',
    afterLayout(chart) {
      if (!chart.legend) return;
      chart.legend.top    -= 40;
      chart.legend.bottom -= 40;
    }
  };

  if (_lurePack) _lurePack.destroy();
  // ── Pack size pie charts (Tab A — Market Structure) ───────────────────────
  const packColors = ['#2563eb','#16a34a','#d97706','#dc2626','#7c3aed','#0891b2'];

  function makePackPie(canvasId, rawData, fmtFn) {
    const el = document.getElementById(canvasId);
    if (!el) return;
    const total = rawData.reduce((a, b) => a + b, 0);
    new Chart(el, {
      type: 'pie',
      plugins: [ChartDataLabels],
      data: { labels: packLabels, datasets: [{ data: rawData, backgroundColor: packColors }] },
      options: {
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { font: { size: 11 }, padding: 10, boxWidth: 14 } },
          datalabels: {
            display: ctx => ctx.dataset.data[ctx.dataIndex] / total >= 0.04,
            formatter: v => Math.round(v / total * 100) + '%',
            color: '#fff', font: { weight: 'bold', size: 12 }
          },
          tooltip: { callbacks: { label: ctx => ctx.label + ': ' + fmtFn(ctx.raw) + ' (' + Math.round(ctx.raw / total * 100) + '%)' } }
        }
      }
    });
  }

  const packUnitData = sizes.map(s => LD.pack_units[s]);
  const packRevData  = sizes.map(s => LD.pack_rev[s]);
  makePackPie('packUnitPieChart', packUnitData, v => (v/1000).toFixed(0) + 'K units');
  makePackPie('packRevPieChart',  packRevData,  v => '$' + (v/1e6).toFixed(2) + 'M');

  _lurePack = new Chart(document.getElementById('lurePackChart'), {
    type: 'bar',
    plugins: [ChartDataLabels, lureRevLabelPlugin, legendLiftPlugin],
    data: {
      labels: packLabels,
      datasets: [
        {
          type: 'bar',
          label: 'Units sold (12M)',
          data: sizes.map(s => LD.pack_units[s]),
          backgroundColor: '#2563eb99',
          borderColor: '#2563eb',
          borderWidth: 1,
          borderRadius: 4,
          yAxisID: 'yUnits',
          datalabels: {
            anchor: (ctx) => (ctx.dataIndex === 2 || ctx.dataIndex === 5) ? 'end' : 'center',
            align:  (ctx) => (ctx.dataIndex === 2 || ctx.dataIndex === 5) ? 'end' : 'center',
            offset: (ctx) => (ctx.dataIndex === 2 || ctx.dataIndex === 5) ? 20 : 0,
            color:  (ctx) => (ctx.dataIndex === 2 || ctx.dataIndex === 5) ? '#1a3a6e' : '#ffffff',
            formatter: v => v >= 1000 ? (v/1000).toFixed(0)+'K' : Math.round(v).toString(),
            font: { weight: 'bold', size: 13 },
            backgroundColor: null,
            padding: 0
          }
        },
        {
          type: 'line',
          label: 'Revenue (12M)',
          data: sizes.map(s => LD.pack_rev[s]),
          borderColor: '#d97706',
          backgroundColor: '#d9770622',
          borderWidth: 2.5,
          pointRadius: 5,
          pointBackgroundColor: '#d97706',
          tension: 0.3,
          yAxisID: 'yRev',
          datalabels: { display: false }  // drawn by lureRevLabelPlugin instead
        }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      layout: { padding: { top: 50 } },
      plugins: {
        legend: { labels: { font: { size: 11 } } },
        datalabels: { display: true }
      },
      scales: {
        x: { ticks: { font: { size: 11 } } },
        yUnits: {
          type: 'linear', position: 'left',
          title: { display: true, text: 'Units sold', font: { size: 10 } },
          ticks: { font: { size: 10 }, callback: v => (v/1000).toFixed(0)+'K' },
          grid: { color: '#f1f5f9' }
        },
        yRev: {
          type: 'linear', position: 'right',
          title: { display: true, text: 'Revenue ($)', font: { size: 10 } },
          ticks: { font: { size: 10 }, callback: v => '$'+(v/1e6).toFixed(1)+'M' },
          grid: { drawOnChartArea: false }
        }
      }
    }
  });
}

lureInit();

// ═══════════════ TAB K — DYNAMIKA UDZIAŁÓW MAREK (LURE) ══════════════════════
(function() {
  const months = ['Mar\'25','Apr\'25','May\'25','Jun\'25','Jul\'25','Aug\'25',
                  'Sep\'25','Oct\'25','Nov\'25','Dec\'25','Jan\'26','Feb\'26'];
  const ds = [
    { label: 'Terro',             data: [61.5,54.2,57.1,60.8,63.7,57.6,64.3,58.1,60.5,59.6,54.5,52.2], borderColor:'#16a34a', borderWidth:2.5 },
    { label: "Aunt Fannie's",     data: [20.0,20.5,18.7,18.9,17.0,19.0,18.5,15.8,15.8,12.9,12.4,14.9], borderColor:'#2563eb', borderWidth:2.5 },
    { label: 'Super Ninja',       data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.4,15.5,12.1,15.2,15.6,16.0], borderColor:'#7c3aed', borderWidth:2.5 },
    { label: 'HOT SHOT',          data: [1.6, 5.1, 9.1, 7.4, 8.9,10.4, 3.4, 1.6, 0.9, 1.0, 2.5, 1.7], borderColor:'#dc2626', borderWidth:2.0 },
    { label: 'Raid',              data: [10.4,13.7, 9.4, 6.9, 5.2, 6.0, 6.4, 5.0, 6.3, 6.2, 7.4, 6.5], borderColor:'#f97316', borderWidth:2.0 },
    { label: 'Qualirey',          data: [4.0, 3.9, 3.3, 3.6, 2.9, 4.0, 3.4, 2.8, 2.9, 3.0, 4.3, 4.8], borderColor:'#0891b2', borderWidth:1.8 },
    { label: 'STEM',              data: [1.9, 2.1, 1.4, 1.2, 1.5, 1.8, 1.1, 0.7, 0.8, 1.0, 1.6, 2.1], borderColor:'#d97706', borderWidth:1.5, borderDash:[5,3] },
    { label: 'Fly Away Product',  data: [0.6, 0.6, 0.0, 0.4, 0.5, 0.7, 0.5, 0.4, 0.5, 0.9, 1.5, 0.9], borderColor:'#be185d', borderWidth:1.5, borderDash:[5,3], hidden:true },
    { label: 'Acme Approved',     data: [0.0, 0.0, 1.0, 0.7, 0.4, 0.4, 0.1, 0.0, 0.3, 0.2, 0.3, 0.3], borderColor:'#64748b', borderWidth:1.5, borderDash:[5,3], hidden:true },
    { label: 'ELEGENZO',          data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5], borderColor:'#94a3b8', borderWidth:1.5, borderDash:[5,3], hidden:true }
  ];
  ds.forEach(d => { d.backgroundColor = 'transparent'; d.tension = 0.3; d.pointRadius = 3; d.pointHoverRadius = 5; });

  new Chart(document.getElementById('lureShareChart'), {
    type: 'line',
    data: { labels: months, datasets: ds },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { font: { size: 11 }, padding: 12, boxWidth: 20 } },
        datalabels: { display: false },
        tooltip: {
          mode: 'index', intersect: false,
          callbacks: {
            label: ctx => ' ' + ctx.dataset.label + ': ' + ctx.parsed.y.toFixed(1) + '%'
          }
        }
      },
      scales: {
        y: {
          min: 0, max: 100,
          ticks: { callback: v => v + '%', stepSize: 10 },
          grid: { color: '#e2e8f0' }
        },
        x: { grid: { display: false } }
      }
    }
  });
})();

// ═══════════════ TAB L — REVIEWS (TERRO vs HOT SHOT) ════════════════════════
(function() {
  // S1: Star distribution — 100% stacked horizontal bar
  new Chart(document.getElementById('starDistChart'), {
    type: 'bar',
    plugins: [ChartDataLabels],
    data: {
      labels: ['Terro  (4.1★ · 24,106 ratings)', 'Hot Shot  (2.4★ · 1,946 ratings)'],
      datasets: [
        { label: '5★', data: [60, 23], backgroundColor: '#16a34a' },
        { label: '4★', data: [15,  8], backgroundColor: '#84cc16' },
        { label: '3★', data: [10, 10], backgroundColor: '#f59e0b' },
        { label: '2★', data: [4,  10], backgroundColor: '#f97316' },
        { label: '1★', data: [11, 49], backgroundColor: '#dc2626' }
      ]
    },
    options: {
      maintainAspectRatio: false, indexAxis: 'y',
      plugins: {
        legend: { position: 'bottom', labels: { font: { size: 11 }, boxWidth: 14, padding: 10 } },
        datalabels: {
          display: ctx => ctx.dataset.data[ctx.dataIndex] >= 5,
          formatter: v => v + '%',
          color: '#fff', font: { weight: 'bold', size: 11 }
        },
        tooltip: { callbacks: { label: ctx => ctx.dataset.label + ': ' + ctx.raw + '%' } }
      },
      scales: {
        x: { stacked: true, max: 100, ticks: { callback: v => v + '%' } },
        y: { stacked: true }
      }
    }
  });

  // S2: Unmet Needs pie
  const unmetLabels = ['Not working','Design flaw','Value disappointment','Ease of use','Hygiene concern','Prob. returns','Misleading expect.','Safety concern'];
  const unmetData   = [404, 8, 28, 55, 23, 6, 0, 4];
  const unmetTotal  = 528;
  const unmetColors = ['#dc2626','#f97316','#d97706','#7c3aed','#0891b2','#16a34a','#2563eb','#94a3b8'];
  new Chart(document.getElementById('unmetNeedsChart'), {
    type: 'pie',
    plugins: [ChartDataLabels],
    data: { labels: unmetLabels, datasets: [{ data: unmetData, backgroundColor: unmetColors }] },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { font: { size: 10 }, padding: 8, boxWidth: 12 } },
        datalabels: {
          display: ctx => unmetData[ctx.dataIndex] / unmetTotal >= 0.04,
          formatter: v => Math.round(v / unmetTotal * 100) + '%',
          color: '#fff', font: { weight: 'bold', size: 11 }
        },
        tooltip: { callbacks: { label: ctx => ctx.label + ': ' + ctx.raw + ' reviews (' + Math.round(ctx.raw / unmetTotal * 100) + '%)' } }
      }
    }
  });

  // S4: Failure by brand — horizontal grouped bar
  new Chart(document.getElementById('failByBrandChart'), {
    type: 'bar',
    data: {
      labels: ['Not working','Design flaw','Value disapp.','Ease of use','Hygiene','Prob. returns','Safety','Misleading'],
      datasets: [
        { label: 'Terro',    data: [77.3, 2.3, 6.0, 7.7, 5.0, 1.3, 0.3, 0.0], backgroundColor: '#2563eb' },
        { label: 'Hot Shot', data: [75.4, 0.4, 4.4, 14.0, 3.5, 0.9, 1.3, 0.0], backgroundColor: '#dc2626' }
      ]
    },
    options: {
      maintainAspectRatio: false, indexAxis: 'y',
      plugins: {
        legend: { position: 'bottom', labels: { font: { size: 11 }, boxWidth: 14 } },
        datalabels: { display: false },
        tooltip: { callbacks: { label: ctx => ctx.dataset.label + ': ' + ctx.raw + '%' } }
      },
      scales: { x: { ticks: { callback: v => v + '%' } } }
    }
  });

  // S5d: Time-to-failure (excluding "Not stated" 75.0%)
  new Chart(document.getElementById('ttfChart'), {
    type: 'bar',
    plugins: [ChartDataLabels],
    data: {
      labels: ['Day 1', '2–3 days', '~1 week', '1+ month'],
      datasets: [{ data: [3.2, 4.9, 13.3, 3.6],
        backgroundColor: ['#dc2626','#f97316','#d97706','#16a34a'], label: '% of negatives' }]
    },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        datalabels: {
          formatter: v => v + '%', color: '#fff',
          font: { weight: 'bold', size: 11 }, anchor: 'center', align: 'center'
        },
        tooltip: { callbacks: { label: ctx => ctx.raw + '% of all 1★+2★+3★ reviews (75.0% did not state time)' } }
      },
      scales: { y: { ticks: { callback: v => v + '%' }, max: 25 } }
    }
  });
})();

// ── Sortable table ────────────────────────────────────────────────────────────
function sortTbl(tableId, col, th) {
  const tbl   = document.getElementById(tableId);
  const tbody = tbl.tBodies[0];
  const rows  = Array.from(tbody.rows);
  const asc   = th.dataset.asc === '1';
  rows.sort((a, b) => {
    const av = parseFloat(a.cells[col].dataset.val) || 0;
    const bv = parseFloat(b.cells[col].dataset.val) || 0;
    return asc ? av - bv : bv - av;
  });
  rows.forEach(r => tbody.appendChild(r));
  tbl.querySelectorAll('.th-sort').forEach(h => {
    h.dataset.asc = '';
    h.innerHTML = h.innerHTML.replace(/\s*[△▽]$/, '') + ' ▽';
  });
  th.innerHTML = th.innerHTML.replace(/\s*[△▽]$/, '') + (asc ? ' △' : ' ▽');
  th.dataset.asc = asc ? '0' : '1';
}
