import streamlit as st
import pandas as pd
from redis_config import get_redis_connection
import streamlit.components.v1 as components

def run():
    r = get_redis_connection()
    if r is None:
        st.error("❌ Não foi possível conectar ao Redis.")
        st.stop()

    st.set_page_config(layout="wide")
    st.title("🏆 Pódio do Festival")

    votos = r.hgetall("votos")
    votos_dict = {k.decode(): int(v.decode()) for k, v in votos.items()} if votos else {}

    if not votos_dict:
        st.info("Ainda não há votos registrados.")
        return

    df = pd.DataFrame(list(votos_dict.items()), columns=["Candidato", "Votos"])
    df_sorted = df.sort_values("Votos", ascending=False).reset_index(drop=True)
    top3 = df_sorted.head(3)

    if len(top3) < 3:
        st.warning("Ainda não há 3 candidatos para exibir no pódio.")
        return

    # Container que engloba o pódio + confete
    with st.container():
        # Colunas do pódio
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"<div style='background:#8c8c8c; padding:20px; border-radius:10px; text-align:center; height:250px;'>"
                f"<h3>🥈 {top3.iloc[1]['Candidato']}</h3>"
                f"<p style='font-size:22px;'>{top3.iloc[1]['Votos']} votos</p>"
                "</div>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div style='background:#ceae0e; padding:20px; border-radius:10px; text-align:center; height:350px;'>"
                f"<h2 style='margin-top:50px;'>🥇 {top3.iloc[0]['Candidato']}</h2>"
                f"<p style='font-size:26px; font-weight:bold;'>{top3.iloc[0]['Votos']} votos</p>"
                "</div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div style='background:#CD7F32; padding:20px; border-radius:10px; text-align:center; height:240px;'>"
                f"<h3>🥉 {top3.iloc[2]['Candidato']}</h3>"
                f"<p style='font-size:20px;'>{top3.iloc[2]['Votos']} votos</p>"
                "</div>",
                unsafe_allow_html=True
            )

        # Confete infinito sobre o container do pódio
        components.html(
            """
            <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
            <canvas id="confetti" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none;"></canvas>
            <script>
            const canvas = document.getElementById('confetti');
            const myConfetti = confetti.create(canvas, { resize: true, useWorker: true });

            function randomInRange(min, max) { return Math.random() * (max - min) + min; }

            function shootConfetti() {
                myConfetti({
                    particleCount: 5,
                    angle: randomInRange(55, 125),
                    spread: randomInRange(50, 70),
                    origin: { y: 0 },
                    colors: ['#ff0','#f0f','#0ff','#f00','#0f0','#00f']
                });
            }

            setInterval(shootConfetti, 200);
            </script>
            """,
            height=0,
        )
