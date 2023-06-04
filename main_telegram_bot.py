#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import pathlib

import telegram  # python-telegram-bot
from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, ApplicationBuilder, MessageHandler, filters

from Commands import commands
from Utils import constants, server_info
from Utils.textfiles import exists_dir, make_dir_if_not_exists

from Objects import admin, utenti


bot = None
timeout = 120
USER_FOLDER = str(pathlib.Path(__file__).parent.resolve()) + "/Users"
MEDIA_FOLDER = str(pathlib.Path(__file__).parent.resolve()) + "/Media"
DATABASE_FOLDER = str(pathlib.Path(__file__).parent.resolve()) + "/Database"


logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def init_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
	for administrator in admin.get_admins().split("\n"):
		if administrator:
			chat_id = utenti.get_chat_id_from_username(administrator)
			if chat_id:
				await context.bot.send_message(chat_id=chat_id, text="*BOT ACCESO*", parse_mode=ParseMode.MARKDOWN)


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if update.effective_user.username in admin.admins:
		await update.message.reply_text("Ciao, sono acceso.")


async def info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if update.effective_user.username in admin.admins:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=server_info.get_all_info())


async def error_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
	logger.error(f'Update {update} caused error {context.error}')


def main():
	"""Run the bot."""
	global bot

	# make_dir_if_not_exists(constants.CHAT_DATA_FOLDER)
	make_dir_if_not_exists(DATABASE_FOLDER)
	make_dir_if_not_exists(MEDIA_FOLDER)
	make_dir_if_not_exists(USER_FOLDER)

	logger.info("\n --- STARTING BOT ---\n")

	admin.reload_admin()
	utenti.reload_chat_ids()

	# Telegram Bot Authorization Token
	builder = Application.builder()
	builder.token(constants.BOT_TOKEN)
	builder.connect_timeout(timeout)
	builder.pool_timeout(timeout)
	builder.read_timeout(timeout)
	builder.write_timeout(timeout)
	builder.get_updates_connect_timeout(timeout)
	builder.get_updates_pool_timeout(timeout)
	builder.get_updates_read_timeout(timeout)
	builder.get_updates_write_timeout(timeout)
	application = builder.build()
	# application = ApplicationBuilder().token(constants.BOT_TOKEN).build()

	bot = ContextTypes.DEFAULT_TYPE.bot

	logger.info("listening for new messages...")

	# Commands
	application.add_handler(CommandHandler("start", start_callback))
	application.add_handler(CommandHandler("info", info_callback))

	# Messages
	application.add_handler(MessageHandler(filters=filters.ALL, callback=commands.command_factory))

	# Errors
	application.add_error_handler(error_callback)

	logger.info("Polling...")
	application.run_polling()


if __name__ == '__main__':
	# with contextlib.suppress(KeyboardInterrupt):  # Ignore exception when Ctrl-C is pressed
	# 	asyncio.run(main())
	main()
