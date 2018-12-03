from tinydb import TinyDB, Query

class RpgDatabase():
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = TinyDB(self.db_path)
        self.Character = Query()

    def set_gm(self, username):
        return self.db.upsert({"username": username, "type": "GM"}, self.Character.type == "GM")

    def get_gm(self, username):
        gm = self.db.search(self.Character.type == "GM")
        if len(gm) == 0:
            return None
        else:
            return gm[0]['username']

    def get_character(self, username):
        data = self.db.search(self.Character.username == username)
        if len(data) == 0:
            return None
        else:
            return data[0]
    def upsert_character(self, username, data):
        data['username'] = username
        data['type'] = "Player"
        return self.db.upsert(data, self.Character.username == username)

    def delete_character(self, username):
        return self.db.delete(self.Character.username == username)
