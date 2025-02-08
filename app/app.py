from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"message": "Aplicação up"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000, debug=True, use_reloader=False)