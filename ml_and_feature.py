#%%
import pandas as pd 
import numpy as np
from text_analytics import TextAnalytics
from text_analytics import AnswerChecker


data = pd.read_csv('data/Jawaban.csv')
data

#%%
#Extract Feature
jawaban = data['jawaban'].values.tolist()
jawaban_benar = data['jawaban_benar'].values.tolist()

#%%
text_key = '75e62813c62143dca9930a226d1811bf'
trans_key = 'c5573255a62a494a874dc4063d9c9f17'
text_anal = TextAnalytics(text_key,trans_key)
answ_cek = AnswerChecker(text_key,trans_key)
print("composing en answer")
jawaban_en = text_anal.get_translation(jawaban)
jawaban_benar_en = text_anal.get_translation(jawaban_benar)
print("get jawaban entities...")
jawaban_entity = text_anal.get_entities(jawaban_en)
print("get jawaban benar entities...")
jawaban_benar_entity = text_anal.get_entities(jawaban_benar_en)
print("get jawaban keyphrase...")
jawaban_keyPH = text_anal.get_key_phrases(jawaban_en)
print("get jawaban benar keyphrase...")
jawaban_benar_keyPH = text_anal.get_key_phrases(jawaban_benar_en)

#%%
print(jawaban_keyPH)
print(jawaban_benar_entity)
print(jawaban_benar_keyPH)
print(jawaban_entity)

#%%
import numpy as np 
np.set_printoptions(precision=4)
data_out = data['kebenaran'].values.tolist()
jawaban_benar_word = []
word_difference = []
cos_sim_all = []
jac_sim_all = []
cos_sim_list_en = []
jac_sim_list_en = []
cos_sim_list_key = []
jac_sim_list_key = []
for i in range(len(jawaban_benar_entity)):
    jawaban_benar_word.append(len(jawaban_benar[i].split()))
    word_difference.append(abs(len(jawaban_benar[i].split())-len(jawaban[i].split())))
    cos_sim_all.append(round(answ_cek.get_similarity(jawaban_benar[i],jawaban[i]),3))
    jac_sim_all.append(round(answ_cek.get_jaccard_sim(jawaban_benar[i],jawaban[i]),3))
    cos_sim_list_en.append(round(answ_cek.get_similarity(jawaban_benar_entity[i],jawaban_entity[i]),3))
    jac_sim_list_en.append(round(answ_cek.get_jaccard_sim(jawaban_benar_entity[i],jawaban_entity[i]),3))
    cos_sim_list_key.append(round(answ_cek.get_similarity(jawaban_benar_keyPH[i],jawaban_keyPH[i]),3))
    jac_sim_list_key.append(round(answ_cek.get_jaccard_sim(jawaban_benar_keyPH[i],jawaban_keyPH[i]),3))

print(word_difference,cos_sim_list_en,jac_sim_list_en)
#%%
import csv
import math
with open('data_kebenaran.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    row = ['correct_ans_word','word_diff','cos_sim_all','jac_sim_all','cos_sim_en','jac_sim_en',"cos_sim_key","jac_sim_key","out"]
    writer.writerow(row)
    for i in range(len(data_out)):
        if not math.isnan(data_out[i]):
            row = [jawaban_benar_word[i],word_difference[i],cos_sim_all[i],jac_sim_all[i],cos_sim_list_en[i],jac_sim_list_en[i],cos_sim_list_key[i],jac_sim_list_key[i],int(data_out[i])]
            writer.writerow(row)

#%%
#ml build package
data_bnr = pd.read_csv('data_kebenaran.csv')
data_bnr

#%%
x = data_bnr.drop('out',axis = 1)
y = data_bnr['out']
x
#%%
y
#%%
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(x,y,test_size = 0.2)
X_test

#%%
from sklearn.ensemble import RandomForestClassifier
clf  = RandomForestClassifier(n_estimators=50)
clf.fit(X_train,Y_train)
clf.score(X_test,Y_test)

#%%
from sklearn.tree import DecisionTreeClassifier
clf  = DecisionTreeClassifier()
clf.fit(X_train,Y_train)
clf.score(X_test,Y_test)

#%%
from sklearn.neural_network import MLPClassifier
clf  = MLPClassifier(hidden_layer_sizes=(5,3,5),max_iter=100000)
clf.fit(X_train,Y_train)
clf.score(X_test,Y_test)

#%%
from sklearn.ensemble import RandomForestClassifier
import pickle
clf  = RandomForestClassifier(n_estimators=50)
clf.fit(X_train,Y_train)
clf.score(X_test,Y_test)
pickle.dump(clf,open('ml_model.pk','wb'))
