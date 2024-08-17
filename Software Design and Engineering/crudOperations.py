"""
crudOperations.py
Author: Nathan Wilson
Contact: nathan.wilson3@outlook.com
Date: 2024-07-21
Version: 1.1
Purpose: This module contains the CRUD operations for the AnimalShelter database.
Added Bulk operations to enhance the program
Issues: None known
"""

import logging

import pymongo
import pymongo.errors

logging.basicConfig(level=logging.INFO)

class BulkOperations:
    """
    Handles bulk operations in the MongoDB collection.
    """

    def __init__(self, collection):
        """
        Initialize the BulkOperations with the given collection.

        :param collection: MongoDB collection object
        """
        self.collection = collection

    def bulk_insert(self, data_list):
        """
        Insert multiple documents into the collection.

        :param data_list: List of dictionaries representing the documents to be inserted
        :return: List of inserted IDs or None if an error occurred
        """
        if not data_list or not isinstance(data_list, list):
            raise ValueError("Data list must be a non-empty list of dictionaries")
        
        try:
            result = self.collection.insert_many(data_list)
            return result.inserted_ids
        # Handle specific exceptions for MongoDB errors
        except pymongo.errors.BulkWriteError as bwe:
            logging.error(f"BulkWriteError: {bwe.details}")
            raise
        except pymongo.errors.PyMongoError as pe:
            logging.error(f"PyMongoError: {pe}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise

    def bulk_update(self, operations_list):
        """
        Perform bulk update operations.

        :param operations_list: List of update operations (each operation is a dictionary with 'filter' and 'update' keys)
        :return: The result of the bulk update operation
        """
        if not operations_list or not isinstance(operations_list, list):
            raise ValueError("Operations list must be a non-empty list of update operations")
        
        for op in operations_list:
            if not isinstance(op, dict) or 'filter' not in op or 'update' not in op:
                raise ValueError("Each operation must be a dictionary with 'filter' and 'update' keys")
        
        try:
            bulk_ops = [pymongo.UpdateOne(op['filter'], {'$set': op['update']}) for op in operations_list]
            result = self.collection.bulk_write(bulk_ops)
            return result.bulk_api_result
        except pymongo.errors.BulkWriteError as bwe:
            logging.error(f"BulkWriteError during bulk update: {bwe.details}")
            raise
        except pymongo.errors.PyMongoError as pe:
            logging.error(f"PyMongoError during bulk update: {pe}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred during bulk update: {e}")
            raise

    def bulk_delete(self, filter_list):
        """
        Perform bulk delete operations.

        :param filter_list: List of filter criteria for deletion
        :return: The result of the bulk delete operation
        """
        if not filter_list or not isinstance(filter_list, list):
            raise ValueError("Filter list must be a non-empty list of dictionaries")
        
        try:
            bulk_ops = [pymongo.DeleteOne(filter) for filter in filter_list]
            result = self.collection.bulk_write(bulk_ops)
            return result.bulk_api_result
        except Exception as e:
            logging.error(f"Failed to perform bulk delete: {e}")
            raise

class CreateOperation:
    """
    Handles the creation of documents in the MongoDB collection.
    """

    def __init__(self, collection):
        """
        Initialize the CreateOperation with the given collection.

        :param collection: MongoDB collection object
        """
        self.collection = collection

    def execute(self, data):
        """
        Insert a document into the collection.

        :param data: Dictionary representing the document to be inserted
        :return: Boolean indicating success of the operation
        """
        if data is None or not isinstance(data, dict):
            raise ValueError("Data parameter must be a non-empty dictionary")
        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except pymongo.errors.DuplicateKeyError as e:
            logging.error(f"Duplicate key error: {e}")
            raise
        except Exception as e:
            logging.error(f"Failed to insert document: {e}")
            raise RuntimeError(f"Failed to insert document: {e}")

class ReadOperation:
    """
    Handles the reading of documents from the MongoDB collection.
    """

    def __init__(self, collection):
        """
        Initialize the ReadOperation with the given collection.

        :param collection: MongoDB collection object
        """
        self.collection = collection

    def execute(self, query, projection=None):
        """
        Retrieve documents from the collection based on the query.

        :param query: Dictionary representing the query criteria
        :param projection: Dictionary representing the fields to include or exclude
        :return: List of documents matching the query
        """
        if query is None or not isinstance(query, dict):
            raise ValueError("Query parameter must be a non-empty dictionary")
        try:
            result = self.collection.find(query, projection)
            return list(result)
        except Exception as e:
            raise RuntimeError(f"Failed to read documents: {e}")

class UpdateOperation:
    """
    Handles the updating of documents in the MongoDB collection.
    """

    def __init__(self, collection):
        """
        Initialize the UpdateOperation with the given collection.

        :param collection: MongoDB collection object
        """
        self.collection = collection

    def execute(self, query, update_data):
        """
        Update a document in the collection based on the query.

        :param query: Dictionary representing the query criteria
        :param update_data: Dictionary representing the update data
        :return: Boolean indicating success of the operation
        """
        if query is None or not isinstance(query, dict):
            raise ValueError("Query parameter must be a non-empty dictionary")
        if update_data is None or not isinstance(update_data, dict):
            raise ValueError("Update data must be a non-empty dictionary")
        try:
            result = self.collection.update_one(query, {'$set': update_data})
            return result.modified_count > 0
        except Exception as e:
            raise RuntimeError(f"Failed to update document: {e}")

class DeleteOperation:
    """
    Handles the deletion of documents from the MongoDB collection.
    """

    def __init__(self, collection):
        """
        Initialize the DeleteOperation with the given collection.

        :param collection: MongoDB collection object
        """
        self.collection = collection

    def execute(self, query):
        """
        Delete a document from the collection based on the query.

        :param query: Dictionary representing the query criteria
        :return: Boolean indicating success of the operation
        """
        if query is None or not isinstance(query, dict):
            raise ValueError("Query parameter must be a non-empty dictionary")
        try:
            result = self.collection.delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            raise RuntimeError(f"Failed to delete document: {e}")
