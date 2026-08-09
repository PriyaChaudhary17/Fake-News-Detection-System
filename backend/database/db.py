from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# ==========================
# MongoDB Connection
# ==========================

client = MongoClient("mongodb://localhost:27017/")
db = client["fake_news_db"]

# Collections
predictions = db["predictions"]
users = db["users"]

print("==========================================")
print("MONGODB DEBUG INFORMATION")
print("Database:", db.name)
print("Predictions collection:", predictions.name)
print("MongoDB address:", client.address)
print("Predictions count:", predictions.count_documents({}))
print("==========================================")

# ==========================
# ADMIN ACCOUNT
# ==========================

ADMIN_EMAIL = "AdminAccountUdesh@gmail.com"
ADMIN_PASSWORD = "@rc@N3o000"

print("MongoDB Connected Successfully!")

print("======================================")
print("USING NEW ADMIN AUTHENTICATION DB.PY")
print("ADMIN EMAIL:", ADMIN_EMAIL)
print("======================================")



# ==========================
# PASSWORD VALIDATION
# ==========================

def validate_password(password):

    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."

    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."

    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."

    if not any(
        char in "!@#$%^&*()_+-=[]{}|;:,.<>?/`~"
        for char in password
    ):
        return False, "Password must contain at least one special character."

    return True, ""


# ==========================
# CREATE ADMIN AUTOMATICALLY
# ==========================

def ensure_admin_exists():

    admin_email = ADMIN_EMAIL.strip().lower()

    admin = users.find_one({
        "email": admin_email
    })
    if not admin:

        hashed_password = generate_password_hash(
            ADMIN_PASSWORD
        )

        users.insert_one({
            "email": admin_email,
            "password": hashed_password,
            "role": "admin",
            "email_verified": True
        })

        print("Admin account created automatically.")
        print("Admin email:", admin_email)

    else:

        # Make sure existing admin is still marked as admin
        users.update_one(
            {"email": admin_email},
            {
                "$set": {
                    "role": "admin",
                    "email_verified": True
                }
            }
        )

        print("Admin account already exists.")


# ==========================
# USER FUNCTIONS
# ==========================

def add_user(email, password, role="user"):

    email = email.strip().lower()

    if users.find_one({"email": email}):
        raise Exception("User already exists")

    # Validate password
    valid, message = validate_password(password)

    if not valid:
        raise Exception(message)

    hashed_pw = generate_password_hash(password)

    users.insert_one({
        "email": email,
        "password": hashed_pw,
        "role": "user",
        "email_verified": False
    })

    return True


# ==========================
# VERIFY USER
# ==========================

def verify_user(email, password):

    email = email.strip().lower()

    user = users.find_one({
        "email": email
    })

    if not user:
        return None

    if check_password_hash(
        user["password"],
        password
    ):
        return user

    return None


# ==========================
# GET USERS
# ==========================

def get_all_users():

    return list(
        users.find(
            {},
            {
                "_id": 0,
                "password": 0
            }
        )
    )


# ==========================
# STARTUP ADMIN SETUP
# ==========================

ensure_admin_exists()