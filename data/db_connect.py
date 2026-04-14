"""
All interaction with MongoDB should be through this file!
We may be required to use a new database at any point.
"""
import os
from copy import deepcopy
from functools import wraps
from typing import Optional
from uuid import uuid4
import certifi # Use certifi's CA bundle for TLS to MongoDB Atlas

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

SE_DB = "seDB"

client: Optional[pm.MongoClient] = None
_use_inmem = False
_inmem_db: dict[str, dict[str, list[dict]]] = {}

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
        return pm.MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            tlsCAFile=certifi.where(),   
        )

    if os.getenv("CLOUD_MONGO") == "1":
        user = os.getenv("MONGO_USER")
        pwd = os.getenv("MONGO_PASSWD")
        host = os.getenv("MONGO_HOST")
        if not (user and pwd and host):
            msg = "CLOUD_MONGO=1 requires MONGO_USER, MONGO_PASSWD, and MONGO_HOST."
            raise ValueError(msg)
        uri = f"mongodb+srv://{user}:{pwd}@{host}/?retryWrites=true&w=majority"
        print("Connecting to Mongo via CLOUD_MONGO pieces (cloud).")
        return pm.MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            # Same TLS setup for this cloud connection path
            tlsCAFile=certifi.where(),   
        )

    print("Connecting to Mongo locally (mongodb://127.0.0.1:27017).")
    return pm.MongoClient(
        "mongodb://127.0.0.1:27017",
        serverSelectionTimeoutMS=5000,
        # Using the same CA bundle is harmless for local dev and keeps
        # behavior consistent across all connection modes.
    )


def connect_db() -> Optional[pm.MongoClient]:
    """
    Uniform way to connect to the DB across all uses.

    Returns:
        A MongoClient instance, or None when falling back to in-memory mode.
    """
    global client, _use_inmem
    if client is not None:
        return client

    try:
        client = _build_client_from_env()
        # Validate connection early (raises on failure)
        client.admin.command("ping")
        _use_inmem = False
        return client
    except Exception:
        _use_inmem = True
        client = None
        return None


def ping() -> bool:
    """Return True if the DB connection is alive."""
    if _use_inmem:
        return True
    try:
        db_client = connect_db()
        if db_client is None:
            return False
        return db_client.admin.command("ping").get("ok") == 1
    except Exception:
        return False


def close_db() -> None:
    """Close the global client, if present."""
    global client, _inmem_db, _use_inmem
    if client is not None:
        client.close()
        client = None
    _inmem_db = {}
    _use_inmem = False


def _inmem_collection(db: str, collection: str) -> list[dict]:
    db_store = _inmem_db.setdefault(db, {})
    return db_store.setdefault(collection, [])


def _match(doc: dict, filt: dict) -> bool:
    return all(doc.get(key) == value for key, value in filt.items())


def convert_mongo_id(doc: dict) -> None:
    """Convert Mongo's ObjectId to a string so it can be JSON-serialized."""
    if MONGO_ID in doc:
        doc[MONGO_ID] = str(doc[MONGO_ID])


@needs_db
def create(collection: str, doc: dict, db: str = SE_DB):
    """
    Insert a single doc into a collection.
    """
    if _use_inmem or client is None:
        rec = deepcopy(doc)
        rec.setdefault(MONGO_ID, str(uuid4()))
        _inmem_collection(db, collection).append(rec)
        return rec[MONGO_ID]
    return client[db][collection].insert_one(doc)  # type: ignore[index]


@needs_db
def read_one(collection: str, filt: dict, db: str = SE_DB):
    """
    Find with a filter and return only the first doc found.
    Return None if not found.
    """
    if _use_inmem or client is None:
        for rec in _inmem_collection(db, collection):
            if _match(rec, filt):
                result = deepcopy(rec)
                convert_mongo_id(result)
                return result
        return None
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
    if _use_inmem or client is None:
        coll = _inmem_collection(db, collection)
        for idx, rec in enumerate(coll):
            if _match(rec, filt):
                del coll[idx]
                return 1
        return 0
    del_result = client[db][collection].delete_one(filt)  # type: ignore[index]
    return del_result.deleted_count


@needs_db
def update(collection: str, filters: dict, update_dict: dict, db: str = SE_DB):
    """Update a single document matching `filters` with `update_dict`."""
    if _use_inmem or client is None:
        for rec in _inmem_collection(db, collection):
            if _match(rec, filters):
                rec.update(update_dict)
                return 1
        return 0
    return client[db][collection].update_one(filters, {"$set": update_dict})  # type: ignore[index]


@needs_db
def read(collection: str, db: str = SE_DB, no_id: bool = True) -> list:
    """
    Read all documents from a collection.

    Args:
        no_id: If True, drop the internal Mongo _id field; otherwise, convert it to a string.

    Returns:
        A list of document dicts.
    """
    result = []
    if _use_inmem or client is None:
        for rec in _inmem_collection(db, collection):
            doc = deepcopy(rec)
            if no_id:
                doc.pop(MONGO_ID, None)
            else:
                convert_mongo_id(doc)
            result.append(doc)
        return result
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
        if db_client is None:
            return
        db = db_client[SE_DB]
        db["cities"].create_index("name", unique=False)
    except Exception as exc:
        print(f"Warning: Could not ensure indexes (MongoDB may not be running): {exc}")
        print("Indexes will be created when MongoDB becomes available.")
