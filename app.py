import streamlit as st
import google.generativeai as genai

# Konfiguracija strani
st.set_page_config(page_title="GymGator Klepetalnik", layout="centered")

# Povezava na ključ
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Manjka API ključ v Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Inicializacija modela - uporabili bomo samo ime, brez 'models/'
# Knjižnica bo sama ugotovila pravo pot, če je verzija >= 0.8.0
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("🤖 GymGator Pomočnik")

# Spomin seje
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(
        history=[],
    )
    # Tukaj dodamo specializacijo neposredno v prvi ukaz, da bo 100% delalo
    st.session_state.gym_rules = "Ti si GymGator pomočnik. Odgovarjaj v slovenščini o fitnesu. Če vprašanje ni o športu, zavrni."

# Prikaz zgodovine
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Vnos uporabnika
if prompt := st.chat_input("Kako vam lahko pomagam?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Pošljemo vprašanje skupaj s pravili, da model ne pozabi vloge
        full_prompt = f"{st.session_state.gym_rules}\n\nUporabnik sprašuje: {prompt}"
        response = st.session_state.chat_session.send_message(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Napaka pri generiranju odgovora. Poskusite osvežiti stran. Podrobnosti: {e}")
