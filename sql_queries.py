import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

LOG_DATA       = config.get("S3","LOG_DATA")
SONG_DATA      = config.get("S3","SONG_DATA")
ARN            = config.get("IAM_ROLE","ARN")
LOG_JSONPATH   = config.get("S3","LOG_JSONPATH")
# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events(
        event_id INT IDENTITY(0,1) PRIMARY KEY
        ,artist  VARCHAR(255)  
        ,auth VARCHAR(255)  
        ,firstName VARCHAR(255)  
        ,gender VARCHAR(1)  
        ,itemInSession INT  
        ,lastName VARCHAR(255)  
        ,length DOUBLE PRECISION
        ,level VARCHAR(255)  
        ,location VARCHAR(255)  
        ,method VARCHAR(10)  
        ,page VARCHAR(255)  
        ,registration VARCHAR(255)  
        ,session_id BIGINT NOT NULL
        ,song VARCHAR(255)  
        ,status INT  
        ,ts BIGINT NOT NULL 
        ,userAgent TEXT
        ,userId INT  
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs(
         num_songs INT NOT NULL
        ,artist_id VARCHAR(255) NOT NULL
        ,artist_latitude DOUBLE PRECISION
        ,artist_longitude DOUBLE PRECISION 
        ,artist_location  VARCHAR(255) NULL
        ,artist_name VARCHAR(255) NOT NULL
        ,song_id VARCHAR(255) NOT NULL
        ,duration  DOUBLE PRECISION
        ,title VARCHAR(255) NOT NULL
        ,year INT NOT NULL
        ,PRIMARY KEY (song_id)
    );  
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays 
    ( 
        songplay_id INT IDENTITY(0,1) PRIMARY KEY
        ,start_time BIGINT NOT NULL
        ,user_id INT NULL
        ,level VARCHAR(255) NOT NULL
        ,song_id VARCHAR(255) NULL
        ,artist_id VARCHAR(255) NULL
        ,session_id INT NOT NULL
        ,location VARCHAR(255)
        ,user_agent VARCHAR(255)
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users 
    ( 
         user_id INT NOT NULL PRIMARY KEY
        ,first_name VARCHAR(255)  NULL
        ,last_name VARCHAR(255)  NULL
        ,gender VARCHAR(255) NOT NULL
        ,level VARCHAR(255) NOT NULL
    );

""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs 
    ( 
         song_id VARCHAR(255) PRIMARY KEY
        ,title VARCHAR(255) NOT NULL
        ,artist_id VARCHAR(255) NOT NULL
        ,year INT NOT NULL
        ,duration DOUBLE PRECISION
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists 
    ( 
         artist_id VARCHAR(255) PRIMARY KEY
        ,name VARCHAR(255) NOT NULL
        ,location VARCHAR(255) NULL
        ,latitude DOUBLE PRECISION
        ,longitude DOUBLE PRECISION
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time 
    ( 
         start_time BIGINT PRIMARY KEY
        ,hour INT NOT NULL
        ,day INT NOT NULL
        ,week INT NOT NULL
        ,month INT NOT NULL
        ,year INT NOT NULL
        ,weekday INT NOT NULL
    );
""")

# STAGING TABLES
staging_events_copy = ("""
    copy {} from {}
    credentials 'aws_iam_role={}'
    region 'us-west-2'
    COMPUPDATE OFF STATUPDATE OFF
 	JSON {};
""").format('staging_events',LOG_DATA,ARN,LOG_JSONPATH)

staging_songs_copy = ("""
    copy {} from {}
    credentials 'aws_iam_role={}'
    region 'us-west-2'
    COMPUPDATE OFF STATUPDATE OFF
 	JSON 'auto';
""").format('staging_songs',SONG_DATA,ARN)

# FINAL TABLES
songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
    SELECT DISTINCT e.ts, e.userId, e.level, s.song_id, s.artist_id, e.session_id, e.location, e.userAgent
    FROM staging_events e LEFT JOIN staging_songs s ON s.artist_name = e.artist  and e.song = s.title and e.length = s.duration
""")

user_table_insert = ("""
    INSERT INTO users 
    SELECT DISTINCT userId, firstName, lastName, gender, level
    FROM staging_events
    WHERE userId is not NULL;
""")

song_table_insert = ("""
    INSERT INTO songs 
    SELECT song_id, title, artist_id, year, duration
    FROM staging_songs;
""")

artist_table_insert = ("""
    INSERT INTO artists 
    SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    FROM staging_songs;
""")

time_table_insert = ("""
    INSERT INTO time 
    SELECT DISTINCT ts
        ,extract(h from TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' ) as hr
        ,extract(day from TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' ) as dy
        ,extract(week from TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' ) as wk 
        ,extract(month from TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' ) as mt 
        ,extract(year from TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' ) as yr
        ,extract(DOW from TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' ) as wkd
    FROM staging_events
""")

# QUERY LISTS
create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [ staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
