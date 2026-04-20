# app.py

import streamlit as st
import speech_recognition as sr 

# -------------------------------
# 🎯 QUESTIONS LIST
# -------------------------------
questions = [
    "Tell me about yourself",
    "What are your strengths?",
    "Why should we hire you?",
    "Describe a challenge you faced",
    "Where do you see yourself in 5 years?"
]

# -------------------------------
# 🎤 SPEECH TO TEXT FUNCTION
# -------------------------------
import streamlit as st
import speech_recognition as sr

st.title("AI Interview Chatbot 🎤")

audio_file = st.file_uploader("Upload your audio (.wav)")

if audio_file is not None:
    recognizer = sr.Recognizer()
    
    with open("temp.wav", "wb") as f:
        f.write(audio_file.read())

    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)

    st.success(text)
# -------------------------------
# 🧠 NLP EVALUATION FUNCTION
# -------------------------------
def evaluate_answer(answer):
    score = 0

    # Length check
    if len(answer.split()) > 5:
        score += 2

    # Keywords check
    keywords = ["team", "hardworking", "problem", "experience", "skills"]

    for word in keywords:
        if word in answer.lower():
            score += 1

    # Final result
    if score >= 4:
        return "✅ Excellent Answer", score
    elif score >= 2:
        return "👍 Good Answer", score
    else:
        return "⚠️ Needs Improvement", score

# -------------------------------
# 🚀 STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="AI Interview Bot", layout="centered")

st.title("🎤 AI Interview Bot")
st.write("Practice your interview with AI")

# Session state
if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

# -------------------------------
# 🎯 MAIN LOGIC
# -------------------------------
if st.session_state.q_index < len(questions):

    question = questions[st.session_state.q_index]

    st.subheader(f"Question {st.session_state.q_index + 1}")
    st.write(question)

    if st.button("🎙️ Answer by Voice"):
        answer = get_audio()

        st.write("🗣️ Your Answer:")
        st.success(answer)

        feedback, score = evaluate_answer(answer)
        st.write("💡 Feedback:")
        st.info(feedback)

        st.session_state.score += score
        st.session_state.q_index += 1

else:
    st.success("🎉 Interview Completed!")

    total = st.session_state.score
    st.write(f"🏆 Your Score: {total} / 25")

    if total > 18:
        st.balloons()
        st.success("Excellent Performance 🚀")
    elif total > 10:
        st.info("Good Job 👍")
    else:
        st.warning("Needs Improvement ⚠️")

    if st.button("🔄 Restart"):
        st.session_state.q_index = 0
        st.session_state.score = 0
