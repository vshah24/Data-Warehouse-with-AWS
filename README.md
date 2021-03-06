This project is part  [Udacity's - Data Engineering Nanodegree ](https://www.udacity.com/course/data-engineer-nanodegree--nd027)

# Data Warehouse Project with Amazon S3 and Redshift-

## Overview
A startup **Sparkify** (music streaming company) has grown their user base and song database and want to move their processes and data from on-premise onto cloud. In this project we will use two Amazon web services `S3 (data storage)` and `Redshift (data warehouse)`.

As a data engineer we will build an ETL pipeline(Extract, Transform, Load) to create Database and tables in AWS Redshift Cluster.
* **Extract** - We will extract data format from Amazon s3 bucket.
* **Transform** - We will perform data transformation as set of dimensional and fact tables.
* **Load** - We will load the transformed data to AWS Redshift DB

The analytics team can now use the tables loaded on AWS Redshift DB to analyze the user behaviour, making it easier for them as they don't have to deal with multiple json files.


## Technologies Used 
  Python, SQL, AWS S3 and AWS Redshift DB.


## Dataset
The data is in Amazon s3 bucket located at `s3://udacity-dend/log_data` and `s3://udacity-dend/song_data` containing log data and songs data respectively.



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
  1. **dwh.cfg** - It stores Amazon Redshift Clusters credentials that gives access to launch a redshift cluster and IAM role that has read access to s3.
  2. **sql_queries.py** - It stores sql statements (create, drop, insert) in String format. It also has a copy statement that extracts data from s3 and loads to staging tables.
  3. **create_tables.py** - creates/drop fact and dimension tables in Redshift.
  4. **etl.py** - Defines the ETL pipeline, which extracts the json data from s3 , processes it and loads them to Redshift.
 

  
  
## How to run the project

1. Create an **IAM role** and attach the **AmazonS3ReadOnlyAccess** Policy to this IAM. 
2. Create a **dc2.large Redshift Cluster** with 4 nodes.
3. Enter all the **credentials** of your cluster and IAM role in **dwh.cfg file**.
4. Run **sql_queries.py**.
5. Run **create_tables.py**
      * Check the table schemas in your redshift database. You can use Query Editor in the AWS Redshift console for this.
6. Run **etl.py** (ETL Process)
      * The data is loaded in the tables inside your redshift database.You can use Query Editor in the AWS Redshift console for this.
7. **Delete** the redshift **cluster** when finished so we don't pay for it unecessarily.

