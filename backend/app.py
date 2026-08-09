from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Existing imports
from backend.ml.predict_text import predict_news
from backend.verification.similarity_search import find_similar_articles
from backend.verification.url_verifier import verify_url, is_url
from backend.database.history import save_prediction, get_history

# New import for user management
from backend.database import db   # updated db.py with add_user, verify_user, get_all_users

app = Flask(__name__)
CORS(app)

# ==========================
# Home + History
# ==========================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Fake News Detection API Running"})

@app.route("/history", methods=["GET"])
def history():
    try:
        logs = get_history()

        if not isinstance(logs, list):
            logs = []

        return jsonify({"logs": logs}), 200

    except Exception as e:
        print("History API Error:", str(e))
        return jsonify({
            "error": "Unable to load history",
            "logs": []
        }), 500

# ==========================
# User Authentication
# ==========================
@app.route("/api/signup", methods=["POST"])
def signup():

    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # ==========================
    # EMAIL REQUIRED
    # ==========================

    if not email:
        return jsonify({
            "message": "Email is required."
        }), 400


    # ==========================
    # GMAIL ONLY
    # ==========================

    if not email.endswith("@gmail.com"):
        return jsonify({
            "message": "Please use a valid Gmail address."
        }), 400


    # ==========================
    # PASSWORD REQUIRED
    # ==========================

    if not password:
        return jsonify({
            "message": "Password is required."
        }), 400


    # ==========================
    # PASSWORD VALIDATION
    # ==========================

    valid, password_message = db.validate_password(
        password
    )

    if not valid:
        return jsonify({
            "message": password_message
        }), 400


    # ==========================
    # CREATE ACCOUNT
    # ==========================

    try:

        db.add_user(
            email,
            password,
            role="user"
        )

        return jsonify({
            "message": "Signup successful!"
        }), 201


    except Exception as e:

        error_message = str(e)

        if "User already exists" in error_message:

            return jsonify({
                "message": "This email is already registered."
            }), 409

        return jsonify({
            "message": error_message
        }), 400
        
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = db.verify_user(email, password)
    if user:
        return jsonify({"message": "Login successful!", "role": user["role"]})
    return jsonify({"message": "Invalid credentials"}), 401

# ==========================
# Admin Routes
# ==========================
@app.route("/api/admin/users", methods=["GET"])
def admin_users():
    role = request.args.get("role")  # frontend should send ?role=admin
    if role != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    users_list = db.get_all_users()
    return jsonify({"users": users_list})   # wrap in object

@app.route("/api/admin/delete_user", methods=["POST"])
def delete_user():
    role = request.args.get("role")
    if role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email required"}), 400

    result = db.users.delete_one({"email": email})
    if result.deleted_count > 0:
        return jsonify({"message": f"User {email} deleted"})
    else:
        return jsonify({"error": "User not found"}), 404

# ==========================
# Prediction
# ==========================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input received."}), 400

        user_input = data.get("text") or data.get("input")
        if not user_input:
            return jsonify({"error": "Input is required."}), 400

        user_input = user_input.strip()

        print("\n" + "=" * 60)
        print("Received Input:")
        print(user_input)
        print("Type:", type(user_input))
        print("is_url():", is_url(user_input))
        print("=" * 60)

        # URL ANALYSIS
        if is_url(user_input):
            print("URL detected. Running URL verification...\n")
            result = verify_url(user_input)
            prediction = result["prediction"]

            save_prediction({
                "input_type": "url",
                "input": user_input,
                "prediction": prediction["prediction"],
                "confidence": float(prediction["confidence"]),
                "real_probability": float(prediction["real_probability"]),
                "fake_probability": float(prediction["fake_probability"]),
                "reasons": prediction["reasons"],
                "sources": result.get("sources", []),
                "verified": result.get("verified", False),
                "trusted_source": result.get("trusted_source", ""),
                "scraped_article": result.get("scraped_article", {}),
                "date": datetime.utcnow().isoformat()   # add timestamp
            })
            return jsonify(result)

        # TEXT ANALYSIS
        print("Normal text detected. Running ML prediction...\n")
        prediction_result = predict_news(user_input)
        similar_sources = find_similar_articles(user_input)

        save_prediction({
            "input_type": "text",
            "input": user_input,
            "prediction": prediction_result["prediction"],
            "confidence": float(prediction_result["confidence"]),
            "real_probability": float(prediction_result["real_probability"]),
            "fake_probability": float(prediction_result["fake_probability"]),
            "reasons": prediction_result["reasons"],
            "sources": similar_sources,
            "date": datetime.utcnow().isoformat()   # add timestamp
        })

        response = {
            "input_type": "text",
            "news": user_input,
            "prediction": prediction_result,
            "sources": similar_sources
        }
        return jsonify(response)

    except Exception as e:
        print("\nERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
