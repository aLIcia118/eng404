"""
All interaction with MongoDB should be through this file!
We may be required to use a new database at any point.
"""
import os
from functools import wraps

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

SE_DB = "seDB"

client: pm.MongoClient | None = None

MONGO_ID = "_id"

MIN_ID_LEN = 4


def is_valid_id(_id: str) -> bool:
    """Return True if `_id` looks like a valid Mongo-style id."""
    if not isinstance(_id, str):
        return False
    if len(_id) < MIN_ID_LEN:
        return False
    return True


def needs_db(fn):
    """
    Decorator to ensure that the DB is connected before
    running the decorated function.

    The test suite expects this decorator to call `connect_db()`
    when the wrapped function is invoked.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Always go through connect_db; it is idempotent and will reuse
        # the existing global client if already connected.
        connect_db()
        return fn(*args, **kwargs)

    return wrapper


def _build_client_from_env() -> pm.MongoClient:
    """
    Build a MongoClient using either:
      - MONGODB_URI (Atlas SRV recommended), or
      - CLOUD_MONGO pieces (MONGO_USER / MONGO_PASSWD / MONGO_HOST), or
      - local default mongodb://127.0.0.1:27017.
    """
    uri = os.getenv("MONGODB_URI")
    if uri:
        print("Connecting to Mongo via MONGODB_URI (cloud).")
        return pm.MongoClient(uri, serverSelectionTimeoutMS=5000)

    if os.getenv("CLOUD_MONGO") == "1":
        user = os.getenv("MONGO_USER")
        pwd = os.getenv("MONGO_PASSWD")
        host = os.getenv("MONGO_HOST")
        if not (user and pwd and host):
            msg = "CLOUD_MONGO=1 requires MONGO_USER, MONGO_PASSWD, and MONGO_HOST."
            raise ValueError(msg)
        uri = f"mongodb+srv://{user}:{pwd}@{host}/?retryWrites=true&w=majority"
        print("Connecting to Mongo via CLOUD_MONGO pieces (cloud).")
        return pm.MongoClient(uri, serverSelectionTimeoutMS=5000)

    print("Connecting to Mongo locally (mongodb://127.0.0.1:27017).")
    return pm.MongoClient("mongodb://127.0.0.1:27017", serverSelectionTimeoutMS=5000)


def connect_db() -> pm.MongoClient:
    """
    Uniform way to connect to the DB across all uses.

    Returns:
        A MongoClient instance, and sets the module-level `client` as well.
    """
    global client
    if client is None:
        client = _build_client_from_env()
        # Validate connection early (raises on failure)
        client.admin.command("ping")
    return client


def ping() -> bool:
    """Return True if the DB connection is alive."""
    try:
        connect_db()
        return client.admin.command("ping").get("ok") == 1  # type: ignore[union-attr]
    except Exception:
        return False


def close_db() -> None:
    """Close the global client, if present."""
    global client
    if client is not None:
        client.close()
        client = None


def convert_mongo_id(doc: dict) -> None:
    """Convert Mongo's ObjectId to a string so it can be JSON-serialized."""
    if MONGO_ID in doc:
        doc[MONGO_ID] = str(doc[MONGO_ID])


@needs_db
def create(collection: str, doc: dict, db: str = SE_DB):
    """
    Insert a single doc into a collection.
    """
    print(f"{doc=}")
    return client[db][collection].insert_one(doc)  # type: ignore[index]


@needs_db
def read_one(collection: str, filt: dict, db: str = SE_DB):
    """
    Find with a filter and return only the first doc found.
    Return None if not found.
    """
    result = client[db][collection].find_one(filt)  # type: ignore[index]
    if result:
        convert_mongo_id(result)
    return result


@needs_db
def delete(collection: str, filt: dict, db: str = SE_DB) -> int:
    """
    Delete a single doc matching the filter.

    Returns:
        The number of documents deleted (0 or 1).
    """
    print(f"{filt=}")
    del_result = client[db][collection].delete_one(filt)  # type: ignore[index]
    return del_result.deleted_count


@needs_db
def update(collection: str, filters: dict, update_dict: dict, db: str = SE_DB):
    """Update a single document matching `filters` with `update_dict`."""
    return client[db][collection].update_one(filters, {"$set": update_dict})  # type: ignore[index]


@needs_db
def read(collection: str, db: str = SE_DB, no_id: bool = True) -> list[dict]:
    """
    Read all documents from a collection.

    Args:
        no_id: If True, drop the internal Mongo _id field; otherwise, convert it to a string.

    Returns:
        A list of document dicts.
    """
    result: list[dict] = []
    for doc in client[db][collection].find():  # type: ignore[index]
        if no_id:
            doc.pop(MONGO_ID, None)
        else:
            convert_mongo_id(doc)
        result.append(doc)
    return result


@needs_db
def read_dict(collection: str, key: str, db: str = SE_DB, no_id: bool = True) -> dict:
    """
    Read all docs and re-key them by `key`.

    Useful for lookups.
    """
    recs = read(collection, db=db, no_id=no_id)
    recs_as_dict: dict[str, dict] = {}
    for rec in recs:
        recs_as_dict[rec[key]] = rec
    return recs_as_dict


def ensure_indexes() -> None:
    """
    Ensure required indexes exist.

    This function will attempt to create indexes but will not raise exceptions
    if MongoDB is not available, allowing the app to start even if DB is down.
    """
    try:
        db_client = connect_db()
        db = db_client[SE_DB]
        db["cities"].create_index("name", unique=False)
    except Exception as exc:
        print(f"Warning: Could not ensure indexes (MongoDB may not be running): {exc}")
        print("Indexes will be created when MongoDB becomes available.")
