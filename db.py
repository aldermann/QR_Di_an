from pymongo import MongoClient
client = MongoClient()
db = client.eat_up


def update(user_id, name, agreement):
    if db.party.count_documents({"id": user_id}) > 0:
        db.party.update_one(
            {"id": user_id}, {"$set": {"name": name, "agreement": agreement}})
    else:
        db.party.insert_one(
            {"id": user_id, "name": name, "agreement": agreement})


def participant_list():
    return db.party.find({"agreement": "yes"})
