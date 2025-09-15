import time
from datetime import datetime, timedelta
import streamlit as st
from streamlit_cookies_controller import CookieController
from dotenv import load_dotenv
from redis_config import get_redis_connection
from cronometro import exibir_cronometro


load_dotenv()

r = get_redis_connection()
if r is None:
    st.error("Não foi possível conectar ao Redis. Verifique a configuração.")
    st.stop()

controller = CookieController()

candidatos = ["Candidato A", "Candidato B", "Candidato C", "Candidato D"]

# Função para verificar o tempo restante
def tempo_restante():
    tempo_fim = r.get("tempo_fim")
    if tempo_fim:
        tempo_fim = datetime.fromisoformat(tempo_fim.decode('utf-8'))
        restante = tempo_fim - datetime.now()
        return restante
    return timedelta(seconds=0)

restante = restante = tempo_restante()

# Verificar se a pessoa já votou
ip_usuario = controller.get("ajs_anonymous_id")
if ip_usuario and r.sismember("votantes", ip_usuario):
    votos_realizados = True
else:
    st.session_state.ip_usuario = ip_usuario
    votos_realizados = False

# Exibir o cronômetro com atualização dinâmica
cronometro = st.empty()  # Criando o componente vazio


# Votação
if restante > timedelta(seconds=0) and not votos_realizados:
    st.title("Vote no seu candidato favorito!")
    # Botões de votação
    for candidato in candidatos:
        if st.button(f"Votar em {candidato}"):
            if ip_usuario is None:  # Registrar o IP da pessoa
                ip_usuario = controller.get("ajs_anonymous_id")
            r.sadd("votantes", ip_usuario)  # Registra que o IP já votou
            r.hincrby("votos", candidato, 1)  # Incrementa o voto para o candidato
            st.success(f"Você votou em {candidato}!")
    exibir_cronometro(r)

elif restante > timedelta(seconds=0) and votos_realizados:
    # Exibir o status da votação, mas sem os botões
    st.warning("Por favor aguarde o fim do período de votação.")
    exibir_cronometro(r)

elif restante <= timedelta(seconds=0) and not votos_realizados:
    st.warning("O período de votação irá começar em instantes!")

elif restante <= timedelta(seconds=0) and votos_realizados:
    st.warning("Obrigado pelo seu voto!")
