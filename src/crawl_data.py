import csv
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

INPUT = "D:\python try hard\project5\Project-05-Data-Collection-Storage-Foundation\csv files result\product_ids_to_crawl.csv"
OUTPUT = "D:\python try hard\project5\Project-05-Data-Collection-Storage-Foundation\csv files result\valid_product_ids.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

SHOW_EACH_URL = False  # Set to True if you want to print every URL


def validate_product_id(product_id):
    # Return True if product page exists and contains an <h1>.
    url = f"https://www.glamira.fr/catalog/product/view/id/{product_id}"

    if SHOW_EACH_URL:
        print(f"🔍 Checking: {url}")

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)

        if r.status_code != 200:
            return (product_id, False)

        soup = BeautifulSoup(r.text, "html.parser")
        h1 = soup.find("h1")

        return (product_id, bool(h1))

    except Exception:
        return (product_id, False)


print("📌 Loading product IDs...")
rows = []
with open(INPUT, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

product_ids = [row["product_id"] for row in rows]

print(f"📌 Total product IDs loaded: {len(product_ids):,}")
print("🚀 Starting validation...\n")

valid_ids = []
invalid_ids = []

MAX_WORKERS = 20

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {
        executor.submit(validate_product_id, pid): pid
        for pid in product_ids
    }

    for future in tqdm(as_completed(futures), total=len(futures), desc="Validating"):
        pid, is_valid = future.result()
        
        if is_valid:
            print(f"✅ VALID: {pid}")
            valid_ids.append(pid)
        else:
            print(f"❌ INVALID: {pid}")
            invalid_ids.append(pid)

print("\n🎉 Validation complete!")
print(f"✔ Valid IDs: {len(valid_ids):,}")
print(f"✖ Invalid IDs: {len(invalid_ids):,}")

print(f"💾 Saving valid IDs to {OUTPUT}...")

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["product_id"])
    for pid in valid_ids:
        writer.writerow([pid])

print("📦 Saved:", OUTPUT)
print("✅ All done!")
