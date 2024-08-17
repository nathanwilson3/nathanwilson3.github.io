import time
import random
from pymongo import MongoClient
import matplotlib.pyplot as plt

# Assuming you have a working connection to your MongoDB and AnimalShelter class
connection_string = "mongodb+srv://nathanwilson3:kAnhKgcq4UvdmpPP@animalsheltercluster.dlcajuu.mongodb.net/?retryWrites=true&w=majority"
db_name = "AAC"
collection_name = "AnimalShelter"

# Establish a database connection
client = MongoClient(connection_string)
db = client[db_name]
collection = db[collection_name]

# Function to measure time complexity
def measure_time(operation, *args):
    start_time = time.time()
    operation(*args)
    end_time = time.time()
    return end_time - start_time

# Create test data
def generate_test_data(n):
    return [{"animal_id": f"A{str(i).zfill(6)}", "name": "Test Animal", "species": "Dog"} for i in range(n)]

# Example usage
def test_time_complexity():
    """
    Test the time complexity of insert and query operations on the database.

    This function measures the time taken to insert and query different sizes of test data.
    """
    test_sizes = [10, 100, 1000, 5000, 10000]
    insert_times = []
    query_times = []

    for size in test_sizes:
        # Insert test data
        test_data = generate_test_data(size)
        collection.delete_many({})  # Clean up the collection before the test

        # Measure the time to insert data
        insert_time = measure_time(collection.insert_many, test_data)
        insert_times.append(insert_time)

        # Measure the time to query data
        query_time = measure_time(lambda: list(collection.find({})))
        query_times.append(query_time)

        # Clean up after testing
        collection.delete_many({})

    # Print the results
    for size, insert_time, query_time in zip(test_sizes, insert_times, query_times):
        print(f"Size: {size}, Insert Time: {insert_time:.4f} seconds, Query Time: {query_time:.4f} seconds")

if __name__ == "__main__":
    test_time_complexity()
