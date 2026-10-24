from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/perpustakaan_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==========================================
# 1. MODEL DATABASE
# ==========================================
class Penulis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Kategori(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), unique=True, nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)

class Buku(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False) # Tambahan dari tugas
    tahun_terbit = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Integer, nullable=True) # Tambahan dari tugas
    penulis_id = db.Column(db.Integer, db.ForeignKey('penulis.id'), nullable=False)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.id'), nullable=False)

with app.app_context():
    db.create_all()

# ==========================================
# 2. ENDPOINT API (PENULIS)
# ==========================================
@app.route('/api/penulis', methods=['GET'])
def get_semua_penulis():
    semua_penulis = Penulis.query.all()
    data = [{"id": p.id, "nama": p.nama, "email": p.email} for p in semua_penulis]
    return jsonify({"status": "success", "message": "Berhasil", "data": data}), 200

@app.route('/api/penulis/<int:id>', methods=['GET'])
def get_detail_penulis(id):
    penulis = Penulis.query.get(id)
    if not penulis:
        return jsonify({"status": "error", "message": "Penulis tidak ditemukan", "data": None}), 404
    data = {"id": penulis.id, "nama": penulis.nama, "email": penulis.email}
    return jsonify({"status": "success", "message": "Berhasil", "data": data}), 200

@app.route('/api/penulis', methods=['POST'])
def tambah_penulis():
    data_input = request.get_json()
    if not data_input or 'nama' not in data_input or 'email' not in data_input:
        return jsonify({"status": "error", "message": "Nama dan email wajib diisi", "data": None}), 400
    
    cek_email = Penulis.query.filter_by(email=data_input['email']).first()
    if cek_email:
        return jsonify({"status": "error", "message": "Email sudah terdaftar", "data": None}), 409

    penulis_baru = Penulis(nama=data_input['nama'], email=data_input['email'])
    db.session.add(penulis_baru)
    db.session.commit()
    return jsonify({"status": "success", "message": "Penulis ditambahkan", "data": {"id": penulis_baru.id}}), 201

@app.route('/api/penulis/<int:id>', methods=['PUT'])
def ubah_penulis(id):
    penulis = Penulis.query.get(id)
    if not penulis:
        return jsonify({"status": "error", "message": "Penulis tidak ditemukan", "data": None}), 404
    
    data_input = request.get_json()
    if 'nama' in data_input: penulis.nama = data_input['nama']
    if 'email' in data_input: penulis.email = data_input['email']
    db.session.commit()
    return jsonify({"status": "success", "message": "Penulis diubah", "data": {"id": penulis.id}}), 200

@app.route('/api/penulis/<int:id>', methods=['DELETE'])
def hapus_penulis(id):
    penulis = Penulis.query.get(id)
    if not penulis:
        return jsonify({"status": "error", "message": "Penulis tidak ditemukan", "data": None}), 404
    
    # Cek apakah penulis masih punya buku (409 Conflict)
    cek_buku = Buku.query.filter_by(penulis_id=id).first()
    if cek_buku:
        return jsonify({"status": "error", "message": "Gagal hapus: Penulis masih memiliki buku", "data": None}), 409
        
    db.session.delete(penulis)
    db.session.commit()
    return jsonify({"status": "success", "message": "Penulis dihapus", "data": None}), 200


# ==========================================
# 3. ENDPOINT API (KATEGORI)
# ==========================================
@app.route('/api/kategori', methods=['GET'])
def get_semua_kategori():
    semua_kategori = Kategori.query.all()
    data = [{"id": k.id, "nama": k.nama, "deskripsi": k.deskripsi} for k in semua_kategori]
    return jsonify({"status": "success", "message": "Berhasil", "data": data}), 200

@app.route('/api/kategori/<int:id>', methods=['GET'])
def get_detail_kategori(id):
    kategori = Kategori.query.get(id)
    if not kategori:
        return jsonify({"status": "error", "message": "Kategori tidak ditemukan", "data": None}), 404
    data = {"id": kategori.id, "nama": kategori.nama, "deskripsi": kategori.deskripsi}
    return jsonify({"status": "success", "message": "Berhasil", "data": data}), 200

@app.route('/api/kategori', methods=['POST'])
def tambah_kategori():
    data_input = request.get_json()
    if not data_input or 'nama' not in data_input:
        return jsonify({"status": "error", "message": "Nama kategori wajib diisi", "data": None}), 400

    cek_nama = Kategori.query.filter_by(nama=data_input['nama']).first()
    if cek_nama:
        return jsonify({"status": "error", "message": "Nama kategori sudah ada", "data": None}), 409

    kategori_baru = Kategori(nama=data_input['nama'], deskripsi=data_input.get('deskripsi', ''))
    db.session.add(kategori_baru)
    db.session.commit()
    return jsonify({"status": "success", "message": "Kategori ditambahkan", "data": {"id": kategori_baru.id}}), 201

