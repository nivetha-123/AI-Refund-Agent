#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:55:19 2026

@author: nivetha
"""

# import sqlite3
# import os

# DB_PATH = os.getenv("DB_PATH", "/app/data/crm.db")


# def init_db():
#     # if os.path.exists(DB_PATH):
#     #     print("Database already exists")
#     #     return
#     os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
#     conn = sqlite3.connect(DB_PATH)

#     # seed_path = os.path.join(os.path.dirname(__file__), "../../data/seed.sql")
#     # seed_path = os.path.abspath(seed_path)
#     BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#     seed_path = os.path.join(BASE_DIR, "data", "seed.sql")
#     print(seed_path,'seed_path_main')
#     with open(seed_path, "r") as f:
#         sql = f.read()

#     conn.executescript(sql)
#     conn.commit()
#     conn.close()
#     print(f"✅ Database ready at {DB_PATH}")


# def get_conn():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn
import sqlite3
from pathlib import Path

DB_PATH = "/app/data/crm.db"


def get_conn():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = sqlite3.connect(DB_PATH)

    # CHECK IF TABLE EXISTS
    cursor = conn.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='customers'
    """)

    table_exists = cursor.fetchone()

    # IF TABLE EXISTS → DB already initialized
    if table_exists:
        print("✅ Database already initialized")
        conn.close()
        return

    print("⚡ Initializing database...")

    seed_path = "/app/data/seed.sql"

    with open(seed_path, "r") as f:
        sql = f.read()

    conn.executescript(sql)

    conn.commit()

    conn.close()

    print("✅ Database initialized successfully")
