from flask import Flask, request, jsonify
from text_analytics import AnswerChecker


app = Flask(__name__)

@app.route("/")
def home():
    return "test ok"

def compare_answer(list_jawaban_benar,list_jawaban_siswa):
    answer_checker = AnswerChecker('969c349c3c4043b3890c3c16a8f1d11f','e662fdd673dc4ad5b2cff8e66e919ddf')
    return answer_checker.compare_jawaban(list_jawaban_benar,list_jawaban_siswa)

@app.route("/koreksi/",methods = ["POST"])
def test_request():
    jawaban_request = request.json
    jawaban_benar = jawaban_request["jawaban_benar"]
    jawaban_siswa = jawaban_request["jawaban_siswa"]
    jawaban_benar_list = []
    jawaban_siswa_list = []
    for jawaban in jawaban_benar:
        jawaban_benar_list.append(jawaban)

    for siswa in jawaban_siswa:
        jawaban_siswa_list.append({"siswa":siswa["nama"],"jawaban":siswa["jawaban"]})
    result = compare_answer(jawaban_benar_list,jawaban_siswa_list)
    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True)

