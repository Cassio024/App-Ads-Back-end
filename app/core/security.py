import bcrypt

def get_password_hash(password: str) -> str:
    """Transforma a senha em texto limpo em um hash seguro para salvar no banco."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara a senha digitada no login com o hash criptografado do banco."""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)