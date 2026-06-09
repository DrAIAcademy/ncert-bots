import streamlit as st
from google import genai
from google.genai import types
import os

st.set_page_config(page_title="NCERT AI Tutor", page_icon="🎓")
st.title("🎓 Your Friendly NCERT Screen Tutor")

# 1. Check Streamlit Secrets for API Key
api_key = "AQ.Ab8RN6KItY6rPYMitr0-RfyIRSXZbPgh_Qrgy4wav64TBvlwxg"
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    # New SDK Client Initialize karne ka tarika
    client = genai.Client(api_key=api_key)
    
    # 2. Read Textbook Data
    ncert_knowledge = ""
    if os.path.exists("ncert_data.txt"):
        try:
            with open("ncert_data.txt", "r", encoding="utf-8") as f:
                ncert_knowledge = f.read().strip()
        except Exception as e:
            st.error(f"File padhne mein dikkat aai: {e}")

    if not ncert_knowledge:
        st.warning("⚠️ 'ncert_data.txt' file khali hai ya read nahi ho paa rahi hai!")
    
    # 3. System Instructions
    system_instruction = f"""
    You are an expert, patient school tutor specialized in the NCERT curriculum. 
    Here is the textbook data for reference:
    ---
    {ncert_knowledge}
    ---
    RULES:
    1. Base explanations directly on the provided textbook text.
    2. If the student asks for a summary, generate a beautiful summary using bullet points.
    3. Keep your tone warm and clear.
    """

    # 4. Initialize Chat History in Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. Handle Questions using the new SDK syntax
    if user_question := st.chat_input("Ask a question from your NCERT book..."):
        with st.chat_message("user"):
            st.markdown(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})

        with st.chat_message("assistant"):
            try:
                # Naye SDK ke mutabik chat session ya direct generate content
                # Hum pure history ko context bana kar bhej rahe hain taaki memory bani rahe
                history_context = ""
                for msg in st.session_state.messages[:-1]:
                    history_context += f"{msg['role']}: {msg['content']}\n"
                
                full_prompt = f"{history_context}user: {user_question}"

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction
                    )
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Please enter your Gemini API Key in the sidebar or set it in Streamlit Secrets!")
