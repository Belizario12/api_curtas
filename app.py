import streamlit as st
import ranking1, resultados, votacao

st.set_page_config(page_title="Festival", layout="wide")

# Capturar rota pela URL (?page=...)
query_params = st.query_params
page = st.query_params.get("page", "votacao")  # pega o valor ou padrão

# Roteamento
if page == "ranking1":
    ranking1.run()
elif page == "resultados":
    resultados.run()
elif page == "votacao":
    votacao.run()
else:
    st.error("Página não encontrada")

if "page" not in query_params: # Rota padrão ao recarregar
    st.query_params["page"] = "votacao"
