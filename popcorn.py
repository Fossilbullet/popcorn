import os
from flask import Flask, request, jsonify
import replicate

app = Flask(__name__)

REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")
client = replicate.Client(api_token=REPLICATE_TOKEN)

@app.route("/get-training-status", methods=["GET"])
def get_training_status():
    training_id = request.args.get("training_id")

    if not training_id:
        return jsonify({"error": "Missing training_id parameter"}), 400

    try:
        training = client.trainings.get(training_id)

        response_data = {
            "status": training.status,
            "training_id": training.id,
            "trigger_word": training.input.get("trigger_word")  # ← added this line
        }

        if training.status == "succeeded":
            response_data["model_version"] = training.output.get("version")

        if training.status == "failed":
            response_data["error"] = training.error

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": f"Failed to fetch training status: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10001)))