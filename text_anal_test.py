import requests
import uuid
from flask import jsonify
from text_analytics import TextAnalytics


subscription_key = '969c349c3c4043b3890c3c16a8f1d11f'

sentences = ['pangeran diponegoro menang perang','campaign sandiaga uno rame',
                'Indonesia merdeka tanggal 17 Agustus 1945']

trans_subscription_key = 'e662fdd673dc4ad5b2cff8e66e919ddf'

text_anal = TextAnalytics(subscription_key,trans_subscription_key)

result = text_anal.compose_all_english_answer(sentences)

print(result)
