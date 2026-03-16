"""
Fetch product listing data from Amazon SP-API Catalog Items API.
Outputs listing_comm_data.json with images, titles, bullet points for 5 target ASINs.
"""
import os, json, time, sys, requests
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

# ── Config ────────────────────────────────────────────────────────────────────
ENV_PATH = r'c:\AI Workspaces\Claude Code Workspace - Tom\.env'
load_dotenv(ENV_PATH)

CLIENT_ID     = os.getenv('SP_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('SP_API_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('SP_API_US_REFRESH_TOKEN')
MARKETPLACE   = 'ATVPDKIKX0DER'  # US marketplace

TARGET_ASINS = [
    'B01MRHXM0I',  # Terro 4-pack
    'B0BX4GQF68',  # Terro 6-pack
    'B07VYPGHFW',  # Aunt Fannie's
    'B0DGWQV8GK',  # HOT SHOT
    'B0D5DJ7V4P',  # Super Ninja
]

OUT_FILE = os.path.join(os.path.dirname(__file__), 'listing_comm_data.json')

# ── Step 1: Get LWA access token ─────────────────────────────────────────────
def get_access_token():
    print('Getting LWA access token...')
    resp = requests.post('https://api.amazon.com/auth/o2/token', data={
        'grant_type':    'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id':     CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    resp.raise_for_status()
    token = resp.json()['access_token']
    print('  Access token obtained.')
    return token

# ── Step 2: Fetch Catalog Items ──────────────────────────────────────────────
def fetch_catalog_item(asin, token):
    url = f'https://sellingpartnerapi-na.amazon.com/catalog/2022-04-01/items/{asin}'
    params = {
        'marketplaceIds': MARKETPLACE,
        'includedData':   'images,summaries,attributes,productTypes',
    }
    headers = {
        'x-amz-access-token': token,
        'user-agent': 'FruitFliesDashboard/1.0',
    }
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()

def parse_item(raw):
    """Extract useful fields from SP-API Catalog Items response."""
    result = {'asin': raw.get('asin', '')}

    # Summaries (title, brand)
    summaries = raw.get('summaries', [])
    if summaries:
        s = summaries[0]
        result['title'] = s.get('itemName', '')
        result['brand'] = s.get('brand', '')
        result['browse_classification'] = s.get('browseClassification', {}).get('displayName', '')

    # Images — all variants
    images_data = raw.get('images', [])
    images = []
    if images_data:
        for img in images_data[0].get('images', []):
            images.append({
                'variant': img.get('variant', ''),
                'url':     img.get('link', ''),
                'width':   img.get('width', 0),
                'height':  img.get('height', 0),
            })
    # Sort: MAIN first, then PT01, PT02, etc.
    variant_order = {'MAIN': 0}
    images.sort(key=lambda x: variant_order.get(x['variant'], 100) if x['variant'] == 'MAIN' else int(x['variant'].replace('PT', '').replace('MAIN', '0') or '99'))
    result['images'] = images

    # Bullet points from attributes
    attrs = raw.get('attributes', {})
    bullets = []
    if 'bullet_point' in attrs:
        for bp in attrs['bullet_point']:
            val = bp.get('value', '')
            if val:
                bullets.append(val)
    result['bullet_points'] = bullets

    # Product type
    pt = raw.get('productTypes', [])
    result['product_type'] = pt[0].get('productType', '') if pt else ''

    return result

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    token = get_access_token()
    products = {}

    for asin in TARGET_ASINS:
        print(f'Fetching {asin}...')
        try:
            raw = fetch_catalog_item(asin, token)
            parsed = parse_item(raw)
            products[asin] = parsed
            print(f'  {parsed.get("brand", "?")} — {len(parsed["images"])} images, {len(parsed["bullet_points"])} bullets')
        except requests.exceptions.HTTPError as e:
            print(f'  ERROR: {e.response.status_code} — {e.response.text[:200]}')
            products[asin] = {'asin': asin, 'error': str(e)}
        time.sleep(1)  # Rate limit safety

    output = {
        'fetched': '2026-03-15',
        'marketplace': 'US (ATVPDKIKX0DER)',
        'products': products,
    }

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f'\nSaved to {OUT_FILE}')
    print(f'Products: {len(products)}')

if __name__ == '__main__':
    main()
