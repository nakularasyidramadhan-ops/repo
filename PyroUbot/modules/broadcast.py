import asyncio
import random
from pyrogram import enums
from pyrogram.errors.exceptions import FloodWait
from PyroUbot import *

__MODULE__ = "ʙʀᴏᴀᴅᴄᴀꜱᴛ"
__HELP__ = """
<blockquote><b>Bantuan Broadcast Premium</b>

<b>PERINTAH GIKES:</b>
<code>{0}gikes</code> [type] (Wajib reply)
Type: <code>all, users, group, channel</code>

<b>PERINTAH FORWARD (CFD):</b>
<code>{0}cfd</code> [type] (Wajib reply)

<b>PERINTAH AUTO BC:</b>
<code>{0}autobc text</code> (Wajib reply)
<code>{0}autobc delay</code> [menit]
<code>{0}autobc on/off</code>

<b>MANAJEMEN BLACKLIST:</b>
<code>{0}addbl</code> | <code>{0}unbl</code> | <code>{0}listbl</code>
<code>{0}stopg</code> → Hentikan proses.</blockquote>
"""

gcast_progress = []
AG = []

# --- HELPER AMBIL LIST CHAT ---
async def get_chats(client, command):
    chats = []
    async for dialog in client.get_dialogs():
        if command == "group" and dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chats.append(dialog.chat.id)
        elif command == "users" and dialog.chat.type == enums.ChatType.PRIVATE:
            chats.append(dialog.chat.id)
        elif command == "channel" and dialog.chat.type == enums.ChatType.CHANNEL:
            chats.append(dialog.chat.id)
        elif command == "all":
            chats.append(dialog.chat.id)
    return chats

# --- GIKES / BC COPY ---
@PY.UBOT("bc|gikes")
@PY.TOP_CMD
async def gcast_handler(client, message):
    global gcast_progress
    if not message.reply_to_message:
        return await message.reply("<blockquote><b>❌ ERROR:</b> Harap reply ke pesan promo!</blockquote>")

    args = message.command
    command = args[1].lower() if len(args) > 1 else "all"
    
    gcast_progress.append(client.me.id)
    prs = await EMO.PROSES(client)
    gcs = await message.reply(f"<b>{prs} ᴍᴇᴍᴘʀᴏsᴇs ʙʀᴏᴀᴅᴄᴀsᴛ...</b>")

    chats = await get_chats(client, command)
    blacklist = await get_list_from_vars(client.me.id, "BL_ID")
    done, failed = 0, 0

    for chat_id in chats:
        if client.me.id not in gcast_progress: break
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT: continue
        try:
            await message.reply_to_message.copy(chat_id)
            done += 1
            await asyncio.sleep(0.3)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(chat_id)
            done += 1
        except Exception:
            failed += 1

    if client.me.id in gcast_progress: gcast_progress.remove(client.me.id)
    
    robot = await EMO.ROBOT(client)
    terompet = await EMO.TEROMPET(client)
    centang = await EMO.CENTANG(client)
    silang = await EMO.SILANG(client)
    pesan = await EMO.PESAN(client)
    jam = await EMO.JAM(client)

    await gcs.delete()
    return await message.reply(f"""
<blockquote>{robot} <b>Youre Broadcast Result</b>{terompet}
  {centang} <b>Success: {done}</b>
  {silang} <b>Failed: {failed}</b>
  {robot} <b>Task ID: {message.id}</b>
  {pesan} <b>Type: {command}</b>
  {jam} <b>Blacklist: {len(blacklist)}</b>
<b>My Bot: @iqbalubot</b></blockquote>
""")

