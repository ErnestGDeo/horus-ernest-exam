from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flasgger import swag_from
from app.services.user_service import (
    create_user, get_all_users, update_user, delete_user, check_login
)
from app.models.user import User
from app.extensions import db

users_bp = Blueprint("users", __name__)

# ---------------------------------------
# REGISTER
# ---------------------------------------
@users_bp.route("/users/register", methods=["POST"])
@swag_from({
    'tags': ['Users'],
    'summary': 'Register user baru',
    'description': 'Endpoint untuk mendaftarkan user baru.',
    'consumes': ['application/json'],
    'produces': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'example': 'ernest'},
                    'password': {'type': 'string', 'example': '12345'},
                    'email': {'type': 'string', 'example': 'ernest@example.com'},
                    'nama': {'type': 'string', 'example': 'Ernest Deo'}
                },
                'required': ['username', 'password', 'email', 'nama']
            }
        }
    ],
    'responses': {
        201: {'description': 'Registrasi berhasil'},
        400: {'description': 'Username atau email sudah terdaftar'}
    }
})
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Data tidak valid"}), 400
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "Username sudah terdaftar"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email sudah terdaftar"}), 400

    create_user(data["username"], data["password"], data["email"], data["nama"])
    return jsonify({"message": "Registrasi berhasil"}), 201

# ---------------------------------------
# LOGIN
# ---------------------------------------
@users_bp.route("/users/login", methods=["POST"])
@swag_from({
    'tags': ['Users'],
    'summary': 'Login user',
    'description': 'Endpoint untuk login dan mendapatkan JWT token.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'example': 'ernest'},
                    'password': {'type': 'string', 'example': '12345'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': 'Login berhasil, JWT token dikembalikan'},
        401: {'description': 'Username atau password salah'}
    }
})
def login():
    data = request.get_json()
    user = check_login(data["username"], data["password"])
    if not user:
        return jsonify({"message": "Username atau password salah"}), 401
    token = create_access_token(identity=user.id)
    return jsonify({"message": "Login berhasil", "token": token}), 200

# ---------------------------------------
# GET USERS
# ---------------------------------------
@users_bp.route("/users", methods=["GET"])
@swag_from({
    'tags': ['Users'],
    'summary': 'Ambil semua data user',
    'responses': {
        200: {'description': 'Daftar semua user'}
    }
})
def get_users():
    users = get_all_users()
    result = [
        {"id": u.id, "username": u.username, "email": u.email, "nama": u.nama}
        for u in users
    ]
    return jsonify(result), 200

# ---------------------------------------
# UPDATE USER
# ---------------------------------------
@users_bp.route("/users/<int:user_id>", methods=["PUT"])
@swag_from({
    'tags': ['Users'],
    'summary': 'Update data user',
    'description': 'Update data user berdasarkan ID.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID user yang ingin diupdate'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'example': 'ernest_new'},
                    'email': {'type': 'string', 'example': 'ernest_new@example.com'},
                    'nama': {'type': 'string', 'example': 'Ernest Updated'}
                },
                'required': ['username', 'email', 'nama']
            }
        }
    ],
    'responses': {
        200: {'description': 'Data user berhasil diperbarui'},
        400: {'description': 'Data tidak valid atau duplikat'},
        404: {'description': 'User tidak ditemukan'}
    }
})
def update(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Data tidak valid"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User tidak ditemukan"}), 404

    # Cek duplikasi username dan email
    if "username" in data and data["username"] != user.username:
        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"message": "Username sudah digunakan"}), 400

    if "email" in data and data["email"] != user.email:
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"message": "Email sudah digunakan"}), 400

    # Update
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.nama = data.get("nama", user.nama)

    db.session.commit()

    return jsonify({
        "message": "Data user berhasil diperbarui",
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "nama": user.nama
        }
    }), 200


# ---------------------------------------
# DELETE USER
# ---------------------------------------
@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
@swag_from({
    'tags': ['Users'],
    'summary': 'Hapus user berdasarkan ID',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'required': True,
            'description': 'ID user yang akan dihapus',
            'schema': {'type': 'integer'}
        }
    ],
    'responses': {
        200: {'description': 'User berhasil dihapus'},
        404: {'description': 'User tidak ditemukan'}
    }
})
def delete(user_id):
    user = delete_user(user_id)
    if not user:
        return jsonify({"message": "User tidak ditemukan"}), 404
    return jsonify({"message": "User berhasil dihapus"}), 200

# ---------------------------------------
# LOGOUT
# ---------------------------------------
@users_bp.route("/users/logout", methods=["POST"])
def logout():
    """
    Logout user (opsional, hanya simulasi)
    """
    return jsonify({"message": "Logout berhasil"}), 200
