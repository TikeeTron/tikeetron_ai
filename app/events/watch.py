from bson.json_util import dumps

from crud import insert_event_vector, update_event_vector, eventCollections


change_stream = eventCollections.watch()
for change in change_stream:
    if change["operationType"] == "insert":
        insert_event_vector(change["fullDocument"])
    elif change["operationType"] == "update":
        print(change["documentKey"]["_id"])
        update_event_vector(
            change["documentKey"]["_id"],
            change["updateDescription"]["updatedFields"],
        )
    print(dumps(change))
