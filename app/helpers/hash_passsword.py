from hashlib import sha256

def hash_password(password):
    password = password.encode()
    password_hash = sha256(password).hexdigest()

    return password_hash