"""Fetch main product images for 13 niche ASINs via Amazon SP-API Catalog Items."""
import os, sys, csv, json, time, requests
from dotenv import load_dotenv
sys.stdout.reconfigure(encoding='utf-8')

ENV_PATH = r'c:\AI Workspaces\Claude Code Workspace - Tom\.env'
load_dotenv(ENV_PATH)

CLIENT_ID     = os.getenv('SP_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('SP_API_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('SP_API_US_REFRESH_TOKEN')
MARKETPLACE   = 'ATVPDKIKX0DER'  # US

# Read ASINs from competitors CSV
with open('../../Data/DD/niche-NbkRzdCvUi-competitors.csv', 'r', encoding='utf-8') as f:
    reader = list(csv.reader(f))
asins = [a.strip() for a in reader[0][6:]]
brands = [b.strip() for b in reader[1][6:]]
print(f'{len(asins)} ASINs to fetch')

# Get LWA access token
def get_token():
    r = requests.post('https://api.amazon.com/auth/o2/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    r.raise_for_status()
    return r.json()['access_token']

token = get_token()
print('Got access token')

# Fetch catalog item images
results = {}
for i, asin in enumerate(asins):
    url = f'https://sellingpartnerapi-na.amazon.com/catalog/2022-04-01/items/{asin}'
    params = {
        'marketplaceIds': MARKETPLACE,
        'includedData': 'images',
    }
    headers = {
        'x-amz-access-token': token,
        'Content-Type': 'application/json',
    }
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200:
        data = r.json()
        images = data.get('images', [])
        main_img = None
        for img_set in images:
            for img in img_set.get('images', []):
                if img.get('variant') == 'MAIN':
                    main_img = img.get('link')
                    break
            if main_img:
                break
        results[asin] = main_img
        print(f'  {i+1}/{len(asins)} {asin} ({brands[i]}): {main_img[:60] if main_img else "NO IMAGE"}')
    else:
        print(f'  {i+1}/{len(asins)} {asin}: HTTP {r.status_code}')
        results[asin] = None

    if i < len(asins) - 1:
        time.sleep(0.5)  # rate limit

# Save results
with open('niche_images.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print(f'\nSaved {len(results)} image URLs to niche_images.json')
print(f'Found: {sum(1 for v in results.values() if v)}/{len(results)}')
