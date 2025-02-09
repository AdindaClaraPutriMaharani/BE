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
    database="property"
)

# Konfigurasi JWT
app.config["JWT_SECRET_KEY"] = "supersecretkey"
jwt = JWTManager(app)

# Fungsi untuk menghasilkan hash MD5 dari password
def hash_password_md5(password):
    return hashlib.md5(password.encode()).hexdigest()

# API Register (Mendaftarkan pengguna baru)
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    nama = data.get("nama")
    alamat = data.get("alamat")

    if not email or not password:
        return jsonify({"error": "Email dan password wajib diisi!"}), 400

    # Hash password menggunakan MD5
    hashed_password = hash_password_md5(password)

    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO pembeli (email, password) VALUES (%s, %s)", (email, hashed_password))
        db.commit()
        return jsonify({"message": "Registrasi berhasil!"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email sudah terdaftar!"}), 400

# API Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pembeli WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Email atau password salah!"}), 401

    # Hash password yang dikirim dengan MD5 dan bandingkan dengan password yang ada di DB
    hashed_password_input = hash_password_md5(password)

    if hashed_password_input != user["password"]:
        return jsonify({"error": "Email atau password salah!"}), 401

    # Buat token JWT
    access_token = create_access_token(identity=user["id"])
    return jsonify({"message": "Login berhasil!", "token": access_token}), 200

if __name__ == "__main__":
    app.run(debug=True)