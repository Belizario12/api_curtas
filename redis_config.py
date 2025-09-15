import os
import redis
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Função para obter a conexão com o Redis
def get_redis_connection():
    host = os.getenv("REDIS_HOST")
    port = os.getenv("REDIS_PORT")
    password = os.getenv("REDIS_PASSWORD")

    # Conectar ao Redis Cloud com SSL configurado
    r = redis.Redis(
        host=host,
        port=port,
        password=password,
    )
    
    # Testar a conexão
    try:
        r.ping()  # Verifica se a conexão está funcionando
        print("Conexão com o Redis estabelecida com sucesso!")
        return r
    except redis.ConnectionError as e:
        print(f"Erro ao conectar ao Redis: {e}")
        return None
