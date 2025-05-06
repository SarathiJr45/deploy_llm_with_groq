import streamlit as st
import requests

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("🤖 Groq Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your Groq-powered chatbot. How can I help you today?"}
    ]

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")

# Chat input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", key="user_input", placeholder="Type your message here...")
    submit = st.form_submit_button("Send")

if submit and user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call the backend
    try:
        response = requests.post(
            "https://deploy-llm-with-groq.onrender.com/chat",
            json={"message": user_input}
        )
        reply = response.json().get("response", "No response received.")
    except Exception as e:
        reply = "⚠️ Error contacting backend."

    # Add assistant reply to history
    st.session_state.messages.append({"role": "assistant", "content": reply})
