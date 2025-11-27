# Project-05-Data-Collection-Storage-Foundation
## 1. Local environment requirements:
* Visual Studio Code editor.
* Python 3.11.
* Python library: ip2location, requests, BeautifulSoup, pandas, time, concurrent.futures, pymongo, tqdm, csv, os

## 2. Folder structure:  
<pre>
PROJECT-05-DATA-COLLECTION-STORAGE
│
├── csv files result/
│   └── product_filtered_outputs/
│       ├── part1_main_collections.csv # Retrieve product_id (or viewing_product_id if product_id is missing) and current_url
│       ├── product_names.csv # Crawl the product name based on the above information; get only one active product name for each distinct product_id
│       ├── product_view_all_recommend_clicked.csv # Retrieve viewing_product_id and referrer_url
│       └── ip_location_results.csv # IP Location Processing 
│
│
└── src/
    ├── crawl_data.py # Step 6: Product name collection
    ├── ip_location.py # Step 5: IP Location Processing
    └── retrieve_data.py # Step 6: Product name collection


</pre>

## 3. Documenting GCS Setup
* Bucket name: project5a
* Location: us-east1 (South Carolina)
* Storage class: Standard
* Public access: Not public
* Protection: Soft Delete enabled
* Encryption: Google-managed encryption keys
* Inside the bucket, I create a raw_data folder with this structure:
<pre>
project5a/                           # GCS Bucket Name
└── raw_data/                        # Folder for raw data storage
    ├── IP-COUNTRY-REGION-CITY.BIN   # IP Geolocation Database (Binary)
    └── glamira_ubl_oct2019_nov2019.tar.gz  # Raw data archive file (October-November 2019)
</pre>

## 4. Google Cloud VM Setup
* Instance name: project5vm
* Zone:	us-central1-a
* Machine type: e2-standard-2 (2 vCPUs, 8 GB Memory)
* OS Image:	ubuntu-2204-jammy-v20251111
* Boot disk: 70 GB, Balanced Persistent Disk

## 5. MongoDB Installation & Configuration
MongoDB Community Edition 8.0 was installed following the official guide:

Reference:
https://www.mongodb.com/docs/v8.0/tutorial/install-mongodb-on-ubuntu/

* Import the public key.
```text
  sudo apt-get install gnupg curl
```
```text
  curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
   --dearmor
```
* Create the list file (Ubuntu 22.04(Jammy))
```text
  echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
```
* Install MongoDB
```text
sudo systemctl start mongod
sudo systemctl enable mongod
```
* Start & Enable the Service
```text
sudo systemctl start mongod
sudo systemctl enable mongod
```
* Verify MongoDB Installation
```text
sudo systemctl status mongod
mongosh
```
## 6. Initial Data Loading
* SSH into your VM on GCP and download data from GCS
```text
    gsutil cp gs://project5a/raw_data/glamira_ubl_oct2019_nov2019.tar.gz ~/
```
* Check file exists
```text
    ls -lh ~/
```
* Extract the dataset
```text
    tar -xvzf glamira_ubl_oct2019_nov2019.tar.gz
```
* This will produce something like:
```text
    ~/glamira_ubl_oct2019_nov2019/dump/countly/
```
Inside, you should see .bson and .json
* Restore the MongoDB dump
Make sure MongoDB is running:
```text
    sudo systemctl start mongod
```
Run restore:
```text
    mongorestore --db glamira_db ~/glamira_ubl_oct2019_nov2019/dump/countly
```
* Validate import
```text
    mongosh
```
Check DB + collections
```text
    use countly
    show collections
```

