# Horus Ernest Exam 🧠

Aplikasi web fullstack yang dibangun menggunakan **Flask (Python)** sebagai backend dan **Vue.js** sebagai frontend.  
Project ini bertujuan untuk mengimplementasikan arsitektur REST API modular yang bersih, mudah di-maintain, dan terintegrasi dengan sistem autentikasi JWT.

---

## 🚀 Tech Stack

### 🔧 Backend
- Python 3.12+
- Flask 3.x
- Flask-JWT-Extended
- Flask-Swagger
- SQLAlchemy
- MySQL / PostgreSQL
- Flask-Migrate

### 💻 Frontend
- Vue 3
- TailwindCSS + DaisyUI
- Axios (untuk komunikasi API)

---

## 📂 Struktur Folder

horus-ernest-exam/
├── backend/
│ ├── app/
│ │ ├── models/ # Struktur tabel database (ORM)
│ │ ├── routes/ # Endpoint / API logic
│ │ ├── services/ # Logika bisnis (CRUD)
│ │ ├── utils/ # Helper, konfigurasi, ekstensi
│ │ └── init.py # Inisialisasi Flask app
│ ├── migrations/ # File migrasi database
│ ├── run.py # Entry point server Flask
│ ├── .env # Environment variable
│ └── requirements.txt # Daftar dependency backend
│
└── frontend/
├── src/ # File Vue (component, router, store)
├── public/
├── package.json
└── tailwind.config.js

---

## ⚙️ Cara Menjalankan Aplikasi

### 1️⃣ Jalankan Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # (Mac/Linux)
venv\Scripts\activate     # (Windows)

pip install -r requirements.txt
flask db upgrade
python run.py
```
### 2️⃣ Jalankan Frontend
cd frontend
npm install
npm run dev

### 🧠 Alur Aplikasi (Backend)
User Register/Login
Endpoint /users/register → daftar user baru
Endpoint /users/login → autentikasi, mengembalikan JWT token
Autentikasi JWT
Token dikirim oleh frontend melalui header Authorization: Bearer <token>
Flask memverifikasi token sebelum memberikan akses
CRUD Operasi
Menggunakan layer services agar logika bisnis terpisah dari endpoint
Semua operasi ke database dilakukan lewat model SQLAlchemy
Swagger Documentation
Dokumentasi API otomatis dihasilkan dengan @swag_from
Dapat diakses di /apidocs (jika diaktifkan)🔐 Contoh Request API
Register
POST /users/register
Content-Type: application/json
{
  "username": "user",
  "password": "123456"
}
Response
{
  "message": "User berhasil dibuat"
}

🧩 Fitur Utama
✅ Register & Login dengan JWT Auth
✅ Modular architecture (routes, services, models)
✅ Swagger API documentation
✅ CRUD user
✅ Integrasi dengan Vue.js frontend
