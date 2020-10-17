class IConnector:
    def add_complex_object(self, doc, many=False):
        raise NotImplementedError

    def collect_all_data(self):
        raise NotImplementedError
