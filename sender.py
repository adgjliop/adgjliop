import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import os
from pymongo import MongoClient, server_api
from pymongo.server_api import ServerApi

def generate_verification_code(size=6):
    """Generate a random alphanumeric verification code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))

def update_verification_code(email):
    """Update the verification code for a user in the database."""
    try:
        # Retrieve environment variables
        uri = os.environ['MONGO_URI']

        # Generate verification code
        verification_code = generate_verification_code()
        print(f"Generated Verification Code: {verification_code}")

        # Connect to MongoDB to update the user document with the verification code
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client['sample_mflix']  
        collection = db['user']  

        # Update user document
        user_update_result = collection.update_one(
            {'email': email},
            {'$set': {'verification_code': verification_code}}
        )
        if user_update_result.matched_count == 0:
            print("No user found with that email.")
            return "No user found with that email."

        print("Verification code updated successfully.")
        return "Verification code updated successfully."

    except Exception as e:
        print(f"An error occurred: {e}")

def send_verification_email(email):
    """Send an email with a verification code."""
    try:
        # Retrieve environment variables
        smtp_server = 'smtp-relay.brevo.com'
        smtp_port = 587
        smtp_username = os.environ['SMTP_USERNAME']
        smtp_password = os.environ['SMTP_PASSWORD']
        uri = os.environ['MONGO_URI']

        # Generate verification code
        verification_code = generate_verification_code()

        # Connect to MongoDB to update the user document with the verification code
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client['sample_mflix']
        collection = db['user']

        # Update user document
        user_update_result = collection.update_one(
            {'email': email},
            {'$set': {'verification_code': verification_code}}
        )
        if user_update_result.matched_count == 0:
            print("No user found with that email.")
            return "No user found with that email."

        # Create the email message
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = email
        message['Subject'] = 'Verify Your Account'
        body = f'Please verify your account by entering this code: {verification_code}'
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)
        server.quit()
        
        print("Verification email sent successfully.")
        return "Verification email sent successfully."

    except Exception as e:
        print(f"An error occurred: {e}")

# Example calls
update_verification_code('caiyitang78@gmail.com')  # This call updates the verification code in the database
send_verification_email('caiyitang78@gmail.com')  # This call sends an email and updates the code
