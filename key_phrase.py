from langdetect import detect_langs

class TextAnalytics:

    def __init__(self,key):
        self.key = key
        self.base_url = "https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/"


    def get_key_phrases(self,list_of_text):
        key_phrase_api_url = self.base_url + "keyPhrases"
        sencente_list = []
        for i in range(len(list_of_text)):
            sencente_list.append({'id':str(i+1),'language':'en','text':list_of_text[i]})

        documents = {'documents' : sencente_list}
        headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
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
        entity_api_url = self.base_url+'entities'
        sencente_list = []
        for i in range(len(sentences)):
            sencente_list.append({'id':str(i+1),'text':sentences[i]})
        documents = {'documents' : sencente_list}
        headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
        response  = requests.post(entity_api_url, headers=headers, json=documents)
        entity = response.json()
        entities = []

        for entity_item in entity['documents']:
            entity_str = "entList "
            for item in entity_item['entities']:
                entity_str += item['matches'][0]['text'] +' '
            entities.append(entity_str)

        return entities




    

    