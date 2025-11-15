Duration: 2 weeks
Goal: Build a cloud-based data foundation using GCP, MongoDB, and Python for event log processing, IP geolocation, and product name mapping.


# A. Documenting GCS Setup
* Bucket name: project5a
* Location: us-east1 (South Carolina)
* Storage class: Standard
* Public access: Not public
* Protection: Soft Delete enabled
* Encryption: Google-managed encryption keys
* Inside the bucket, I create a raw_data folder with this structure:

project5a/
└── raw_data/
       ├── IP-COUNTRY-REGION-CITY.BIN
       └── glamira_ubl_oct2019_nov2019.tar.gz


## B. Google Cloud VM Setup
* Instance name	prj5vm
* Zone:	us-central1-a
* Machine type: e2-micro (2 vCPUs, 1 GB RAM)
* OS Image:	ubuntu-2204-jammy-v20251111
* Boot disk:	50 GB, Balanced Persistent Disk
* Additional disk	newdisk – 50 GB, Balanced Persistent Disk

## 
