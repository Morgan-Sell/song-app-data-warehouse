import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

DWH_IAM_ROLE_NAME = config.get("IAM_ROLE", "ARN")
DWH_LOG_DATA = config.get("S3", "LOG_DATA")
DWH_SONG_DATA = config.get("S3", "SONG_DATA")
DWH_LOG_JSONPATH = config.get("S3", "LOG_JSONPATH")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
# Staging stables are in S3.

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events (
        artist            VARCHAR,
        auth              VARCHAR,
        firstName         VARCHAR,
        gender            VARCHAR,
        itemInSession     INT,
        lastName          VARCHAR,
        length            FLOAT8,
        level             VARCHAR,
        location          VARCHAR,
        method            VARCHAR,
        page              VARCHAR,
        registration      VARCHAR,
        sessionId         INT,
        song              VARCHAR,
        status            INT,
        ts                BIGINT,
        userAgent         VARCHAR,
        userId            INT    
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs         INT,
        artist_id         VARCHAR,
        artist_latitude   FLOAT8,
        artist_longitude  FLOAT8,
        artist_location   VARCHAR,
        artist_name       VARCHAR, 
        song_id           VARCHAR,
        title             VARCHAR,
        duration          FLOAT8,
        year              INT
    );   
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id       INT IDENTITY(0,1),
        start_time        TIMESTAMP NOT NULL SORTKEY,
        user_id           INT NOT NULL,
        level             VARCHAR NOT NULL DISTKEY,
        song_id           VARCHAR NOT NULL,
        artist_id         VARCHAR NOT NULL,
        session_id        VARCHAR NOT NULL,
        location          VARCHAR,
        user_agent        VARCHAR NOT NULL
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id          INT IDENTITY(0,1) SORTKEY,
        first_name       VARCHAR NOT NULL,
        last_name        VARCHAR NOT NULL,
        gender           VARCHAR NOT NULL,
        level            VARCHAR NOT NULL DISTKEY
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id         VARCHAR SORTKEY,
        title           VARCHAR NOT NULL,
        artist_id       VARCHAR NOT NULL DISTKEY,
        year            INT NOT NULL,
        duration        NUMERIC NOT NULL
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id     VARCHAR SORTKEY,
        name          VARCHAR NOT NULL,
        location      VARCHAR NOT NULL,
        latitude      FLOAT8,
        longitude     FLOAT8
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time    TIMESTAMP SORTKEY,
        hour          INT NOT NULL,
        day           INT NOT NULL,
        week          INT NOT NULL,
        month         INT NOT NULL,
        year          INT NOT NULL DISTKEY,
        weekday       INT NOT NULL
    );
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM {}
    CREDENTIALS 'aws_iam_role={}'
    JSON {} 
    COMPUPDATE OFF REGION 'us-west-2';
""").format(DWH_LOG_DATA, DWH_IAM_ROLE_NAME, DWH_LOG_JSONPATH)

staging_songs_copy = ("""
    COPY staging_songs FROM {}
    CREDENTIALS 'aws_iam_role={}'
    JSON 'auto'
    COMPUPDATE OFF REGION 'us-west-2';
""").format(DWH_SONG_DATA, DWH_IAM_ROLE_NAME)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (
        songplay_id,
        start_time,
        user_id,
        level,
        song_id,
        artist_id,
        session_id,
        location,
        user_agent
    ) \
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT(songplay_id) DO NOTHING;
""")

user_table_insert = ("""
    INSERT INTO users
    (
      user_id,
      first_name,
      last_name,
      gender,
      level
    ) \
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT(user_id) DO UPDATE SET level=EXCLUDED.level;
""")

song_table_insert = ("""
    INSERT INTO songs
    (
      song_id,
      title,
      artist_id,
      year,
      duration
    ) \
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT(song_id) DO NOTHING;
""")

artist_table_insert = ("""
    INSERT INTO artists
    (
      artist_id,
      name,
      location,
      latitude,
      longitude
    ) \
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT(artist_id) DO NOTHING;
""")

time_table_insert = ("""
    INSERT INTO time
    (
      start_time,
      hour,
      day,
      week,
      month,
      year,
      weekday
    ) \
    VALUES (%s, %s, %s, %s, %s, %s, %s);
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
