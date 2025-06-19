from telegram import Update, ReactionTypeEmoji
from telegram.ext import ContextTypes
from telegram.constants import MessageOriginType
from telegram.error import Forbidden
from bot import config
from bot.helpers import BuildKeyboard
from bot.utils.decorators.error_hunter import error_hunter

@error_hunter
async def func_filterAll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message
    re_msg = message.reply_to_message
    victim_id = None

    if user.id == config.owner_id:
        # this section is for owner logic
        if not re_msg:
            await message.reply_text("Reply to user messages to send the message.")
            return
        
        # getting victim_id
        if re_msg.forward_origin:
            # if victim account isn't hidden
            if re_msg.forward_origin.type != MessageOriginType.HIDDEN_USER:
                victim_id = re_msg.forward_origin.sender_user.id
        else:
            # if victim is hidden
            if re_msg.from_user.is_bot:
                check_msg = re_msg.text.split("#id")
                if len(check_msg) >= 2:
                    victim_id = check_msg[1]
                else:
                    await message.reply_text("You have replied the wrong message.")
                    return
            else:
                await message.reply_text("Reply to user messages to send the message.")
                return
        
        if not victim_id:
            await message.reply_text("Error: victim_id not found!")
            return
        
        # check message type and send message to victim
        try:
            text = message.text_html
            caption = message.caption_html
            photo = message.photo
            audio = message.audio
            video = message.video
            document = message.document
            voice = message.voice
            video_note = message.video_note
            reaction = "👍"

            if text:
                await context.bot.send_message(victim_id, text)

            elif photo:
                await context.bot.send_photo(victim_id, photo[-1].file_id, caption)

            elif audio:
                await context.bot.send_audio(victim_id, audio.file_id, title=audio.file_name, caption=caption, filename=audio.file_name)

            elif video:
                await context.bot.send_video(victim_id, video.file_id, caption=caption)

            elif document:
                await context.bot.send_document(victim_id, document.file_id, caption, filename=document.file_name)
            
            elif voice:
                await context.bot.send_voice(victim_id, voice.file_id, caption=caption)
            
            elif video_note:
                await context.bot.send_video_note(victim_id, video_note.file_id)
            
            else:
                await message.reply_text("This message type isn't added yet!")
                return
        except Forbidden:
            reaction = "👎"
        except:
            reaction = "🤷‍♂"

        await message.set_reaction([ReactionTypeEmoji(reaction)])
    
    else:
        # this section is for user logic
        try:
            forward_message = await message.forward(config.owner_id)
            reaction = "👍"
        except Exception as e:
            await message.reply_text(str(e))
            forward_message = None
            reaction = "👎"
        
        await message.set_reaction([ReactionTypeEmoji(reaction)])

        if not forward_message:
            return
        
        # if user is hidden or its audio file
        if forward_message.audio or forward_message.forward_origin.type == MessageOriginType.HIDDEN_USER:
            text = (
                f"» To answer {user.mention_html()} reply to this message!!\n\n"
                f"<b>User Info:</b>\n"
                f"<b>Name:</b> <code>{user.full_name}</code>\n"
                f"<b>Mention:</b> {user.mention_html()}\n"
                f"<b>Username:</b> {user.name}\n"
                f"<b>ID:</b> <code>{user.id}</code>\n"
                f"<b>Lang:</b> <code>{user.language_code}</code>\n"
                f"#id{user.id}"
            )
            
            btn = BuildKeyboard.ubutton([{"User Profile": f"tg://user?id={user.id}"}]) if user.username else None
            await context.bot.send_message(config.owner_id, text, reply_markup=btn)
