# Project-05-Data-Collection-Storage-Foundation
# A. Documenting GCS Setup
* Bucket name: project5a
* Location: us-east1 (South Carolina)
* Storage class: Standard
* Public access: Not public
* Protection: Soft Delete enabled
* Encryption: Google-managed encryption keys
* Inside the bucket, I create a raw_data folder with this structure:

```text
project5a/                           # GCS Bucket Name
└── raw_data/                        # Folder for raw data storage
    ├── IP-COUNTRY-REGION-CITY.BIN   # IP Geolocation Database (Binary)
    └── glamira_ubl_oct2019_nov2019.tar.gz  # Raw data archive file (October-November 2019)
```

## B. Google Cloud VM Setup
* Instance name	prj5vm
* Zone:	us-central1-a
* Machine type: e2-micro (2 vCPUs, 1 GB RAM)
* OS Image:	ubuntu-2204-jammy-v20251111
* Boot disk: 50 GB, Balanced Persistent Disk
* Additional disk: newdisk – 50 GB, Balanced Persistent Disk

## C. MongoDB Installation & Configuration
MongoDB Community Edition 8.0 was installed following the official guide:

Reference:
https://www.mongodb.com/docs/v8.0/tutorial/install-mongodb-on-ubuntu/

* Import the public key.
<pre>
  sudo apt-get install gnupg curl
</pre>
<pre>
  curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
   --dearmor
</pre>
* Create the list file (Ubuntu 22.04(Jammy))
<pre>
  echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
</pre>
* Install MongoDB
<pre>
sudo systemctl start mongod
sudo systemctl enable mongod
</pre>
* Start & Enable the Service
<pre>
sudo systemctl start mongod
sudo systemctl enable mongod
</pre>
* Verify MongoDB Installation
<pre>
sudo systemctl status mongod
mongosh
</pre>
## 
