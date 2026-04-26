import streamlit as st
import pandas as pd

# Cargar usuarios
@st.cache_data
def cargar_usuarios():
    df = pd.read_csv("data/hey_clientes.csv")
    return df["user_id"].astype(str).tolist()

usuarios_validos = cargar_usuarios()

# Estado de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login
if not st.session_state.logged_in:
    st.title("Havi 2.0")

    user_input = st.text_input("Ingresa tu user_id")

    if st.button("Entrar"):
        if user_input in usuarios_validos:
            st.session_state.logged_in = True
            st.session_state.user_id = user_input
            st.success("Acceso concedido")
            st.rerun()
        else:
            st.error("Usuario no válido")

# Pantalla después de login
else:
    st.title("Bienvenido")
    st.write(f"Tu user_id es: {st.session_state.user_id}")

    if st.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()
