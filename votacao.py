import time
from datetime import timedelta
import streamlit as st
from streamlit_cookies_controller import CookieController
from dotenv import load_dotenv
from redis_config import get_redis_connection
from cronometro import exibir_cronometro
from utils import tempo_restante

def run():
    # ----------------- Configurações iniciais -----------------
    load_dotenv()
    st.set_page_config(page_title="Votação Festival", layout="wide")

    r = get_redis_connection()
    if r is None:
        st.error("❌ Não foi possível conectar ao Redis. Verifique a configuração.")
        st.stop()

    controller = CookieController()
    candidatos = [
        "Rastreio na Produção de Imagens e Vídeos Gerados por IA e Suas Implicações Legais",
        "O Despertar da Consciência: Inteligência Artificial sob a Perspectiva de Frankenstein",
        "ECO: O Silêncio da Mente",
        "O Futuro Fácil",
        "IA e Ética: Até Onde a Tecnologia Pode Substituir a Humanidade?",
        "Confissões para a Máquina",
        "O Impacto dos Criadores de Conteúdo na Subjetividade dos Usuários",
        "IA: Quem é o Dono da Arte?",
        "Segurança Digital: Golpes Mais Comuns de IA na Internet",
        "Quem é o Dono? Um Curta sobre Arte, IA e Propriedade Intelectual",
        "O Robô Preconceituoso",
        "IARA",
        "Robôs Artistas: Quem Leva o Crédito? A Guerra da Desinformação",
    ]

    # ----------------- Lógica de votação -----------------
    restante = tempo_restante(r)
    ip_usuario = controller.get("ajs_anonymous_id")

    if ip_usuario and r.sismember("votantes", ip_usuario):
        votos_realizados = True
    else:
        st.session_state.ip_usuario = ip_usuario
        votos_realizados = False

    # ----------------- Página de Votação -----------------
    st.title("🗳️ Vote no seu curta favorito!")

    if restante > timedelta(seconds=0) and not votos_realizados:
        st.info("Escolha um curta abaixo e confirme seu voto.")

        # Layout em duas colunas
        cols = st.columns(2)

        for idx, candidato in enumerate(candidatos):
            with cols[idx % 2]:
                # Card do candidato usando container
                with st.container(border=True):
                    st.subheader(f"🎬 {candidato}")
                    if st.button("Votar", key=candidato, use_container_width=True, type="primary"):
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
