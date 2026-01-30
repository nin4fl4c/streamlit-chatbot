import streamlit as st
import google.generativeai as genai

# 1. Nastavitev strani (Metapodatki in postavitev)
st.set_page_config(page_title="GymGator Klepetalnik", layout="centered")

# 2. Povezava na Gemini ključ (Varno pridobljeno iz Streamlit Secrets)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Nastavitev modela s polno potjo, da preprečimo NotFound napako
# Dodali smo "models/" pred ime modela za boljšo združljivost
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction="""
    Ti si GymGator pomočnik, strokovnjak za fitnes in zdravo prehrano. 
    Odgovarjaj izključno v slovenščini. Bodi motivacijski in prijazen. 
    Če te kdo vpraša kaj, kar ni povezano s športom ali prehrano, 
    vljudno odgovori, da si specializiran le za GymGator področje.
    """
)

st.title("🤖 GymGator Pomočnik")

# 4. Upravljanje seje klepeta (Spomin chatbota)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Prikaz zgodovine vseh sporočil v trenutni seji
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. Interakcija z uporabnikom (Vnos in generiranje odgovora)
if prompt := st.chat_input("Kako vam lahko GymGator pomaga danes?"):
    # Takojšen prikaz uporabnikovega vprašanja
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Pošiljanje vprašanja AI modelu
        response = st.session_state.chat_session.send_message(prompt)
        
        # Prikaz odgovora chatbota
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        # Prikaz prijaznejšega obvestila v primeru tehnične napake
        st.error(f"Prišlo je do napake pri povezavi z GymGator strežnikom. Prosimo, poskusite znova. (Napaka: {e})")
