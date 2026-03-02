import os
import streamlit as st
from google import genai  # THE NEW SDK
from google.genai import types

# Page configuration
st.set_page_config(page_title="BattleBorn Infrastructures", page_icon="⚡", layout="wide")

# --- TOOLS ---
def submit_service_request(name: str, email: str, phone: str, service_type: str, site_type: str, location: str, issue_description: str, urgency: str) -> str:
    """Logs a service request for BBI infrastructure projects."""
    # Logic remains the same as before...
    return "Mission Logged."

def initialize_agent():
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None

    try:
        # NEW: Initializing the GenAI Client
        client = genai.Client(api_key=api_key)
        
        # MISSION PARAMETERS
        system_instruction = (
            "You are the BattleBorn Infrastructures (BBI) AI Assistant. "
            "BBI is a VETERAN-OWNED and VETERAN-LED infrastructure firm. "
            "Tone: Mission-oriented and professional."
        )

        return client, system_instruction
    except Exception as e:
        st.error(f"⚠️ System Error: {e}")
        return None, None

# --- EXECUTION ---
client, sys_instr = initialize_agent()

if client is None:
    st.error("🚨 Critical Failure: AI Engine offline. Check API key in Secrets.")
    st.stop()

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI HEADER ---
logo_url = "https://static.wixstatic.com/media/81481d_94bfdbe4f7e14881ae95ce01c458fe7d~mv2.png"
col1, col2 = st.columns([1, 8])
with col1:
    st.image(logo_url, width=80)
with col2:
    st.title("BattleBorn Infrastructures")
    st.caption("Veteran-Owned | Infrastructure Intelligence & Operations")

# Render History
for msg in st.session_state.messages:
    current_avatar = logo_url if msg["role"] == "assistant" else "user"
    with st.chat_message(msg["role"], avatar=current_avatar):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("How can BattleBorn help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=logo_url):
        with st.spinner("Analyzing Mission Parameters..."):
            try:
                # NEW: Generating response with the upgraded SDK
                response = client.models.generate_content(
                    model="gemini-2.0-flash", # Upgraded to 2.0
                    contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=sys_instr)
                )
                
                text = response.text
                st.markdown(text)
                st.session_state.messages.append({"role": "assistant", "content": text})
            except Exception as e:
                st.error(f"❌ Mission Interrupted: {e}")