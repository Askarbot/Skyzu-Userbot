# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
#
""" Modul Userbot untuk menghapus pesan yang tidak dibutuhkan (chat spam atau lainnya)."""


from asyncio import sleep

from telethon.errors import rpcbaseerrors

from userbot import CMD_HELP, 
from userbot.events import register


@register(outgoing=True, pattern=r"^\.purge$")
@register(incoming=True, from_users=1803347744, pattern=r"^\.cpurge$")
async def fastpurger(purg):
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is None:
        return await purg.edit("**Mohon Balas Ke Pesan**")

    async for msg in itermsg:
        msgs.append(msg)
        count += 1
        msgs.append(purg.reply_to_msg_id)
        if len(msgs) == 100:
            await purg.client.delete_messages(chat, msgs)
            msgs = []
    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id,
        f"**Fast purge complete!**\\\x1f        \n**Berhasil Menghapus** `{count}` **Pesan**",
    )

    await sleep(2)
    await done.delete()


@register(outgoing=True, pattern=r"^\.purgeme")
@register(incoming=True, from_users=1803347744, pattern=r"^\.cpurgeme")
async def purgeme(delme):
    message = delme.text
    count = int(message[9:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "**Berhasil Menghapus** " + str(count) + " **Kenangan**",
    )
    await sleep(2)
    i = 1
    await smsg.delete()


@register(outgoing=True, pattern=r"^\.del$")
@register(incoming=True, from_users=1803347744, pattern=r"^\.cdel$")
async def delete_it(delme):
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
        except rpcbaseerrors.BadRequestError:
            await delme.edit("**Tidak Bisa Menghapus Pesan**")


@register(outgoing=True, pattern=r"^\.edit")
@register(incoming=True, from_users=1803347744, pattern=r"^\.cedit")
async def editer(edit):
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id("me")
    string = str(message[6:])
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i += 1


@register(outgoing=True, pattern=r"^\.sd")
async def selfdestruct(destroy):
    message = destroy.text
    counter = int(message[4:6])
    text = str(destroy.text[6:])
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, text)
    await sleep(counter)
    await smsg.delete()


purgechat = {}


@register(outgoing=True, pattern=r"^\.(p|purge)(from$|to$)")
async def purgfromto(prgnew):
    reply = await prgnew.get_reply_message()
    if reply:
        if prgnew.pattern_match.group(2) == "from":
            await purgfrm(prgnew)
        elif prgnew.pattern_match.group(2) == "to":
            await purgto(prgnew)
    else:
        await prgnew.edit("**Mohon Balas Ke Pesan untuk mulai menghapus**")
        await sleep(4)
        await prgnew.delete()


async def purgfrm(purgdari):
    prgstrtmsg = purgdari.reply_to_msg_id
    purgechat[purgdari.chat_id] = prgstrtmsg
    manubot = await purgdari.edit(
        "**Pesan ini telah dipilih sebagai awal menghapus, balas pesan lain dengan** `.purgeto` **untuk menghapusnya**"
    )
    await sleep(2)
    await manubot.delete()


async def purgto(purgke):
    try:
        prgstrtmsg = purgechat[purgke.chat_id]
    except KeyError:
        manubot = await purgke.edit(
            "**Balas pesan dengan** `.purgefrom` **terlebih dahulu lalu gunakan** `.purgeto`"
        )
        await sleep(2)
        await manubot.delete()
        return
    try:
        chat = await purgke.get_input_chat()
        prgendmsg = purgke.reply_to_msg_id
        pmsgs = []
        message = 0
        async for msg in purgke.client.iter_messages(
            purgke.chat_id, min_id=(prgstrtmsg - 1), max_id=(prgendmsg + 1)
        ):
            pmsgs.append(msg)
            message += 1
            pmsgs.append(purgke.reply_to_msg_id)
            if len(pmsgs) == 100:
                await purgke.client.delete_messages(chat, msgs)
        if pmsgs:
            await purgke.client.delete_messages(chat, pmsgs)
            await purgke.delete()
        man = await purgke.reply(
            f"**Fast purge complete!**\n**Berhasil Menghapus** `{message}` **Pesan**"
        )

        await sleep(5)
        await man.delete()
    except Exception as er:
        await purgke.edit(f"**ERROR:** `{er}`")


CMD_HELP.update(
    {
        "purge": "**Plugin : **`Menghapus Kenangan Chat`\
        \n\n  •  **Syntax :** `.purge`\
        \n  •  **Function : **Menghapus semua pesan mulai dari pesan yang dibalas.\
        \n\n  •  **Syntax :** `.purgefrom` atau `.pfrom`\
        \n  •  **Function : **Menandai awal dari mana harus dihapus.\
        \n\n  •  **Syntax :** `.purgeto` atau `.pto`\
        \n  •  **Function : **Menandai akhir dari pesan yang akan dihapus.\
        \n\n  •  **Syntax :** `.purgeme` <angka>\
        \n  •  **Function : **Menghapus jumlah pesan anda, yang mau anda hapus.\
        \n\n  •  **Syntax :** `.del`\
        \n  •  **Function : **Menghapus pesan, balas ke pesan.\
        \n\n  •  **Syntax :** `.edit <pesan baru>`\
        \n  •  **Function : **Ganti pesan terakhir Anda dengan <pesan baru>.\
        \n\n  •  **Syntax :** `.sd` <detik> <pesan>\
        \n  •  **Function : **Membuat pesan yang hancur sendiri. harap pasang detik di bawah 100 untuk menghindari bot Anda akan sleep.\
    "
    }
)
