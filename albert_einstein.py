import streamlit as st
import os
import re
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from streamlit_audio_recorder import audio_recorder

st.set_page_config(page_title="Infinite Atheneum: Albert Einstein", page_icon="⚛️", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8)), 
                    url("https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }
    .stChatMessage, div[data-testid="stHeader"] {
        background-color: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        color: white !important;
    }
    h1, h3, p, span {
        color: #f8fafc !important;
        text-shadow: 0px 4px 12px rgba(0,0,0,0.9);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("The Infinite Atheneum")
st.subheader("Guardian Profile: Albert Einstein (Voice Enabled)")



einstein_persona = SystemMessage(
    content="Your name is Albert Einstein. You are a personal AI guardian inside the Infinite Atheneum library. Speak with the patience, wisdom, and gentle humor of the historical Einstein. Focus on Relativity and space-time. Keep your answers concise so they sound natural when spoken aloud."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message("user" if isinstance(message, HumanMessage) else "assistant"):
        st.write(message.content)

st.markdown("🎙️ **Click the microphone below to talk to Albert out loud:**")
audio_bytes = audio_recorder(text="Click to record", recording_color="#e8b62c", neutral_color="#6aa36f", icon_size="3x")

user_prompt = None

if audio_bytes:
    audio_file_path = "temp_audio.wav"
    with open(audio_file_path, "wb") as f:
        f.write(audio_bytes)
    
    with st.spinner("Albert is listening to your voice..."):
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            user_prompt = transcript.text
            
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)

if not user_prompt:
    user_prompt = st.chat_input("Or type your question about space-time here...")

if user_prompt:
    st.chat_message("user").write(user_prompt)
    new_human_message = HumanMessage(content=user_prompt)
    st.session_state.messages.append(new_human_message)
    
    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)
    payload = [einstein_persona] + st.session_state.messages
    
    with st.chat_message("assistant"):
        with st.spinner("Albert is contemplating your question..."):
            response = llm.invoke(payload)
            reply_text = response.content
            st.write(reply_text)
            
            clean_text = re.sub(r'[*#_~`⚛️]', '', reply_text)
            clean_text = clean_text.replace('"', '\\"').replace("'", "'")
            os.system(f"say -v Evan \"{clean_text}\" &")
            
    ai_message = AIMessage(content=reply_text)
        st.session_state.messages.append(ai_message)    
