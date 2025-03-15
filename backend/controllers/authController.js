const fs = require("fs");
const path = "./data/users.json";

// Fungsi untuk membaca users.json
const getUsers = () => {
  const data = fs.readFileSync(path);
  return JSON.parse(data);
};

// Fungsi untuk menyimpan users.json
const saveUsers = (users) => {
  fs.writeFileSync(path, JSON.stringify(users, null, 2));
};

// **REGISTER**
exports.register = (req, res) => {
  const { username, password } = req.body;
  const users = getUsers();

  if (users.find(u => u.username === username)) {
    return res.status(400).json({ message: "Username already exists" });
  }

  const newUser = { id: users.length + 1, username, password };
  users.push(newUser);
  saveUsers(users);

  res.json({ message: "Registration successful", user: newUser });
};

// **LOGIN**
exports.login = (req, res) => {
  const { username, password } = req.body;
  const users = getUsers();

  const user = users.find(u => u.username === username && u.password === password);
  
  if (!user) {
    return res.status(401).json({ message: "Invalid credentials" });
  }

  res.json({ message: "Login successful", token: "dummy-jwt-token" });
};

// **LOGOUT**
exports.logout = (req, res) => {
  res.json({ message: "Logout successful" });
};