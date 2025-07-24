class FileNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)

class MissingKeyError(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidKeyError(Exception):
    def __init__(self, message):
        super().__init__(message)

class JSONDecodeError(Exception):
    def __init__(self, message):
        super().__init__(message)

class FileNotFoundInPath(Exception):
    def __init__(self, message):
        super().__init__(message)

class IncorrectFileFormat(Exception):
    def __init__(self, message):
        super().__init__(message)

class ReportTypeNotExist(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidResponseTimeFormat(Exception):
    def __init__(self, message):
        super().__init__(message)


