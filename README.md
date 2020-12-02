# Sparkify's Cloud Transformation
## Designing and Deploying a Scalable and Efficient Data Warehouse for a Music Streaming Startup

<img src="https://github.com/Morgan-Sell/song-app-data-warehouse/blob/main/img/music_data.png" width="800" height="250">

# Objective
Sparkify, a **fake** streaming music app that was launched during the COVID-19 pandemic, experienced exponential growth and required a scalable and computationally efficient data analytics solution. As such, the company decided to adopt Amazon Web Services (AWS) and host its database on Redshift.

# Data Warehouse Design
To enhance the efficacy of the ETL process and ensure high data quality, I implemented a **staging area** comprised of two tables that mirror the data sources: (1) metadata of songs/artists available on Sparkify and (2) played song events. The format of both datasets is JSON and are stored in AWS's S3.

The architecture used in this project is commonly referred to as "Kimball's Bus Architecture" named in recognition of Ralph Kimball, one of the godfathers of data warehousing. The principal concept of Bus Architecture is the use of conformed dimensions, meaning a data warehouse structure that can be used by all business units within an enterprise.

Note the naming of "backroom" and "frontroom". The back room is where the data is transformed/process. The end user, i.e. data analyst, does not have access to these tables. On the other hand, a data analyst can directly query from the tables located in the front room. A common analogy is a restaurant's kitchen (backroom) and dining area (frontroom).

![DWH Design](https://github.com/Morgan-Sell/song-app-data-warehouse/blob/main/img/dwh_design.png)
       
The tables and database are stored on AWS Redshift, which also provides a query editor, enabling analytics.

## An Optimized Table Design

As mentioned, Sparkify has experienced extraordinary growth and expects for it to continue. Consequently, I expect the cost of queries to increase significantly. To mitigate this risk, I implemented distribution keys on a couple of the tables.

The distribution key determines how the data is partitioned across the various machines/vCPUs. After gathering business requirements, I was able to determine recurring needs of the data analytics team. The table below lists the respective tables and their corresponding distribution keys.

<p align="center">
    <img src="https://github.com/Morgan-Sell/song-app-data-warehouse/blob/main/img/table_dist_key.png" alt="Dist Key Table" width="350" height="150">
</p>

Based on this structure, the "**users**" will be partitioned into two nodes that correspond with “free” or “paid” membership. Sparkify’s analysts commonly assess these two groups in different manners.

Also, in some tables, I labeled certain attributes as **sorting keys**. Before being allocating to different nodes/vCPUs, the table is sorted by the **sorting key**. Consequently, the rows are organized in contiguous ranges, determined by the sorting key, and partitioned accordingly across the nodes. Applying this design will decrease the query time of some analyses. It will substantially decrease the computational cost when a query uses `ORDER BY`.

<p align="center">
    <img src="https://github.com/Morgan-Sell/song-app-data-warehouse/blob/main/img/table_sort_key.png" alt="Sort Key Table" width="350" height="150">
</p>

# ETL Pipeline
1. Create/resume a Redshift Cluster
2. Execute `create_tables.py` to create connection with the respective database and Redshift cluster.
3. Erase existing staging, dimension and facts tables.
4. Create new staging, dimension, and facts tables.
5. Run `etl.py` to load the data from S3 to staging tables.
6. Exports data from staging tables to facts and dimension tables.
7. Perform analysis using AWS Redshift.



# Packages
- Psycopg2
- ConfigParser