import mysql.connector

# Konfigurasi koneksi database
host = "localhost"       # Server database
user = "root"            # Username default XAMPP
password = ""            # Password default (kosong)
database = "pengguna" # Nama database yang dibuat

try:
    # Membuat koneksi ke MySQL
    koneksi = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if koneksi.is_connected():
        print("✅ Koneksi ke database berhasil!")
    
except mysql.connector.Error as e:
    print(f"❌ Koneksi gagal: {e}")

finally:
    if 'koneksi' in locals() and koneksi.is_connected():
        koneksi.close()
        print("🔌 Koneksi ditutup.")