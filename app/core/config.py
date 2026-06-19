import os
from pathlib import Path

def load_dotenv(path: str = ".env") -> None:
    # 1. Tenta achar o .env no diretório atual do terminal
    env_path = Path(path)
    
    # 2. Se não achar, calcula o caminho dinamicamente baseado na posição deste arquivo config.py
    if not env_path.exists():
        # Se config.py está em app/core/config.py, parent.parent.parent volta para a raiz do projeto
        env_path = Path(__file__).resolve().parent.parent.parent / ".env"
        
    if not env_path.exists():
        return

    with env_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value

# Executa o carregador inteligente antes de criar as configurações
load_dotenv()

class Settings:
    PROJECT_NAME: str = "API APP-ECOVETOR"
    
    # Inteligente: tenta pegar DATABASE_URL, se não achar tenta MONGO_URI, se não achar usa o local
    DATABASE_URL: str = os.getenv("DATABASE_URL") or os.getenv("MONGO_URI") or "mongodb://localhost:27017"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "chave-super-secreta-mudar-depois")

settings = Settings()