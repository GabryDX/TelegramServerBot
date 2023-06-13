from Utils import constants
from Utils.server_info import run_command


def get_plex_library():
    command = 'find "' + constants.CUSTOM.PLEX_MEDIA_FOLDER \
              + '" | sed -e "s/[^-][^\\/]*\\// |/g" -e "s/|\\([^ ]\\)/|-\1/"'
    response = run_command(command)
    splitted = response.split("\n")
    init = splitted[0]
    len_init = len(init)
    new_response = ""
    for s in splitted[1:]:
        if init in s:
            new_response += s[len_init:].strip() + "\n"
    return new_response


def update_plex_library():
    command = '"' + constants.CUSTOM.PLEX_SCANNER_FOLDER + 'Plex Media Scanner" --refresh --force'
    response = run_command(command)
    return response
