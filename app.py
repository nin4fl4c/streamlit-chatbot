import streamlit as st
import google.generativeai as genai

# 1. Konfiguracija strani
st.set_page_config(page_title="GymGator Klepetalnik", layout="centered")

# 2. Varna nastavitev API ključa
if "GEMINI_API_KEY" not in st.secrets:
    st.error("API ključ ni nastavljen v Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Pametna izbira modela
# Poskusimo najprej najnovejšo pot, če ne gre, uporabimo stabilno rezervo
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    model = genai.GenerativeModel("gemini-pro")

st.title("🤖 GymGator Pomočnik")

# 4. Inicializacija seje klepeta
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.gym_rules = (
        "Ti si GymGator pomočnik, strokovnjak za fitnes in zdravo prehrano. "
        "Govori izključno v slovenščini. Če vprašanje ni povezano s športom, "
        "prijazno zavrni odgovor."
    )

# Prikaz zgodovine sporočil
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. Vnos uporabnika in odgovor
if prompt := st.chat_input("Vprašaj GymGatorja..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Pošljemo vprašanje skupaj z navodili za vlogo
        response = st.session_state.chat_session.send_message(
            f"{st.session_state.gym_rules}\n\nUporabnik: {prompt}"
        )
        
        with st.chat_message("assistant"):
            # Očistimo odgovor morebitnih sistemskih navodil
            answer = response.text.replace(st.session_state.gym_rules, "").strip()
            st.markdown(answer)
            
    except Exception as e:
        st.error("Nekaj je šlo narobe. Poskusite klikniti 'Reboot App' v nastavitvah Streamlita.")
        st.info(f"Podrobnost: {e}")
