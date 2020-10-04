class ILogger:
    def log(self, message):
        raise NotImplementedError

    def session_log(self, func):
        raise NotImplementedError
