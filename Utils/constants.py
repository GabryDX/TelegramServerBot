import pathlib
from typing import Final

from Utils import textfiles
from Utils.Custom import Custom


BASE_PROJECT_FOLDER: Final[str] = str(pathlib.Path(__file__).parent.resolve()) + "/../"
DATABASE_FOLDER: Final[str] = BASE_PROJECT_FOLDER + "Database/"

# Users and chats
CHAT_DATA_FOLDER: Final[str] = DATABASE_FOLDER + "ChatData/"
USERS_FOLDER: Final[str] = DATABASE_FOLDER + "Users/"
ADMIN_FILE: Final[str] = DATABASE_FOLDER + "Admin.txt"
CHATIDS_FILE: Final[str] = DATABASE_FOLDER + "ChatIDs.txt"

# Media
MEDIA_FOLDER: Final[str] = DATABASE_FOLDER + "Media/"
AUDIOID_FILE: Final[str] = DATABASE_FOLDER + "Audio.txt"
DOCUMENTID_FILE: Final[str] = DATABASE_FOLDER + "Document.txt"
PHOTOID_FILE: Final[str] = DATABASE_FOLDER + "Photo.txt"
STICKERID_FILE: Final[str] = DATABASE_FOLDER + "Sticker.txt"
VIDEOID_FILE: Final[str] = DATABASE_FOLDER + "Video.txt"
VIDEONOTEID_FILE: Final[str] = DATABASE_FOLDER + "VideoNote.txt"
VOICEID_FILE: Final[str] = DATABASE_FOLDER + "Voice.txt"
CONTACTID_FILE: Final[str] = DATABASE_FOLDER + "Contact.txt"
LOCATIONID_FILE: Final[str] = DATABASE_FOLDER + "Location.txt"
VENUEID_FILE: Final[str] = DATABASE_FOLDER + "Venue.txt"

CUSTOM_CONSTANTS_FILE: Final[str] = BASE_PROJECT_FOLDER + 'Utils/custom_constants.txt'


def load_customs() -> dict:
    custom_dict = dict()
    if textfiles.exists(CUSTOM_CONSTANTS_FILE):
        lista = textfiles.readLines(CUSTOM_CONSTANTS_FILE)
        for line in lista:
            (key, val) = line.split()
            custom_dict[key] = val
    else:
        textfiles.write("BOT_TOKEN:\nPLEX_MEDIA_FOLDER:\nPLEX_SCANNER_FOLDER:", CUSTOM_CONSTANTS_FILE)
    return custom_dict


CUSTOM = Custom(load_customs())
