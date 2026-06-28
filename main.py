import os
import asyncio
import logging
import discord

# Konfigurasi Logging (Waktu menggunakan standar server, akan otomatis tercatat)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Mengambil variabel lingkungan dari Railway
TOKEN = os.getenv("DISCORD_TOKEN")
ALLOWED_CHANNELS_RAW = os.getenv("ALLOWED_CHANNELS", "")

# Parsing ID Channel
ALLOWED_CHANNELS = []
if ALLOWED_CHANNELS_RAW:
    for channel_id in ALLOWED_CHANNELS_RAW.split(","):
        cleaned_id = channel_id.strip()
        if cleaned_id.isdigit():
            ALLOWED_CHANNELS.append(int(cleaned_id))

# Menggunakan discord.Client (Paling aman untuk Self-Bot)
client = discord.Client()

@client.event
async def on_ready():
    logging.info("="*50)
    logging.info(f"✅ BOT BERHASIL ONLINE!")
    logging.info(f"👤 Akun          : {client.user.name}")
    
    # Memeriksa dan memastikan bot tersambung ke Channel DC yang tepat
    if ALLOWED_CHANNELS:
        logging.info("📡 Memeriksa koneksi ke Channel Discord...")
        for ch_id in ALLOWED_CHANNELS:
            channel = client.get_channel(ch_id)
            if channel:
                logging.info(f"   ✔️ Tersambung ke channel : #{channel.name}")
            else:
                logging.warning(f"   ❌ Gagal membaca channel ID {ch_id}. (Apakah ID salah?)")
    else:
        logging.warning("⚠️ TIDAK ADA CHANNEL YANG DIATUR! Bot aktif di semua channel (Sangat Berbahaya).")
    logging.info("="*50)

@client.event
async def on_message(message):
    # 1. Pastikan yang mengirim pesan adalah AKUN ANDA SENDIRI
    if message.author.id != client.user.id:
        return

    # 2. Pastikan pesan dikirim di channel yang terdaftar
    if ALLOWED_CHANNELS and (message.channel.id not in ALLOWED_CHANNELS):
        return

    content = message.content.strip()

    # 3. Abaikan jika pesan SUDAH berupa Kotak Salin
    if content.startswith("```") and content.endswith("```"):
        return

    # Pemisahan teks berdasarkan baris baru
    lines = [line.strip() for line in content.splitlines() if line.strip()]

    if not lines:
        return

    # Eksekusi A: Hapus pesan asli
    try:
        await message.delete()
        logging.info(f"🗑️ Pesan asli dihapus dari #{message.channel.name}")
    except Exception as e:
        logging.error(f"❌ Gagal menghapus pesan asli: {e}")
        return 

    # Eksekusi B: Kirim ulang setiap baris sebagai pesan Kotak Salin (Tombol Copy)
    for line in lines:
        try:
            # Menggunakan TRIPLE BACKTICKS (```)
            await message.channel.send(f"```text\n{line}\n```")
            logging.info(f"➡️ Berhasil mengirim kode ke #{message.channel.name}")
        except Exception as e:
            logging.error(f"❌ Gagal mengirim kode: {e}")
        
        # JEDA AMAN: 1.2 Detik (Anti-banned)
        await asyncio.sleep(1.2)

if __name__ == "__main__":
    if not TOKEN:
        logging.critical("❌ Variabel 'DISCORD_TOKEN' tidak ditemukan di Railway!")
    else:
        try:
            client.run(TOKEN)
        except Exception as e:
            logging.critical(f"❌ Gagal menjalankan bot: {e}")
