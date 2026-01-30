import streamlit as st
import google.generativeai as genai

# 1. Nastavitev strani
st.set_page_config(page_title="GymGator Klepetalnik", layout="centered")

# 2. Povezava na Gemini ključ (iz tvojih Secrets)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Nastavitev modela s specializacijo za GymGator
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
    Ti si GymGator pomočnik, strokovnjak za fitnes in zdravo prehrano. 
    Odgovarjaj izključno v slovenščini. Bodi motivacijski in prijazen. 
    Če te kdo vpraša kaj, kar ni povezano s športom ali prehrano, 
    vljudno odgovori, da si specializiran le za GymGator področje.
    """
)

st.title("🤖 GymGator Pomočnik")

# 4. Spomin klepeta (Session State)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Prikaz zgodovine sporočil
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. Vnos uporabnika in generiranje odgovora
if prompt := st.chat_input("Kako vam lahko pomagam pri treningu?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Pošiljanje vprašanja modelu in prejem odgovora
    response = st.session_state.chat_session.send_message(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
