import streamlit as st
import os
from dotenv import load_dotenv
from src.mentor import get_mentor_response

# Charger la clé API du fichier .env
load_dotenv()

# Configuration de la page
st.set_page_config(page_title="Data Tech Mentor", page_icon="🤖")

st.title("🎓 Mentor Technique Data")
st.markdown("Révisez SQL, Python, ML et Data Engineering avec un expert IA.")

# Initialiser l'historique des messages dans la session Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Premier message du Mentor
    initial_prompt = "Bonjour ! Je suis ton mentor. Es-tu prêt pour une question de Data Science ou de Data Engineering aujourd'hui ?"
    st.session_state.messages.append({"role": "assistant", "content": initial_prompt})

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie de l'utilisateur
if prompt := st.chat_input("Ta réponse ou ton code ici..."):
    # Ajouter le message de l'utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Générer la réponse du Mentor
    with st.chat_message("assistant"):
        with st.spinner("Le mentor réfléchit..."):
            # On passe l'historique pour garder le contexte
            full_history = st.session_state.messages
            response = get_mentor_response(prompt, full_history)
            st.markdown(response)
            
    # Ajouter la réponse du mentor à l'historique
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar pour les options
with st.sidebar:
    st.header("Paramètres")
    role = st.selectbox("Cible", ["Data Scientist", "Data Engineer", "ML Ops"])
    if st.button("Réinitialiser la session"):
        st.session_state.messages = []
        st.rerun()