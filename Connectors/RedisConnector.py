import json

import redis

from Connectors.IConnector import IConnector


class RedisConnector(IConnector):
    def __init__(self, host, port, db):
        self.api = redis.Redis(host=host, port=port, db=db)

    def add_complex_object(self, key, value):
        json_value = json.dumps(value)
        self.api.set(key, json_value)

    def get_complex_object(self, key):
        json_value = self.api.get(key)
        return json.loads(json_value)

    def collect_all_data(self):
        data = {}
        for key in self.api.scan_iter():
            data[key.decode("utf-8")] = self.get_complex_object(key)
        return data
