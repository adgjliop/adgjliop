# main.py
from sender import send_verification_email, update_verification_code
import os
from pymongo import MongoClient, server_api
from pymongo.server_api import ServerApi

def verify_email_code(email, code):
    """
    This function takes an email and a verification code as input and checks if the code matches the one stored in MongoDB.
    
    Parameters:
    email (str): The email of the user to verify.
    code (str): The verification code provided by the user.
    
    Returns:
    str: A message indicating whether the verification was successful or not.
    """
    uri = os.environ['MONGO_URI']
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['sample_mflix']
    collection = db['user']

    user = collection.find_one({'email': email})
    if not user:
        return "No user found with that email."

    stored_code = user.get('verification_code')
    if stored_code and stored_code == code:
        # If the code matches, update the 'verified' status to True
        collection.update_one({'email': email}, {'$set': {'verified': True}})
        return "Email verified successfully!"
    else:
        return "Invalid verification code."

if __name__ == "__main__":
    # Interactive script to verify a user's email
    email = input("Enter your email: ")
    code = input("Enter your verification code: ")
    result = verify_email_code(email, code)
    print(result)
