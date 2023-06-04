import pathlib
from typing import Final

BOT_TOKEN: Final = 'BOT-TOKEN'

BASE_PROJECT_FOLDER: Final = str(pathlib.Path(__file__).parent.resolve()) + "/../"
DATABASE_FOLDER: Final = BASE_PROJECT_FOLDER + "Database/"

# Users and chats
CHAT_DATA_FOLDER: Final = DATABASE_FOLDER + "ChatData/"
USERS_FOLDER: Final = DATABASE_FOLDER + "Users/"
ADMIN_FILE: Final = DATABASE_FOLDER + "Admin.txt"
CHATIDS_FILE: Final = DATABASE_FOLDER + "ChatIDs.txt"

# Media
MEDIA_FOLDER: Final = DATABASE_FOLDER + "Media/"
AUDIOID_FILE: Final = DATABASE_FOLDER + "Audio.txt"
DOCUMENTID_FILE: Final = DATABASE_FOLDER + "Document.txt"
PHOTOID_FILE: Final = DATABASE_FOLDER + "Photo.txt"
STICKERID_FILE: Final = DATABASE_FOLDER + "Sticker.txt"
VIDEOID_FILE: Final = DATABASE_FOLDER + "Video.txt"
VIDEONOTEID_FILE: Final = DATABASE_FOLDER + "VideoNote.txt"
VOICEID_FILE: Final = DATABASE_FOLDER + "Voice.txt"
CONTACTID_FILE: Final = DATABASE_FOLDER + "Contact.txt"
LOCATIONID_FILE: Final = DATABASE_FOLDER + "Location.txt"
VENUEID_FILE: Final = DATABASE_FOLDER + "Venue.txt"
