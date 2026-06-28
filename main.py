import os
import asyncio
import logging
from discord.ext import commands

# 1. Konfigurasi Logging (Agar riwayat aktivitas terlihat rapi di panel Railway)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 2. Mengambil variabel lingkungan dari Railway
TOKEN = os.getenv("DISCORD_TOKEN")
ALLOWED_CHANNELS_RAW = os.getenv("ALLOWED_CHANNELS", "")

# 3. Parsing ID Channel dengan aman
ALLOWED_CHANNELS = []
if ALLOWED_CHANNELS_RAW:
    for channel_id in ALLOWED_CHANNELS_RAW.split(","):
        cleaned_id = channel_id.strip()
        if cleaned_id.isdigit():
            ALLOWED_CHANNELS.append(int(cleaned_id))

# 4. Setup Self-Bot
bot = commands.Bot(command_prefix="", self_bot=True)

@bot.event
async def on_ready():
    logging.info("="*50)
    logging.info(f"✅ BOT BERHASIL ONLINE!")
    logging.info(f"👤 Akun          : {bot.user.name}")
    if ALLOWED_CHANNELS:
        logging.info(f"📡 Channel Aktif : {ALLOWED_CHANNELS}")
    else:
        logging.warning("⚠️ TIDAK ADA CHANNEL! Bot akan aktif di semua channel (Sangat Berbahaya).")
    logging.info("="*50)

@bot.event
async def on_message(message):
    # Pengecekan 1: Pastikan yang mengirim pesan adalah AKUN ANDA SENDIRI
    if message.author.id != bot.user.id:
        return

    # Pengecekan 2: Pastikan pesan dikirim di channel yang terdaftar di Railway
    if ALLOWED_CHANNELS and (message.channel.id not in ALLOWED_CHANNELS):
        return

    content = message.content.strip()

    # Pengecekan 3: Abaikan jika pesan SUDAH berupa Kotak Salin (mencegah looping tanpa henti)
    if content.startswith("```") and content.endswith("```"):
        return

    # Pemisahan teks berdasarkan baris baru (enter), hapus baris yang kosong/spasi
    lines = [line.strip() for line in content.splitlines() if line.strip()]

    # Jika tidak ada teks valid, hentikan proses
    if not lines:
        return

    # Eksekusi A: Hapus pesan asli Anda (Pesan yang panjang)
    try:
        await message.delete()
        logging.info(f"🗑️ Pesan asli berhasil dihapus (Channel ID: {message.channel.id})")
    except Exception as e:
        logging.error(f"❌ Gagal menghapus pesan asli: {e}")
        return # Jika gagal dihapus, batalkan pengiriman ulang agar tidak dobel/spam

    # Eksekusi B: Kirim ulang setiap baris sebagai pesan baru (Kotak Salin/Tombol Copy)
    for line in lines:
        try:
            # Menggunakan TRIPLE BACKTICKS (```) agar menjadi Kotak Salin resmi Discord
            await message.channel.send(f"```text\n{line}\n```")
            logging.info(f"➡️ Berhasil mengirim: {line}")
        except Exception as e:
            logging.error(f"❌ Gagal mengirim kode [{line}]: {e}")
        
        # JEDA AMAN: 1.2 Detik (Wajib ada agar sistem keamanan Discord tidak mem-banned akun Anda)
        await asyncio.sleep(1.2)

# Perintah untuk menjalankan bot
if __name__ == "__main__":
    if not TOKEN:
        logging.critical("❌ Variabel 'DISCORD_TOKEN' tidak ditemukan di Railway! Bot dihentikan.")
    else:
        try:
            bot.run(TOKEN)
        except Exception as e:
            logging.critical(f"❌ Gagal menjalankan bot (Pastikan token valid!): {e}")
