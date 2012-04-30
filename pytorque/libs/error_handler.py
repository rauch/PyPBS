import logging

server_logger = logging.getLogger('pytorque.custom')

class ErrorHandler():
    _errorMessage = None

    def handle(self, throwable):
        server_logger.error(throwable)
        self._errorMessage = str(throwable)

    def resetHandler(self):
        self._errorMessage = None

    def getMessage(self):
        if self._errorMessage and self._errorMessage != '':
            return self._errorMessage
        else:
            return None


