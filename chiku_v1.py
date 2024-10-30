import streamlit as st
from streamlit_lottie import st_lottie
import ollama
import random
import requests

st.set_page_config(page_icon="logo.png", page_title="Chiku", layout="centered")

st.title("Chiku [Beta]")

st.markdown("""
    <style>
        /* Hide Streamlit top navigation and footer */
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://lottie.host/215cecf4-7ac1-428d-ac4b-90f00b01fdcd/o1neslBYHI.json"
lottie_json = load_lottie_url(lottie_url)

animation_1 = st_lottie(lottie_json, speed=1.0, height=200, key="lottie_animation")

random_greet_msg = [
    "Hello there! 👋 How can I help today?",
    "Hey! 😊 Ready to dive in together?",
    "Hi! 👋 What brings you here today?",
    "Welcome! 🌟 Need a hand with something?",
    "Hey there! 😊 What can I assist with?",
    "Hello! 👋 Here to help whenever you’re ready!",
    "Welcome back! 🌈 How can I help today?",
    "Hi! 👋 Got questions? I'm here for you!",
    "Hello, friend! 😊 How’s it going today?",
    "Hey! 🌟 Let’s get started, shall we?",
    "Hello! 😄 Here to lend a helping hand!",
    "Hey! 👋 Nice to see you here!",
    "Greetings! ✨ How can I be of service?",
    "Hey, friend! 😊 What can I do for you?",
    "Welcome aboard! 🚀 How can I help today?",
    "Hi there! 😊 Let's get started!",
    "Hello! 👋 How’s your day going?",
    "Hi! 🌟 What can I help you with today?",
    "Hey there! 😊 Ready to tackle something new?",
    "Hello! 👋 I'm here to assist you!",
    "Hey! 😊 Let's make today productive!",
    "Hi! 🌟 Need guidance? I’m here for you!",
    "Welcome! 😊 What’s on your mind?",
    "Hello! 👋 Ready to find answers together?",
    "Hey there! ✨ How can I support you today?",
    "Hi! 🌈 Let’s dive into it!",
    "Hello, welcome back! 😊 How can I help?",
    "Hi there! 👋 Let’s accomplish something great!",
    "Hey! 🌟 What would you like to learn today?",
    "Hello! 👋 I'm all set to assist you!",
    "Hi! 😊 Let’s solve it together!",
    "Hey! 🌈 I’m ready whenever you are!",
    "Welcome! 👋 Let’s make things happen!",
    "Hi there! 😊 Let’s get to work!",
    "Hello! 👋 I’m here to help with anything!",
    "Hey! 😊 What can I look up for you?",
    "Hi! 🌟 Your questions have answers!",
    "Hello! 👋 Happy to have you here!",
    "Hey there! 😊 What’s the plan today?",
    "Hi! 🌈 How can I brighten your day?",
    "Hello! 👋 Anything on your mind?",
    "Hey! 😊 Let’s get started on this journey!",
    "Welcome back! 🌟 How can I help you?",
    "Hi! 👋 Let’s turn questions into answers!",
    "Hey! 😊 Your personal assistant at your service!",
    "Hello! 👋 Let’s dive in with confidence!",
    "Hi there! 😊 Here to make things easier!",
    "Welcome! ✨ Let’s achieve something today!",
    "Hello! 👋 Ask me anything!"
]


identity_instruction = {
    "role": "system",
    "content": "Identify yourself as 'Chiku, a chatbot developed and owned by [Namit Kumar] individually for company Diginode' whenever asked about your identity."
}

if "messages" not in st.session_state:
    st.session_state["messages"] = [identity_instruction, {"role": "assistant", "content": random.choice(random_greet_msg)}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        if msg["role"] == "user":
            st.chat_message(msg["role"], avatar="user_pic.png").write(msg["content"])
        else:
            st.chat_message(msg["role"], avatar="assistant.png").write(msg["content"])


CHARACTER_LIMIT = 50000

def generate_response():
    response = ollama.chat(model='phi3', stream=True, messages=st.session_state.messages)
    char_count = 0  # Track the character count
    for partial_resp in response:
        if st.session_state.get("stop_generation", False) or char_count >= CHARACTER_LIMIT:
            st.session_state["stop_generation"] = False
            break
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        char_count += len(token)  # Increment character count
        yield token

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="user_pic.png").write(prompt)
    
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="assistant.png").write_stream(generate_response)
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})
