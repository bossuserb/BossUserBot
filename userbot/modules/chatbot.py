# Copyright (C) 2019 The HydraBots 
#
# Licensed under the Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Siri UserBot - Berceste

# credit @sandy1709 
#

from userbot.events import register
from userbot import rs_client, AI_LANG, RANDOM_STUFF_API_KEY,MYID
import asyncio
import logging
from userbot.cmdhelp import CmdHelp
from telethon.utils import get_display_name


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# ██████ LANGUAGE CONSTANTS ██████ #

#from userbot.language import get_value
#LANG = get_value("chatbot") # Sonradan eklenicek

# ████████████████████████████████ #

try:
    from userbot.modules.sql_helper.chatbot_sql import (
    addai,
    get_all_users,
    get_users,
    is_added,
    remove_ai,
    remove_all_users,
    remove_users,
) 
except:
    logging.log(level=logging.WARNING,
                msg="ChatBot data bağlantısı uğursuz oldu")


@register(outgoing=True, pattern="^.addai$")
async def add_chatbot(event):
    "Yanıtlanan kişi üçün zəkayı etkin edir"
    if not RANDOM_STUFF_API_KEY:
        return await event.edit(
            "`ChatBot'u etkinləştirmek üçün bir API key ayarlayın! `"
        )
    if event.reply_to_msg_id is None:
        return await event.edit(
            "`ChatBot'u etkinləştirmək üçün bir userin mesajını yanıtlayın! `"
        )
    catevent = await event.edit("`Useri ChatBot'a salıram...`")
    previous_message = await event.get_reply_message()
    user = await event.client.get_entity(previous_message.from_id)
    if not user:
        return
    reply_msg = await event.get_reply_message()
    chat_id = event.chat_id
    user_id = reply_msg.sender_id
    if event.is_private:
        chat_name = user.first_name
        chat_type = "Personal"
    else:
        chat_name = event.chat.title
        chat_type = "Group"
    user_name = user.first_name
    user_username = user.username
    if is_added(chat_id, user_id):
        return await event.edit("`User də  ChatBot etkinləştirildi.`")
    try:
        addai(chat_id, user_id, chat_name, user_name, user_username, chat_type)
    except Exception as e:
        await event.edit(f"**Error:**\n`{str(e)}`")
    else:
        await event.reply("`🐟 Uğurlu!`")

@register(outgoing=True, pattern="^.remai$")
async def remove_chatbot(event):
    "Kullanıcı için ChatBot'u durdurmak"
    if not RANDOM_STUFF_API_KEY:
        return await event.edit(
            "`ChatBot'u etkinləştirmek üçün2 bir API key ayarlayın! `"
        )
    if event.reply_to_msg_id is None:
        return await event.edit(
            "Yapay zekayı durdurmak için bir kullanıcının mesajını yanıtlayın."
        )
    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    chat_id = event.chat_id
    if is_added(chat_id, user_id):
        try:
            remove_ai(chat_id, user_id)
        except Exception as e:
            await event.edit(f"**Error:**\n`{str(e)}`")
        else:
            await event.edit("`ChatBot kullanıcı için durduruldu!`")
    else:
        await event.edit("`Kullanıcıda zaten ChatBot etkinleştirilmedi!`")


#@register(incoming=True, disable_edited=True,disable_errors=True)
@register(incoming=True, disable_edited=True)
async def ai_reply(event):
    if is_added(event.chat_id, event.sender_id) and (event.message.text):
        global AI_LANG
        master_name = get_display_name(await event.client.get_me())
        response = await rs_client.get_ai_response(
            message=event.message.text,
            server="primary",
            master="SiriUserbot",
            bot=master_name,
            uid=MYID,
            language=AI_LANG,
        )
        await event.reply(response.message)

CmdHelp('chatbot').add_command(
    'addai', '<yanıtlayaraq>', 'ChatBot\'un avto söhbətini etkinləştirir.'
).add_command(
    'remai', '<yanıtlayaraq>', 'ChatBot\'un avto söhbətini geri buraxır.'
).add()