# --- CFD / FORWARD ---
@PY.UBOT("bcfd|cfd")
@PY.TOP_CMD
async def cfd_handler(client, message):
    if not message.reply_to_message:
        return await message.reply("<blockquote><b>❌ ERROR:</b> Harap reply pesan!</blockquote>")

    args = message.command
    command = args[1].lower() if len(args) > 1 else "all"
    
    prs = await EMO.PROSES(client)
    gcs = await message.reply(f"{prs} ᴍᴇᴍᴘʀᴏsᴇs ғᴏʀᴡᴀʀᴅ...")

    chats = await get_chats(client, command)
    blacklist = await get_list_from_vars(client.me.id, "BL_ID")
    done, failed = 0, 0

    for chat_id in chats:
        if chat_id in blacklist: continue
        try:
            await message.reply_to_message.forward(chat_id)
            done += 1
            await asyncio.sleep(0.3)
        except Exception: failed += 1

    await gcs.delete()
    return await message.reply(f"<blockquote><b>✅ Forward Selesai</b>\n<b>Success: {done}</b>\n<b>Failed: {failed}</b>\n<b>My Bot: @iqbalubot</b></blockquote>")

# --- AUTO BROADCAST ---
@PY.UBOT("autobc")
@PY.TOP_CMD
async def autobc_handler(client, message):
    args = message.command
    if len(args) < 2: return
    query = args[1].lower()
    auto_text_vars = await get_vars(client.me.id, "AUTO_TEXT") or []

    if query == "on":
        if not auto_text_vars: return await message.reply("Teks kosong! .autobc text (reply)")
        if client.me.id not in AG:
            AG.append(client.me.id)
            await message.reply("<blockquote><b>✅ Auto BC Aktif!</b></blockquote>")
            while client.me.id in AG:
                delay = await get_vars(client.me.id, "DELAY_GCAST") or 1
                txt = random.choice(auto_text_vars)
                chats = await get_chats(client, "group")
                blacklist = await get_list_from_vars(client.me.id, "BL_ID")
                done = 0
                for c in chats:
                    if c in blacklist: continue
                    try:
                        await client.send_message(c, txt)
                        done += 1
                        await asyncio.sleep(1)
                    except Exception: pass
                await client.send_message(message.chat.id, f"<blockquote>📢 <b>Auto BC Done</b>\n<b>Success: {done} Grup</b>\n<b>My Bot: @iqbalubot</b></blockquote>")
                await asyncio.sleep(int(60 * int(delay)))

    elif query == "off":
        if client.me.id in AG: AG.remove(client.me.id)
        return await message.reply("<blockquote><b>✅ Auto BC Mati!</b></blockquote>")

    elif query == "text":
        if not message.reply_to_message: return
        val = message.reply_to_message.text or message.reply_to_message.caption
        auto_text_vars.append(val)
        await set_vars(client.me.id, "AUTO_TEXT", auto_text_vars)
        await message.reply("<blockquote><b>✅ Teks Auto BC Tersimpan!</b></blockquote>")

    elif query == "delay":
        if len(args) < 3: return
        await set_vars(client.me.id, "DELAY_GCAST", args[2])
        await message.reply(f"✅ Delay set ke {args[2]} menit.")

# --- BLACKLIST & STOP ---
@PY.UBOT("stopg")
@PY.TOP_CMD
async def _(client, message):
    global gcast_progress, AG
    if client.me.id in gcast_progress: gcast_progress.remove(client.me.id)
    if client.me.id in AG: AG.remove(client.me.id)
    await message.reply("<blockquote><b>✅ Semua proses dihentikan!</b></blockquote>")

@PY.UBOT("addbl")
@PY.TOP_CMD
async def _(client, message):
    await add_to_vars(client.me.id, "BL_ID", message.chat.id)
    await message.reply("✅ Blacklist ditambahkan.")

@PY.UBOT("unbl")
@PY.TOP_CMD
async def _(client, message):
    await remove_from_vars(client.me.id, "BL_ID", message.chat.id)
    await message.reply("✅ Blacklist dihapus.")

@PY.UBOT("listbl")
@PY.TOP_CMD
async def _(client, message):
    bl = await get_list_from_vars(client.me.id, "BL_ID")
    res = "<b>📁 Daftar Blacklist:</b>\n" + "\n".join([f"• <code>{x}</code>" for x in bl])
    await message.reply(res)
    
    