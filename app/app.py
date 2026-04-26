import streamlit as st

# Inicializar estado
if "usuario" not in st.session_state:
    st.session_state.usuario = None

def login():
    st.title("Inicio de sesión")

    usuario = st.text_input("Ingresa tu usuario")

    if st.button("Entrar"):
        if usuario.strip() != "":
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.warning("Por favor ingresa un usuario")

def app_principal():
    st.title("App del banco 🏦")
    st.write(f"Bienvenido, {st.session_state.usuario}")

    if st.button("Cerrar sesión"):
        st.session_state.usuario = None
        st.rerun()

# Control de flujo
if st.session_state.usuario is None:
    login()
else:
    app_principal()
