class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CustomConstants(metaclass=Singleton):
    BOT_TOKEN = None
    PLEX_MEDIA_FOLDER = None
    PLEX_SCANNER_FOLDER = None

    def __init__(self):
        pass

    def load_data(self, dictionary: dict):
        print(dictionary)
        self.__dict__.update(dictionary)
        print(self.BOT_TOKEN)
