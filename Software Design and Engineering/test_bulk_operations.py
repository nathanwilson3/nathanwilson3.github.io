import time
import logging
from pymongo import MongoClient
from bson import ObjectId
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from crudOperations import BulkOperations

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Assuming you have a working connection to your MongoDB
connection_string = "mongodb+srv://nathanwilson3:kAnhKgcq4UvdmpPP@animalsheltercluster.dlcajuu.mongodb.net/?retryWrites=true&w=majority"
db_name = "AAC"
collection_name = "AnimalShelterTwo"

# Establish a database connection
client = MongoClient(connection_string)
db = client[db_name]
collection = db[collection_name]

# Create instance of BulkOperations
bulk_ops = BulkOperations(collection)

# Function to measure time complexity
def measure_time(operation, *args):
    start_time = time.time()
    operation(*args)
    end_time = time.time()
    return end_time - start_time

# Create test data
def generate_test_data(n):
    return [{"_id": ObjectId(), "animal_id": f"A{str(i).zfill(6)}", "name": "Test Animal", "species": "Dog"} for i in range(n)]

# Define test sizes and data
def test_bulk_operations():
    test_sizes = [10, 100, 1000, 10000]
    bulk_insert_times = []
    bulk_update_times = []
    bulk_delete_times = []

    for size in test_sizes:
        # Generate test data
        test_data = [{'animal_id': f'A{i}', 'name': f'Animal {i}'} for i in range(size)]

        # Measure the time for bulk insert
        try:
            bulk_insert_time = measure_time(bulk_ops.bulk_insert, test_data)
            bulk_insert_times.append(bulk_insert_time)
        except Exception as e:
            logging.error(f"Failed bulk insert: {e}")
            bulk_insert_times.append(float('nan'))  # Use NaN for plotting purposes

        # Prepare update operations
        update_data = {"name": "Updated Animal"}
        update_operations = [{'filter': {'animal_id': data['animal_id']}, 'update': update_data} for data in test_data]

        # Measure the time for bulk update
        try:
            bulk_update_time = measure_time(bulk_ops.bulk_update, update_operations)
            bulk_update_times.append(bulk_update_time)
        except Exception as e:
            logging.error(f"Failed bulk update: {e}")
            bulk_update_times.append(float('nan'))

        # Prepare delete filters
        delete_filters = [{'animal_id': data['animal_id']} for data in test_data]

        # Measure the time for bulk delete
        try:
            bulk_delete_time = measure_time(bulk_ops.bulk_delete, delete_filters)
            bulk_delete_times.append(bulk_delete_time)
        except Exception as e:
            logging.error(f"Failed bulk delete: {e}")
            bulk_delete_times.append(float('nan'))

        # Clean up after testing
        bulk_ops.collection.delete_many({})

    # Print the results
    for size, bulk_insert_time, bulk_update_time, bulk_delete_time in zip(
            test_sizes, bulk_insert_times, bulk_update_times, bulk_delete_times):
        print(f"Size: {size}, Bulk Insert Time: {bulk_insert_time:.4f} sec, "
              f"Bulk Update Time: {bulk_update_time:.4f} sec, Bulk Delete Time: {bulk_delete_time:.4f} sec")

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(test_sizes, bulk_insert_times, label='Bulk Insert Time', marker='o')
    plt.plot(test_sizes, bulk_update_times, label='Bulk Update Time', marker='o')
    plt.plot(test_sizes, bulk_delete_times, label='Bulk Delete Time', marker='o')
    plt.xlabel('Number of Records')
    plt.ylabel('Time (seconds)')
    plt.title('Bulk Operations Performance')
    plt.legend()
    plt.grid(True)
    plt.show()
