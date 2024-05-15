from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Define the username and password variable
username = "caiyitang78"
password = "adgjliop"

# Use string formatting to include the password in the URI
uri = "mongodb+srv://caiyitang78:adgjliop@eric.za5bcmt.mongodb.net/?retryWrites=true&w=majority&appName=Eric"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Select database
db = client['sample_mflix']

# Select collection
collection = db['comments']

comments = collection.find()

# Print each comment
print(comments[0])

# Close the client connection
client.close()