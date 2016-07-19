from psycopg2 import extras, connect
from flask import g, abort
import os
import logging

logging.basicConfig(level=logging.DEBUG)


def record_not_found(f):
        def decorator(s):
            r = f(s)
            if r is None or r is []:
                abort(404)
            else:
                return r
        return decorator


class IBCursor(extras.RealDictCursor, extras.LoggingCursor):

    @record_not_found
    def fetchall(self):
        return super(extras.RealDictCursor, self).fetchall()

    @record_not_found
    def fetchone(self):
        return super(extras.RealDictCursor, self).fetchone()

    @record_not_found
    def fetchmany(self, size=None):
        return super(extras.RealDictCursor, self).fetchmany(size)


def get_ib_conn():
    conn = getattr(g, '_ib_conn', None)
    if conn is None:
        base_config = {
            'host': '45.55.219.203',
            'port': '5432',
            'user': 'indiebrigade',
            'connection_factory': extras.LoggingConnection
        }
        conn = g._ib_conn = {
            "dev": connect(
                database="indiebrigade_development",
                password="n0n0n0n0",
                **base_config
            ),
            "production": connect(
                database="indiebrigade_production",
                password=os.getenv("INDIEBRIGADE_DATABASE_PASSWORD"),
                **base_config
            )
        }[os.getenv("INDIEBRIGADE_DB", "dev")]
        conn.initialize(logging.getLogger('DB'))
    return conn



def get_ib_cursor():
    return get_ib_conn().cursor(cursor_factory=IBCursor)

