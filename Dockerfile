# Menggunakan Python versi 3.11 (Bebas dari error audioop)
FROM python:3.11-slim

# Menentukan direktori kerja di dalam kontainer
WORKDIR /app

# Menyalin file requirements.txt
COPY requirements.txt .

# Menginstal pustaka tanpa menyimpan cache (lebih ringan)
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh file proyek
COPY . .

# Menjalankan bot (-u agar log langsung tampil secara live di Railway)
CMD ["python", "-u", "main.py"]
