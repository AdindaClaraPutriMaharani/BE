const { pool } = require('../config/database');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'sapakapolri_jwt_secret_key';
const JWT_EXPIRES_IN = '24h';

async function login(email, password) {
  try {
    const [rows] = await pool.execute(
      'SELECT id, username, email, password_hash, role FROM Users WHERE email = ? AND status = "active"',
      [email]
    );

    if (rows.length === 0) {
      return { success: false, message: 'Email atau password salah' };
    }

    const user = rows[0];
    const isValidPassword = await bcrypt.compare(password, user.password_hash);
    if (!isValidPassword) {
      return { success: false, message: 'Email atau password salah' };
    }

    const token = jwt.sign(
      { userId: user.id, email: user.email, role: user.role },
      JWT_SECRET,
      { expiresIn: JWT_EXPIRES_IN }
    );

    return { success: true, token, user };
  } catch (error) {
    console.error('Login error:', error);
    return { success: false, message: 'Terjadi kesalahan pada server' };
  }
}

async function logout(token) {
  try {
    await pool.execute('UPDATE Sessions SET expires_at = NOW() WHERE session_token = ?', [token]);
    return { success: true };
  } catch (error) {
    console.error('Logout error:', error);
    return { success: false, message: 'Gagal logout' };
  }
}

module.exports = { login, logout };