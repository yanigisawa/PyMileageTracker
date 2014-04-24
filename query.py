from app.models import FillUp
from ZODB import FileStorage, DB
from datetime import timedelta
import transaction

class db_obj(object):
    def __init__(self, path):
        self.storage = FileStorage.FileStorage(path)
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.dbroot = self.connection.root()

    def close(self):
        self.connection.close()
        self.db.close()
        self.storage.close()

dbFilePath = "db/mileageDb.fs"

db = db_obj(dbFilePath)
tree = db.dbroot['fillUps']

key = tree.maxKey()
count = 0
while count < 5:
    print("Key: {0} - fillup: {1}".format(key, tree[key]))
    oneSecondEarlier = key + timedelta(seconds = -1)
    key = tree.maxKey(oneSecondEarlier)
    count += 1





