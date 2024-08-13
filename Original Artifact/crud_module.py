from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, user, password, host, port, db, collection):
        # Initialize MongoDB client
        self.client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
        self.database = self.client[db]
        self.collection = self.database[collection]

    def create(self, data):
        """ Insert a document into the collection """
        if data is not None:
            result = self.collection.insert_one(data)
            return result.acknowledged
        else:
            raise ValueError("Data parameter is empty")

    def read(self, query):
        """ Query documents from the collection """
        if query is not None:
            result = self.collection.find(query)
            return list(result)
        else:
            raise ValueError("Query parameter is empty")

    def update(self, query, update_data):
        """ Update a document in the collection """
        if query is not None and update_data is not None:
            result = self.collection.update_one(query, {'$set': update_data})
            return result.modified_count > 0
        else:
            raise ValueError("Query or update_data parameter is empty")

    def delete(self, query):
        """ Delete a document from the collection """
        if query is not None:
            result = self.collection.delete_one(query)
            return result.deleted_count > 0
        else:
            raise ValueError("Query parameter is empty")
