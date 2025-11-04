from db_connect import create, read_one, update, delete

COL = "smoke"

r = create(COL, {"k": "v1"})
_id = r.inserted_id
print("inserted:", _id)

print("read_one:", read_one(COL, {"_id": _id}))

print("update.matched:", update(COL, {"_id": _id}, {"k": "v2"}).matched_count)

print("deleted:", delete(COL, {"_id": _id}))
