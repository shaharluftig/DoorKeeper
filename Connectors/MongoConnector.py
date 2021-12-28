from pymongo import MongoClient

from Connectors.IConnector import IConnector


class MongoConnector(IConnector):
    def __init__(self, host, port, username, password, db, collection):
        self.api = MongoClient(host=host, port=port, username=username, password=password)[db][collection]

    def add_complex_object(self, docs, many=False):
        docs = self.__to_dict(docs)
        if many:
            return self.api.insert_many(docs)
        return self.api.insert_one(docs)

    def collect_all_data(self):
        data = []
        for doc in self.api.find():
            data.append(doc)
        return data

    @staticmethod
    def __to_dict(docs):
        if isinstance(docs, list):
            return [item.__dict__ for item in docs]
        return docs.__dict__
