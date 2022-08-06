from models.Guests import Guests


class IOutputStream:
    def notify(self, path: str, guests: Guests):
        raise NotImplementedError
