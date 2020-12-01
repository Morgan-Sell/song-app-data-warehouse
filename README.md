# Sparkify's Data Warehouse Cloud Transformation
## ETL Pipeline Enabling Music Startup to Manage and Analyze Data on AWS

<img src="https://github.com/Morgan-Sell/song-app-data-warehouse/blob/main/img/music_data.png" width="800" height="250">

# Objective
Sparkify, a **fake** streaming music app that was launched during the COVID-19 pandemic, experienced exponential growth and required a scalable and computationally efficient data analytics solution. As such, the company decided to adopt Amazon Web Services (AWS) and host its database on Redshift.

# Data Warehouse Design
To enhance the efficiency of the ETL process and ensure data quality, I implemented a **staging area** comprised of two tables that mirror the data sources: (1) metadata of songs/artists available on Sparkify and (2) played song events. The format of both datasets are JSON and are stored in AWS's S3.

The architecture used in this project is commonly referred to as "Kimball's Bus Architecture" named in recognize of Ralph Kimball, one of the godfathers of data warehousing. The principal concept of Bus Architecture is the use of conformed dimensions meaning a data warehouse structure that can be used by all business units within an enterprise.

Note the naming of "backroom" and "frontroom". The back room is where the data is transformed/process. The end user, i.e. data analyst, does not have access to these tables. On the other hand, a data analyst can directly query from the tables located in the front room. A common analogy is a resturant's kitchen (backroom) and dining area (frontroom).

![DWH Design](https://github.com/Morgan-Sell/song-app-data-warehouse/blob/main/img/dwh_design.png)
    
    
The tables and database are stored on AWS Redshift, which also provides a query editor, enabling analytics.

## Optimize Table Design

As mentioned, Sparkify has experienced extraordinary growth and expects for it to continue. Consequently, I expect the cost of queries to increase significantly. To mitigitate this risk, I implemented distribution keys on a couple of the tables.

The distribution key determines how the data is partitioned across the various machines/vCPUS. The idea is to predict how analysts may group/analyze the data. The table below lists the respective tables and their corresponding distribution keys.


<center><img src="https://github.com/Morgan-Sell/song-app-data-warehouse/blob/main/img/table_dist_key.png" alt="Dist Key Table" width="400" height="225"></center>


Based on this structure, the "**users**" we will be partitioned into two nodes that correspond with a free or premium membership. It is common for Sparkify's analysts to apply different methods when analyzing these two groups.


# ETL Pipeline
1. Execute `create_tables.py` to create connection with the provided Redshift cluster.
2, Erase existing staging, dimension and facts tables and create new ones of each table.
2. Run `etl.py` 
3. 
