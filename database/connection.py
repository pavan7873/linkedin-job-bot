import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """
    Returns a PostgreSQL connection.
    """

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")

    return psycopg.connect(database_url)