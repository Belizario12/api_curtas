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
        col1, col2, col3 = st.columns([1,1,1])

        with col1:
            st.markdown(
                f"""
                <div style="background:linear-gradient(135deg,#C0C0C0,#E0E0E0);
                            padding:20px; border-radius:15px; text-align:center;
                            height:200px; box-shadow:0px 4px 12px rgba(0,0,0,0.3);">
                    <h2 style="margin:0;">🥈</h2>
                    <h3 style="margin:5px 0;">{top3.iloc[1]['Candidato']}</h3>
                    <p style="font-size:22px; font-weight:bold; margin:0;">
                        {top3.iloc[1]['Votos']} votos
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style="background:linear-gradient(135deg,#FFD700,#FFEA70);
                            padding:25px; border-radius:15px; text-align:center;
                            height:260px; box-shadow:0px 6px 15px rgba(0,0,0,0.4);">
                    <h2 style="margin:0;">🥇</h2>
                    <h2 style="margin:5px 0; font-size:28px;">{top3.iloc[0]['Candidato']}</h2>
                    <p style="font-size:28px; font-weight:bold; margin:0;">
                        {top3.iloc[0]['Votos']} votos
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div style="background:linear-gradient(135deg,#CD7F32,#E6A36D);
                            padding:20px; border-radius:15px; text-align:center;
                            height:160px; box-shadow:0px 4px 12px rgba(0,0,0,0.3);">
                    <h2 style="margin:0;">🥉</h2>
                    <h3 style="margin:5px 0;">{top3.iloc[2]['Candidato']}</h3>
                    <p style="font-size:20px; font-weight:bold; margin:0;">
                        {top3.iloc[2]['Votos']} votos
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.info("Ainda não há votos registrados.")
