#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

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


logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
	"""Run the bot."""
	logger.info("\n --- STARTING BOT ---\n")

	global bot

	# make_dir_if_not_exists(constants.CHAT_DATA_FOLDER)
	make_dir_if_not_exists(constants.DATABASE_FOLDER)
	make_dir_if_not_exists(constants.MEDIA_FOLDER)
	make_dir_if_not_exists(constants.USERS_FOLDER)

	admin.reload_admin()
	utenti.reload_chat_ids()

	# Telegram Bot Authorization Token
	builder = Application.builder()
	builder.token(constants.CUSTOM.BOT_TOKEN)
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
	application.add_handler(CommandHandler("start", commands.start_callback))
	application.add_handler(CommandHandler("info", commands.info_callback))

	# Messages
	application.add_handler(MessageHandler(filters=filters.ALL, callback=commands.command_factory))

	# Errors
	application.add_error_handler(commands.error_callback)

	logger.info("Polling...")
	application.run_polling()


if __name__ == '__main__':
	# with contextlib.suppress(KeyboardInterrupt):  # Ignore exception when Ctrl-C is pressed
	# 	asyncio.run(main())
	main()
