import os
import json
import requests
import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="BattleBorn Infrastructures", page_icon="⚡", layout="wide")

# --- TOOLS ---
def submit_service_request(name: str, email: str, phone: str, service_type: str, site_type: str, location: str, issue_description: str, urgency: str) -> str:
    """Logs a service request for BBI infrastructure projects."""
    wix_webhook_url = "https://www.battleborninfrastructures.com/_functions/your_wix_webhook"
    payload = {
        "customer_name": name,
        "contact_email": email,
        "phone_number": phone,
        "service_requested": service_type,
        "site_type": site_type,
        "location_zip": location,
        "issue_summary": issue_description,
        "urgency_level": urgency,
        "source": "BattleBorn_AI_Agent",
    }
    try:
        resp = requests.post(wix_webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        if resp.status_code in (200, 201):
            return f"Success! The request for {name} has been securely logged."
        return f"Request sent, server responded with status: {resp.status_code}."
    except Exception as e:
        return f"Error communicating with the server: {e}"

def initialize_agent():
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("❌ API Key missing. Check Streamlit Secrets.")
        return None  # Explicitly return None so we can catch it

    genai.configure(api_key=api_key)

    system_instruction = (
        "You are the BattleBorn Infrastructures (BBI) AI Assistant. "
        "BBI is a VETERAN-OWNED and VETERAN-LED infrastructure firm. "
        "Tone: Mission-oriented and professional."
    )

    models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    
    for m_name in models_to_try:
        try:
            # MISSION: Attempt to build the model
            return genai.GenerativeModel(
                model_name=m_name, 
                system_instruction=system_instruction,
                tools=[submit_service_request]
            )
        except Exception as e:
            print(f"Skipping {m_name}: {e}") # Log the failure internally
            continue
    
            return None # Return None if all scouts fail

# --- Initialization Logic ---
    model = initialize_agent()

# --- Initialization Guard ---
if model is None:
    st.error("🚨 Critical Failure: Could not initialize any AI models. Please check your GOOGLE_API_KEY permissions.")
    st.stop() # Prevents the 'NoneType' error by stopping the script here

if "chat_session" not in st.session_state:
    # Now this is safe because we checked if model is None above
    st.session_state.chat_session = model.start_chat(enable_automatic_function_calling=True)
    st.session_state.messages = []

# --- UI HEADER ---
logo_url = "https://static.wixstatic.com/media/81481d_94bfdbe4f7e14881ae95ce01c458fe7d~mv2.png"
col1, col2 = st.columns([1, 8])
with col1:
    st.image(logo_url, width=80)
with col2:
    st.title("BattleBorn Infrastructures")
    st.caption("Veteran-Owned | Infrastructure Intelligence & Operations")

# --- CHAT INTERFACE ---
for msg in st.session_state.messages:
    current_avatar = logo_url if msg["role"] == "assistant" else "user"
    with st.chat_message(msg["role"], avatar=current_avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("How can BattleBorn help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=logo_url):
        with st.spinner("Analyzing Mission Parameters..."):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                text = response.text if hasattr(response, "text") else "Mission Briefing: Connection error."
                if text:
                    st.markdown(text)
                    st.session_state.messages.append({"role": "assistant", "content": text})
            except Exception as e:
                st.error(f"❌ System Error: {e}")