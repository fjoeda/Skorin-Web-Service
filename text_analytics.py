from langdetect import detect_langs
import uuid
import requests

class TextAnalytics:

    def __init__(self,text_key,trans_key):
        self.text_key = text_key
        self.trans_key = trans_key
        self.text_cs_url = "https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/"
        self.text_translate_url = "https://api.cognitive.microsofttranslator.com"


    def get_key_phrases(self,list_of_text):
        key_phrase_api_url = self.text_cs_url + "keyPhrases"
        sencente_list = []
        for i in range(len(list_of_text)):
            sencente_list.append({'id':str(i+1),'language':'en','text':list_of_text[i]})

        documents = {'documents' : sencente_list}
        headers   = {'Ocp-Apim-Subscription-Key': self.key}
        response  = requests.post(key_phrase_api_url, headers=headers, json=documents)
        key_phrases = response.json()
        phrases = []
        for phrase in key_phrases['documents']:
            phrase_str = ""
            for item in phrase['keyPhrases']:
                phrase_str += item +" "
            phrases.append(phrase_str)

        return phrases

    def get_entities(self, list_of_text):
        entity_api_url = self.text_cs_url+'entities'
        sencente_list = []
        for i in range(len(list_of_text)):
            sencente_list.append({'id':str(i+1),'text':list_of_text[i]})
        documents = {'documents' : sencente_list}
        headers   = {'Ocp-Apim-Subscription-Key': self.key}
        response  = requests.post(entity_api_url, headers=headers, json=documents)
        entity = response.json()
        entities = []

        for entity_item in entity['documents']:
            entity_str = "entList "
            for item in entity_item['entities']:
                entity_str += item['matches'][0]['text'] +' '
            entities.append(entity_str)

        return entities

    def get_translation(self,list_of_text):
        base_url = self.text_translate_url
        path = '/translate?api-version=3.0'
        params = '&to=en'
        constructed_url = base_url + path + params

        headers = {
            'Ocp-Apim-Subscription-Key': self.trans_key,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        body = []
        
        for text in list_of_text:
            body.append({'text':text})

        response = requests.post(constructed_url, headers=headers, json=body)
        res = response.json()
        result_txt = res[0]['translations'][0]['text']
        result = []
        for i in len(res):
            result.append(res[i]['translations'][0]['text'])

        return result

    def is_all_english(list_of_text):
        for text in list_of_text:
            