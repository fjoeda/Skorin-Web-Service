import requests

subscription_key = '969c349c3c4043b3890c3c16a8f1d11f'
base_url = "https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/"
entity_api_url = base_url+'entities'

sentences = ['i have a good feeleng about John Terry', 'Joko Widodo seems so nice of meeting Joko Widodo at 26 June 1996', 
        'i didnt want to come over to Nebraska ','it is wonderful day','i didnt want to come over to Nebraska ','it is wonderful day']

sencente_list = []
for i in range(len(sentences)):
    sencente_list.append({'id':str(i+1),'text':sentences[i]})

documents = {'documents' : sencente_list}
headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
response  = requests.post(entity_api_url, headers=headers, json=documents)
entity = response.json()
entites = []

for entity_item in entity['documents']:
    entity_str = "entList "
    for item in entity_item['entities']:
        entity_str += item['matches'][0]['text'] +' '
    entites.append(entity_str)

print(entites)

print(entity['documents'][0]['entities'][0]['matches'][0]['text'])