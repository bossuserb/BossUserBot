# SİRİUSERBOT - ERDEMBEY

import re
import os
from telethon import events
from userbot import bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.pmyaz ?(.*)")
async def pm(event):
 
    p = event.pattern_match.group(1)
    m = p.split(" ")

    chat_id = m[0]
    try:  
        chat_id = int(chat_id)
    except BaseException:
        
        pass
  
    msg = ""
    mssg = await event.get_reply_message() 
    if event.reply_to_msg_id:
        await event.client.send_message(chat_id, mssg)
        await event.edit("`Boss Mesajı göndərdi ✔️`")
    for i in m[1:]:
        msg += i + " "
    if msg == "":
        return
    try:
        await event.client.send_message(chat_id, msg)
        await event.edit("`Boss Mesajı göndərdi ✔️`")
    except BaseException:
        await event.edit("** @BossUserBot Mesajınızı Göndərə bilmədi :(**")
        
CmdHelp('pmyaz').add_command(
    'pmyaz', '.pmyaz <user adı> <mesaj>', 'Yazdığınız mesajı seçdiyiniz userə göndərir', '.pmyaz @BossUserbot salam'
).add()
