

from face_auth.config.database import MongodbClient
from face_auth.constant.database_constants import USER_COLLECTION_NAME
class UserData:
    """
    this user have the mongodb operation to get the data and fetch the data
    """
    def __init__(self):
        self.client = MongodbClient()
        self.collection_name = USER_COLLECTION_NAME
        self.collection = self.client.database[self.collection_name]

    def save_user(self,user):
        self.collection.insert_one(user)
    def get_user(self,query):
        user = self.collection.find_one(query)
        return user
