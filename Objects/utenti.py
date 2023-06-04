#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Utils import textfiles
import pathlib
import re

CHATIDS = str(pathlib.Path(__file__).parent.resolve()) + "/../Database/ChatIDs.txt"
chatIDs = []
chatTitles = []


def info(messaggio):
	"""Ritorna una stringa con tutte le informazioni riguardanti il messaggio"""
	if messaggio:  # your bot can receive updates without messages
		utente = messaggio.from_user
		user_id = utente.id
		nome = utente.first_name
		cognome = utente.last_name
		username = utente.username
		data = messaggio.date
		formula = "[" + str(user_id) + "] "
		if nome:
			formula += nome
		if cognome:
			formula += "^" + cognome
		if username:
			formula += "^^^" + username
		formula += " (" + str(data) + ")"
		return formula


def get_full_name(utente):
	"""Ritorna una stringa con le informazioni sull'utente"""
	if utente:
		nome = utente.first_name
		cognome = utente.last_name
		username = utente.username
		titolo = ""
		if nome:
			titolo += nome
		if cognome:
			titolo += "^" + cognome
		if username:
			titolo += "^^^" + username
		return titolo


def get_titolo(chat):
	"""Ritorna una stringa con le informazioni sulla chat"""
	if chat:
		nome = chat.first_name
		cognome = chat.last_name
		title = chat.title
		username = chat.username
		titolo = ""
		if title:
			titolo += title
		else:
			if nome:
				titolo += nome
			if cognome:
				titolo += "^" + cognome
		if username:
			titolo += "^^^" + username
		return titolo


def get_titolo_clean(chat):
	"""Ritorna una stringa con le informazioni sulla chat"""
	if chat:
		nome = chat.first_name
		cognome = chat.last_name
		title = chat.title
		username = chat.username

		titolo = ""
		if title:
			titolo += re.sub(r'[^a-zA-Z0-9\._-]', '', title)
		else:
			if nome:
				titolo += re.sub(r'[^a-zA-Z0-9\._-]', '', nome)
			if cognome:
				titolo += "^" + re.sub(r'[^a-zA-Z0-9\._-]', '', cognome)
		if username:
			titolo += "^^^" + re.sub(r'[^a-zA-Z0-9\._-]', '', username)

		print(titolo)
		return titolo


def reload_chat_ids():
	"""Ricarico informazioni salvate su utenti e chat"""
	if textfiles.exists(CHATIDS):
		lista = textfiles.readLines(CHATIDS)
		del chatIDs[:]
		del chatTitles[:]
		for s in lista:
			if "___" in s:
				index = find_str(s, "___")
				cid = s[:index]
				cid = cid.replace("___", "")
				if cid.isnumeric():
					print(cid)
					chatIDs.extend([int(cid)])
					titolo = s[index:]
					titolo = titolo.replace("___", "")
					chatTitles.extend([titolo])
	else:
		textfiles.write("", CHATIDS)

	print("------------------------------")
	print("CHAT ID UPDATED")
	print(str(len(chatIDs)) + " CHAT ID FOUND")
	print("------------------------------")


def update_chat_ids(messaggio):
	"""Aggiunta o aggiornamento informazioni su utenti e chat vecchi o nuovi"""
	# global chat_id
	# global chatTitles

	if messaggio:  # your bot can receive updates without messages
		utente = messaggio.from_user
		chat = messaggio.chat
		utente_id = utente.id
		utente_id_str = str(utente_id)
		chat_id = chat.id
		chat_id_str = str(chat_id)

		nome = ""
		if utente.first_name:
			nome = utente.first_name
		if utente.last_name:
			nome += "*" + utente.last_name
		if utente.username:
			nome += "***" + utente.username

		titolo = ""
		if chat.title:
			titolo = chat.title
		if chat.username:
			titolo += "***" + chat.username

		riga_u = utente_id_str + "___" + nome
		riga_c = chat_id_str + "___" + titolo

		if utente_id in chatIDs:
			indice = chatIDs.index(utente_id)
			vecchio_nome = chatTitles[indice]
			if vecchio_nome != nome:
				print("NUOVO NOME TROVATO --> AGGIORNAMENTO NOME")
				chatTitles[indice] = nome
				vecchia_riga = utente_id_str + "___" + vecchio_nome
				textfiles.updateLine(vecchia_riga, riga_u, CHATIDS)
				print("L'utente [" + utente_id_str + "] " + vecchio_nome + " è diventato " + nome)
				# i = 0
				# found = False
				# while not found and i < len(chatIDs):
				#     if utente_id == chatIDs[i]:
				#         chatTitles[i] = nome
				#         found = True
				# i += 1
		else:
			print("NUOVO UTENTE TROVATO --> AGGIUNTA UTENTE")
			chatIDs.extend([utente_id])
			chatTitles.extend([nome])
			textfiles.append(riga_u + "\n", CHATIDS)
			print("Nuovo utente [" + utente_id_str + "] " + nome)

		if str(chat_id).startswith("-"):
			if chat_id in chatIDs:
				indice = chatIDs.index(chat_id)
				vecchio_nome = chatTitles[indice]
				if vecchio_nome != titolo:
					print("NUOVO TITOLO CHAT TROVATO --> AGGIORNAMENTO TITOLO")
					chatTitles[indice] = titolo
					vecchia_riga = chat_id_str + "___" + vecchio_nome
					textfiles.updateLine(vecchia_riga, riga_c, CHATIDS)
					print("La chat [" + chat_id_str + "] " + vecchio_nome + " è diventata " + titolo)
					# i = 0
					# found = False
					# while not found and i < len(chatIDs):
					#     if chat_id == chatIDs[i]:
					#         chatTitles[i] = titolo
					#         found = True
					# i += 1
			else:
				print("NUOVA CHAT TROVATA --> AGGIUNTA CHAT")
				chatIDs.extend([chat_id])
				chatTitles.extend([titolo])
				textfiles.append(riga_c, CHATIDS)
				print("Nuova chat [" + chat_id_str + "] " + titolo)


def get_chat_id_str():
	"""ritorna una stringa con le chat concatenate"""
	lista = textfiles.readLines(CHATIDS)
	utenti = ""
	for s in lista:
		utenti += s + "\n"
	return utenti


def get_chat_id_from_username(username):
	"""ritorna il chat id dell'utente con username"""
	username = username.replace("@", "")
	lista = textfiles.readLines(CHATIDS)
	utente = ""
	for s in lista:
		if username in s:
			utente = s
			break
	return utente


# QUESTION: y tho -> è il metodo String.indexOf di Java che manca in Python
def find_str(s, char):
	"""ritorna l'indice in cui si trova il carattere char"""
	index = 0

	if char in s:
		c = char[0]
		for ch in s:
			if ch == c:
				if s[index:index + len(char)] == char:
					return index

			index += 1

	return -1
