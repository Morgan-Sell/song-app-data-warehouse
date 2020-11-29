import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

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
        gender            VARCHAR(1),
        itemInSession     INT,
        lastName          VARCHAR(50),
        length            FLOAT8,
        level             VARCHAR(10),
        location          VARCHAR(50),
        method            VARCHAR(10),
        page              VARCHAR(25),
        registration      VARCHAR(50),
        sessionId         INT,
        song              VARCHAR,
        status            INT,
        ts                NUMERIC,
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
        song_id           VARCHAR(50),
        title             VARCHAR,
        duration          FLOAT8,
        year              INT
    );   
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id       INT IDENTITY(0,1),
        start_time        NUMERIC NOT NULL SORTKEY,
        user_id           INT NOT NULL SORTKEY,
        level             VARCHAR(10) NOT NULL DISTKEY,
        song_id           VARCHAR(50) NOT NULL SORTKEY,
        artist_id         VARCHAR(50) NOT NULL SORTKEY,
        session_id        VARCHAR(50) NOT NULL SORTKEY,
        location          VARCHAR DISTKEY,
        user_agent        VARCHAR NOT NULL
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id          INT IDENTITY(0,1) SORTKEY,
        first_name       VARCHAR(40) NOT NULL,
        last_name        VARCHAR(40) NOT NULL,
        gender           VARCHAR(1) NOT NULL,
        level            VARCHAR(10) NOT NULL DISTKEY
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id         VARCHAR(50) SORTKEY,
        title           VARCHAR NOT NULL,
        artist_id       VARCHAR(50) NOT NULL DISTKEY,
        year            INT NOT NULL,
        duration        NUMERIC NOT NULL
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id     VARCHAR(50) SORTKEY,
        name          VARCHAR NOT NULL,
        location      VARCHAR NOT NULL,
        latitude      FLOAT8,
        longitude     FLOAT8
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time    NUMERIC SORTKEY,
        hour          INT NOT NULL,
        day           INT NOT NULL,
        week          INT NOT NULL,
        month         INT NOT NULL DISTKEY,
        year          INT NOT NULL DISTKEY,
        weekday       INT NOT NULL DISTKEY
    );
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM {}
    CREDENTIALS 'aws_iam_role={}'
    GZIP DELIMITER ';' COMPUPDATE OFF REGION 'us-west-2';
""").format(LOG_DATA, ARN)

staging_songs_copy = ("""
    COPY staging_songs FROM {}
    CREDENTIALS 'aws_iam_role={}'
    GZIP DELIMITER ';' COMPUPDATE OFF REGION 'us-west-2';
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays
    (
      songplay_id,
      start_time,
      user_id,
      level,
      song_id,
      artist_id,
      session_id,
      location,
      user_agent
    )
    VALUES (%s, TO_TIMESTAMP(%s), %s, 
      %s, %s, %s, %s, %s, %s)
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
    )
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
    )
    VALUES(%s, %s, %s, %s, %s)
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
    )
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
    )
     VALUES (TO_TIMESTAMP(%s), %s, %s, %s,
       %s, %s, %s);
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
