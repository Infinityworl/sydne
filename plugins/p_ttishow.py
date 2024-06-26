import random, os, sys
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import ADMINS, LOG_CHANNEL
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import get_size, temp, get_settings
from Script import script
from pyrogram.errors import ChatAdminRequired


@Client.on_chat_member_updated(filters.group)
async def welcome(bot, message):
    if message.new_chat_member and not message.old_chat_member:
        if message.new_chat_member.user.id == temp.ME:
            buttons = [[
                InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇ', url=UPDATES_LINK),
                InlineKeyboardButton('ꜱᴜᴘᴘᴏʀᴛ', url=SUPPORT_LINK)
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            user = message.from_user.mention if message.from_user else "Dear"
            await bot.send_photo(chat_id=message.chat.id, photo=random.choice(PICS), caption=f"👋 Hello {user},\n\nThank you for adding me to the <b>'{message.chat.title}'</b> group, Don't forget to make me admin. If you want to know more ask the support group. 😘</b>", reply_markup=reply_markup)
            if not await db.get_chat(message.chat.id):
                total = await bot.get_chat_members_count(message.chat.id)
                username = f'@{message.chat.username}' if message.chat.username else 'Private'
                await bot.send_message(LOG_CHANNEL, script.NEW_GROUP_TXT.format(message.chat.title, message.chat.id, username, total))       
                await db.add_chat(message.chat.id, message.chat.title)
            return
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            WELCOME = settings['welcome_text']
            welcome_msg = WELCOME.format(
                mention = message.new_chat_member.user.mention,
                title = message.chat.title
            )
            await bot.send_message(chat_id=message.chat.id, text=welcome_msg)
