import streamlit as st
from google import genai
from google.genai import types
import os

st.set_page_config(page_title="NCERT AI Tutor", page_icon="🎓")

# Custom CSS for Embed Look (Menus aur footers ko chhupane ke liye)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Your Friendly NCERT Screen Tutor")

# 1. Aapki AQ wali API Key seedhe yahan lock hai
api_key = "AQ.Ab8RN6J4jRIkD5HeH1mn7m-yAeYBBobxeRa57io2aG8EBAmRSQ"

try:
    # Naye SDK mein direct api_key parameter pass karne ka sahi tarika
    client = genai.Client(api_key=api_key)
    
    # 2. Read Textbook Data
    ncert_knowledge = ""
    if os.path.exists("ncert_data.txt"):
        try:
            with open("ncert_data.txt", "r", encoding="utf-8") as f:
                ncert_knowledge = f.read().strip()
        except Exception as e:
            st.error(f"File read karne mein dikkat: {e}")

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
    3. Keep your tone warm, encouraging, and clear.
    """

    # 4. Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Past chat history display
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. Handle Questions (Using 3.5-flash)
    if user_question := st.chat_input("Ask a question from your NCERT book..."):
        with st.chat_message("user"):
            st.markdown(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})

        with st.chat_message("assistant"):
            try:
                # History context taiyar karna
                history_context = ""
                for msg in st.session_state.messages[:-1]:
                    history_context += f"{msg['role']}: {msg['content']}\n"
                
                full_prompt = f"{history_context}user: {user_question}"

                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction
                    )
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")

except Exception as init_error:
    st.error(f"Client setup mein dikkat aai: {init_error}")
