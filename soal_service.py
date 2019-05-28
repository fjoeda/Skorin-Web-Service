from pymongo import MongoClient


class SoalService:

    def __init__(self, conn_string):
        self.conn_string = conn_string

    def get_soal(self, id):
        client = MongoClient("mongodb+srv://admin:admin@cluster0-aikuf.mongodb.net/quizdb?retryWrites=true")
        db = client["quizdb"]
        collection = db['soals']
        soals = []
        for post in collection.find({"tipe":id}):
            post.pop('_id')
            soals.append(post)
        return soals

