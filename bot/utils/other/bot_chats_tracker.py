from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.utils.database import MemoryDB, MongoDB

async def bot_chats_tracker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    **Tracks private chat (where bot is Started/Blocked)**
    """
    chat = update.effective_chat
    chat_update = update.my_chat_member

    user = chat_update.from_user
    new_status = chat_update.new_chat_member.status

    if chat.type in [ChatType.PRIVATE]:
        # checking database entry
        user_data = MongoDB.find_one("users_data", "user_id", user.id)
        if not user_data:
            data = {
                "user_id": user.id,
                "name": user.full_name,
                "username": user.username,
                "lang": user.language_code
            }

            MongoDB.insert("users_data", data)
            MemoryDB.insert("users_data", user.id, data)
        
        # checking member status & updating database
        active_status = new_status == ChatMember.MEMBER
        MongoDB.update("users_data", "user_id", user.id, "active_status", active_status)
    
    elif chat.type in [ChatType.CHANNEL] and new_status == ChatMember.ADMINISTRATOR:
        await user.send_message(f"You have added me in {chat.title}\nChatID: <code>{chat.id}</code>")
