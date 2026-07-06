import os
import requests
from PyroUbot import *
from pyrogram.types import Message

# GANTI DENGAN API KEY YANG KAMU DAPET TADI
DEEPAI_API_KEY = "683ec25f-5283-4f6e-8183-759a78b95114"

def get_hd_image(image_path):
    """Fungsi untuk memproses gambar ke DeepAI"""
    try:
        response = requests.post(
            "https://api.deepai.org/api/torch-srgan",
            files={
                'image': open(image_path, 'rb'),
            },
            headers={'api-key': DEEPAI_API_KEY},
            timeout=60
        )
        
        # Ambil hasil JSON
        data = response.json()
        
        # DeepAI mengembalikan output_url kalau berhasil
        if "output_url" in data:
            return data["output_url"]
        else:
            print(f"DeepAI Error: {data}")
            return None
    except Exception as e:
        print(f"Request Error: {e}")
        return None

__MODULE__ = "𝚁𝙴𝙼𝙸𝙽𝙸"
__HELP__ = """
<b>✮ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʜᴅ ✮</b>

<blockquote><b>perintah :
<code>{0}remini</code> atau <code>{0}hd</code></b>
<i>balas ke foto untuk menjernihkan gambar</i></blockquote>
"""

@PY.UBOT("remini|hd")
@PY.TOP_CMD
async def process_remini(client, message):
    # Cek apakah me-reply foto
    target = message.reply_to_message
    if not target or not (target.photo or (target.document and "image" in target.document.mime_type)):
        return await message.reply("<blockquote><b>Reply foto yang mau dijernihin dong King!</b></blockquote>")

    pros = await message.reply("<blockquote><b>Lagi dijernihin sama AI Kingz... Sabar ya! ⏳</b></blockquote>")

    try:
        # 1. Download foto dari Telegram
        photo_path = await client.download_media(target)

        # 2. Kirim ke API DeepAI
        hd_url = get_hd_image(photo_path)

        if hd_url:
            # 3. Kirim balik hasilnya ke user (bisa langsung pakai URL)
            await client.send_photo(
                chat_id=message.chat.id,
                photo=hd_url,
                caption="<blockquote><b>SUDAH JERNIH (HD) NIH KINGZ! ✅</b>\n<i>Powered by Aing</i></blockquote>",
                reply_to_message_id=message.id
            )
        else:
            await message.reply("<blockquote><b>Waduh Gagal Kingz! Cek API Key kamu atau coba lagi nanti.</b></blockquote>")

        # Bersihkan file sampah di VPS/Server
        if os.path.exists(photo_path):
            os.remove(photo_path)

    except Exception as e:
        await message.reply(f"<blockquote><b>YAAH EROR NIH!</b></blockquote>\n<code>{str(e)}</code>")
    
    finally:
        await pros.delete()


