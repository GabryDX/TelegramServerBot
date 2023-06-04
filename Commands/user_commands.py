#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from random import randrange

from telegram import ReplyKeyboardMarkup
from telegram.constants import ParseMode

from Objects import admin, utenti
from Objects.media import get_document_list, get_photo_list
from Utils.server_info import get_all_info

MARKDOWN = ParseMode.MARKDOWN
MARKDOWN_V2 = ParseMode.MARKDOWN_V2
logger = logging.getLogger(__name__)

# default_menu_keyboard = [['Azioni'], ['Dati correnti', 'Valori migliori'], ['Test', 'Info']]
# default_menu_markup = ReplyKeyboardMarkup(default_menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
sub_menu = {"scegli_titolo": False, "compra_vendi": False, "compra": False, "vendi": False, "soglia": False, "soglia_value": ""}


def default_menu(messaggio):
	default_menu_keyboard = [['Menu', 'Azioni'], ['Dati correnti', 'Valori migliori']]
	if admin.is_admin(messaggio.from_user.username):
		default_menu_keyboard += [['Info']]

	default_menu_markup = ReplyKeyboardMarkup(default_menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
	return default_menu_markup


async def user_command(messaggio):
	logger.info("USER COMMAND - START")
	testo = messaggio.text.lower()
	if testo == "/start" or testo == "menu":
		# text = "INIZIO"
		text = get_main_menu()
		await messaggio.reply_text(text, reply_markup=default_menu(messaggio), parse_mode=MARKDOWN_V2)
	elif testo == "test":
		await messaggio.reply_text("TEST", reply_markup=default_menu(messaggio))
	elif testo.startswith("/comandi"):
		comandi = "*COMANDI UTENTE:*\n\n*/start* Messaggio iniziale di benvenuto\n"
		comandi += "*/comandi* Lista dei comandi utente\n"
		comandi += "/*random_pic* Invia un'immagine presa causalmente dal database\n"
		comandi += "/*raspberry* Informazioni sul server raspberry"
		await messaggio.reply_text(comandi, parse_mode=MARKDOWN)
	elif testo == "torna al menu":
		await messaggio.reply_text(get_main_menu(), reply_markup=default_menu(messaggio), parse_mode=MARKDOWN_V2)
		for key in sub_menu:
			if isinstance(sub_menu[key], str):
				sub_menu[key] = ""
			else:
				sub_menu[key] = False
	if admin.is_admin(messaggio.from_user.username):
		if testo == "info":
			menu_keyboard = [['Server'], ["Ricarica Database"], ['Torna al menu']]
			menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
			await messaggio.reply_text(text="Vuoi le informazioni sul server?", reply_markup=menu_markup)
		elif testo == "ricarica database":
			await reload_database(messaggio)
		elif testo == "server":
			try:
				await messaggio.reply_text(get_all_info(), reply_markup=default_menu(messaggio))
			except Exception as e:
				await messaggio.reply_text("Non mi trovo su server Linux in questo momento",
									 reply_markup=default_menu(messaggio))
				# messaggio.reply_text(str(e), reply_markup=default_menu_markup)
	print(sub_menu)
	logger.info("USER COMMAND - END")


# elif testo.startswith("/tastiera"):
# 	messaggio.reply_text("aaa")
# 	keyboard = [['7', '8', '9'],['4', '5', '6'],['1', '2', '3'],['0']]
# 	menu_keyboard = [['MenuItem1'], ['MenuItem2']]
# 	menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
# 	messaggio.reply_text(text='Some text here', reply_markup=menu_markup)


async def get_random_pic(messaggio):
	lista = get_photo_list()
	if len(lista) > 0:
		r = randrange(0, len(lista))
		await messaggio.reply_photo(lista[r], reply_markup=default_menu(messaggio))
	else:
		await messaggio.reply_text("Non ho meme al momento, mandamene uno.", reply_markup=default_menu(messaggio))


async def get_random_doc(messaggio):
	lista = get_document_list()
	if len(lista) > 0:
		r = randrange(0, len(lista))
		await messaggio.reply_document(lista[r], reply_markup=default_menu(messaggio))
	else:
		await messaggio.reply_text("Non ho meme al momento, mandamene uno.", reply_markup=default_menu(messaggio))


def get_main_menu():
	info = ""
	# ordered = sorted(azioni.azioni_id)
	# borsa = [x for x in ordered if "-EUR" not in x]
	# crypto = [x for x in ordered if "-EUR" in x]
	# listona = [borsa, crypto]
	# titolo = "🔁 AZIONE    PREZZO    SOGLIA\n"
	# titolo2 = "\n\n🆕 CRIPTOVALUTE"
	#
	# for lista in listona:
	# 	if info:
	# 		info += titolo2
	# 	for key in lista:
	# 		if info:
	# 			info += "\n"
	# 		space = "          "[len(key):]
	# 		if key in azioni.azioni_comprate:
	# 			info += "✅ "
	# 		else:
	# 			info += "❌ "
	#
	# 		last = "0"
	# 		if key in analisi_azioni.last_detected:
	# 			if analisi_azioni.last_detected[key] < 10.0:
	# 				last = str(round(analisi_azioni.last_detected[key], 3))
	# 			else:
	# 				last = str(round(analisi_azioni.last_detected[key], 2))
	# 		space2 = "          "[len(last):]
	#
	# 		soglia = "0"
	# 		if key in azioni.azioni_soglia:
	# 			soglia = str(azioni.azioni_soglia[key])
	#
	# 		info += key + space + last + space2 + soglia
	# text = "Menu Principale:\n\n```\n" + titolo + info + "\n```"
	text = "MENU"
	return text


async def reload_database(messaggio):
	admin.reload_admin()
	utenti.reload_chat_ids()
	await messaggio.reply_text("<b>Database ricaricato</b>", reply_markup=default_menu(messaggio),
						 parse_mode=ParseMode.HTML)
