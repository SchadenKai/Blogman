import urllib.parse
from collections.abc import Generator

from sqlalchemy import text
from sqlalchemy.engine import create_engine
from sqlalchemy.engine import Engine
from config import Settings
from sqlmodel import Session

SYNC_DB_API = "pyodbc"
SYNC_POSTGRES_DB_API = "psycopg2"
# ASYNC_DB_API = "asyncpg"

_SYNC_ENGINE: Engine | None = None


# def build_connection_string(
#     db_api: str = SYNC_DB_API,
#     user: str = Settings().sql_user,
#     password: str = Settings().sql_password,
#     host: str = Settings().sql_host,
#     port: str = Settings().sql_port,
#     db: str = Settings().sql_db,
# ) -> str:
#     params = urllib.parse.quote_plus(
#         f"DRIVER={{ODBC Driver 18 for SQL Server}};"
#         f"SERVER=tcp:{host}.database.windows.net,{port};"
#         f"DATABASE={db};"
#         f"UID={user};"
#         f"PWD={password};"
#         f"Encrypt=yes;"
#         f"TrustServerCertificate=no;"
#         f"Connection Timeout=30;"
#     )
#     return f"mssql+pyodbc:///?odbc_connect={params}"


def build_postgres_connection_string(
    db_api: str = SYNC_POSTGRES_DB_API,
    user: str = Settings().POSTGRES_USER,
    password: str = Settings().POSTGRES_PASSWORD,
    host: str = Settings().POSTGRES_SERVER,
    port: str = Settings().POSTGRES_PORT,
    db: str = Settings().POSTGRES_DB,
) -> str:
    return f"postgresql+{db_api}://{user}:{password}@{host}:{port}/{db}"


def get_sqlalchemy_engine() -> Engine:
    global _SYNC_ENGINE
    if _SYNC_ENGINE is None:
        connection_string = build_postgres_connection_string()
        _SYNC_ENGINE = create_engine(
            connection_string, pool_size=5, max_overflow=10, pool_timeout=30
        )
    return _SYNC_ENGINE


async def warm_up_connections(sync_connections_to_warm_up: int = 3) -> None:
    sync_engine = get_sqlalchemy_engine()
    connections = []
    try:
        for _ in range(sync_connections_to_warm_up):
            conn = sync_engine.connect()
            conn.execute(text("SELECT 1"))
            connections.append(conn)
    finally:
        for conn in connections:
            conn.close()


def get_session() -> Generator[Session, None, None]:
    with Session(get_sqlalchemy_engine(), expire_on_commit=False) as session:
        yield session