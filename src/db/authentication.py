import hashlib
import bcrypt

def hash_password(password: str) -> str:
    sha_hex = hashlib.sha256(password.encode("utf-8")).hexdigest().encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(sha_hex, salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    sha_hex = hashlib.sha256(password.encode("utf-8")).hexdigest().encode("utf-8")
    return bcrypt.checkpw(sha_hex, hashed.encode("utf-8"))
