import streamlit as st
import google.generativeai as genai

# 1. Nastavitev strani
st.set_page_config(page_title="NinaGym Klepetalnik", layout="centered")

# 2. Povezava na Gemini ključ (iz tvojih Secrets)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Nastavitev modela - tukaj smo dodali tvojo fitnes specializacijo
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
    Ti si NinaGym pomočnik, strokovnjak za fitnes in zdravo prehrano. 
    Odgovarjaj izključno v slovenščini. Bodi motivacijski in prijazen. 
    Če te kdo vpraša kaj, kar ni povezano s športom ali prehrano, 
    vljudno odgovori, da si specializiran le za NinaGym področje.
    """
)

st.title("🤖 NinaGym Pomočnik")

# 4. Spomin klepeta
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Prikaz zgodovine
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. Vnos uporabnika
if prompt := st.chat_input("Kako vam lahko pomagam pri treningu?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Odgovor modela
    response = st.session_state.chat_session.send_message(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
