from functools import wraps
from flask import session, redirect
import helpers
from werkzeug.security import generate_password_hash, check_password_hash

import helpers.database

def signed_in():
    return 0

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signin/")
        return f(*args, **kwargs)
    return decorated_function

def sign_in(email, password):
    row = helpers.database.execute_without_freezing("SELECT * FROM user WHERE email = ?", email)
    if len(row) != 1:
        return 1, "Parece que esa cuenta no existe"
    else:
        row = row[0]
    if check_password_hash(row['hash'], password):
        session["user_id"] = row['ID']
        return 0, None
    else:
        return 1, "Contraseña incorrecta"

def sign_up(email, password):
    row = helpers.database.execute_without_freezing("SELECT * FROM user WHERE email = ?", email)
    if len(row) > 0:
        return 1, "Ya existe una cuenta con este correo electrónico"
    else:
        helpers.database.execute("INSERT INTO user (email, hash) VALUES (?, ?)", email, generate_password_hash(password))
        session["user_id"] = row['ID']
        return 0, ""
    
def link_center():
    if session.get("user_id") == None:
        return 1, "No user logged in"
    row = helpers.database.execute_without_freezing("SELECT ID FROM center WHERE account_id = ?", session.get("user_id"))