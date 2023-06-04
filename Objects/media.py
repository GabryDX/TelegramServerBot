#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Utils import textfiles
import pathlib

BASE_MEDIA_FOLDER = str(pathlib.Path(__file__).parent.resolve()) + "/../Media/"
AUDIOID = BASE_MEDIA_FOLDER + "Audio.txt"
DOCUMENTID = BASE_MEDIA_FOLDER + "Document.txt"
PHOTOID = BASE_MEDIA_FOLDER + "Photo.txt"
STICKERID = BASE_MEDIA_FOLDER + "Sticker.txt"
VIDEOID = BASE_MEDIA_FOLDER + "Video.txt"
VIDEONOTEID = BASE_MEDIA_FOLDER + "VideoNote.txt"
VOICEID = BASE_MEDIA_FOLDER + "Voice.txt"
CONTACTID = BASE_MEDIA_FOLDER + "Contact.txt"
LOCATIONID = BASE_MEDIA_FOLDER + "Location.txt"
VENUEID = BASE_MEDIA_FOLDER + "Venue.txt"


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
    if textfiles.exists(AUDIOID):
        lista = textfiles.readLines(AUDIOID)
    return lista


def get_document_list():
    """"Ritorna una lista con tutti gli id di document"""
    lista = []
    if textfiles.exists(DOCUMENTID):
        lista = textfiles.readLines(DOCUMENTID)
    return lista


def get_photo_list():
    """"Ritorna una lista con tutti gli id di photo"""
    lista = []
    if textfiles.exists(PHOTOID):
        lista = textfiles.readLines(PHOTOID)
    return lista


def get_sticker_list():
    """"Ritorna una lista con tutti gli id di sticker"""
    lista = []
    if textfiles.exists(STICKERID):
        lista = textfiles.readLines(STICKERID)
    return lista


def get_video_list():
    """"Ritorna una lista con tutti gli id di video"""
    lista = []
    if textfiles.exists(VIDEOID):
        lista = textfiles.readLines(VIDEOID)
    return lista


def get_videonote_list():
    """"Ritorna una lista con tutti gli id di videonote"""
    lista = []
    if textfiles.exists(VIDEONOTEID):
        lista = textfiles.readLines(VIDEONOTEID)
    return lista


def get_voice_list():
    """"Ritorna una lista con tutti gli id di voice"""
    lista = []
    if textfiles.exists(VOICEID):
        lista = textfiles.readLines(VOICEID)
    return lista


def get_contact_list():
    """"Ritorna una lista con tutti gli id di contact"""
    lista = []
    if textfiles.exists(CONTACTID):
        lista = textfiles.readLines(CONTACTID)
    return lista


def get_location_list():
    """"Ritorna una lista con tutti gli id di location"""
    lista = []
    if textfiles.exists(LOCATIONID):
        lista = textfiles.readLines(LOCATIONID)
    return lista


def get_venue_list():
    """"Ritorna una lista con tutti gli id di venue"""
    lista = []
    if textfiles.exists(VENUEID):
        lista = textfiles.readLines(VENUEID)
    return lista

# TODO metodo per rimuovere i doppioni nei file
# TODO liste utilizzabili per i get dei file
