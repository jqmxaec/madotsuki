import sqlite3

from sqlalchemy import create_engine, Engine, MetaData, Connection, text, event

from mado.utils import absolute_appdata_path

engine: Engine = None
conn: Connection = None


def setup_database_connection(meta: MetaData) -> None:
    global engine, conn

    engine = create_engine(
        "sqlite:///" + absolute_appdata_path("storage.db"),
        echo=True,
    )

    raw = engine.raw_connection()
    for line in raw.iterdump():
        print(line)

    @event.listens_for(engine, "connect")
    def setup_functions(dbapi_connection: sqlite3.Connection, _) -> None:
        dbapi_connection.create_function("pylower", 1, str.lower)
        dbapi_connection.create_function("pyupper", 1, str.upper)

    meta.create_all(bind=engine)

    conn = engine.connect()
    conn.execute(text("PRAGMA foreign_keys = ON"))  # pk functionality have to be enabled manually


def get_conn() -> Connection:
    return conn
