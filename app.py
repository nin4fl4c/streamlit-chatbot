import streamlit as st
import google.generativeai as genai

# Konfiguracija strani
st.set_page_config(page_title="GymGator Klepetalnik", layout="centered")

# Preverjanje ključa
if "GEMINI_API_KEY" not in st.secrets:
    st.error("API ključ ni nastavljen v Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Inicializacija modela (brez models/ predpone, nove knjižnice to naredijo same)
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("🤖 GymGator Pomočnik")

# Inicializacija seje in navodil
if "chat_session" not in st.session_state:
    # Navodila vključimo neposredno v zgodovino seje, da model ve, kdo je
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.gym_instructions = (
        "Ti si GymGator pomočnik, strokovnjak za fitnes in prehrano. "
        "Govori slovensko. Če te vprašajo kaj drugega, vljudno zavrni."
    )

# Prikaz zgodovine
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Vnos uporabnika
if prompt := st.chat_input("Vprašaj GymGatorja..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Pošljemo vprašanje skupaj s skritim kontekstom za specializacijo
        response = st.session_state.chat_session.send_message(
            f"{st.session_state.gym_instructions}\n\nUporabnik: {prompt}"
        )
        
        with st.chat_message("assistant"):
            # Odstranimo morebitne ponovitve navodil v odgovoru, če se pojavijo
            clean_response = response.text.replace(st.session_state.gym_instructions, "").strip()
            st.markdown(clean_response)
            
    except Exception as e:
        st.error(f"Tehnična napaka: {e}")
        st.info("Nasvet: Preverite, če ste posodobili requirements.txt na GitHubu!")
