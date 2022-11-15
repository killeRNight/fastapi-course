"""

Password hashing utils.

"""


from passlib.context import CryptContext


pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


def hash_password(password: str):
    """Hash password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Compare passwords"""
    return pwd_context.verify(plain_password, hashed_password)
