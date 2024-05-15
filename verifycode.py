from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def store_verification_code(email, code, uri):
    """
    Store the verification code in the user's document in MongoDB.
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['app']
    collection = db['user-info']

    result = collection.update_one({'email': email}, {'$set': {'verification_code': code}})
    if result.matched_count == 0:
        return False, "No user found with that email."
    return True, "Verification code updated successfully."

def verify_user_code(email, code, uri):
    """
    Verify the user's input code against the stored verification code in MongoDB.
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['app']
    collection = db['user-info']

    user = collection.find_one({'email': email})
    if not user:
        return False, "No user found with that email."

    stored_code = user.get('verification_code')
    if stored_code == code:
        collection.update_one({'email': email}, {'$set': {'verified': True}})
        return True, "Verification successful."
    return False, "Verification failed, incorrect code."
