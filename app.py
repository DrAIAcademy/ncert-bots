import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="NCERT AI Tutor", page_icon="🎓")
st.title("🎓 Your Friendly NCERT Screen Tutor")

# 1. Aapki API key yahan set kar di gayi hai
api_key = "AQ.Ab8RN6J4jRIkD5HeH1mn7m-yAeYBBobxeRa57io2aG8EBAmRSQ"

if api_key:
    genai.configure(api_key=api_key)
    
    # 2. Strict UTF-8 Encoding to read Hindi and English properly
    ncert_knowledge = ""
    if os.path.exists("ncert_data.txt"):
        try:
            with open("ncert_data.txt", "r", encoding="utf-8") as f:
                ncert_knowledge = f.read().strip()
        except Exception as e:
            st.error(f"File padhne mein dikkat aai: {e}")

    # Debugging check
    if not ncert_knowledge:
        st.warning("⚠️ Aapki 'ncert_data.txt' file khali hai ya read nahi ho paa rahi hai!")
    
    # 3. Flexible System Instructions
    system_instruction = f"""
    You are an expert, patient school tutor specialized in the NCERT curriculum. 
    Here is the textbook data for your reference:
    ---
    {ncert_knowledge}
    ---
    
    RULES:
    1. Look at the textbook data provided above. If the student's question is mentioned or related to this data, answer it completely and clearly.
    2. Do NOT be too strict. If the text contains the concept, explain it beautifully in simple words.
    3. If the student asks for a summary, read the entire provided text and generate a clean summary with bullet points.
    4. Only say "I'm sorry, that topic isn't covered in this chapter" if the student asks something completely random (like cricket, movies, or coding) which has 0% connection with the textbook text.
    5. Keep your tone encouraging and warm.
    """

    # 4. Initialize the chat memory with gemini-2.5-flash
    if "messages" not in st.session_state:
        st.session_state.messages = []
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )
        st.session_state.chat = model.start_chat(history=[])

    # Display past chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. Handle new questions
    if user_question := st.chat_input("Ask a question from your NCERT book..."):
        with st.chat_message("user"):
            st.markdown(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})

        with st.chat_message("assistant"):
            try:
                response = st.session_state.chat.send_message(user_question)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")