#
# import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "zerodha_journal")

client: Any | None = None


def connect_to_mongodb():
    global client

    if client is None:
        try:
            from pymongo import MongoClient
        except ImportError as exc:
            raise RuntimeError(
                "pymongo is not installed. Run 'pip install pymongo' in your virtual environment."
            ) from exc

        client = MongoClient(MONGODB_URL)

    return client[MONGODB_DB_NAME]


def get_database():
    if client is None:
        return connect_to_mongodb()

    return client[MONGODB_DB_NAME]


def close_mongodb_connection() -> None:
    global client

    if client is not None:
        client.close()
        client = None
