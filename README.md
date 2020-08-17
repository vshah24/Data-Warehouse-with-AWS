# Data Warehouse Project with S3 and Redshift

## Overview
A startup **Sparkify** (music streaming company) has grown their user base and song database and want to move their processes and data from on-premise onto cloud. In this project we will use two Amazon web services `S3 (data storage)` and `Redshift (data warehouse)`.

As a data engineer we will build an ETL pipeline that extracts data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to analyze and understand the user behaviour. 

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
  1. **song_data/ and log_data/** - contains song and log files on user activity in json format.
  2. **sql_queries.py** - Contains sql queries that has a creation,insertion and dropping templates of fact and dimension tables.
  3. **create_tables.py** - creates fact and dimension tables in Redshift.
  5. **etl.py** - Defines the ETL pipeline, which extracts the json data from s3 , processes it and loads them to Redshift.
  
