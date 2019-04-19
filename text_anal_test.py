import requests
import uuid
from flask import jsonify
from text_analytics import TextAnalytics,AnswerChecker
import json 


subscription_key = '969c349c3c4043b3890c3c16a8f1d11f'

with open('jawaban_benar.json') as f:
    jawaban_benar = json.load(f)

with open('jawaban_siswa.json') as f:
    jawaban_siswa = json.load(f)

jawaban_benar_list = []
jawaban_siswa_list = []

for jawaban in jawaban_benar["jawaban_benar"]:
    jawaban_benar_list.append(jawaban)

for siswa in jawaban_siswa["jawaban_siswa"]:
    jawaban_siswa_list.append({"siswa":siswa["nama"],"jawaban":siswa["jawaban"]})



trans_subscription_key = 'e662fdd673dc4ad5b2cff8e66e919ddf'

text_anal = TextAnalytics(subscription_key,trans_subscription_key)

ans_check = AnswerChecker(subscription_key,trans_subscription_key)


print(text_anal.get_translation(jawaban_benar_list))

skor = ans_check.compareJawaban(jawaban_benar_list,jawaban_siswa_list)
print(skor)
     