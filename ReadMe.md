# 🏫 Kolachi 😋 – AI Hotel Assistant 🤖

An **AI-powered hotel chatbot** built using **Streamlit**, **Hugging Face LLaMA 3**, and **Speech Recognition**, designed specifically for **Kolachi Hotel**.  
The chatbot provides **accurate hotel-related responses** using a private knowledge base (`HotelData.docx`) and supports **both text and voice interaction**.

---

## 📌 Project Overview

**Kolachi AI Assistant** is a conversational chatbot that:
- Answers guest queries related to hotel services, menu, rules, and policies
- Uses **hotel-specific data** as context
- Supports **voice input (speech-to-text)**
- Maintains **chat memory**
- Streams AI responses in real time

If a question is **outside the provided hotel data**, the assistant politely redirects the user to **contact the manager Raja**.

---

## 🚀 Key Features

### 💬 Conversational AI
- Powered by **Meta LLaMA 3.2 – 3B Instruct**
- Context-aware responses using hotel documentation

### 🎤 Voice Input Support
- Converts user speech into text using **Google Speech Recognition**
- Prevents repeated transcription of the

same audio

### 📄 Private Knowledge Base
- Reads data from **HotelData.docx**
- Cached for performance using `st.cache_resource`

### 🧠 Short-Term Memory
- Remembers last **5 conversation messages**
- Ensures relevant and concise responses

### ⚡ Real-Time Streaming
- Token-by-token streaming using Hugging Face Inference API

### 🧹 Chat Management
- Sidebar button to clear chat history instantly

---

## 🛠️ Tech Stack

| Component | Technology |
|---------|-----------|
| Frontend | Streamlit |
| LLM | Meta LLaMA 3.2 (3B Instruct) |
| API | Hugging Face Inference Client |
| Speech Recognition | Google Speech API (via `speech_recognition`) |
| File Parsing | docx2txt |
| Language | Python |

---

## 📂 Project Structure

```
ChatBot_Hotel/
│
├── app.py                 # Main Streamlit application
├── HotelData.docx         # Hotel knowledge base
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
```

---

## ⚙️ How the Code Works (Deep Analysis)

### 1️⃣ Page Configuration
```python
st.set_page_config(page_title="Kolachi", layout="wide")
st.title("🏫 Kolachi😋 - AI Assistant🤖")
```
Sets branding and layout for the chatbot UI.

---

### 2️⃣ Model Initialization
```python
MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"
hf_client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)
```
- Uses Hugging Face’s hosted **LLaMA 3.2**
- Requires `HF_TOKEN` stored securely in Streamlit secrets

---


---

## 👨‍💼 Managed By
**Kolachi Hotel**  
AI Assistant supervised by **Raja**

---

## 📜 License
This project is for **educational and demonstration purposes**.  
Feel free to enhance and customize.