@app.route('/api/kategori/<int:id>', methods=['PUT'])
def ubah_kategori(id):
    kategori = Kategori.query.get(id)
    if not kategori:
        return jsonify({"status": "error", "message": "Kategori tidak ditemukan", "data": None}), 404
    
    data_input = request.get_json()
    if 'nama' in data_input: kategori.nama = data_input['nama']
    if 'deskripsi' in data_input: kategori.deskripsi = data_input['deskripsi']
    db.session.commit()
    return jsonify({"status": "success", "message": "Kategori diubah", "data": {"id": kategori.id}}), 200

@app.route('/api/kategori/<int:id>', methods=['DELETE'])
def hapus_kategori(id):
    kategori = Kategori.query.get(id)
    if not kategori:
        return jsonify({"status": "error", "message": "Kategori tidak ditemukan", "data": None}), 404
    
    # Cek apakah kategori masih dipakai buku (409 Conflict)
    cek_buku = Buku.query.filter_by(kategori_id=id).first()
    if cek_buku:
        return jsonify({"status": "error", "message": "Gagal hapus: Kategori masih digunakan buku", "data": None}), 409
        
    db.session.delete(kategori)
    db.session.commit()
    return jsonify({"status": "success", "message": "Kategori dihapus", "data": None}), 200


# ==========================================
# 4. ENDPOINT API (BUKU)
# ==========================================
@app.route('/api/buku', methods=['GET'])
def get_semua_buku():
    # Mendukung Filter dan Pencarian
    penulis_id = request.args.get('penulis_id')
    kategori_id = request.args.get('kategori_id')
    q = request.args.get('q')

    query = Buku.query
    if penulis_id: query = query.filter_by(penulis_id=penulis_id)
    if kategori_id: query = query.filter_by(kategori_id=kategori_id)
    if q: query = query.filter(Buku.judul.ilike(f'%{q}%')) # Pencarian judul mirip

    semua_buku = query.all()
    data = [{
        "id": b.id, "judul": b.judul, "isbn": b.isbn, 
        "tahun_terbit": b.tahun_terbit, "harga": b.harga,
        "penulis_id": b.penulis_id, "kategori_id": b.kategori_id
    } for b in semua_buku]
    return jsonify({"status": "success", "message": "Berhasil", "data": data}), 200


@app.route('/api/buku/<int:id>', methods=['GET'])
def get_detail_buku(id):
    buku = Buku.query.get(id)
    if not buku:
        return jsonify({"status": "error", "message": "Buku tidak ditemukan", "data": None}), 404
    
    # KITA TAMBAHKAN FIELD LAINNYA DI SINI
    data = {
        "id": buku.id, 
        "judul": buku.judul, 
        "isbn": buku.isbn,
        "tahun_terbit": buku.tahun_terbit,
        "harga": buku.harga,
        "penulis_id": buku.penulis_id,
        "kategori_id": buku.kategori_id
    }
    return jsonify({"status": "success", "message": "Berhasil", "data": data}), 200



@app.route('/api/buku', methods=['POST'])
def tambah_buku():
    data_input = request.get_json()
    # Validasi field wajib
    if not data_input or 'judul' not in data_input or 'isbn' not in data_input or 'penulis_id' not in data_input or 'kategori_id' not in data_input:
        return jsonify({"status": "error", "message": "Judul, isbn, penulis_id, kategori_id wajib diisi", "data": None}), 400
    
    # Validasi duplikasi ISBN (409)
    cek_isbn = Buku.query.filter_by(isbn=data_input['isbn']).first()
    if cek_isbn:
        return jsonify({"status": "error", "message": "ISBN sudah terdaftar", "data": None}), 409

    buku_baru = Buku(
        judul=data_input['judul'],
        isbn=data_input['isbn'],
        tahun_terbit=data_input.get('tahun_terbit', 2023),
        harga=data_input.get('harga', 0),
        penulis_id=data_input['penulis_id'],
        kategori_id=data_input['kategori_id']
    )
    db.session.add(buku_baru)
    db.session.commit()
    return jsonify({"status": "success", "message": "Buku ditambahkan", "data": {"id": buku_baru.id}}), 201

@app.route('/api/buku/<int:id>', methods=['PUT'])
def ubah_buku(id):
    buku = Buku.query.get(id)
    if not buku:
        return jsonify({"status": "error", "message": "Buku tidak ditemukan", "data": None}), 404
    
    data_input = request.get_json()
    if 'judul' in data_input: buku.judul = data_input['judul']
    if 'tahun_terbit' in data_input: buku.tahun_terbit = data_input['tahun_terbit']
    if 'harga' in data_input: buku.harga = data_input['harga']
    db.session.commit()
    return jsonify({"status": "success", "message": "Buku diubah", "data": {"id": buku.id}}), 200

@app.route('/api/buku/<int:id>', methods=['DELETE'])
def hapus_buku(id):
    buku = Buku.query.get(id)
    if not buku:
        return jsonify({"status": "error", "message": "Buku tidak ditemukan", "data": None}), 404
    db.session.delete(buku)
    db.session.commit()
    return jsonify({"status": "success", "message": "Buku dihapus", "data": None}), 200

if __name__ == '__main__':
    app.run(debug=True)