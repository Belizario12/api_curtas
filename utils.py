from datetime import datetime, timedelta
from redis_config import get_redis_connection

r = get_redis_connection()

def tempo_restante(r):
    """Calcula o tempo restante da votação baseado no Redis"""
    tempo_fim = r.get("tempo_fim")
    if tempo_fim:
        tempo_fim = datetime.fromisoformat(tempo_fim.decode("utf-8"))
        restante = tempo_fim - datetime.now()
        return restante
    return timedelta(seconds=0)

def get_votos():
    votos = r.hgetall("votos")
    return {k.decode(): int(v.decode()) for k, v in votos.items()}


