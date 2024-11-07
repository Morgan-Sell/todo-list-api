import bcrypt


def generate_password_hash(password: str) -> str:
    # generates a random sequence of bytes to be added to the password before hashing
    # salting makes hasing unique and non-reversible
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def check_password_hash(hashed_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
