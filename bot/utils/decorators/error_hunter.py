import traceback
from functools import wraps
from telegram.error import BadRequest
from bot import DEFAULT_ERROR_CHANNEL_ID, logger, config

def error_hunter(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        try:
            return await func(update, context, *args, **kwargs)
        except Exception as e:
            error = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            # Remove excessive path details for readability
            error = "\n".join(line for line in error.split("\n") if "site-packages" not in line)
            # telegram message limit ?
            error = error[-1800:]

            text = (
                "<blockquote>An error occured</blockquote>\n\n"

                f"<b>• Type:</b> <code>{type(e).__name__}</code>\n"
                f"<b>• Message:</b> <code>{str(e)}</code>\n"
                "<b>• Traceback:</b>\n\n"
                f"<pre>{error}</pre>"
            )
    
            if DEFAULT_ERROR_CHANNEL_ID:
                try:
                    await context.bot.send_message(DEFAULT_ERROR_CHANNEL_ID, text)
                    return
                except BadRequest:
                    pass
                except Exception as e:
                    logger.error(e)
                    return
            # if not DEFAULT_ERROR_CHANNEL_ID or BadRequest
            try:
                await context.bot.send_message(config.owner_id, text)
            except Exception as e:
                logger.error(e)
    return wrapper
