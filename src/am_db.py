import sqlite3


# Connects to the database and sets up a cursor.
db_conn = sqlite3.connect("automoji.db")
db_cur = db_conn.cursor()

# Creates tables for the Quotes cog, if they don't exist already.
db_cur.execute(
    "SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND (name='quote_channels' OR name='quotes');"
)
if db_cur.fetchone()[0] != 2:
    db_cur.execute(
        "CREATE TABLE quote_channels (guild INTEGER PRIMARY KEY NOT NULL, channel INTEGER);"
    )
    db_cur.execute(
        "CREATE TABLE quotes (guild INTEGER NOT NULL, quote TEXT NOT NULL, FOREIGN KEY (guild) REFERENCES quote_channels(guild) ON DELETE CASCADE);"
    )

# Creates a table for the User Emojis cog, if it doesn't exist already.
db_cur.execute(
    "SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='emojis';"
)
if db_cur.fetchone()[0] != 1:
    db_cur.execute(
        "CREATE TABLE emojis (guild INTEGER NOT NULL, user INTEGER NOT NULL, emoji TEXT, PRIMARY KEY (guild, user));"
    )

db_conn.commit()
