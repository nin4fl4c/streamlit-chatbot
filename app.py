import streamlit as st
import google.generativeai as genai

# Nastavitev strani
st.set_page_config(page_title="Pametni Klepetalnik", layout="centered")

# Povezava na tvoj Gemini ključ iz Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Nastavitev modela in specializacije
# TUKAJ spremeni navodila glede na tvojo temo!
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Ti si prijazen slovenski pomočnik. Odgovarjaj samo v slovenščini. Če te vprašajo kaj izven tvoje teme, vljudno zavrni."
)

st.title("🤖 Moj Chatbot")

# Upravljanje s spominom (Session State)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Prikaz preteklih sporočil
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Vnos uporabnika in odgovor
if prompt := st.chat_input("Vprašaj me kaj..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Pošiljanje vprašanja in prejemanje odgovora
    response = st.session_state.chat.send_message(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
