import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_event"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
#songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
staging_events_table_create= ("""create table if not exists staging_event
                                (artist VARCHAR(120),
                                 auth VARCHAR(20),
                                 firstName  VARCHAR(20),
                                 gender char(1),
                                 itemInSession Integer,
                                 lastName VARCHAR(20),
                                 length NUMERIC,
                                 level VARCHAR(10),
                                 location  VARCHAR(120),
                                 method  VARCHAR(20),
                                 page  VARCHAR(20),
                                 registration  VARCHAR(20),
                                 sessionId  INTEGER,
                                 song  VARCHAR(250),
                                 status  VARCHAR(20),
                                 ts  VARCHAR(20),
                                 userAgent  VARCHAR(400),
                                 userId  VARCHAR(20)
                                );
""")

staging_songs_table_create = ("""create table if not exists staging_songs
                               (
                                num_songs INTEGER,
                                artist_id VARCHAR(20),
                                artist_latitude VARCHAR,
                                artist_longitude VARCHAR,
                                artist_location VARCHAR,
                                artist_name VARCHAR,
                                song_id VARCHAR,
                                title VARCHAR,
                                duration NUMERIC,
                                year INTEGER
                                );
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays 
                            (
                            songplay_id bigint identity(1,1) primary key,
                            starttime timestamp,
                            user_id varchar(20),
                            level varchar(20), 
                            song_id varchar(20), 
                            artist_id varchar(20), 
                            session_id integer, 
                            location varchar, 
                            user_agent varchar,
                            FOREIGN KEY (user_id) references users(user_id),
                            FOREIGN KEY (song_id) references songs(song_id),
                            FOREIGN KEY (artist_id) references artists(artist_id),
                            FOREIGN KEY (starttime) references time(start_time)
                            );
""")


user_table_create = ("""Create table if not exists users
                        (
                        user_id varchar(20) primary key sortkey, 
                        first_name varchar, 
                        last_name varchar, 
                        gender varchar(20), 
                        level varchar(20)
                        )
                        diststyle all;
                    """)


song_table_create = ("""Create table if not exists songs 
                        (
                        song_id varchar(20) primary key sortkey distkey, 
                        title varchar not null, 
                        artist_id varchar(20) not null, 
                        year integer, 
                        duration float
                        )
                        ;
                    """)



artist_table_create = ("""Create table if not exists artists 
                        (
                        artist_id varchar(20) primary key sortkey, 
                        name varchar not null, 
                        location varchar, 
                        latitude varchar, 
                        longitude varchar
                        )
                        diststyle all;
                    """)


time_table_create = ("""Create table if not exists time 
                        (
                        start_time timestamp primary key sortkey,
                        hour varchar(20), 
                        day varchar(20), 
                        week varchar(20), 
                        month varchar(20), 
                        year varchar(20) , 
                        weekday varchar(20)
                        ) diststyle all;
                    """)


# STAGING TABLES

staging_events_copy = (""" 
                        copy staging_event 
                        from {}
                        credentials 'aws_iam_role={}'
                        JSON {}
                        COMPUPDATE OFF
                        region 'us-west-2'; 
""").format(config.get("S3","LOG_DATA"),config.get("IAM_ROLE","ARN"),config.get("S3","LOG_JSONPATH"))


staging_songs_copy = ("""
                        copy staging_songs
                        from {} 
                        credentials 'aws_iam_role={}'
                        JSON 'auto' 
                        COMPUPDATE OFF
                        region 'us-west-2';
""").format(config.get("S3","SONG_DATA"),config.get("IAM_ROLE","ARN"))

# FINAL TABLES

songplay_table_insert = ("""
                            INSERT INTO songplays(starttime, user_id, level, song_id, artist_id, session_id, location, user_agent)
                            SELECT 
                                TIMESTAMP 'epoch' + a.ts/1000 *INTERVAL '1 second',
                                a.userid,
                                a.level,
                                b.song_id,
                                b.artist_id,
                                a.sessionid,
                                a.location,
                                a.useragent 
                            FROM 
                            staging_event as a LEFT JOIN staging_songs as b 
                            ON 
                            a.artist=b.artist_name and a.length=b.duration and a.song=b.title
                            WHERE 
                            a.Page='NextSong'
""")

user_table_insert = ("""
                        INSERT INTO users
                        (
                        SELECT
                            userId as user_id,
                            firstName as first_name,
                            lastName as last_name,
                            gender,
                            level
                        FROM 
                            staging_event
                        )
""")

song_table_insert = ("""
                        INSERT INTO songs
                        (
                        SELECT 
                            song_id,
                            title,
                            artist_id,
                            year,
                            duration
                        FROM
                            staging_songs
                        )
""")

artist_table_insert = ("""
                        INSERT INTO artists
                        (
                        SELECT
                            artist_id,
                            artist_name as name,
                            artist_location as location,
                            artist_latitude as latitude,
                            artist_longitude as longitude
                        FROM 
                            staging_songs
                        )
""")

time_table_insert = ("""
                    INSERT INTO time 
                    (SELECT 
                            TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' as start_time,
                            DATE_PART(HOUR,TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second') as Hour,
                            DATE_PART(Day,TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second') as Day,
                            DATE_PART(Week,TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second') as Week,
                            DATE_PART(Month,TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second') as Month,
                            DATE_PART(Year,TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second') as Years,
                            DATE_PART(Weekday,TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second') as Weekday
                    FROM 
                            staging_event    
                        )
""")


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create,songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
