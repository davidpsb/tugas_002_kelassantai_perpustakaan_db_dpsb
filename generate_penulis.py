import requests
import time

url = 'http://127.0.0.1:5000/api/penulis'

# Daftar 20 Penulis Acak
data_penulis = [
    {"nama": "Pramoedya Ananta Toer", "email": "pramoedya@email.com"},
    {"nama": "Ayu Utami", "email": "ayu.utami@email.com"},
    {"nama": "Eka Kurniawan", "email": "eka.k@email.com"},
    {"nama": "Dee Lestari", "email": "dee@email.com"},
    {"nama": "Tere Liye", "email": "tereliye@email.com"},
    {"nama": "Habiburrahman El Shirazy", "email": "kang_abik@email.com"},
    {"nama": "Raditya Dika", "email": "raditya@email.com"},
    {"nama": "Chairil Anwar", "email": "chairil@email.com"},
    {"nama": "Sapardi Djoko Damono", "email": "sapardi@email.com"},
    {"nama": "NH Dini", "email": "nhdini@email.com"},
    {"nama": "Umar Kayam", "email": "umar.kayam@email.com"},
    {"nama": "Iwan Setyawan", "email": "iwan.s@email.com"},
    {"nama": "Fiersa Besari", "email": "fiersa@email.com"},
    {"nama": "Boy Candra", "email": "boycandra@email.com"},
    {"nama": "Ika Natassa", "email": "ika.n@email.com"},
    {"nama": "Almira Bastari", "email": "almira@email.com"},
    {"nama": "Valiant Budi", "email": "valiant@email.com"},
    {"nama": "Achi TM", "email": "achi.tm@email.com"},
    {"nama": "Kaka Alfarisi", "email": "kaka@email.com"},
    {"nama": "Mira W.", "email": "mira.w@email.com"}
]

print("Mulai memasukkan 20 data penulis...")

for p in data_penulis:
    response = requests.post(url, json=p)
    if response.status_code == 201:
        print(f"Berhasil: {p['nama']}")
    else:
        print(f"Gagal: {p['nama']} (Error: {response.status_code})")
    
    time.sleep(0.1) # Jeda sebentar agar server tidak kewalahan

print("Selesai!")