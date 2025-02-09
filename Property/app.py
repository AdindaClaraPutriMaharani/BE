from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import mysql.connector

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Ganti dengan secret key yang aman
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Koneksi ke database MySQL
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='real_estate'  # Menggunakan database baru
)
cursor = db.cursor()

# ------------------ USER AUTH ------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nama = data['nama']
    email = data['email']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    no_telepon = data['no_telepon']
    
    sql = "INSERT INTO Users (nama, email, password_hash, no_telepon) VALUES (%s, %s, %s, %s)"
    values = (nama, email, password, no_telepon)
    
    try:
        cursor.execute(sql, values)
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    sql = "SELECT id, password_hash FROM Users WHERE email = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    # Debugging
    print("User fetched from DB:", user)  # Cek isi variabel user

    if user is str:
        return jsonify({"message": "User not found"}), 404  # Jika user tidak ditemukan

    user_id, stored_password_hash = user  # Unpacking hasil query
    
    # Debugging
    print("Stored Password Hash:", stored_password_hash)  # Cek isi hash dari database
    
    if stored_password_hash is None:
        return jsonify({"message": "Password hash is empty"}), 500

    if bcrypt.check_password_hash(stored_password_hash, password):
        access_token = create_access_token(identity=str(user_id))  # Ubah ID ke string
        return jsonify({"token": access_token})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ------------------ CRUD RUMAH ------------------
@app.route('/houses', methods=['GET'])
def get_houses():
    cursor.execute("SELECT * FROM Rumah")
    houses = cursor.fetchall()
    return jsonify(houses)

@app.route('/houses/<int:id>', methods=['GET'])
def get_house(id):
    cursor.execute("SELECT * FROM Rumah WHERE id_rumah = %s", (id,))
    house = cursor.fetchone()
    return jsonify(house) if house else jsonify({"message": "House not found"}), 404

@app.route('/houses', methods=['POST'])
@jwt_required()
def add_house():
    data = request.get_json()
    sql = "INSERT INTO Rumah (id_pemilik, alamat, luas, jumlah_kamar, jumlah_kamar_mandi, harga, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (data['id_pemilik'], data['alamat'], data['luas'], data['jumlah_kamar'], data['jumlah_kamar_mandi'], data['harga'], data['status']))
    db.commit()

    return jsonify({"message": "House added successfully"}), 201

@app.route('/houses/<int:id>', methods=['PUT'])
@jwt_required()
def update_house(id):
    data = request.get_json()
    sql = "UPDATE Rumah SET id_pemilik=%s, alamat=%s, luas=%s, jumlah_kamar=%s, jumlah_kamar_mandi=%s, harga=%s, status=%s WHERE id_rumah=%s"
    cursor.execute(sql, (data['id_pemilik'], data['alamat'], data['luas'], data['jumlah_kamar'], data['jumlah_kamar_mandi'], data['harga'], data['status'], id))
    db.commit()
    return jsonify({"message": "House updated successfully"})

@app.route('/houses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_house(id):
    cursor.execute("DELETE FROM Rumah WHERE id_rumah = %s", (id,))
    db.commit()
    return jsonify({"message": "House deleted successfully"})

# ------------------ CRUD TRANSAKSI ------------------
@app.route('/transactions', methods=['GET'])
def get_transactions():
    cursor.execute("SELECT * FROM Transaksi")
    transactions = cursor.fetchall()
    return jsonify(transactions)

@app.route('/transactions', methods=['POST'])
@jwt_required()
def add_transaction():
    data = request.get_json()
    sql = "INSERT INTO Transaksi (id_rumah, id_pembeli, tanggal_transaksi, harga) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (data['id_rumah'], data['id_pembeli'], data['tanggal_transaksi'], data['harga']))
    db.commit()
    return jsonify({"message": "Transaction added successfully"}), 201

# ------------------ RUN APP ------------------
if __name__ == '__main__':
    app.run(debug=True)