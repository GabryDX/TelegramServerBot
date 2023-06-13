#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from Utils import constants, textfiles, server_info
from Objects import utenti, admin
from Commands.admin_commands import admin_command
from Commands.user_commands import user_command

logger = logging.getLogger(__name__)


statements = {"messaggio.audio": ["audio", "save_media(messaggio.audio.file_id, constants.AUDIOID_FILE)",
                                  "Grazie per l'audio toccante"],
              "messaggio.document": ["document", "save_media(messaggio.document.file_id, constants.DOCUMENTID_FILE)",
                                     "Grazie per la bella gif"],
              "messaggio.game": ["game", "", "Non gioco ad altri giochi scusa"],
              "messaggio.photo": ["foto", "save_media(messaggio.photo[0].file_id, constants.PHOTOID_FILE)",
                                  "Grazie per la bella foto"],
              "messaggio.sticker": ["sticker", "", "Grazie per lo sticker"],
              "messaggio.video": ["video", "save_media(messaggio.video.file_id, constants.VIDEOID_FILE)",
                                  "Grazie per il video"],
              "messaggio.voice": ["voice", "save_media(messaggio.voice.file_id, constants.VOICEID_FILE)",
                                  "Grazie per il vocale toccante"],
              "messaggio.video_note": ["video_note",
                                       "save_media(messaggio.video_note.file_id, constants.VIDEONOTEID_FILE)",
                                       "Grazie per il video"],
              "messaggio.new_chat_members": ["new_chat_members", "", "Un altro tonto si è aggiunto "],
              "messaggio.caption": ["caption", "", "Dimmi"],
              "messaggio.contact": ["contact", "save_media(media.get_contact(messaggio.contact), "
                                               "constants.CONTACTID_FILE)",
                                    "Eh eh"],
              "messaggio.location": ["location", "save_media(media.get_location(messaggio.location), "
                                                 "constants.LOCATIONID_FILE)",
                                     "Eh eh"],
              "messaggio.venue": ["venue", "save_media(media.get_venue(messaggio.venue), constants.VENUEID_FILE)",
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


async def command_factory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manages all the messages if they match a command"""
    logger.info(update)
    messaggio = update.message

    # controllo se nuovo utente e lo aggiungo nel database
    utenti.update_chat_ids(messaggio)

    if messaggio:  # your bot can receive updates without messages
        # Reply to the message
        
        formula = utenti.info(messaggio) + ": "
        
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
        save_info(messaggio, formula)


def save_info(messaggio, formula):
    file_utente = constants.USERS_FOLDER + utenti.get_titolo_clean(messaggio.chat) + ".txt"
    formula += "\n"
    if textfiles.exists(file_utente):
        textfiles.append(formula, file_utente)
    else:
        textfiles.write(formula, file_utente)


def save_media(message_id, filename):
    message_id += "\n"
    filename = constants.MEDIA_FOLDER + filename
    if textfiles.exists(filename):
        textfiles.append(message_id, filename)
    else:
        textfiles.write(message_id, filename)


async def init_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # controllo se nuovo utente e lo aggiungo nel database
    utenti.update_chat_ids(update.message)
    # save as log on disk
    formula = utenti.info(update.message) + ": " + update.message.text
    save_info(update.message, formula)
    # callback
    for administrator in admin.get_admins().split("\n"):
        if administrator:
            chat_id = utenti.get_chat_id_from_username(administrator)
            if chat_id:
                await context.bot.send_message(chat_id=chat_id, text="*BOT ACCESO*", parse_mode=ParseMode.MARKDOWN)


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # controllo se nuovo utente e lo aggiungo nel database
    utenti.update_chat_ids(update.message)
    # save as log on disk
    formula = utenti.info(update.message) + ": " + update.message.text
    save_info(update.message, formula)
    # callback
    if update.message.from_user.username in admin.admins:
        await update.message.reply_text("Ciao, sono acceso.")


async def info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # controllo se nuovo utente e lo aggiungo nel database
    utenti.update_chat_ids(update.message)
    # save as log on disk
    formula = utenti.info(update.message) + ": " + update.message.text
    save_info(update.message, formula)
    # callback
    if update.message.from_user.username in admin.admins:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=server_info.get_all_info())


async def error_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update {update} caused error {context.error}')
    