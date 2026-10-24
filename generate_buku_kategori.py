import requests
import random
import time

URL_KATEGORI = 'http://127.0.0.1:5000/api/kategori'
URL_BUKU = 'http://127.0.0.1:5000/api/buku'

# ==========================================
# 1. GENERATE KATEGORI
# ==========================================
print("--- Memasukkan Data Kategori ---")
kategori_list = [
    {"nama": "Fiksi", "deskripsi": "Buku cerita rekaan dan imajinatif"},
    {"nama": "Non-Fiksi", "deskripsi": "Buku berdasarkan fakta dan kejadian nyata"},
    {"nama": "Sains", "deskripsi": "Buku tentang ilmu pengetahuan alam"},
    {"nama": "Sejarah", "deskripsi": "Buku tentang peristiwa masa lalu"},
    {"nama": "Teknologi", "deskripsi": "Buku tentang perkembangan teknologi dan komputer"},
    {"nama": "Biografi", "deskripsi": "Kisah hidup tokoh terkenal"},
    {"nama": "Komik", "deskripsi": "Cerita bergambar"},
    {"nama": "Bisnis", "deskripsi": "Buku tentang ekonomi dan kewirausahaan"},
    {"nama": "Agama", "deskripsi": "Buku tentang ajaran dan spiritualitas"},
    {"nama": "Anak", "deskripsi": "Buku bacaan untuk anak-anak"}
]

for kat in kategori_list:
    response = requests.post(URL_KATEGORI, json=kat)
    if response.status_code == 201:
        print(f"Berhasil tambah kategori: {kat['nama']}")
    elif response.status_code == 409:
        print(f"Kategori {kat['nama']} sudah ada (Skip).")
    else:
        print(f"Gagal: {kat['nama']} (Error: {response.status_code})")
    time.sleep(0.1)

print("\n--- Memasukkan Data Buku ---")

# ==========================================
# 2. GENERATE BUKU
# ==========================================
# Daftar judul buku acak
judul_buku_list = [
    "Bumi Manusia", "Laskar Pelangi", "Perahu Kertas", "Pulang", "Cantik Itu Luka",
    "Lelaki Harimau", "Supernova", "Dilan 1990", "Matahari", "Hujan",
    "Filosofi Teras", "Sapiens", "Atomic Habits", "Bumi", "Rumah Kaca",
    "Jejak Langkah", "Gadis Kretek", "Olenka", "Arok Dedes", "Ronggeng Dukuh Paruk",
    "Laskar Pelangi 2", "Bulan", "Matahari Kecil", "Bintang", "Komet",
    "Algoritma", "Python untuk Pemula", "Dasar Ilmu Ekonomi", "Sejarah Indonesia", "Psikologi Umum"
]

jumlah_buku = 30 # Kita akan generate 30 buku

for i in range(jumlah_buku):
    judul = random.choice(judul_buku_list) + f" Edisi {random.randint(1, 10)}"
    
    # Generate ISBN unik secara acak (format: 978-XXX-XXXX-XX-X)
    isbn_acak = f"978-{random.randint(100, 999)}-{random.randint(1000, 9999)}-{random.randint(10, 99)}-{random.randint(0, 9)}"
    
    # Pilih ID secara acak (Asumsi ID Penulis 1-20, Kategori 1-10)
    penulis_id_acak = random.randint(1, 20)
    kategori_id_acak = random.randint(1, 10)
    
    data_buku = {
        "judul": judul,
        "isbn": isbn_acak,
        "tahun_terbit": random.randint(1990, 2024),
        "harga": random.randint(45, 150) * 1000, # Harga acak antara 45.000 - 150.000
        "penulis_id": penulis_id_acak,
        "kategori_id": kategori_id_acak
    }

    response = requests.post(URL_BUKU, json=data_buku)
    
    if response.status_code == 201:
        print(f"Berhasil: {judul}")
    else:
        print(f"Gagal: {judul} (Error: {response.status_code}) - {response.text}")
    
    time.sleep(0.1)

print("\nSelesai! Silakan cek HeidiSQL.")