from psycopg2 import extras, connect
from flask import g
import os


def get_ib_conn():
    conn = getattr(g, '_ib_conn', None)
    if conn is None:
        ib_host = "45.55.219.203"
        ib_port = "5432"
        conn = g._ib_conn = {
            "dev":connect(
                host=ib_host,
                port=ib_port,
                database="indiebrigade_development",
                user="indiebrigade",
                password="n0n0n0n0"
            ),
            "production":connect(
                host=ib_host,
                port=ib_port,
                database="indiebrigade_production",
                user="indiebrigade",
                password=os.getenv("INDIEBRIGADE_DATABASE_PASSWORD")
            )
        }[os.getenv("INDIEBRIGADE_DB", "dev")]
    return conn


def get_ib_cursor():
    return get_ib_conn().cursor(cursor_factory=extras.RealDictCursor)
