import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from redis_config import get_redis_connection
from cronometro import exibir_cronometro
from votacao import tempo_restante

r = get_redis_connection()
if r is None:
    st.error("Não foi possível conectar ao Redis. Verifique a configuração.")
    st.stop()

# Função para exibir os resultados
def exibir_resultados():
    votos = r.hgetall("votos")  # Pega os votos do Redis
    if votos:
        votos_formatados = {k.decode('utf-8'): int(v) for k, v in votos.items()}

        # Criar um DataFrame com os resultados
        df = pd.DataFrame(list(votos_formatados.items()), columns=["Candidatos", "Votos"])

        # Exibir título
        st.title("Resultados da Votação")

        # Exibir a tabela
        st.subheader("Cotação dos Votos")
        st.table(df.set_index('Candidatos'))  # Remover o índice extra

        # Mostrar o total de votos
        total_votos = df["Votos"].sum()  # Soma dos votos
        st.subheader(f"Total de Votos: {total_votos}")
    else:
        st.warning("Ainda não há votos registrados.")

# Lógica de controle de abertura da votação
restante = tempo_restante()
if restante <= timedelta(seconds=0):
    # Exibir um botão para iniciar a votação
    admin_token = st.text_input("Código de Admin", type="password")
    if admin_token == "admin123":
        st.success("Acesso de administrador concedido!")
        tempo_votacao = st.number_input("Defina o tempo de votação (em minutos)", min_value=1, value=4)
        tempo_votacao = timedelta(minutes=tempo_votacao)  # Definindo o tempo da votação
        if st.button("Iniciar Votação"):
            tempo_fim = datetime.now() + tempo_votacao  # Calcula o tempo de fim
            r.set("tempo_fim", tempo_fim.isoformat())  # Armazena o tempo de fim no Redis
            st.success(f"Votação iniciada! A votação terminará em {tempo_votacao}.")
        if st.button("Encerrar Votação Agora"):
            r.set("tempo_fim", datetime.now().isoformat())
            st.success("✅ Votação encerrada!")
    else:
        st.warning("Você precisa inserir o código de administrador para iniciar a votação.")
else:
    st.warning("A votação já foi iniciada.")
    if st.button("Encerrar Votação Agora"):
            r.set("tempo_fim", datetime.now().isoformat())
            st.success("✅ Votação encerrada!")

exibir_resultados()
exibir_cronometro(r)