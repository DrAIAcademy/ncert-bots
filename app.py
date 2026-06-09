import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="NCERT AI Tutor", page_icon="🎓")

# Menus ko chhupane ke liye
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)
st.title("🎓 Your Friendly NCERT Screen Tutor")

# Direct key configuration
genai.configure(api_key="AQ.Ab8RN6J4jRIkD5HeH1mn7m-yAeYBBobxeRa57io2aG8EBAmRSQ")

# Textbook read karna
ncert_knowledge = ""
try:
    with open("ncert_data.txt", "r", encoding="utf-8") as f:
        ncert_knowledge = f.read().strip()
except:
    pass

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_question := st.chat_input("Ask a question..."):
    with st.chat_message("user"):
        st.markdown(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("assistant"):
        try:
            # Purana sabse stable model jo AQ keys ko bina nakhre ke chalata hai
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=f"You are an NCERT tutor. Base answers on: {ncert_knowledge}"
            )
            response = model.generate_content(user_question)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
