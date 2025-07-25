class FileNotFound(Exception):
    """
    Файл не найден.
    """
    def __init__(self, message):
        super().__init__(message)

class MissingKeyError(Exception):
    """
    Не найден искомый ключ в файле.
    """
    def __init__(self, message):
        super().__init__(message)

class InvalidKeyError(Exception):
    """
    Неверный формат ключа.
    """
    def __init__(self, message):
        super().__init__(message)

class JSONDecodeError(Exception):
    """
    Ошибка при декодировании.
    """
    def __init__(self, message):
        super().__init__(message)

class FileNotFoundInPath(Exception):
    """
    Файл не найлен по пути.
    """
    def __init__(self, message):
        super().__init__(message)

class IncorrectFileFormat(Exception):
    """
    Некорректный формат файла.
    """
    def __init__(self, message):
        super().__init__(message)

class ReportTypeNotExist(Exception):
    """
    Не существует такого репорта.
    """
    def __init__(self, message):
        super().__init__(message)

class InvalidResponseTimeFormat(Exception):

    def __init__(self, message):
        super().__init__(message)


