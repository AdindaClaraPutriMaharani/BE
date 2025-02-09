<?php
$host = "localhost"; // Server database
$user = "root"; // Username default XAMPP
$pass = ""; // Password default kosong
$db   = "pengguna"; // Ganti dengan nama database yang sudah dibuat

// Membuat koneksi
$koneksi = mysqli_connect($host, $user, $pass, $db);

// Cek koneksi
if (!$koneksi) {
    die("Koneksi gagal: " . mysqli_connect_error());
}
echo "Koneksi berhasil!";
?>