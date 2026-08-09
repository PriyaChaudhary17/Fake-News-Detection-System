from datetime import datetime
from backend.database.db import predictions


# ==========================================
# SAVE PREDICTION
# ==========================================

def save_prediction(data):

    try:
        # ------------------------------------------
        # Remove existing MongoDB _id
        # ------------------------------------------
        # MongoDB will automatically generate a new
        # unique _id for every prediction.
        data.pop("_id", None)

        # ------------------------------------------
        # Add creation timestamp
        # ------------------------------------------
        data["created_at"] = datetime.now().isoformat()

        # ------------------------------------------
        # Save prediction to MongoDB
        # ------------------------------------------
        result = predictions.insert_one(data)

        # ------------------------------------------
        # Debug information
        # ------------------------------------------
        print("\n" + "=" * 60)
        print("PREDICTION SAVED SUCCESSFULLY")
        print("MongoDB ID:", result.inserted_id)
        print("Input type:", data.get("input_type"))
        print("Prediction:", data.get("prediction"))
        print("=" * 60)

        return True

    except Exception as e:

        print("\n" + "=" * 60)
        print("ERROR SAVING PREDICTION")
        print("Error:", str(e))
        print("=" * 60)

        return False


# ==========================================
# GET HISTORY
# ==========================================

def get_history():

    try:

        history = list(
            predictions.find(
                {},
                {
                    "_id": 0
                }
            ).sort(
                "created_at",
                -1
            )
        )

        # ------------------------------------------
        # Make sure every record is JSON-safe
        # ------------------------------------------

        for item in history:

            # Convert created_at datetime to string
            if isinstance(
                item.get("created_at"),
                datetime
            ):
                item["created_at"] = (
                    item["created_at"].isoformat()
                )

            # Convert date datetime to string
            if isinstance(
                item.get("date"),
                datetime
            ):
                item["date"] = (
                    item["date"].isoformat()
                )

        return history

    except Exception as e:

        print("\n" + "=" * 60)
        print("ERROR GETTING HISTORY")
        print("Error:", str(e))
        print("=" * 60)

        return []