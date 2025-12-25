import streamlit as st
import os
import tempfile
import speech_recognition as sr
from huggingface_hub import InferenceClient
import docx2txt  # Lightweight Word processing

# --------------------------------------------------
# CONFIG & SETTINGS
# --------------------------------------------------
st.set_page_config(page_title="Kolachi", layout="wide")
st.title("🏫 Kolachi😋 - AI Assistant🤖")

# API Setup
HF_TOKEN = st.secrets["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"]

MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"
hf_client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

# --------------------------------------------------
# DATA LOADING (Simplified RAG)
# --------------------------------------------------
@st.cache_resource
def load_hotel_knowledge():
    try:
        # یہاں بھی r" " کا استعمال کریں
        path = "HotelData.docx"
        if os.path.exists(path):
            return docx2txt.process(path)
        else:
            # یہاں r" " لگانے سے \R والی وارننگ ختم ہو جائے گی
            return r"Error: HotelData.docx not found at E:\RajaCCP\HotelData.docx"
    except Exception as e:
        return f"Error reading document: {e}"
# Load the hotel data into memory
hotel_context = load_hotel_knowledge()

# --------------------------------------------------
# VOICE & RESPONSE LOGIC
# --------------------------------------------------
def speech_to_text(audio_bytes):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        audio_path = f.name
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

def generate_hotel_response(user_query):
    # System instructions using your provided HotelData.docx content
    system_prompt = f"""
    You are the official AI assistant for Kolachi (managed by Raja).
    Use the following hotel information to answer questions. 
    If the answer isn't in the info, politely say "Please contact our manager Raja  directly for that!"
    
    HOTEL INFORMATION:
    {hotel_context}
    """
    
    messages = [{"role": "system", "content": system_prompt}]
    # Context window: last 5 messages
    for msg in st.session_state.messages[-5:]:
        messages.append(msg)
    messages.append({"role": "user", "content": user_query})

    try:
        response = ""
        # Improved error handling for the API stream
        for chunk in hf_client.chat_completion(messages, max_tokens=500, stream=True):
            if chunk.choices and chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
        return response if response else "I'm sorry, I couldn't generate a response. Please try again."
    except Exception as e:
        return f"⚠️ Service is busy: {str(e)}"

# --------------------------------------------------
# UI & SESSION STATE
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to Kolachi! How can I help you today?"}]

if "last_processed_audio" not in st.session_state:
    st.session_state.last_processed_audio = None

# Sidebar for controls
with st.sidebar:
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = [{"role": "assistant", "content": "Welcome back! How can I help you?"}]
        st.session_state.last_processed_audio = None
        st.rerun()

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --------------------------------------------------
# INPUT HANDLING
# --------------------------------------------------
col1, col2 = st.columns([0.85, 0.15])
with col1:
    text_input = st.chat_input("Ask about the menu, check-in, or hotel rules...")
with col2:
    voice_data = st.audio_input("🎤", label_visibility="collapsed")

user_query = None

if text_input:
    user_query = text_input

elif voice_data:
    # Hash unique audio to prevent infinite loops
    current_audio_id = hash(voice_data.getvalue())
    if st.session_state.last_processed_audio != current_audio_id:
        with st.spinner("🎧 Transcribing your request..."):
            try:
                user_query = speech_to_text(voice_data.getvalue())
                st.session_state.last_processed_audio = current_audio_id
            except Exception:
                st.error("Speech not recognized. Try speaking closer to the mic.")

# --------------------------------------------------
# GENERATION
# --------------------------------------------------
if user_query:
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)
    
    # 2. Assistant Message
    with st.chat_message("assistant"):
        with st.spinner("Checking records..."):
            answer = generate_hotel_response(user_query)
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
    
    st.rerun()