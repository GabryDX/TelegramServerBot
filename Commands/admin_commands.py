#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from time import sleep

from telegram.constants import ParseMode

from Objects import admin, utenti, media

logger = logging.getLogger(__name__)

comandi_admin = ["/admin", "/addadmin", "/getadmins",
                 "/getchatids", "/getdatabaseinfo",
                 "/getpropic", "/reload", "/exec",
                 "/sendall", "/sendmessage"]


async def admin_command(messaggio, bot):
    logger.info("ADMIN COMMAND - START")
    comando_admin = False
    testo = messaggio.text
    contain = False
    i = 0
    while not contain and i < len(comandi_admin):
        if comandi_admin[i] in testo:
            contain = True
        i += 1
    if contain:
        if admin.is_admin(messaggio.from_user.username):
            comando_admin = True
            if testo.startswith("/admin"):
                await messaggio.reply_text(admin.admin(), parse_mode=ParseMode.HTML)
            elif testo.startswith("/addadmin"):
                await messaggio.reply_text(admin.add_admin(messaggio))
            elif testo == "/getadmins":
                await messaggio.reply_text(admin.get_admins_command(), parse_mode=ParseMode.HTML)
            elif testo == "/getchatids":
                await messaggio.reply_text(utenti.get_chat_id_str())
            elif testo == "/getdatabaseinfo":
                await messaggio.reply_text(get_database_info(), parse_mode=ParseMode.HTML)
            elif testo.startswith("/getpropic"):
                await get_propic(messaggio, bot)
            elif testo.startswith("/reload"):
                await reload(messaggio)
            elif testo.startswith("/sendall"):
                await send_all(messaggio, bot)
            elif testo.startswith("/sendmessage"):
                await send_message(messaggio, bot)
            elif testo.startswith("/exec"):
                await execute_server_command(messaggio)
            else:
                comando_admin = False
        else:
            await messaggio.reply_text("<b>Devi essere un amministratore per usare questo comando</b>",
                                       parse_mode=ParseMode.HTML)
    logger.info("ADMIN COMMAND - END")
    return comando_admin


def get_database_info():
    database = "<b>DATABASE</b>\n\n"
    database += "--------------------\n"
    database += "<b>ADMIN</b> " + str(len(admin.admins)) + "\n"
    database += "<b>CHAT IDS</b> " + str(len(utenti.chatIDs)) + "\n"
    database += "--------------------\n"
    database += "<b>AUDIO</b> " + str(len(media.get_audio_list())) + "\n"
    database += "<b>DOCUMENT</b> " + str(len(media.get_document_list())) + "\n"
    database += "<b>PHOTO</b> " + str(len(media.get_photo_list())) + "\n"
    database += "<b>STICKER</b> " + str(len(media.get_sticker_list())) + "\n"
    database += "<b>VIDEO</b> " + str(len(media.get_video_list())) + "\n"
    database += "<b>VIDEONOTE</b> " + str(len(media.get_videonote_list())) + "\n"
    database += "<b>VOICE</b> " + str(len(media.get_voice_list())) + "\n"
    database += "<b>CONTACT</b> " + str(len(media.get_contact_list())) + "\n"
    database += "<b>LOCATION</b> " + str(len(media.get_location_list())) + "\n"
    database += "<b>VENUE</b> " + str(len(media.get_venue_list())) + "\n"
    return database


async def get_propic(messaggio, bot):
    """Invia al chiamante tutte le propic di un utente"""
    testo = messaggio.text
    rimuovi = "/getpropic "
    userid = testo.replace(rimuovi, "", 1)
    if admin.is_digit(userid):
        if userid.startswith("-"):
            chat = bot.get_chat(userid)
            # print(chat)
            chatphoto = chat.photo
            # print(chatphoto)
            chatphotoid = chatphoto.big_file_id
            # print(chatphotoid)
            # messaggio.reply_photo(chatphotoid)
            await messaggio.reply_text(
                "Al momento non è possibile inviare la propic del gruppo, in compenso posso darti questo: "+chatphotoid)
        else:
            listonaphoto = bot.get_user_profile_photos(userid)
            # print(listonaphoto)
            listaphoto = listonaphoto.photos
            # print(listaphoto)
            print("Trovate " + str(len(listaphoto)) + " foto profilo")
            for photo in listaphoto:
                await messaggio.reply_photo(photo[0], photo[0].file_id)
                sleep(2)
    else:
        await messaggio.reply_text("ERRORE: nessun ID trovato o è stato inserito un ID non numerico")


async def reload(messaggio):
    admin.reload_admin()
    utenti.reload_chat_ids()
    await messaggio.reply_text("<b>DATABASE RICARICATO</b>", parse_mode=ParseMode.HTML)


async def send_all(messaggio, bot):
    """Invia un messaggio a tutti gli utenti che hanno usato il bot"""
    testo = messaggio.text
    rimuovi = "/sendall"
    mex = testo.replace(rimuovi, "", 1).strip()
    if len(mex) > 0:
        lista_utenti = utenti.chatIDs
        for uid in lista_utenti:
            await bot.send_message(uid, mex)
            message_to_send = "Messaggio <i>" + mex + "</i> inviato a <b>" + str(uid) + "</b>"
            await messaggio.reply_text(message_to_send, parse_mode=ParseMode.HTML)
            sleep(2)
    else:
        await messaggio.reply_text("Sintassi del comando errata")


async def send_message(messaggio, bot):
    """Invia un messaggio ad uno specifico utente"""
    testo = messaggio.text
    if "[" in testo and "]" in testo:
        rimuovi = "/sendmessage ["
        s = testo.replace(rimuovi, "")
        index = utenti.find_str(s, "]")
        uid = s[:index].replace("]", "")
        mex = s[index:].replace("]", "").strip()
        await bot.send_message(uid, mex)
        message_to_send = "Messaggio <i>" + mex + "</i> inviato a <b>" + str(uid) + "</b>"
        await messaggio.reply_text(message_to_send, parse_mode=ParseMode.HTML)
    else:
        await messaggio.reply_text("Sintassi del comando errata")


async def execute_server_command(messaggio):
    command = messaggio.text.replace("/exec", "", 1).strip()
    if command:
        res = os.popen(command)
        res = res.read().strip()
        res = "<code>" + res + "</code>"
    else:
        res = "Nessun comando da eseguire"
    await messaggio.reply_text(res, parse_mode=ParseMode.HTML)
