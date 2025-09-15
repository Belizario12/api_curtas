import time
import streamlit as st
from datetime import datetime, timedelta
from redis_config import get_redis_connection

# Função para exibir o cronômetro
def exibir_cronometro(r):
    tempo_fim = r.get("tempo_fim")
    
    if tempo_fim:
        tempo_fim = datetime.fromisoformat(tempo_fim.decode('utf-8'))
        restante = tempo_fim - datetime.now()

        # Usar o st.empty() para atualizar o cronômetro
        cronometro = st.empty()  # Componente vazio para atualizar dinamicamente

        if restante > timedelta(seconds=0):
            # Atualiza o cronômetro a cada segundo
            while restante > timedelta(seconds=0):
                cronometro.subheader(f"Tempo restante: {str(restante).split('.')[0]}")
                time.sleep(1)  # Espera 1 segundo antes de atualizar
                restante = tempo_fim - datetime.now()

            cronometro.subheader("Tempo de votação encerrado!")
        else:
            cronometro.subheader("Tempo de votação encerrado!")