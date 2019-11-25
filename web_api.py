from flask import Flask, request, jsonify
from text_analytics import AnswerChecker
from soal_service import SoalService


app = Flask(__name__)

@app.route("/")
def home():
    return "test ok"

def compare_answer(list_jawaban_benar,list_jawaban_siswa):
    answer_checker = AnswerChecker('bc94d092eca0417eaf16594265ef5190','e780503cff4a4ff78e260a030302c91e ')
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


def koreksi_per_item(list_benar,list_jawab):
    answer_checker = AnswerChecker('bc94d092eca0417eaf16594265ef5190','e780503cff4a4ff78e260a030302c91e ')
    return answer_checker.compare_jawaban_single(list_benar,list_jawab)

@app.route("/koreksi-satu/",methods = ["POST"])
def koreksi_item():
    jawaban_request = request.json
    jawaban_benar = jawaban_request["jawaban_benar"]
    jawaban_siswa = jawaban_request["jawaban_siswa"]
    result = koreksi_per_item(jawaban_benar,jawaban_siswa)
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

