import streamlit as st
import requests

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("🤖 Groq Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! How can i help you today?"}
    ]

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Upload file
uploaded_file = st.file_uploader("Upload PDF, DOCX, TXT, or Image", type=["pdf", "docx", "txt", "jpg", "png", "jpeg"])
if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    try:
        res = requests.post("https://deploy-llm-with-groq.onrender.com/upload", files=files)
        extracted = res.json().get("response", "")
        st.session_state.messages.append({"role": "user", "content": f"[Uploaded file: {uploaded_file.name}]"})
        st.session_state.messages.append({"role": "assistant", "content": f"Here's what I found in the document:\n\n{extracted}"})
    except Exception as e:
        st.error("Error processing file.")

# Chat input
user_input = st.chat_input("Type your message...")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = requests.post(
            "https://deploy-llm-with-groq.onrender.com/chat",
            json={"message": user_input}
        )
        reply = response.json().get("response", "No response received.")
    except:
        reply = "⚠️ Error contacting backend."

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})


