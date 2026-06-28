# Menggunakan Python versi 3.11
FROM python:3.11-slim

# Menentukan direktori kerja
WORKDIR /app

# MENGINSTAL GIT (Wajib agar bisa mengunduh discord.py-self versi terbaru dari GitHub)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Menyalin file requirements.txt
COPY requirements.txt .

# Menginstal pustaka langsung dari source GitHub
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh file proyek
COPY . .

# Menjalankan bot
CMD ["python", "-u", "main.py"]
