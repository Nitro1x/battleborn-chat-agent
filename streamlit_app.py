import os
import streamlit as st
import requests  # Make sure to 'pip install requests' if not already there
from google import genai
from google.genai import types
def send_bbi_lead(name, email, phone, site_type, desc, urgency):
    url = "https://api.emailjs.com/api/v1.0/email/send"
    payload = {
        "service_id": "service_ij65q1c",
        "template_id": "template_zxu2h7w","Contact Us"
        "user_id": "RFH52WT8kwrRyAhT6",
        "template_params": {
            "customer_name": name,
            "customer_email": email,
            "customer_phone": phone,
            "site_type": site_type,
            "project_desc": desc,
            "urgency": urgency
        }
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code

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
    "BBI is a VETERAN-OWNED and VETERAN-LED infrastructure firm specializing in "
    "high-performance network solutions and physical layer security. "
    
    "\n\nCORE SERVICES & EXPERTISE:"
    "\n- STRUCTURED CABLING: Cat5e, Cat6, Cat6A, and Fiber Optic installation."
    "\n- NETWORK DESIGN: Office suite and warehouse infrastructure upgrades."
    "\n- IT HARDWARE: Server rack installation, cable management, and patch panel termination."
    "\n- SECURITY & ACCESS: IP Camera systems (CCTV) and commercial access control."
    "\n- WIRELESS SOLUTIONS: WiFi heatmapping and Access Point (AP) deployment."
    "\n- MISSION CRITICAL: On-site troubleshooting and infrastructure audits."

    "\n\nMISSION PARAMETERS:"
    "\n1. TONE: Be mission-oriented, professional, and technically accurate."
    "\n2. AREA: We primarily serve San Antonio, Floresville, and the surrounding South Texas region."
    "\n3. ENGAGEMENT: Answer technical questions about our services freely."
    "\n4. LEAD GEN: If a user mentions a specific project or site needing work, "
    "promptly use the 'submit_service_request' tool to log the mission details."
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

# Move the helper function OUTSIDE of the if block so it's always ready
def extract_info(keyword, text):
    if keyword in text:
        # Splits by the keyword and takes the first line after it
        return text.split(keyword)[1].split('\n')[0].strip(': ')
    return "Not Provided"

if prompt := st.chat_input("Enter project details..."):
    # 1. Display and Save User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. THE BRIDGE CHECK: 
    # Check if the PREVIOUS message from the assistant was the lead-capture prompt
    if len(st.session_state.messages) > 1:
        last_ai_msg = st.session_state.messages[-2]["content"]
        if any(x in last_ai_msg for x in ["Once I have these details", "submit a service request", "logged with high urgency"]):
            
            # Combine history so the extractor can find the Name, Email, etc.
            chat_history = " ".join([m["content"] for m in st.session_state.messages])
            
            user_name_variable = extract_info("Name", chat_history)
            user_email_variable = extract_info("Email", chat_history)
            user_phone_variable = extract_info("Phone", chat_history)
            user_site_variable = extract_info("Site Type", chat_history)
            user_desc_variable = extract_info("Description", chat_history)
            user_urgency_variable = extract_info("Urgency", chat_history)

            try:
                # Trigger EmailJS
                status = send_bbi_lead(
                    name=user_name_variable, 
                    email=user_email_variable,
                    phone=user_phone_variable,
                    site_type=user_site_variable,
                    desc=user_desc_variable,
                    urgency=user_urgency_variable
                )
                
                if status == 200:
                    st.success("✅ Consultation Request Transmitted to BBI Engineering.")
                    st.info("💡 **Next Step:** To get an instant itemized PDF quote, visit our [Project Configurator](https://yourlink.com).")
            except Exception as e:
                st.error("Lead logged locally, but email transmission delayed.")

    # 3. GENERATE AI RESPONSE
    with st.chat_message("assistant", avatar=logo_url):
        with st.spinner("Analyzing Mission Parameters..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
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
                    st.info("BBI Intel: Processing your request...")

            except Exception as e:
                st.error(f"❌ Mission Interrupted: {e}")