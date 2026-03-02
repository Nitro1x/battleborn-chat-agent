import os
import streamlit as st
import requests
import json
from google import genai
from google.genai import types

# Page configuration
st.set_page_config(page_title="BattleBorn Infrastructures", page_icon="⚡", layout="wide")

# --- 1. TOOLS ---
def submit_service_request(name: str, email: str, phone: str, service_type: str, site_type: str, location: str, issue_description: str, urgency: str) -> str:
    """Logs a service request for BBI projects."""
    return f"Mission Logged for {name}."

# --- 2. INITIALIZATION ---
def initialize_agent():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    try:
        # The modern 2026 client initialization
        return genai.Client(api_key=api_key)
    except Exception:
        return None

client = initialize_agent()

# --- 3. SAFETY GUARD ---
if client is None:
    st.error("🚨 Critical Failure: Verify GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

BBI_INSTRUCTION = (
    "You are the BattleBorn Infrastructures (BBI) AI Assistant. "
    "BBI is a VETERAN-OWNED and VETERAN-LED infrastructure firm. "
    "Tone: Mission-oriented and professional."
)

# --- 4. UI ---
logo_url = "https://static.wixstatic.com/media/81481d_94bfdbe4f7e14881ae95ce01c458fe7d~mv2.png"
if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2 = st.columns([1, 8])
with col1:
    st.image(logo_url, width=80)
with col2:
    st.title("BattleBorn Infrastructures")
    st.caption("Veteran-Owned | Infrastructure Intelligence & Operations")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=logo_url if msg["role"] == "assistant" else "user"):
        st.markdown(msg["content"])

# --- 5. THE CHAT LOGIC ---
if prompt := st.chat_input("How can BattleBorn help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=logo_url):
        with st.spinner("Analyzing Mission Parameters..."):
            try:
                # PRECISION FIX: Remove 'models/' prefix for the 2.0 SDK
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=BBI_INSTRUCTION,
                        tools=[submit_service_request]
                    )
                )
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.info("System: Processing mission data (Tool Call).")

            except Exception as e:
                st.error(f"❌ Mission Interrupted: {e}")