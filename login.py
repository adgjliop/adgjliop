from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt
from pymongo.errors import DuplicateKeyError

def check_email(email):
    """
    Validates the email format using a regular expression.
    """
    pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return pattern.match(email) is not None

def check_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[0-9]', password):
        return False, "Password must include at least one digit."
    if not re.search(r'[A-Z]', password):
        return False, "Password must include at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must include at least one lowercase letter."
    if not re.search(r'[\W_]', password):
        return False, "Password must include at least one special character."
    return True, "Password is strong."

def add_user(email, password, uri):
    """
    Adds a new user to the MongoDB database with hashed password. Ensures email is unique.
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['app']
    collection = db['user-info']

    # Check if email already exists
    if collection.find_one({'email': email}):
        return "A user with this email already exists."

    # Hashing the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Creating the user document
    user_document = {
        'email': email,
        'hashed_password': hashed_password,
        'salt': salt
    }

    # Inserting the user into the database
    try:
        result = collection.insert_one(user_document)
        return f"User added with _id: {result.inserted_id}"
    except DuplicateKeyError:
        return "A user with this email already exists."
    except Exception as e:
        return f"Error inserting user: {e}"
    
    
def find_user(email, uri):
    """
    Finds a user by their email in the MongoDB database.

    Parameters:
    email (str): The email of the user to find.

    Returns:
    dict: User document or None if no user is found.
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['app']
    collection = db['user-info']

    try:
        user = collection.find_one({'email': email})
        if user:
            return user
        else:
            return None
    except Exception as e:
        return f"Error retrieving user: {e}"
    

def login(email, password, uri):
    """
    Authenticates a user by email and password.

    Parameters:
    email (str): The email of the user trying to log in.
    password (str): The plain-text password provided by the user at login.

    Returns:
    bool: True if the login is successful, False otherwise.
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['app']
    collection = db['user-info']

    # Retrieve the user by email
    user = collection.find_one({'email': email})
    if not user:
        print("No user found with that email.")
        return False

    # Retrieve stored hashed password from the database
    stored_hashed_password = user['hashed_password']

    # Hash the provided password using the stored salt and compare
    if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
        print("Login successful.")
        return True
    else:
        print("Login failed. Incorrect password.")
        return False

def signup_user(email, password, uri):
    if not check_email(email):
        return "Invalid email format."
    is_strong, message = check_password(password)
    if not is_strong:
        return message
    return add_user(email, password, uri)

    
def main():
    # Define the password variable
    username = "USERNAME"
    password = "PASSWORD"

    # Use string formatting to include the password in the URI
    uri = f"mongodb+srv://{username}:{password}@cluster0.yf41kon.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # Select database
    db = client['app']

    # Select collection
    collection = db['user-info']

    # Example usage of the function
    email = "TEST_EMAIL@TEST.COM"
    password = "PASSWORD"

    print(add_user(email, password, uri))
    print(find_user(email, uri))
    print(login(email, password, uri))


if __name__ == "__main__":
    main()
