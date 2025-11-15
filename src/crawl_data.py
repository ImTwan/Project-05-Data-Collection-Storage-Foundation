import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Input CSV
INPUT_CSV = "D:\python try hard\project5\product_filtered_outputs\part1_main_collections.csv"
OUTPUT_CSV = "product_filtered_outputs/product_names.csv"

# Read CSV
df = pd.read_csv(INPUT_CSV)
df['product_id_final'] = df['product_id'].fillna(df['viewing_product_id'])
df_unique = df.drop_duplicates(subset=['product_id_final'])

# Filter out rows with missing URLs
df_unique = df_unique[df_unique['current_url'].notna() & (df_unique['current_url'] != "")]

print(f"Total URLs to crawl: {len(df_unique)}")

# Function to crawl a single URL
def crawl_product(row):
    url = row['current_url']
    product_id = row['product_id_final']

    try:
        session = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = session.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[Warning] Status {response.status_code} for URL: {url}")
            return {"product_id": product_id, "product_name": None, "url": url}

        soup = BeautifulSoup(response.text, "html.parser")
        title_tag = soup.find("h1") or soup.find("title")
        product_name = title_tag.get_text(strip=True) if title_tag else None

        return {"product_id": product_id, "product_name": product_name, "url": url}

    except Exception as e:
        print(f"[Error] {url} → {e}")
        return {"product_id": product_id, "product_name": None, "url": url}

# Crawl concurrently
results = []
MAX_WORKERS = 10

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    future_to_url = {executor.submit(crawl_product, row): row['current_url'] for idx, row in df_unique.iterrows()}

    for i, future in enumerate(as_completed(future_to_url), 1):
        res = future.result()
        results.append(res)
        if i % 10 == 0 or i == len(future_to_url):
            print(f"Crawled {i}/{len(future_to_url)} URLs")

# Save results
df_result = pd.DataFrame(results)
df_result.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')

print(f"\n🎉 Crawling complete! Results saved → {OUTPUT_CSV}")
