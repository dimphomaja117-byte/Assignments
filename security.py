# security.py
# Secure password hashing using PBKDF2

import hashlib
import os

def hash_password(password: str) -> str:
    """Returns a salted hash in the form 'salt$hash' (PBKDF2-HMAC-SHA256)."""
    salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt), 200_000
    ).hex()
    return f"{salt}${digest}"

def verify_password(password: str, stored: str) -> bool:
    """Checks a plain password against a stored hash."""
    if not stored:
        return False
    if "$" in stored:
        salt, expected = stored.split("$", 1)
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt), 200_000
        ).hex()
        return digest == expected
    # Legacy unsalted SHA-256 fallback
    return hashlib.sha256(password.encode()).hexdigest() == stored