import streamlit as st
import google.generativeai as genai
import requests
import json

# --- 1. PAGE CONFIGURATION ---
# This sets the colors and titles for the browser tab
st.set_page_config(page_title="BattleBorn Assistant", page_icon="🛠️")
st.title("BattleBorn Infrastructures Support")
st.caption("Ask us about network design, installs, or request a free consultation!")

# --- 2. THE WIX WEBHOOK TOOL ---
def submit_service_request(name: str, email: str, phone: str, service_type: str, site_type: str, location: str, issue_description: str, urgency: str) -> str:
    """Submits a structured service request directly to the Wix backend."""
    wix_webhook_url = "https://www.yourdomain.com/_functions/your_wix_webhook" # REPLACE THIS LATER
    
    payload = {
        "customer_name": name, "contact_email": email, "phone_number": phone,
        "service_requested": service_type, "site_type": site_type,
        "location_zip": location, "issue_summary": issue_description,
        "urgency_level": urgency, "source": "BattleBorn_AI_Agent"
    }
    
    try:
        response = requests.post(wix_webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        if response.status_code in [200, 201]:
            return f"Success! The request for {name} has been securely logged."
        return f"Request sent, but server responded with status: {response.status_code}."
    except Exception as e:
        return f"Error communicating with the server: {str(e)}"

# --- 3. INITIALIZE GEMINI ---
# Streamlit handles API keys securely using a secrets file
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

system_instruction = """
You are the friendly, humble, and enthusiastic AI assistant for BattleBorn Infrastructures. 
You specialize in discussing our network design, professional installations, and repair services. 
Consultations are free. If a customer needs a service, you MUST collect their Name, Email, Phone, 
Service Type, Site Type (Residential/Commercial), Zip Code, and Urgency. 
Once you have all details, use the submit_service_request tool to log it, then warmly confirm with the user.
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools=[submit_service_request],
    system_instruction=system_instruction
)

# --- 4. STREAMLIT CHAT MEMORY ---
# This ensures the chatbot remembers the conversation history
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(enable_automatic_function_calling=True)
    st.session_state.messages = []

# Display previous messages on screen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. THE CHAT INTERFACE ---
# This creates the text input box at the bottom of the screen
if user_input := st.chat_input("How can we upgrade your network today?"):
    
    # Show the user's message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Send to Gemini and get the response
    with st.spinner("Thinking..."):
        response = st.session_state.chat_session.send_message(user_input)
        
    # Show the AI's response
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
