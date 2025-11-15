import csv
from pymongo import MongoClient
import IP2Location
from tqdm import tqdm

# ============================
# CONFIG
# ============================
MONGO_URI = "mongodb://34.27.109.23:27017/"
DB_NAME = "countly"
MAIN_COLLECTION = "summary"
OUTPUT_COLLECTION = "ip_location_results"
OUTPUT_CSV = "ip_location_results.csv"

BIN_FILE = "D:\python try hard\project5\dataset\IP-COUNTRY-REGION-CITY.BIN"
BATCH_SIZE = 50000  # process 50k IPs at once

# ============================
# MAIN LOGIC
# ============================

def process_ip_locations():
    print("🔌 Connecting to MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    col = db[MAIN_COLLECTION]
    out_col = db[OUTPUT_COLLECTION]

    print("📥 Fetching unique IPs from MongoDB...")
    unique_ips = col.distinct("ip")
    print(f"✅ Found {len(unique_ips):,} unique IPs")

    ip2 = IP2Location.IP2Location(BIN_FILE)

    # Prepare CSV
    csv_file = open(OUTPUT_CSV, "w", newline="", encoding="utf-8")
    writer = csv.writer(csv_file)
    writer.writerow(["ip", "country", "region", "city"])

    print("🚀 Processing IP locations...")

    batch = []
    for ip in tqdm(unique_ips):
        try:
            rec = ip2.get_all(ip)
            data = {
                "ip": ip,
                "country": rec.country_long,
                "region": rec.region,
                "city": rec.city
            }
            batch.append(data)
            writer.writerow([ip, rec.country_long, rec.region, rec.city])

            # batch insert
            if len(batch) >= BATCH_SIZE:
                out_col.insert_many(batch)
                batch = []

        except Exception:
            continue

    # Insert last batch
    if batch:
        out_col.insert_many(batch)

    csv_file.close()
    print("🎉 DONE! Results saved to CSV + MongoDB collection.")


if __name__ == "__main__":
    process_ip_locations()
