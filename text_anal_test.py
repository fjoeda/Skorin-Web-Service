import requests
import uuid
from flask import jsonify
from text_analytics import TextAnalytics, AnswerChecker
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

def get_list_compare(entity_cor,keyph_cor,jawab_entity,jawab_keyph):
    skor_list = []
    for i in range(len(entity_cor)):
        entity_skor = ans_check.get_similarity(entity_cor[i],jawab_entity[i])
        keyph_skor = ans_check.get_similarity(keyph_cor[i],jawab_keyph[i])
        avg_skor = (entity_skor+keyph_skor)/2
        skor_list.append(avg_skor)

    return skor_list

def compareJawaban(list_benar, list_siswa):
    list_skor = []
    correct_entity = text_anal.get_entities(list_benar)
    correct_keyPhrase = text_anal.get_key_phrases(list_benar)
    for siswa in jawaban_siswa_list:
        jawab_entity = text_anal.get_entities(siswa["jawaban"])
        jawab_keyPh = text_anal.get_key_phrases(siswa["jawaban"])
        list_skor_siswa = get_list_compare(correct_entity,correct_keyPhrase,jawab_entity,jawab_keyPh)
        list_skor.append({"siswa":siswa["siswa"],"skor_jawaban":list_skor_siswa})

    return list_skor

skor = compareJawaban(jawaban_benar_list,jawaban_siswa_list)
print(skor)
     