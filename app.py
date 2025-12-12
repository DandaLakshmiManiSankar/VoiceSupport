from flask import Flask, request, jsonify, render_template
from datetime import datetime, timezone 

app = Flask(__name__)

# --- IN-MEMORY STORE FOR SPEAK TO TYPE FIELD (Field 1) ---
TRANSCRIPTS = {
    1: {"text": "", "updated_at": None}, # Speak to Type (Multi-line)
}
# --------------------------------------------------------

@app.route("/")
def index():
    # Serves templates/index.html
    return render_template("index.html")

@app.route("/save_transcript", methods=["POST"])
def save_transcript():
    """
    API endpoint to receive and save the transcribed text for field 1.
    Expects JSON: {"field": 1, "text": "Final text"}
    """
    data = request.get_json(force=True)
    field = int(data.get("field", 0))
    text = data.get("text", "").strip()

    # Only process requests for field 1
    if field != 1:
        return jsonify({"success": False, "message": f"Invalid field number: {field} for this app."}), 400

    # Update the in-memory store
    TRANSCRIPTS[field]["text"] = text
    
    # Use timezone-aware datetime
    TRANSCRIPTS[field]["updated_at"] = datetime.now(timezone.utc).isoformat()

    return jsonify({
        "success": True, 
        "field": field, 
        "text": text, 
        "updated_at": TRANSCRIPTS[field]["updated_at"]
    })

@app.route("/get_transcripts", methods=["GET"])
def get_transcripts():
    """Return all saved transcripts (JSON)"""
    return jsonify({"success": True, "data": TRANSCRIPTS})

if __name__ == "__main__":
    # Run on a distinct port for easy concurrent testing
    app.run(host="0.0.0.0", port=5001, debug=True)
