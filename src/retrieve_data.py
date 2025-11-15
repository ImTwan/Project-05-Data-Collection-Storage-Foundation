from pymongo import MongoClient
import csv
import os

MONGO_URL = "mongodb://104.197.232.152:27017/"
DB_NAME = "countly"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
summary_col = db["summary"]

OUTPUT_FOLDER = "product_filtered_outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -------------------------
# Part 1: 6 collections → one CSV
# -------------------------
part1_types = [
    "view_product_detail",
    "select_product_option",
    "select_product_option_quality",
    "add_to_cart_action",
    "product_detail_recommendation_visible",
    "product_detail_recommendation_noticed"
]

output_file_part1 = os.path.join(OUTPUT_FOLDER, "part1_main_collections.csv")
with open(output_file_part1, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["product_id", "viewing_product_id", "current_url"])

    cursor = summary_col.find({"collection": {"$in": part1_types}},
                              {"product_id": 1, "viewing_product_id": 1, "current_url": 1})

    for doc in cursor:
        product_id = doc.get("product_id")
        viewing_product_id = doc.get("viewing_product_id")
        current_url = doc.get("current_url")
        writer.writerow([product_id, viewing_product_id, current_url])

print(f"Saved → {output_file_part1}")

# -------------------------
# Part 2: product_view_all_recommend_clicked → separate CSV
# -------------------------
output_file_part2 = os.path.join(OUTPUT_FOLDER, "product_view_all_recommend_clicked.csv")
with open(output_file_part2, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["viewing_product_id", "referrer_url"])

    cursor = summary_col.find({"collection": "product_view_all_recommend_clicked"},
                              {"viewing_product_id": 1, "referrer_url": 1})

    for doc in cursor:
        viewing_product_id = doc.get("viewing_product_id")
        referrer_url = doc.get("referrer_url")
        writer.writerow([viewing_product_id, referrer_url])

print(f"Saved → {output_file_part2}")

print("\n🎉 DONE — CSVs created successfully from summary collection!")
