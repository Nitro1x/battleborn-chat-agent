import os
import json
import requests
import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="BattleBorn Infrastructures", page_icon="⚡", layout="wide")

def submit_service_request(name: str, email: str, phone: str, service_type: str, site_type: str, location: str, issue_description: str, urgency: str) -> str:
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
    api_key = None
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        pass
    api_key = api_key or os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("❌ API Key missing. Set GOOGLE_API_KEY in Streamlit secrets or environment.")
        st.stop()

    genai.configure(api_key=api_key)

    # REINFORCED SYSTEM PROMPT: Veteran-Owned DNA
    system_instruction = (
        "You are the BattleBorn Infrastructures (BBI) AI Assistant. "
        "BBI is a VETERAN-OWNED and VETERAN-LED infrastructure firm specializing in "
        "networking, low-voltage cabling, and IT automation. "
        "Tone: Mission-oriented, technical, and professional. "
        "When asked about the company, always highlight that BBI is Veteran-Owned "
        "and brings military-grade precision and discipline to every project."
    )

    # List available models and pick the first that supports text generation
    try:
        available_models = genai.list_models()
        for model_info in available_models:
            if "generateContent" in getattr(model_info, "supported_generation_methods", []):
                return genai.GenerativeModel(model_name=getattr(model_info, "name", None), system_instruction=system_instruction)
    except Exception as e:
        st.warning(f"Could not list models: {e}. Falling back to configured defaults.")

    # Fallback to known stable model resource names
    models_to_try = [
        "models/gemini-pro-latest",
        "models/gemini-flash-latest",
        "models/gemini-2.5-flash",
    ]
    for model_name in models_to_try:
        try:
            return genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
        except Exception:
            continue

    st.error("❌ No available models. API key may have limited access. Contact support.")
    st.stop()

# Initialize model and chat session
model = initialize_agent()

if "chat_session" not in st.session_state:
    # Adding the service request function as a tool the AI can use
    st.session_state.chat_session = model.start_chat(enable_automatic_function_calling=True)
    st.session_state.messages = []

# UI Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://static.wixstatic.com/media/81481d_94bfdbe4f7e14881ae95ce01c458fe7d~mv2.png", width=100)
st.title("BattleBorn Infrastructures")
st.caption("Veteran-Owned | Infrastructure Intelligence & Operations")
# Render existing messages
for msg in st.session_state.messages:for msg in st.session_state.messages:
    # This sets the logo for the assistant and a user icon for you
    current_avatar = "https://static.wixstatic.com/media/81481d_94bfdbe4f7e14881ae95ce01c458fe7d~mv2.png" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=current_avatar):
        st.markdown(msg["content"])
    

if prompt := st.chat_input("How can BattleBorn help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    wwith st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="https://static.wixstatic.com/media/81481d_94bfdbe4f7e14881ae95ce01c458fe7d~mv2.png"): # Sets logo for the new response
        with st.spinner("Analyzing Mission Parameters..."):
            # ... (the rest of your AI logic)"): # Sets logo for the new response
        

    with st.chat_message("assistant"):
        with st.spinner("Analyzing Mission Parameters..."):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                text = getattr(response, "text", None) or (response.parts[0].text if getattr(response, "parts", None) else "")
                if text:
                    st.markdown(text)
                    st.session_state.messages.append({"role": "assistant", "content": text})
                else:
                    st.warning("⚠️ No response received from the AI. Try rephrasing.")
            except Exception as e:
                st.error(f"❌ System Error: {e}")