from flask import Flask, request, jsonify

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


if __name__ == "__main__":
    app.run(debug=True)

