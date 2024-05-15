from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://caiyitang78:adgjliop@eric.za5bcmt.mongodb.net/?retryWrites=true&w=majority&appName=Eric')

# Select the database and collection
db = client['sample_mflix']
collection = db['user']

# Define a test user document
test_user = {
    "name": "Eric Tang",
    "email": "caiyitang78@gmail.com",
    "verification_code": "123456"
}

# Insert the test user
result = collection.insert_one(test_user)
print(f"User added with ID: {result.inserted_id}")
