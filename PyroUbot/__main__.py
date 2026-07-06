import signal
import tornado.ioloop
import tornado.platform.asyncio
from pyrogram import Client
from PyroUbot import *

async def shutdown(signal, loop):
    print(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

# --- FUNGSI NOTIFIKASI BOT API ---
async def send_log_startup():
    await asyncio.sleep(5) # Jeda agar bot stabil
    ID_LOG_CHANNEL = -1003659966140 # Ganti dengan ID Channel Log kamu
    
    # Ambil modul yang terdaftar
    modul_list = ", ".join(HELP.keys()) if HELP else "Tidak ada modul"
    
    if ubot._ubot:
        # Menggunakan data dari userbot pertama untuk nama akun
        akun_utama = ubot._ubot[0]
        try:
            # 1. Pesan Userbot Diaktifkan
            text_start = (
                f"<b>my ubot premium</b>\n"
                f"<b>❑ USERBOT DIAKTIFKAN</b>\n"
                f"<b>├ AKUN: {akun_utama.me.first_name}</b>\n"
                f"<b>└ ID: <code>{akun_utama.me.id}</code></b>"
            )
            await bot.send_message(ID_LOG_CHANNEL, text_start)

            # 2. Pesan Module Baru (Sesuai gambar kamu)
            text_module = (
                f"<b>my ubot premium</b>\n"
                f"📦 <b>SUKSES ADD MODULE</b>\n\n"
                f"🛠 <b>Module:</b> <code>{modul_list}</code>\n"
                f"✨ <b>Status:</b> <code>File Terdeteksi</code>\n"
                f"💡 <i>Silakan restart bot untuk mengaktifkan modul ini.</i> 💡"
            )
            await bot.send_message(ID_LOG_CHANNEL, text_module)
        except Exception as e:
            print(f"Gagal kirim log ke CH: {e}")

async def main():
    await bot.start()
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            await asyncio.wait_for(ubot_.start(), timeout=10)
        except asyncio.TimeoutError:
            await remove_ubot(int(_ubot["name"]))
            print(f"[ɪɴғᴏ]: {int(_ubot['name'])} ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇʀᴇsᴘᴏɴ")
        except Exception:
            await remove_ubot(int(_ubot["name"]))
            print(f"[ɪɴғᴏ]: {int(_ubot['name'])} ʙᴇʀʜᴀsɪʟ ᴅɪ ʜᴀᴘᴜs")
    
    await bash("rm -rf *session*")
    
    # Memuat plugin dan fungsi lainnya
    await asyncio.gather(loadPlugins(), installPeer(), expiredUserbots())
    
    # --- JALANKAN NOTIFIKASI DI SINI ---
    asyncio.create_task(send_log_startup())
    
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            s, lambda: asyncio.create_task(shutdown(s, loop))
        )

    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        pass
    finally:
        await bot.stop()

if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop
    loop.run_until_complete(main())
    