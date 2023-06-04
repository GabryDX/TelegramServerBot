#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Utils import constants, textfiles


def get_contact(contact):
    """"Ritorna una stringa con le informazioni su un contatto"""
    if contact:
        numero = contact.phone_number
        nome = contact.first_name
        cognome = contact.last_name
        userid = str(contact.user_id)
        contatto = "[" + numero + "] "
        if nome:
            contatto += nome
        if cognome:
            contatto += "^" + cognome
        if userid:
            contatto += "(" + userid + ")"
        return contatto


def get_location(location):
    """"Ritorna una stringa con le informazioni su un contatto"""
    if location:
        lon = str(location.longitude)
        lat = str(location.latitude)
        localita = "Coordinate: (" + lon + ", " + lat + ")"
        return localita


def get_venue(venue):
    """"Ritorna una stringa con le informazioni su un contatto"""
    if venue:
        location = get_location(venue.location)
        nome = venue.title
        indirizzo = venue.address
        edificio = venue.foursquare_id
        via = location + " - Via: " + nome + " " + indirizzo
        if edificio:
            via += " Edificio: " + edificio
        return via


def get_audio_list():
    """"Ritorna una lista con tutti gli id di audio"""
    lista = []
    if textfiles.exists(constants.AUDIOID_FILE):
        lista = textfiles.readLines(constants.AUDIOID_FILE)
    return lista


def get_document_list():
    """"Ritorna una lista con tutti gli id di document"""
    lista = []
    if textfiles.exists(constants.DOCUMENTID_FILE):
        lista = textfiles.readLines(constants.DOCUMENTID_FILE)
    return lista


def get_photo_list():
    """"Ritorna una lista con tutti gli id di photo"""
    lista = []
    if textfiles.exists(constants.PHOTOID_FILE):
        lista = textfiles.readLines(constants.PHOTOID_FILE)
    return lista


def get_sticker_list():
    """"Ritorna una lista con tutti gli id di sticker"""
    lista = []
    if textfiles.exists(constants.STICKERID_FILE):
        lista = textfiles.readLines(constants.STICKERID_FILE)
    return lista


def get_video_list():
    """"Ritorna una lista con tutti gli id di video"""
    lista = []
    if textfiles.exists(constants.VIDEOID_FILE):
        lista = textfiles.readLines(constants.VIDEOID_FILE)
    return lista


def get_videonote_list():
    """"Ritorna una lista con tutti gli id di videonote"""
    lista = []
    if textfiles.exists(constants.VIDEONOTEID_FILE):
        lista = textfiles.readLines(constants.VIDEONOTEID_FILE)
    return lista


def get_voice_list():
    """"Ritorna una lista con tutti gli id di voice"""
    lista = []
    if textfiles.exists(constants.VOICEID_FILE):
        lista = textfiles.readLines(constants.VOICEID_FILE)
    return lista


def get_contact_list():
    """"Ritorna una lista con tutti gli id di contact"""
    lista = []
    if textfiles.exists(constants.CONTACTID_FILE):
        lista = textfiles.readLines(constants.CONTACTID_FILE)
    return lista


def get_location_list():
    """"Ritorna una lista con tutti gli id di location"""
    lista = []
    if textfiles.exists(constants.LOCATIONID_FILE):
        lista = textfiles.readLines(constants.LOCATIONID_FILE)
    return lista


def get_venue_list():
    """"Ritorna una lista con tutti gli id di venue"""
    lista = []
    if textfiles.exists(constants.VENUEID_FILE):
        lista = textfiles.readLines(constants.VENUEID_FILE)
    return lista

# TODO metodo per rimuovere i doppioni nei file
# TODO liste utilizzabili per i get dei file
