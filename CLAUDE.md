# Dashboard Fruit Flies

> **Living document** — Update after every bug fix or new pattern found. No permission needed for additions. Ask before removing.

---

## Project Overview

- **Purpose:** Amazon US market analysis dashboard — fruit fly trap category
- **Active file:** `reports/h10-2026-02-25/index.html` (single-file HTML, ~1720 lines)
- **Git repo:** root of this folder (branch: `master`)
- **Tech stack:** Chart.js 4.4.0 + chartjs-plugin-datalabels 2.2.0, vanilla JS, no build step

---

## Tab Structure

| ID | Label | Key content |
|----|-------|-------------|
| `ti` | 1 — Main Segments (Total Market) | Segment KPIs, segment bar charts, segment summary table |
| `tb` | 2 — Market Structure | Pack size pies, brand pies, PSC charts, lure share line, seasonality |
| `tl` | 3 — Reviews | Terro vs HOT SHOT review analysis |

**Default active tab:** `ti`

---

## Key Canvas IDs

| Canvas ID | Chart type | Tab | Description |
|-----------|-----------|-----|-------------|
| `packUnitPieChart` | pie | tb | Pack Size — Unit Share |
| `packRevPieChart` | pie | tb | Pack Size — Revenue Share |
| `brandUnitsPieChart` | pie | tb | Brand Units Share — Lure |
| `brandRevPieChart` | pie | tb | Brand Revenue Share — Lure |
| `packBrand2/4/6Chart` | pie | tb | Brand share per pack size (units) |
| `packBrand2/4/6RevChart` | pie | tb | Brand share per pack size (revenue) |
| `lureShareChartTb` | line | tb | % Unit Share — Brand vs. Total Lure (max Y: 70%) |
| `pscPie2/4/6Chart` | pie | tb | Brand Unit Share per Pack Size |
| `pscPriceChart` | bar | tb | Price Positioning — TOP 3 Brands |
| `pscScatterChart` | scatter | tb | Price vs Unit Share |
| `seasIdxChartTb` | bar | tb | Monthly Seasonality Index |

---

## JS Data Structures

- **`SHARE_DATA`** — main data object (asin_data, p2_units, p2_rev, etc.)
- **`ASIN_DS`** — per-ASIN monthly unit arrays
- **`MONTHS`** — array of month strings (format: `"YYYY-MM"`)
- **`SD`** — segment dynamics (monthly_units, monthly_rev, kpis, month_labels)
- **`SEG_COLORS`** — segment color map

---

## Source Data

| Path | Description |
|------|-------------|
| `Data/sales-units/` | Per-ASIN sales CSVs (3y history) — not git tracked |
| `Data/x-ray/` | Full X-Ray export — not git tracked |
| `Data/reviews/` | Amazon review scraper JSONs — not git tracked |
| `reports/h10-2026-02-25/lure_data.json` | Pre-processed lure segment data |
| `reports/h10-2026-02-25/segment_data.json` | Pre-processed segment data |

---

## Known Bugs & Fixes

### 1. Chart.js 0×0 hidden panel bug (recurring!)
**Symptom:** Charts in `display:none` panels render at 0×0 and appear blank on tab switch.
**Fix:**
1. All canvas IDs in HTML must exist in JS — missing canvas = `TypeError` kills entire `<script>` block
2. Use `window.load + setTimeout(100)` + `Object.values(Chart.instances).forEach(c => c.resize())` for force-resize
3. On tab switch: use `void panel.offsetHeight` before resize (forces synchronous reflow)

### 2. TypeError propagation kills all subsequent charts
**Symptom:** One missing canvas (`new Chart(null, ...)`) stops ALL chart initialization in the same `<script>` block.
**Fix:** Add null guard to every chart creation function:
```javascript
const el = document.getElementById(canvasId);
if (!el) return;
new Chart(el, { ... });
```

### 3. Shared dataset hidden state between duplicate charts
**Symptom:** Toggling legend on one chart affects another chart using the same dataset array.
**Fix:** Use shallow copy: `ds.map(d => ({ ...d }))` when passing dataset to second chart instance.

### 4. KPI selectors targeting removed panels
**Symptom:** `document.querySelectorAll('#td .kpi')` throws or silently fails after panel is deleted.
**Fix:** Remove or null-guard JS that references deleted HTML elements.

---

## Editing Conventions

- **Python scripts** for large HTML section replacements (Edit tool struggles with 100+ line exact matches)
- **Edit tool** for targeted JS changes and small HTML edits
- **Always verify** canvas IDs in HTML match JS after any structural change
- **Never remove** canvas from HTML without adding null guard in JS, or removing the JS entirely

---

## Self-Update Rules

**Update this file when:**
- A new bug is discovered and fixed → add to Known Bugs & Fixes
- A new canvas/chart is added → add to Canvas IDs table
- Tab structure changes → update Tab Structure table
- A new data structure is used → add to JS Data Structures

**Ask first before:**
- Removing existing bug entries
- Changing canvas ID naming conventions
