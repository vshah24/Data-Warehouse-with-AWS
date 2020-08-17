# Data Warehouse Project with S3 and Redshift

## Overview
A startup **Sparkify** (music streaming company) has grown their user base and song database and want to move their processes and data from on-premise onto cloud. In this project we will use two Amazon web services `S3 (data storage)` and `Redshift (data warehouse)`.

As a data engineer we will build an ETL pipeline that extracts data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to analyze the user behaviour. 

## Data
The data is on Amazon s3 bucket located at `s3://udacity-dend/log_data` and `s3://udacity-dend/song_data` containing log data and songs data respectively.



## Database Schema - 
#### Fact Tables
1. **Songplays** - records in log data associated with song plays i.e. records with page `Next Song`
  
  ```songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent```

#### Dimension Tables
2. **users** - users in the app

    ```user_id, first_name, last_name, gender, level```
    
3. **songs** - songs in music database

    ```song_id, title, artist_id, year, duration```
    
4. **artists** - artists in music database

   ``` artist_id, name, location, latitude, longitude```
 
5. **time** - timestamps of records in songplays broken down into specific units

    ```start_time, hour, day, week, month, year, weekday```
    
    
## Project Files
  1. **dwh.cfg** - It stores Amazon Redshift Clusters credentials and IAM role to access the cluster.
  2. **sql_queries.py** - .
  3. **create_tables.py** - creates fact and dimension tables in Redshift.
  4. **etl.py** - Defines the ETL pipeline, which extracts the json data from s3 , processes it and loads them to Redshift.
  
  
## Project Steps
Below are steps you can follow to complete each component of this project.

1. Create Table Schemas
  * Design schemas for your fact and dimension tables
  * Write a SQL CREATE statement for each of these tables in sql_queries.py
  * Complete the logic in create_tables.py to connect to the database and create these tables
  * Write SQL DROP statements to drop tables in the beginning of create_tables.py if the tables already exist. This way, you can run create_tables.py whenever you want to reset your database and test your ETL pipeline.
  * Launch a redshift cluster and create an IAM role that has read access to S3.
  * Add redshift database and IAM role info to dwh.cfg.
  * Test by running create_tables.py and checking the table schemas in your redshift database. You can use Query Editor in the AWS Redshift console for this.
  
2. Build ETL Pipeline
  * Implement the logic in etl.py to load data from S3 to staging tables on Redshift.
  * Implement the logic in etl.py to load data from staging tables to analytics tables on Redshift.
  * Test by running etl.py after running create_tables.py and running the analytic queries on your Redshift database to compare your results with the expected results.
  * Delete your redshift cluster when finished.
   
