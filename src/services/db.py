import psycopg
from psycopg.rows import dict_row
from src.config import settings

def get_conn():
    # opens a connection with a dict-style row factory and auto‑commit when leaving the context
    return psycopg.connect(settings.database_url, row_factory=dict_row)