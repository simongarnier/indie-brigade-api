from psycopg2 import extras
import psycopg2
import os

def ib_conn():
    ib_host = "45.55.219.203"
    ib_port = "5432"
    return {
        "dev":psycopg2.connect(
            host=ib_host,
            port=ib_port,
            database="indiebrigade_development",
            user="indiebrigade",
            password="n0n0n0n0"
        ),
        "production":psycopg2.connect(
            host=ib_host,
            port=ib_port,
            database="indiebrigade_production",
            user="indiebrigade",
            password=os.getenv("INDIEBRIGADE_DATABASE_PASSWORD")
        )
    }[os.getenv("INDIEBRIGADE_DB", "dev")]


def dict_cursor():
    return ib_conn().cursor(cursor_factory=extras.RealDictCursor)

