from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        # Convierte la contraseña en un Hash seguro usando bcrypt
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # verifica que la contraseña ingresada por el usuario coincida con el hash almacenado en la base de datos
        return pwd_context.verify(plain_password, hashed_password)
