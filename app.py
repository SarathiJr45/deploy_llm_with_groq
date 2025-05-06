import streamlit as st
import requests

st.title("Groq Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("You:", key="user_input")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    response = requests.post(
        "https://deploy-llm-with-groq.onrender.com",  
        json={"message": user_input}
    )

    reply = response.json()["response"]
    st.session_state["messages"].append({"role": "assistant", "content": reply})

for msg in st.session_state["messages"]:
    st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")
