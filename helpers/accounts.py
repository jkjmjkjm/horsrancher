from functools import wraps
from flask import session, redirect, request
import helpers
from werkzeug.security import generate_password_hash, check_password_hash

import helpers.database

def signed_in():
    return session.get("user_id") != None;

def current_email():
    if signed_in():
        return helpers.database.execute_without_freezing("SELECT email FROM user WHERE ID = ?", session.get("user_id"))[0]['email']
    else:
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signin/?f=1&next="+request.path)
        return f(*args, **kwargs)
    return decorated_function

def can_create_center(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signin/?f=1&next="+request.path)
        if not link_center()[1] == "No center linked to user":
            return redirect("/manage/")
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
        session["user_id"] = helpers.database.execute("INSERT INTO user (email, hash) VALUES (?, ?)", email, generate_password_hash(password))
        return 0, ""

def sign_out():
    session["user_id"] = None
    session["center_id_auth"] = None

def link_center():
    if session.get("user_id") == None:
        return 1, "No user logged in"
    row = helpers.database.execute_without_freezing("SELECT ID FROM center WHERE accountID = ?", session.get("user_id"))
    if len(row) != 1:
        return 1, "No center linked to user"
    return 0, row[0]['ID']
