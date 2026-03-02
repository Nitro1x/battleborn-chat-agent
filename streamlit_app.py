import streamlit as st
import google.generativeai as genai
<<<<<<< HEAD
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
=======
import os
import requests
import json  # <--- Add this line!

# --- BBI Brand Configuration ---
st.set_page_config(page_title="BBI AI Chat Agent", page_icon="⚡", layout="wide")

def initialize_agent():
    """
    Initializes the Gemini 3 Flash engine with BBI System Instructions.
    """
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            st.error("❌ BBI System Error: API Key missing in Secrets.")
            st.stop()

        genai.configure(api_key=api_key)
        
        # BBI Persona - Veteran-led IT Infrastructure Specialist
        system_instruction = (
            "You are the BattleBorn Infrastructures AI Agent. "
            "You provide expert-level guidance on enterprise networking, "
            "low-voltage infrastructure, and AI automation. "
            "Tone: Direct, technical, and mission-oriented."
        )

        # Using Gemini 3 Flash for 2026 performance standards
        return genai.GenerativeModel(
            model_name="gemini-3-flash",
            system_instruction=system_instruction
        )
    except Exception as e:
        # Fallback to 2.5 if 3 is not yet provisioned for your key
        try:
            return genai.GenerativeModel(model_name="gemini-2.5-flash")
        except:
            st.error(f"Critical System Failure: {str(e)}")
            st.stop()

# --- Mission Logic ---
model = initialize_agent()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- UI Layout ---
st.title("⚡ BattleBorn Infrastructures")
st.caption("v3.0 | Infrastructure Intelligence & Operations")

# Display Chat History
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Chat Input
if prompt := st.chat_input("Input technical query or site data..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing Infrastructure..."):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"⚠️ Link Lost: {str(e)}")

# --- 2. THE WIX WEBHOOK TOOL ---
def submit_service_request(name: str, email: str, phone: str, service_type: str, site_type: str, location: str, issue_description: str, urgency: str) -> str:
    """
    Submits a structured service request directly to the Wix backend.
    
    Args:
        name: The customer's full name.
        email: The customer's email address.
        phone: The customer's phone number.
        service_type: The type of service requested (e.g., Installation, Repair).
        site_type: Residential or Commercial.
        location: The zip code or city.
        issue_description: A brief summary of the network issue.
        urgency: Standard or High.
    """
    
    # REPLACE THIS LATER WITH YOUR ACTUAL WIX URL
    wix_webhook_url = "https://www.battleborninfrastructures.com/_functions/your_wix_webhook" 
    
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
>>>>>>> 05b497a (Fix: Add missing imports for requests and json, and update requirements.txt)
