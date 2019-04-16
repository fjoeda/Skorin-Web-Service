import uuid
import requests
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
        headers   = {'Ocp-Apim-Subscription-Key': self.text_key}
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
        headers   = {'Ocp-Apim-Subscription-Key': self.text_key}
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
        result = []
        for i in range(len(res)):
            result.append(res[i]['translations'][0]['text'])

        return result

    def get_non_english_answer(self,list_of_text):
        language_api_url = self.text_cs_url + "languages"
        sentence_list = []

        for i in range(len(list_of_text)):
            sentence_list.append({'id':str(i+1),'text':list_of_text[i]})
        documents = {'documents' : sentence_list}
        headers   = {'Ocp-Apim-Subscription-Key': self.text_key}
        response  = requests.post(language_api_url, headers=headers, json=documents)
        languages = response.json()
        result = []
        for i in range(len(languages['documents'])):
            if languages['documents'][i]['detectedLanguages'][0]['iso6391Name'] != 'en':
                result.append(i)
        return result
            

    def compose_all_english_answer(self,list_of_text):
        non_en_list = []
        non_en_index = self.get_non_english_answer(list_of_text)
        for i in range(len(list_of_text)):
            if i in non_en_index:
                non_en_list.append(list_of_text[i])

        non_en_translated = self.get_translation(non_en_list)

        for i in range(len(non_en_index)):
            list_of_text[non_en_index[i]] = non_en_translated[i]
        
        return list_of_text

class AnswerChecker:

    def __init__(self,text_key,trans_key):
        self.text_key = text_key
        self.trans_key = trans_key
        self.text_analytics = TextAnalytics(text_key,trans_key)

    def get_similarity(self,text1,text2):
        similarity_val = self.get_cosine_sim(text1,text2)
        return similarity_val[0][1]

    def get_cosine_sim(self,*strs): 
        vectors = [t for t in self.get_vectors(*strs)]
        return cosine_similarity(vectors)
    
    def get_vectors(self,*strs):
        text = [t for t in strs]
        vectorizer = CountVectorizer(text)
        vectorizer.fit(text)
        return vectorizer.transform(text).toarray()

    def get_list_compare(self,entity_cor,keyph_cor,jawab_entity,jawab_keyph):
        skor_list = []
        for i in range(len(entity_cor)):
            entity_skor = self.get_similarity(entity_cor[i],jawab_entity[i])
            keyph_skor = self.get_similarity(keyph_cor[i],jawab_keyph[i])
            avg_skor = (entity_skor+keyph_skor)/2
            skor_list.append(avg_skor)

        return skor_list

    def compareJawaban(self,list_benar, list_siswa):
        list_skor = []
        correct_entity = self.text_analytics.get_entities(list_benar)
        correct_keyPhrase = self.text_analytics.get_key_phrases(list_benar)
        for siswa in list_siswa:
            jawab_entity = self.text_analytics.get_entities(siswa["jawaban"])
            jawab_keyPh = self.text_analytics.get_key_phrases(siswa["jawaban"])
            list_skor_siswa = self.get_list_compare(correct_entity,correct_keyPhrase,jawab_entity,jawab_keyPh)
            list_skor.append({"siswa":siswa["siswa"],"skor_jawaban":list_skor_siswa})

        return list_skor

