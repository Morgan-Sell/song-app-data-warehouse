# Sparkify's Data Warehouse Cloud Tranformation
## ETL Pipeline Enabling Music Startup to Manage and Analyze Data on AWS

<img src="https://github.com/Morgan-Sell/song-app-data-warehouse/img/music_data.png" width="800" weight="200">

# Objective
Sparkify, a **fake** streaming music app that was launched during the COVID-19 pandemic, experienced exponential growth and required a scalable and computationally efficient data analytics solution. As such, the company decided to adopt Amazon Web Services (AWS) and host its database on Redshift.

# Data Warehouse Design
To enhance the efficiency of the ETL process and ensure data quality, I implemented a **staging area** comprised of two tables that mirror the data sources: (1) metadata of songs/artists available on Sparkity and (2) played song events. The format of both datasets are JSON.



