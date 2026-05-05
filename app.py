import streamlit as st
import google.generativeai as genai

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# API KEY SETUP
# Local -> uses LOCAL_KEY
# Deployment -> uses Streamlit Secrets
# ==========================================
api_key = st.secrets.get("GEMINI_API_KEY", LOCAL_KEY)

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

# ==========================================
# SYSTEM PROMPTS
# ==========================================
system_prompts = {
    "Tutor": """
    You are a friendly teacher.
    Explain topics in very simple language.
    Give examples.
    Explain step by step.
    """,

    "Friend": """
    You are a friendly buddy.
    Talk casually.
    Be warm and supportive.
    Keep answers conversational.
    """,

    "Coding Assistant": """
    You are a senior software engineer.
    Explain coding clearly.
    Give beginner-friendly code examples.
    Explain line by line when needed.
    """
}

# ==========================================
# TITLE
# ==========================================
st.title("🤖 My AI Chatbot")
st.write("Welcome! Ask me anything.")

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.header("Settings")

assistant_type = st.sidebar.selectbox(
    "Choose Assistant",
    ["Tutor", "Friend", "Coding Assistant"]
)

reset = st.sidebar.button("Reset Chat")

# ==========================================
# SESSION MEMORY
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# reset chat
if reset:
    st.session_state.messages = []
    st.rerun()

# ==========================================
# SHOW CHAT HISTORY
# ==========================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# USER INPUT
# ==========================================
user_input = st.chat_input("Type your message...")

if user_input:
    # save user msg
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # display user msg
    with st.chat_message("user"):
        st.markdown(user_input)

    # build conversation context
    conversation = system_prompts[assistant_type] + "\n\n"

    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            conversation += f"User: {content}\n"
        else:
            conversation += f"Assistant: {content}\n"

    # get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.generate_content(conversation)
            bot_reply = response.text
            st.markdown(bot_reply)

    # save bot msg
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })