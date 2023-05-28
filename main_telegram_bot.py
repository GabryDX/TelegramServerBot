#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import asyncio
import contextlib
import logging
import os

import telegram  # python-telegram-bot
from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, ApplicationBuilder, MessageHandler, filters

from Commands import commands
from Utils import constants, server_info
from Utils.textfiles import exists_dir

from Objects import admin, utenti


bot = None
read_timeout = 10
USER_FOLDER = "Users"
MEDIA_FOLDER = "Media"
DATABASE_FOLDER = "Database"


logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
	for administrator in admin.get_admins().split("\n"):
		if administrator:
			chat_id = utenti.get_chat_id_from_username(administrator)
			if chat_id:
				await context.bot.send_message(chat_id=chat_id, text="*BOT ACCESO*", parse_mode=ParseMode.MARKDOWN)


async def info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if update.effective_user.username in admin.admins:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=server_info.get_all_info)


def main():
	"""Run the bot."""
	global bot

	if not os.path.exists(constants.CHAT_DATA_FOLDER):
		os.makedirs(constants.CHAT_DATA_FOLDER)

	print("\n --- AVVIO DEL BOT ---\n")
	admin.reload_admin()
	utenti.reload_chat_ids()
	exists_dir(DATABASE_FOLDER)
	exists_dir(USER_FOLDER)

	# Telegram Bot Authorization Token
	# builder = Application.builder()
	# builder.token(constants.BOT_TOKEN)
	# # builder.read_timeout(read_timeout)
	# application = builder.build()
	application = ApplicationBuilder().token(constants.BOT_TOKEN).build()

	bot = ContextTypes.DEFAULT_TYPE.bot

	logger.info("listening for new messages...")

	#application.add_handler(CommandHandler("start", start_callback))
	#application.add_handler(MessageHandler(filters=filters.ALL, callback=commands.command_factory))
	application.add_handler(CommandHandler("info", info_callback))


	application.run_polling()


if __name__ == '__main__':
	# with contextlib.suppress(KeyboardInterrupt):  # Ignore exception when Ctrl-C is pressed
	# 	asyncio.run(main())
	main()
