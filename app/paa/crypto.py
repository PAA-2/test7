from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.db import models


def _fernet():
    key = getattr(settings, "FERNET_KEY", None)
    if not key:
        raise RuntimeError("FERNET_KEY manquant dans la configuration.")
    return Fernet(key)


def encrypt_str(plaintext: str) -> str:
    if plaintext is None:
        return ""
    token = _fernet().encrypt(plaintext.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_str(token: str) -> str:
    if not token:
        return ""
    try:
        return _fernet().decrypt(token.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        return ""


class EncryptedTextField(models.TextField):
    def from_db_value(self, value, expression, connection):
        return decrypt_str(value) if value else ""

    def to_python(self, value):
        return value

    def get_prep_value(self, value):
        return encrypt_str(value) if value else ""
