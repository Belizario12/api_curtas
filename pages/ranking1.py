import streamlit as st
import pandas as pd
from redis_config import get_redis_connection

r = get_redis_connection()
if r is None:
    st.error("❌ Não foi possível conectar ao Redis. Verifique a configuração.")
    st.stop()

def get_votos():
    votos = r.hgetall("votos")
    return {k.decode(): int(v.decode()) for k, v in votos.items()}

st.set_page_config(page_title="Ranking Festival", layout="wide")
st.title("🏆 Pódio do Festival")

votos_dict = get_votos()

if votos_dict:
    df = pd.DataFrame(list(votos_dict.items()), columns=["Candidato", "Votos"])
    df_sorted = df.sort_values("Votos", ascending=False).reset_index(drop=True)
    top3 = df_sorted.head(3)

    if len(top3) < 3:
        st.warning("Ainda não há 3 candidatos para exibir no pódio.")
    else:
        # Colunas para o pódio (2º, 1º, 3º)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div style="background:#C0C0C0; padding:20px; border-radius:10px; text-align:center; height:180px;">
                    <h3>🥈 {top3.iloc[1]['Candidato']}</h3>
                    <p style="font-size:22px;">{top3.iloc[1]['Votos']} votos</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style="background:#FFD700; padding:20px; border-radius:10px; text-align:center; height:240px;">
                    <h3>🥇 {top3.iloc[0]['Candidato']}</h3>
                    <p style="font-size:26px; font-weight:bold;">{top3.iloc[0]['Votos']} votos</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div style="background:#CD7F32; padding:20px; border-radius:10px; text-align:center; height:140px;">
                    <h3>🥉 {top3.iloc[2]['Candidato']}</h3>
                    <p style="font-size:20px;">{top3.iloc[2]['Votos']} votos</p>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.info("Ainda não há votos registrados.")
