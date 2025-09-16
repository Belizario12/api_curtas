import time
from datetime import datetime, timedelta
import streamlit as st
from streamlit_cookies_controller import CookieController
from dotenv import load_dotenv
from redis_config import get_redis_connection
from cronometro import exibir_cronometro
import pandas as pd

# ----------------- Configurações iniciais -----------------
load_dotenv()
st.set_page_config(page_title="Votação Festival", layout="wide")

r = get_redis_connection()
if r is None:
    st.error("❌ Não foi possível conectar ao Redis. Verifique a configuração.")
    st.stop()

controller = CookieController()
candidatos = ["Candidato A", "Candidato B", "Candidato C", "Candidato D"]

# ----------------- Funções auxiliares -----------------
def tempo_restante():
    tempo_fim = r.get("tempo_fim")
    if tempo_fim:
        tempo_fim = datetime.fromisoformat(tempo_fim.decode("utf-8"))
        restante = tempo_fim - datetime.now()
        return restante
    return timedelta(seconds=0)

def get_votos():
    votos = r.hgetall("votos")
    return {k.decode(): int(v.decode()) for k, v in votos.items()}

# ----------------- Lógica de votação -----------------
restante = tempo_restante()
ip_usuario = controller.get("ajs_anonymous_id")

if ip_usuario and r.sismember("votantes", ip_usuario):
    votos_realizados = True
else:
    st.session_state.ip_usuario = ip_usuario
    votos_realizados = False

# ----------------- Sidebar de navegação -----------------
st.sidebar.title("📌 Navegação")
pagina = st.sidebar.radio("Ir para:", ["Votação", "Resultados"])

# ----------------- Página de Votação -----------------
if pagina == "Votação":
    st.title("🗳️ Vote no seu candidato favorito!")
    st.info("Escolha um candidato abaixo e confirme seu voto.")

    if restante > timedelta(seconds=0) and not votos_realizados:
        cols = st.columns(2)  # Mostrar 2 candidatos por linha
        for idx, candidato in enumerate(candidatos):
            with cols[idx % 2]:
                st.markdown(f"### 🎬 {candidato}")
                if st.button(f"Votar em {candidato}", key=candidato, type="primary"):
                    if ip_usuario is None:
                        ip_usuario = controller.get("ajs_anonymous_id")
                    r.sadd("votantes", ip_usuario)
                    r.hincrby("votos", candidato, 1)
                    st.success(f"✅ Você votou em **{candidato}**!")
                    st.balloons()

        exibir_cronometro(r)

    elif restante > timedelta(seconds=0) and votos_realizados:
        st.warning("⚠️ Você já votou. Aguarde o fim do período de votação.")
        exibir_cronometro(r)

    elif restante <= timedelta(seconds=0) and not votos_realizados:
        st.warning("⏳ O período de votação ainda não começou!")

    elif restante <= timedelta(seconds=0) and votos_realizados:
        st.warning("✅ Obrigado pelo seu voto!")

# ----------------- Página de Resultados -----------------
elif pagina == "Resultados":
    st.title("📊 Resultados da Votação")
    votos_dict = get_votos()

    if votos_dict:
        df = pd.DataFrame(list(votos_dict.items()), columns=["Candidato", "Votos"])
        df_sorted = df.sort_values("Votos", ascending=False)

        st.subheader("Ranking dos candidatos")
        for i, row in df_sorted.iterrows():
            medalha = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🎬"
            st.markdown(f"{medalha} **{row['Candidato']}** — {row['Votos']} votos")

        st.subheader("Gráfico de Votos")
        st.bar_chart(df.set_index("Candidato"))
    else:
        st.info("Ainda não há votos registrados.")

# ----------------- Estilo customizado -----------------
st.markdown("""
    <style>
    .stButton button {
        background-color: #3A46FF;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #2c34cc;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)
