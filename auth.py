import hashlib
import json
import os
import secrets

FICHIER = "users.json"


def _hasher(mot_de_passe, sel_hex):
    return hashlib.pbkdf2_hmac(
        "sha256", mot_de_passe.encode(), bytes.fromhex(sel_hex), 200_000
    ).hex()


def _charger():
    if not os.path.exists(FICHIER):
        return {}
    with open(FICHIER, "r", encoding="utf-8") as f:
        return json.load(f)


def creer_utilisateur(nom, mot_de_passe):
    users = _charger()
    sel = secrets.token_hex(16)
    users[nom] = {"sel": sel, "hash": _hasher(mot_de_passe, sel)}
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def verifier(nom, mot_de_passe):
    user = _charger().get(nom)
    if not user:
        return False
    return secrets.compare_digest(user["hash"], _hasher(mot_de_passe, user["sel"]))