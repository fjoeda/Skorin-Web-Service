from flask import Flask, request, jsonify
from text_analytics import TextAnalytics

app = Flask(__name__)

@app.route("/")
def home():
    return "test ok"

@app.route("/test_request/",methods = ["POST"])
def test_request():
    jawaban_request = request.json
    jawaban_list = jawaban_request["jawaban"]
    print(jawaban_list)
    return "ok"

@app.route("/koreksi/",methods = ["POST"])
def koreksi():
    jawaban_request = request.json
    jawaban_list = jawaban_request["jawaban"]


if __name__ == "__main__":
    app.run(debug=True)

