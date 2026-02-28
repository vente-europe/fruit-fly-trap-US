# Methodology & Limitations

## Data Sources
- **Amazon product listings:** Scraped via Apify (live data at time of scrape)
- **Amazon reviews:** Scraped via Apify (1–3 star reviews only by default)
- **No Helium10 data used in this run** (Apify-first pipeline)

## Revenue Estimation
Revenue is estimated using the BSR power-law model:
```
est_units/month = base_multiplier × BSR^(-0.7)
base_multiplier (category: home): 2000
est_revenue = est_units × price
```

**Total category estimate:** top ASINs are assumed to represent 40% of the market. This is configurable in `category.yaml`.

## Claims Extraction
- Model: `claude-haiku-4-5-20251001`
- Input: title + bullet points for top 50 ASINs
- Output: structured claim objects with type + confidence score

## Review Theme Clustering
- Model: `claude-haiku-4-5-20251001`
- Fixed theme schema: shipping, quality, packaging, sizing, scent, misleading_description, value, durability, defective, performance, customer_service, safety_concern, other
- Only 1–3 star reviews included

## Limitations
1. BSR->revenue formula is an approximation; actual sales may differ by 2–3×
2. Long-tail Pareto estimate is configurable but unverified without Brand Analytics access
3. Seasonality index requires multiple monthly scrapes — not available in single-run mode
4. Review scraping is subject to Apify/Amazon availability; may miss recent reviews
5. Claims confidence is model-estimated; manual review recommended for compliance

**Scrape date:** 2026-02-19