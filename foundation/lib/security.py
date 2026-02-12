from passlib.context import CryptContext

class PasswordManager:
    """
    Manages password hashing and verification.
    Decouples from 'passlib' specifics for the rest of the application.
    """
    # Use bcrypt which is standard
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls._pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls._pwd_context.hash(password)
