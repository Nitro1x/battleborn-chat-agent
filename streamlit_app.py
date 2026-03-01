import streamlit as st
import google.generativeai as genai
import requests
import json

# 1. Setup Branding
st.set_page_config(page_title="BattleBorn AI Assistant", page_icon="⚡")
st.title("⚡ BattleBorn Infrastructures")
st.subheader("Local IT & Network Support")

# 2. Securely Load API Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("🔑 API Key Missing! Check your .streamlit/secrets.toml file.")
    st.stop()

# 3. Define the Agent Persona & Model
system_instruction = (
    "You are the BattleBorn Infrastructures AI Assistant. "
    "Your persona is happy, humble, and enthusiastic. "
    "You specialize in Network Infrastructure and IT services in Texas."
)

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        system_instruction=system_instruction
    )
except Exception as e:
    st.error(f"⚠️ Model Initialization Failed: {e}")
    st.stop()

# 4. Handle Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. The Chat Logic
if prompt := st.chat_input("How can BattleBorn help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We use a simple generation for the local test
            response = model.generate_content(prompt)
            
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("The AI returned an empty response. Try rephrasing.")
                
        except Exception as e:
            # This will now show the EXACT error message from Google
            st.error(f"❌ BattleBorn System Error: {e}")
            if "API_KEY_INVALID" in str(e):
                st.info("Tip: Your API Key in secrets.toml might be incorrect.")
            elif "429" in str(e):
                st.info("Tip: You're sending messages too fast for the free tier. Wait a moment!")
