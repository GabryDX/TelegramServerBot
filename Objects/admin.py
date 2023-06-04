#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Comandi per gli admin
"""

from Utils import constants, textfiles

admins = []


def admin():
    comandi = "<b>COMANDI ADMIN:</b>\n\n"
    comandi += "<b>/addadmin<b> Seguito da @username, aggiunge l'username alla lista degli admin.\n"
    comandi += "<b>/admin<b> Mostra i comandi utilizzabili esclusivamente dagli admin.\n"
    comandi += "<b>/getadmins<b> Mostra una lista con tutti gli admin.\n"
    comandi += "<b>/getchatids<b> Restituisce tutti gli ID delle chat in cui è stato utilizzato "
    comandi += "il Bot con relativo nome della chat.\n"
    comandi += "<b>/getdatabaseinfo<b> Mostra le informazioni su tutti i Database del Bot.\n"
    comandi += "<b>/getpropic<b> <i>Seguito dallo user ID</i>, restituisce tutte le immagini del profilo "
    comandi += "della persona corrispondente a quell'ID.\n"
    comandi += "<b>/reload<b> Riavvia i Database ricaricando gli ID dai file.\n"
    comandi += "<b>/sendall<b> <i>Seguito da un messaggio</i>, invia il messaggio a tutti gli utenti che hanno usato il Bot.\n"
    comandi += "<b>/sendmessage<b> <i>Seguito da [ID chat] e da un messaggio</i>, "
    comandi += "invia il messaggio alla chat con l'ID inserito.\n"
    comandi += "\n<b>SPECIALI</b>\n"
    comandi += "<b>/aggiungititolo<b> seguito da [ID azione] e dal nome dell'azione, "
    comandi += "aggiunge una nuova azione alla lista delle azioni seguite.\n"
    return comandi


def add_admin(messaggio):
    testo = messaggio.text
    rimuovi = "/addadmin @"
    if testo.startswith(rimuovi):
        adm = testo.replace(rimuovi, "")
        textfiles.append(adm + "\n", constants.ADMIN_FILE)
        admins.extend([adm])
        return "L'admin @" + adm + " è stato aggiunto."
    else:
        return "ERRORE: formulazione della richiesta"


def get_admins():
    testo = ""
    for a in admins:
        testo += "@" + a + "\n"
    return testo


def get_admins_command():
    testo = "<b>ADMINS:</b>\n\n"
    testo += get_admins()
    return testo


def is_admin(user):
    return user in admins


def reload_admin():
    if textfiles.exists(constants.ADMIN_FILE):
        lista = textfiles.readLines(constants.ADMIN_FILE)
        del admins[:]
        for s in lista:
            admins.extend([s])
    else:
        textfiles.write("", constants.ADMIN_FILE)


def is_digit(n):
    try:
        float(n)
        return True
    except ValueError:
        return False
