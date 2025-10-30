from app.models.user import User
from app.extensions import db, bcrypt

def create_user(username, password, email, nama):
    hashed = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, password=hashed, email=email, nama=nama)
    db.session.add(user)
    db.session.commit()
    return user

def get_all_users():
    return User.query.with_entities(User.id, User.username, User.email, User.nama).all()

def update_user(user_id, username, email, nama):
    user = User.query.get(user_id)
    if not user:
        return None
    user.username = username
    user.email = email
    user.nama = nama
    db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return None
    db.session.delete(user)
    db.session.commit()
    return user

def check_login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None
