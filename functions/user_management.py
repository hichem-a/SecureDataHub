import json
import os

def load_users():
    """Lädt die Benutzer aus der JSON-Datei"""
    try:
        with open(os.path.join("json", "users.json"), "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_admin_account(username, password, users):
    """Speichert das Admin-Konto in der JSON-Datei"""
    users[username] = {"password": password, "role": "admin"}
    save_users(users)

def add_user_to_system(username, password, users):
    """Fügt einen neuen Benutzer hinzu und speichert ihn in der JSON-Datei"""
    users[username] = {"password": password, "role": "user"}
    save_users(users)

def delete_user(username, users):
    """Löscht einen Benutzer aus der JSON-Datei"""
    if username in users:
        del users[username]
        save_users(users)

def update_user_role(username, role, users):
    """Aktualisiert die Rolle eines Benutzers in der JSON-Datei"""
    if username in users:
        users[username]["role"] = role
        save_users(users)

def save_users(users):
    """Speichert die Benutzer in der JSON-Datei"""
    with open(os.path.join("json", "users.json"), "w") as file:
        json.dump(users, file, indent=4)
