from typing import Dict


class IConnector:
    def add_complex_object(self, key, value):
        raise NotImplementedError

    def get_complex_object(self, key):
        raise NotImplementedError

    def collect_all_data(self) -> Dict:
        raise NotImplementedError
