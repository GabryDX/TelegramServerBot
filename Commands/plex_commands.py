from Utils import constants
from Utils.server_info import run_command


def get_plex_library():
    command = 'find "' + constants.CUSTOM.PLEX_MEDIA_FOLDER \
              + '" | sed -e "s/[^-][^\\/]*\\//  |/g" -e "s/|\\([^ ]\\)/|-\1/"'
    response = run_command(command)
    return response


def update_plex_library():
    command = '"' + constants.CUSTOM.PLEX_SCANNER_FOLDER + 'Plex Media Scanner" --refresh --force'
    response = run_command(command)
    return response
