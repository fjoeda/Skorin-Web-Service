from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@cluster0-aikuf.mongodb.net/quizdb?retryWrites=true")
db = client["quizdb"]
collection = db['soals']
soals = []
for post in collection.find({"tipe":"A"}):
    soals.append(post)
