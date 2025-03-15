const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'sapakapolri_jwt_secret_key';

function authenticate(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ success: false, message: 'Token tidak ditemukan' });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = { userId: decoded.userId, role: decoded.role };
    next();
  } catch {
    return res.status(401).json({ success: false, message: 'Token tidak valid' });
  }
}

module.exports = { authenticate };