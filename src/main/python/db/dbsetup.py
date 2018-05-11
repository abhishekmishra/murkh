import sqlite3
import os

# copied from rssjanadb-schema.sql
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS FEED (
    ID INTEGER NOT NULL PRIMARY KEY,
    NAME TEXT NOT NULL,
    URL TEXT NOT NULL UNIQUE,
    ADDED_DATE NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS ENTRY (
    ID INTEGER NOT NULL PRIMARY KEY,
    ITEM_ID TEXT NOT NULL,
    PERMALINK TEXT NOT NULL,
    ADDED_DATE NUMERIC NOT NULL,
    PUBLISHED_DATE NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS FEED_ENTRY (
    FEED_ID INTEGER NOT NULL,
    ENTRY_ID INTEGER NOT NULL,
    FOREIGN KEY (FEED_ID) REFERENCES FEED(ID),
    FOREIGN KEY (ENTRY_ID) REFERENCES ENTRY(ID),
    PRIMARY KEY (FEED_ID, ENTRY_ID)
);

CREATE TABLE IF NOT EXISTS FEED_STATUS (
    FEED_ID INTEGER NOT NULL PRIMARY KEY,
    ALL_READ INTEGER NOT NULL,
    LAST_MODIFIED NUMERIC NOT NULL,
    LAST_CHECKED NUMERIC NOT NULL,
    FOREIGN KEY (FEED_ID) REFERENCES FEED(ID)
);

CREATE TABLE IF NOT EXISTS ENTRY_STATUS (
    ENTRY_ID INTEGER NOT NULL PRIMARY KEY,
    READ INTEGER NOT NULL,
    RATING INTEGER NOT NULL,
    JUNK INTEGER NOT NULL,
    AD INTEGER NOT NULL,
    CLICKBAIT INTEGER NOT NULL,
    FOREIGN KEY (ENTRY_ID) REFERENCES ENTRY(ID)
);

CREATE TABLE IF NOT EXISTS CATEGORY (
    ID INTEGER NOT NULL PRIMARY KEY,
    NAME TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS CATEGORY_FEED (
    CATEGORY_ID INTEGER NOT NULL,
    FEED_ID INTEGER NOT NULL,
    FOREIGN KEY (CATEGORY_ID) REFERENCES CATEGORY(ID),
    FOREIGN KEY (FEED_ID) REFERENCES FEED(ID),
    PRIMARY KEY (CATEGORY_ID, FEED_ID)
);
"""


def main(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    stmts = SCHEMA_SQL.split(';')
    for stmt in stmts:
        c.execute(stmt)
        conn.commit()
    conn.close()


if __name__ == "__main__":
    murkhdb = os.path.join(os.environ['HOME'], ".murkh/murkh.db")
    main(murkhdb)
