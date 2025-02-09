from flask import Flask, request, jsonify
import mysql.connector
import hashlib  # Import hashlib untuk MD5
from flask_jwt_extended import create_access_token, JWTManager

app = Flask(__name__)

# Konfigurasi MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Sesuaikan dengan user MySQL kamu
    password="",  # Kosongkan jika tidak ada password di XAMPP
    database="pengguna"
)

# Konfigurasi JWT
app.config["JWT_SECRET_KEY"] = "supersecretkey"
jwt = JWTManager(app)

# Fungsi untuk menghasilkan hash MD5 dari password
def hash_password_md5(password):
    return hashlib.md5(password.encode()).hexdigest()

# API untuk Menambah Kategori
@app.route("/kategori", methods=["POST"])
def add_category():
    data = request.json
    nama = data.get("nama")

    if not nama:
        return jsonify({"error": "Nama kategori wajib diisi!"}), 400

    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO kategori (nama) VALUES (%s)", (nama,))
        db.commit()
        return jsonify({"message": "Kategori berhasil ditambahkan!"}), 201
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

# API untuk Melihat Daftar Kategori
@app.route("/kategori", methods=["GET"])
def get_categories():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kategori")
    categories = cursor.fetchall()

    return jsonify({"kategori": categories}), 200

# API untuk Mengupdate Kategori
@app.route("/kategori/<int:id_kategori>", methods=["PUT"])
def update_category(id_kategori):
    data = request.json
    nama = data.get("nama")

    if not nama:
        return jsonify({"error": "Nama kategori wajib diisi!"}), 400

    try:
        cursor = db.cursor()
        cursor.execute("UPDATE kategori SET nama = %s WHERE id_kategori = %s", (nama, id_kategori))
        db.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Kategori berhasil diperbarui!"}), 200
        else:
            return jsonify({"error": "Kategori tidak ditemukan!"}), 404
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

# API untuk Menghapus Kategori
@app.route("/kategori/<int:id_kategori>", methods=["DELETE"])
def delete_category(id_kategori):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM kategori WHERE id_kategori = %s", (id_kategori,))
        db.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Kategori berhasil dihapus!"}), 200
        else:
            return jsonify({"error": "Kategori tidak ditemukan!"}), 404
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)