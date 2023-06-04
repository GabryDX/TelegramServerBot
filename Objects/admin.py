#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Comandi per gli admin
"""

from Utils import textfiles
import pathlib

ADMIN = str(pathlib.Path(__file__).parent.resolve()) + "/../Database/Admin.txt"
admins = []


def admin():
    comandi = "*COMANDI ADMIN:*\n\n"
    comandi += "*/addadmin* Seguito da @username, aggiunge l'username alla lista degli admin.\n"
    comandi += "*/admin* Mostra i comandi utilizzabili esclusivamente dagli admin.\n"
    comandi += "*/getadmins* Mostra una lista con tutti gli admin.\n"
    comandi += "*/getchatids* Restituisce tutti gli ID delle chat in cui è stato utilizzato "
    comandi += "il Bot con relativo nome della chat.\n"
    comandi += "*/getdatabaseinfo* Mostra le informazioni su tutti i Database del Bot.\n"
    comandi += "*/getpropic* _Seguito dallo user ID_, restituisce tutte le immagini del profilo "
    comandi += "della persona corrispondente a quell'ID.\n"
    comandi += "*/reload* Riavvia i Database ricaricando gli ID dai file.\n"
    comandi += "*/sendall* _Seguito da un messaggio_, invia il messaggio a tutti gli utenti che hanno usato il Bot.\n"
    comandi += "*/sendmessage* _Seguito da [ID chat] e da un messaggio_, "
    comandi += "invia il messaggio alla chat con l'ID inserito.\n"
    comandi += "\n*SPECIALI*\n"
    comandi += "*/aggiungititolo* seguito da [ID azione] e dal nome dell'azione, "
    comandi += "aggiunge una nuova azione alla lista delle azioni seguite.\n"
    return comandi


def add_admin(messaggio):
    testo = messaggio.text
    rimuovi = "/addadmin @"
    if testo.startswith(rimuovi):
        adm = testo.replace(rimuovi, "")
        textfiles.append(adm + "\n", ADMIN)
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
    testo = "*ADMINS:*\n\n"
    testo += get_admins()
    return testo


def is_admin(user):
    return user in admins


def reload_admin():
    if textfiles.exists(ADMIN):
        lista = textfiles.readLines(ADMIN)
        del admins[:]
        for s in lista:
            admins.extend([s])
    else:
        textfiles.write("", ADMIN)


def is_digit(n):
    try:
        float(n)
        return True
    except ValueError:
        return False
