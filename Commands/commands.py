#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from Utils import constants, textfiles
from Objects import utenti
from Commands.admin_commands import admin_command
from Commands.user_commands import user_command

update_id = None

AUDIOID = "Audio.txt"
DOCUMENTID = "Document.txt"
PHOTOID = "Photo.txt"
STICKERID = "Sticker.txt"
VIDEOID = "Video.txt"
VIDEONOTEID = "VideoNote.txt"
VOICEID = "Voice.txt"
CONTACTID = "Contact.txt"
LOCATIONID = "Location.txt"
VENUEID = "Venue.txt"

MARKDOWN = ParseMode.MARKDOWN


async def command_factory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the message the user sent."""
    print(update)
    messaggio = update.message
    print(messaggio)

    # controllo se nuovo utente e lo aggiungo nel database
    utenti.update_chat_ids(messaggio)

    if messaggio:  # your bot can receive updates without messages
        # Reply to the message

        formula = utenti.info(messaggio) + ": "
        statements = {"messaggio.audio": ["audio", "salva_info(messaggio.audio.file_id, AUDIOID)",
                                          "Grazie per l'audio toccante"],
                      "messaggio.document": ["document", "salva_info(messaggio.document.file_id, DOCUMENTID)",
                                             "Grazie per la bella gif"],
                      "messaggio.game": ["game", "", "Non gioco ad altri giochi scusa"],
                      "messaggio.photo": ["foto", "salva_info(messaggio.photo[0].file_id, PHOTOID)",
                                          "Grazie per la bella foto"],
                      "messaggio.sticker": ["sticker", "", "Grazie per lo sticker"],
                      "messaggio.video": ["video", "salva_info(messaggio.video.file_id, VIDEOID)",
                                          "Grazie per il video"],
                      "messaggio.voice": ["voice", "salva_info(messaggio.voice.file_id, VOICEID)",
                                          "Grazie per il vocale toccante"],
                      "messaggio.video_note": ["video_note",
                                               "salva_info(messaggio.video_note.file_id, VIDEONOTEID)",
                                               "Grazie per il video"],
                      "messaggio.new_chat_members": ["new_chat_members", "", "Un altro tonto si è aggiunto "],
                      "messaggio.caption": ["caption", "", "Dimmi"],
                      "messaggio.contact": ["contact",
                                            "salva_info(media.get_contact(messaggio.contact), CONTACTID)",
                                            "Eh eh"],
                      "messaggio.location": ["location",
                                             "salva_info(media.get_location(messaggio.location), LOCATIONID)",
                                             "Eh eh"],
                      "messaggio.venue": ["venue", "salva_info(media.get_venue(messaggio.venue), VENUEID)",
                                          "Scusa a che via?"],
                      "messaggio.left_chat_member": ["left_chat_member", "", "Adios"],
                      "messaggio.new_chat_title": ["new_chat_title", "", "Ok"],
                      "messaggio.new_chat_photo": ["new_chat_photo", "", "Ok"],
                      "messaggio.delete_chat_photo": ["delete_chat_photo", "", "Bravo leva tutto!!!"],
                      "messaggio.group_chat_created": ["group_chat_created", "", "Non ho capito..."],
                      "messaggio.supergroup_chat_created": ["supergroup_chat_created", "", "Non ho supercapito..."],
                      "messaggio.channel_chat_created": ["channel_chat_created", "", "Ok..."],
                      "messaggio.migrate_to_chat_id": ["migrate_to_chat_id", "", "Stiamo degenerando"],
                      "messaggio.migrate_from_chat_id": ["migrate_from_chat_id", "", "Stiamo degenerando ancora"],
                      "messaggio.pinned_message": ["pinned_message", "", "Aspetta che me lo segno..."],
                      "messaggio.invoice": ["invoice", "", "Non ho invoice capito..."],
                      "messaggio.successful_payment": ["successful_payment", "", "I soldi!!!"],
                      "messaggio.forward_signature": ["forward_signature", "", "Inoltri cosa?"],
                      "messaggio.author_signature": ["author_signature", "", "La firma di chi?"],
                      "messaggio.bot": ["bot", "", "Un altro bot?"], }

        testo = messaggio.text
        if testo:  # se messaggio testuale (caso più comune)
            formula += testo
            # messaggio.reply_text(messaggio.text)
            is_admin_command = await admin_command(messaggio, context.bot)
            if not is_admin_command:  # se non è un comando admin
                await user_command(messaggio)
        else:
            found = False
            for state in statements.keys():  # cerca tra le altre tipologie di messaggio note
                if eval(state) and type(statements[state]) is list:
                    found = True
                    if statements[state][1] == "":
                        formula += statements[state][0]
                        await messaggio.reply_text(statements[state][2])
                    else:
                        formula += statements[state][0]
                        exec(statements[state][1])
                        await messaggio.reply_text(statements[state][2])  # messaggio di risposta
            if not found:  # se non riconosce il messaggio
                formula += "MESSAGGIO NON RICONOSCIUTO"
                await messaggio.reply_text("Comando non riconosciuto")

        print(formula)

        file_utente = constants.USERS_FOLDER + utenti.get_titolo_clean(messaggio.chat) + ".txt"
        formula += "\n"
        if textfiles.exists(file_utente):
            textfiles.append(formula, file_utente)
        else:
            textfiles.write(formula, file_utente)


def salva_info(message_id, filename):
    message_id += "\n"
    filename = constants.MEDIA_FOLDER + filename
    if textfiles.exists(filename):
        textfiles.append(message_id, filename)
    else:
        textfiles.write(message_id, filename)
