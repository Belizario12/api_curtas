import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from redis_config import get_redis_connection
from cronometro import exibir_cronometro
from utils import tempo_restante

def run():
    r = get_redis_connection()
    if r is None:
        st.error("❌ Não foi possível conectar ao Redis.")
        st.stop()

    st.title("📊 Resultados da Votação")

    restante = tempo_restante(r)

    if restante <= timedelta(seconds=0):
        admin_token = st.text_input("Código de Admin", type="password")
        if admin_token == "admin123":
            st.success("Acesso de administrador concedido!")
            tempo_votacao = st.number_input("Defina o tempo (em minutos)", min_value=1, value=4)
            tempo_votacao = timedelta(minutes=tempo_votacao)

            if st.button("Iniciar Votação"):
                tempo_fim = datetime.now() + tempo_votacao
                r.set("tempo_fim", tempo_fim.isoformat())
                st.success(f"✅ Votação iniciada por {tempo_votacao} minutos!")

            if st.button("Encerrar Votação Agora"):
                r.set("tempo_fim", datetime.now().isoformat())
                st.success("✅ Votação encerrada!")
        else:
            st.warning("⚠️ Insira o código de administrador para iniciar a votação.")
    else:
        st.warning("⚠️ A votação já foi iniciada.")
        if st.button("Encerrar Votação Agora"):
            r.set("tempo_fim", datetime.now().isoformat())
            st.success("✅ Votação encerrada!")

    # Exibir votos
    votos = r.hgetall("votos")
    if votos:
        votos_dict = {k.decode(): int(v) for k, v in votos.items()}
        df = pd.DataFrame(list(votos_dict.items()), columns=["Candidato", "Votos"])

        st.subheader("📋 Tabela de Votos")
        st.table(df.set_index("Candidato"))

        st.subheader(f"📊 Total de Votos: {df['Votos'].sum()}")
    else:
        st.info("Ainda não há votos registrados.")

    exibir_cronometro(r)
