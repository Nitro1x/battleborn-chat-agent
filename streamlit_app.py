import os
import streamlit as st
import requests
import json
import google
from google.genai import types
# Page configuration
st.set_page_config(page_title="BattleBorn Infrastructures", page_icon="⚡", layout="wide")

# --- 1. TOOL DEFINITION ---
def submit_service_request(name: str, email: str, phone: str, service_type: str, site_type: str, location: str, issue_description: str, urgency: str) -> str:
    """Logs a service request for BBI infrastructure projects."""
    # Your Wix Webhook logic here...
    return f"Mission Logged for {name}."

# --- 2. ENGINE INITIALIZATION ---
def initialize_agent():
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    
    try:
        # Initializing the modern GenAI Client
        client = google.genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"⚠️ Connection Error: {e}")
        return None

client = initialize_agent()

# --- 3. SAFETY GUARD ---
if client is None:
    st.error("🚨 Critical Failure: AI Engine offline. Verify GOOGLE_API_KEY in Secrets.")
    st.stop()

# System Instruction
BBI_INSTRUCTION = (
    "You are the BattleBorn Infrastructures (BBI) AI Assistant. "
    "BBI is a VETERAN-OWNED and VETERAN-LED infrastructure firm. "
    "Tone: Mission-oriented, technical, and professional."
)

# --- 4. UI & CHAT ---
logo_url = "https://static.wixstatic.com/media/81481d_94bfdbe4f7e14881ae95ce01c458fe7d~mv2.png"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
col1, col2 = st.columns([1, 8])
with col1:
    st.image(logo_url, width=80)
with col2:
    st.title("BattleBorn Infrastructures")
    st.caption("Veteran-Owned | Infrastructure Intelligence & Operations")

# Chat Logic
for msg in st.session_state.messages:
    avatar = logo_url if msg["role"] == "assistant" else "user"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("How can BattleBorn help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=logo_url):
        with st.spinner("Analyzing Mission Parameters..."):
            try:
                # Using Gemini 2.0 Flash for maximum speed/accuracy
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=BBI_INSTRUCTION,
                        tools=[submit_service_request] # Tools are handled here now
                    )
                )
                text = response.text
                st.markdown(text)
                st.session_state.messages.append({"role": "assistant", "content": text})
            except Exception as e:
                st.error(f"❌ Mission Interrupted: {e}")