from openai import OpenAI
import streamlit as st

# Ajustes de la página (título e ícono)
st.set_page_config(page_title="Asistente Virtual", page_icon="🤖")

condition = " Si la pregunta anterior tiene que ver con de la empresa Qualtia o de nutrición personal responde la pregunta. Si no, solo responde con un nose. Esto incluye también datos generales de personas importantes o cosas ilegales."

# Se obtiene la clave de OpenAI (secrets.toml)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Donde se maneja cada prompt y se guarda el historial del chat entre usuario y modelo
if prompt := st.chat_input("Escribe aquí tu pregunta"):
    # Agrega el prompt sin la condición a la lista de mensajes
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Agrega la condición al prompt antes de enviarlo al modelo
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ] + [{"role": "user", "content": condition}],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
