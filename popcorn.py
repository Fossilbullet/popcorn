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
        return jsonify({
            "status": training.status,
            "urls": training.urls,
            "completed_at": training.completed_at,
            "started_at": training.started_at,
            "error": training.error
        })
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve training status: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10001)))