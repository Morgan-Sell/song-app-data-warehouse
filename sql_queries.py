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

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS songplays (
    
    
    
    
    
    
    )
""")

staging_songs_table_create = ("""
    
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (
      songplay_id       SERIAL PRIMARY KEY,
      start_time        TIME FOREIGN KEY NOT NULL,
      user_id           INT FOREIGN KEY NOT NULL,
      level             VARCHAR(10) NOT NULL,
      song_id           VARCHAR(50) FOREIGN KEY NOT NULL,
      artist_id         VARCHAR(50) FOREIGN KEY NOT NULL,
      session_id        VARCHAR(50) FOREIGH KEY NOT NULL,
      location          VARCHAR,
      user_agent        VARCHAR NOT NULL
    )
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (
      user_id          SERIAL PRIMARY KEY,
      first_name       VARCHAR(40) NOT NULL,
      last_name        VARCHAR(40) NOT NULL,
      gender           VARCHAR(1) NOT NULL,
      level            VARCHAR(10) NOT NULL
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs
    (
      song_id         VARCHAR(50) PRIMARY KEY,
      title           VARCHAR NOT NULL,
      artist_id       VARCHAR(50) NOT NULL,
      year            INT NOT NULL,
      duration        NUMERIC NOT NULL
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists
    (
      artist_id     VARCHAR(50) PRIMARY KEY,
      name          VARCHAR NOT NULL,
      location      VARCHAR NOT NULL,
      latitude      FLOAT8,
      longitude     FLOAT8
      )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time
    (
      start_time    TIME PRIMARY KEY,
      hour          INT NOT NULL,
      day           INT NOT NULL,
      week          INT NOT NULL,
      month         INT NOT NULL,
      year          INT NOT NULL,
      weekday       INT NOT NULL
    )
""")

# STAGING TABLES

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
