import asyncio
import aiohttp

from telegram import Update, LinkPreviewOptions, BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    InlineQueryHandler,
    filters,
    CallbackQueryHandler,
    ChatMemberHandler,
    ContextTypes,
    Defaults
)
from telegram.error import BadRequest
from telegram.constants import ChatID, ParseMode

from . import DEFAULT_ERROR_CHANNEL_ID, RUN_SERVER, bot, logger, config
from .utils.alive import alive
from .utils.update_db import update_database
from .utils.database import MemoryDB

from .handlers import (
    func_start,
    func_help,

    func_id,
    func_info,

    func_filterAll
)

from .utils.other.bot_chats_tracker import bot_chats_tracker


async def post_init():
    try:
        await bot.set_my_commands([
            BotCommand("start", "Introducing..."),
            BotCommand("help", "Bots help section...")
        ])
    except Exception as e:
        logger.error(e)

    # Send alive message to bot owner
    try:
        await bot.send_message(config.owner_id, "<blockquote><b>Bot Started!</b></blockquote>", parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(e)
    
    logger.info("Bot Started...")


async def server_alive():
    # executing after updating database so getting data from memory...
    if not RUN_SERVER:
        return
    
    server_url = MemoryDB.bot_data.get("server_url")
    if not server_url:
        logger.warning("'Server URL' wasn't found. Bot may fall asleep if deployed on Render (free instance)")
        return
    
    while True:
        # everytime check if there is new server_url
        server_url = MemoryDB.bot_data.get("server_url")
        if not server_url:
            return
        if server_url[0:4] != "http":
            server_url = f"http://{server_url}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(server_url) as response:
                    if not response.ok:
                        logger.warning(f"{server_url} is down or unreachable. ❌ - code - {response.status}")
        except Exception as e:
            logger.error(f"{server_url} > {e}")
        await asyncio.sleep(180) # 3 min


def main():
    default_param = Defaults(
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        block=False,
        allow_sending_without_reply=True
    )

    application = ApplicationBuilder().token(config.bot_token).defaults(default_param).build()

    main_handlers = [
        CommandHandler("start", func_help, filters.Regex("help")), # this need to register before main start handler
        # core func
        CommandHandler("start", func_start),
        CommandHandler("help", func_help),
        # group management func
        # CommandHandler("server", func_server),
        # owner func
        # CommandHandler("broadcast", func_broadcast),
        # CommandHandler("database", func_database),
        # CommandHandler("log", func_log),
        # CommandHandler("say", func_say),
        # CommandHandler("send", func_send),
        # CommandHandler("shell", func_shell),
        # CommandHandler("sys", func_sys),
        # user func
        CommandHandler("id", func_id),
        CommandHandler("info", func_info)
    ]

    # main handlers register
    application.add_handlers(main_handlers)
    # Bot chat tracker (PRIVATE: only if bot is blocked or unblocked;)
    application.add_handler(ChatMemberHandler(bot_chats_tracker, ChatMemberHandler.MY_CHAT_MEMBER))
    # filterALL : Core for this bot
    application.add_handler(MessageHandler(filters.ALL, func_filterAll))

    

    # # Inline Query Handler
    # application.add_handler(InlineQueryHandler(inline_query.inline_query_handler))

    # # Callback query handlers
    # application.add_handlers([
    #     CallbackQueryHandler(query_help_menu.query_help_menu, "help_menu_[A-Za-z0-9]+"),
    #     CallbackQueryHandler(query_bot_settings.query_bot_settings, "bsettings_[A-Za-z0-9]+"),
    #     CallbackQueryHandler(query_chat_settings.query_chat_settings, "csettings_[A-Za-z0-9]+"),
    #     CallbackQueryHandler(query_admin_task.query_groupManagement, "admin_[A-Za-z0-9]+"),
    #     CallbackQueryHandler(query_misc.query_misc, "misc_[A-Za-z0-9]+"),
    #     CallbackQueryHandler(query_broadcast.query_broadcast, "broadcast_[A-Za-z0-9]+"),
    #     CallbackQueryHandler(query_db_editing.query_db_editing, "database_[A-Za-z0-9]+")
    # ])

    # Check Updates
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


async def app_init():
    if RUN_SERVER:
        alive() # Server breathing
    # maintain the sequence
    update_database()
    await post_init()
    await server_alive()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(app_init())
    loop.create_task(main())
    loop.run_forever()
