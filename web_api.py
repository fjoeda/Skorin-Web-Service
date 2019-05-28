from flask import Flask, request, jsonify
from text_analytics import AnswerChecker
from soal_service import SoalService


app = Flask(__name__)

@app.route("/")
def home():
    return "test ok"

def compare_answer(list_jawaban_benar,list_jawaban_siswa):
    answer_checker = AnswerChecker('969c349c3c4043b3890c3c16a8f1d11f','c5573255a62a494a874dc4063d9c9f17')
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

def collect_soal(soal_id):
    soal_ser = SoalService("test")
    return soal_ser.get_soal(soal_id)


@app.route("/soal/",methods = ["GET"])
def get_soal():

    if "id" in request.args:
        args = request.args
        print(args['id'])
        soals = collect_soal(args['id'])
        print(soals)
        return_val = {"soals":soals}
        return jsonify(return_val)
    else:
        return_val = {"error":"invalid parameter"}
        return jsonify(return_val)
    



if __name__ == "__main__":
    app.run(debug=True)

