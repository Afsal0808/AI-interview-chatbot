import streamlit as st
import speech_recognition as sr
import matplotlib.pyplot as plt
import PyPDF2
import docx
import json
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # loads .env file
client = Groq()  # reads GROQ_API_KEY from .env

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="AI Interview Pro", layout="wide", page_icon="🎙️")

# ─────────────────────────────────────────────
# STYLING
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background: #07090f;
    color: #e8eaf0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d1117;
    border-right: 1px solid #1e2535;
}

/* Gradient title */
.main-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
}

.subtitle {
    text-align: center;
    color: #4b5563;
    font-size: 0.9rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 2rem;
    font-family: 'JetBrains Mono', monospace;
}

/* Question card */
.question-card {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border: 1px solid #334155;
    border-left: 4px solid #38bdf8;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 20px;
    font-size: 1.1rem;
    font-weight: 500;
}

.q-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #38bdf8;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

/* Score box */
.score-box {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 14px;
    text-align: center;
    margin: 8px 0;
}

.score-label {
    font-size: 0.72rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-family: 'JetBrains Mono', monospace;
}

.score-value {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Feedback card */
.feedback-card {
    background: #0f1f0f;
    border: 1px solid #166534;
    border-radius: 10px;
    padding: 16px;
    margin: 10px 0;
    color: #bbf7d0;
}

.suggestion-card {
    background: #0f172a;
    border: 1px solid #1d4ed8;
    border-radius: 10px;
    padding: 16px;
    margin: 10px 0;
    color: #bfdbfe;
}

.motivation-card {
    background: #1e0f2e;
    border: 1px solid #7e22ce;
    border-radius: 10px;
    padding: 16px;
    margin: 10px 0;
    color: #e9d5ff;
}

/* Skill tags */
.skill-tag {
    display: inline-block;
    background: #1e293b;
    border: 1px solid #38bdf8;
    color: #38bdf8;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    margin: 3px;
    font-family: 'JetBrains Mono', monospace;
}

/* Final report */
.report-card {
    background: linear-gradient(135deg, #0f172a, #1a1040);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    margin: 20px 0;
}

/* Progress */
.progress-bar-bg {
    background: #1e293b;
    border-radius: 4px;
    height: 6px;
    margin: 6px 0 16px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
    color: #07090f !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: 0.5px !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Answer transcript */
.transcript-box {
    background: #0d1117;
    border: 1px dashed #334155;
    border-radius: 8px;
    padding: 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #94a3b8;
    margin: 10px 0;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown('<div class="main-title"> Crab AI Interview Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by CRAB AI · Real-time Evaluation</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ANTHROPIC CLIENT
# ─────────────────────────────────────────────
cclient = Groq(api_key="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")  # reads GROQ_API_KEY from env

# ─────────────────────────────────────────────
# RESUME PARSING
# ─────────────────────────────────────────────
def extract_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

SKILLS_DB = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "machine learning", "deep learning", "nlp", "computer vision",
    "sql", "mysql", "postgresql", "mongodb", "redis",
    "html", "css", "react", "vue", "angular", "node.js", "fastapi", "django", "flask",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
    "ai", "data science", "data analysis", "pandas", "numpy", "tensorflow", "pytorch",
    "git", "linux", "bash", "api", "rest", "graphql",
    "communication", "leadership", "teamwork", "problem solving"
]

def extract_skills(text):
    return [s for s in SKILLS_DB if s in text.lower()]

# ─────────────────────────────────────────────
# CLAUDE: GENERATE QUESTIONS
# ─────────────────────────────────────────────
def generate_questions_claude(skills: list[str], resume_text: str = "") -> list[str]:
    skills_str = ", ".join(skills) if skills else "general software engineering"
    prompt = f"""You are an expert technical HR interviewer.

Resume Skills: {skills_str}
Resume Summary (first 600 chars): {resume_text[:600]}

Generate exactly 5 interview questions tailored to this candidate.
Mix: 1 intro, 2 technical (based on skills), 1 behavioral, 1 situational.
Return ONLY a JSON array of 5 strings, no explanation, no markdown.
Example: ["Q1", "Q2", "Q3", "Q4", "Q5"]"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content.strip()
    # strip markdown fences if any
    raw = re.sub(r"```[a-z]*", "", raw).strip().strip("`")
    try:
        qs = json.loads(raw)
        if isinstance(qs, list) and len(qs) >= 1:
            return qs[:5]
    except Exception:
        pass
    # fallback
    return [
        "Tell me about yourself.",
        "What are your core technical skills?",
        "Describe a challenging project you completed.",
        "How do you handle tight deadlines?",
        "Where do you see yourself in 5 years?"
    ]

# ─────────────────────────────────────────────
# CLAUDE: EVALUATE ANSWER
# ─────────────────────────────────────────────
def evaluate_with_claude(skills: list[str], question: str, answer: str) -> dict:
    skills_str = ", ".join(skills) if skills else "general"
    prompt = f"""You are an advanced AI Interviewer evaluating a candidate's answer.

Resume Skills: {skills_str}
Question: {question}
Candidate Answer: {answer}

Score the answer on these dimensions (each 0–10):
- communication_score: clarity, fluency, structure
- content_score: technical accuracy, relevance to skills and question
- confidence_score: assertiveness, avoidance of filler words, decisiveness

Also provide:
- feedback: 1-2 sentences on what was done well
- suggestion: 1-2 sentences on specific improvement (mention STAR method, measurable results, etc.)
- motivation: 1 encouraging sentence like a real interviewer would say

Return ONLY a JSON object with keys: communication_score, content_score, confidence_score, total_score, feedback, suggestion, motivation
total_score = communication_score + content_score + confidence_score
No markdown, no explanation."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```[a-z]*", "", raw).strip().strip("`")
    try:
        result = json.loads(raw)
        # Ensure total_score is computed
        result.setdefault("total_score",
            result.get("communication_score", 0) +
            result.get("content_score", 0) +
            result.get("confidence_score", 0)
        )
        return result
    except Exception:
        return {
            "communication_score": 5,
            "content_score": 5,
            "confidence_score": 5,
            "total_score": 15,
            "feedback": "Answer received and evaluated.",
            "suggestion": "Try to use the STAR method for structured answers.",
            "motivation": "Keep going — every answer is a chance to shine!"
        }

# ─────────────────────────────────────────────
# AUDIO CAPTURE
# ─────────────────────────────────────────────
def get_audio() -> str | None:
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 1.0
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening… speak now (up to 15 seconds)")
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
        return r.recognize_google(audio)
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception:
        return None

# ─────────────────────────────────────────────
# AUDIO FROM UPLOADED WAV
# ─────────────────────────────────────────────
def transcribe_wav(wav_file) -> str | None:
    r = sr.Recognizer()
    try:
        with sr.AudioFile(wav_file) as source:
            audio = r.record(source)
        return r.recognize_google(audio)
    except Exception:
        return None

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.markdown("## 📄 Resume Upload")
resume_file = st.sidebar.file_uploader("PDF or DOCX", type=["pdf", "docx"])

resume_text = ""
skills = []

if resume_file:
    resume_text = extract_text(resume_file)
    skills = extract_skills(resume_text)
    st.sidebar.success("✅ Resume parsed")
    if skills:
        tags_html = "".join(f'<span class="skill-tag">{s}</span>' for s in skills)
        st.sidebar.markdown(tags_html, unsafe_allow_html=True)
    else:
        st.sidebar.warning("No known skills found — using generic questions.")
else:
    st.sidebar.info("Upload your resume to get personalized questions.")

st.sidebar.markdown("---")
st.sidebar.markdown("## 🎙️ Answer Method")
answer_method = st.sidebar.radio(
    "How will you answer?",
    ["🎤 Live Microphone", "📁 Upload WAV File", "⌨️ Type Answer"],
    index=0
)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
defaults = {
    "q_index": 0,
    "total_score": 0,
    "history": [],          # list of per-question result dicts
    "answered": False,
    "result": None,
    "questions": [],
    "questions_ready": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
# GENERATE QUESTIONS (once per session / resume change)
# ─────────────────────────────────────────────
if not st.session_state.questions_ready:
    if resume_file or st.button("🚀 Start Interview (no resume)"):
        with st.spinner("🧠 BOT  is crafting your personalized questions…"):
            st.session_state.questions = generate_questions_claude(skills, resume_text)
            st.session_state.questions_ready = True
        st.rerun()

if not st.session_state.questions_ready:
    st.markdown("""
    <div style='text-align:center; color:#4b5563; margin-top:4rem;'>
        <div style='font-size:3rem;'>🎙️</div>
        <div style='font-size:1.1rem; margin-top:1rem;'>Upload your resume or click Start to begin.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

questions = st.session_state.questions
q_index = st.session_state.q_index

# ─────────────────────────────────────────────
# MAIN LAYOUT
# ─────────────────────────────────────────────
col_main, col_sidebar = st.columns([3, 1])

with col_sidebar:
    # Live Score Card
    st.markdown(f"""
    <div class="score-box">
        <div class="score-label">Total Score</div>
        <div class="score-value">{st.session_state.total_score}</div>
        <div class="score-label">/ {len(questions) * 30}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="score-box">
        <div class="score-label">Question</div>
        <div class="score-value">{min(q_index + 1, len(questions))}/{len(questions)}</div>
    </div>
    """, unsafe_allow_html=True)

    # Performance chart
    if st.session_state.history:
        fig, ax = plt.subplots(figsize=(3, 2.2))
        fig.patch.set_facecolor("#0d1117")
        ax.set_facecolor("#0d1117")
        scores = [h["total_score"] for h in st.session_state.history]
        ax.plot(range(1, len(scores)+1), scores, color="#38bdf8", marker="o",
                linewidth=2, markersize=6)
        ax.fill_between(range(1, len(scores)+1), scores, alpha=0.15, color="#38bdf8")
        ax.set_xlim(0.5, max(len(questions), len(scores)) + 0.5)
        ax.set_ylim(0, 32)
        ax.set_xticks(range(1, len(questions)+1))
        ax.tick_params(colors="#4b5563", labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor("#1e293b")
        ax.set_title("Performance", color="#64748b", fontsize=9)
        st.pyplot(fig)
        plt.close(fig)

with col_main:
    if q_index < len(questions):
        question = questions[q_index]

        # Question card
        st.markdown(f"""
        <div class="question-card">
            <div class="q-label">Question {q_index + 1} of {len(questions)}</div>
            {question}
        </div>
        """, unsafe_allow_html=True)

        # ── ANSWER INPUT ──────────────────────────────
        answer_text = None

        if not st.session_state.answered:
            if answer_method == "🎤 Live Microphone":
                if st.button("🎤 Record Answer"):
                    answer_text = get_audio()
                    if not answer_text:
                        st.warning("⚠️ Could not capture audio. Check your microphone.")

            elif answer_method == "📁 Upload WAV File":
                wav_upload = st.file_uploader("Upload WAV answer", type=["wav"], key=f"wav_{q_index}")
                if wav_upload and st.button("📤 Transcribe & Evaluate"):
                    with st.spinner("Transcribing audio…"):
                        answer_text = transcribe_wav(wav_upload)
                    if not answer_text:
                        st.warning("⚠️ Could not transcribe the audio file.")

            elif answer_method == "⌨️ Type Answer":
                typed = st.text_area("Your answer:", height=120, key=f"text_{q_index}",
                                     placeholder="Type your answer here…")
                if st.button("✅ Submit Answer") and typed.strip():
                    answer_text = typed.strip()

            # ── EVALUATE ─────────────────────────────
            if answer_text:
                st.markdown(f'<div class="transcript-box">📝 {answer_text}</div>', unsafe_allow_html=True)

                with st.spinner("🧠 BOT is evaluating your answer…"):
                    result = evaluate_with_claude(skills, question, answer_text)

                result["question"] = question
                result["answer"] = answer_text
                st.session_state.result = result
                st.session_state.total_score += result["total_score"]
                st.session_state.history.append(result)
                st.session_state.answered = True
                st.rerun()

        # ── SHOW RESULT ───────────────────────────────
        if st.session_state.answered and st.session_state.result:
            r = st.session_state.result

            st.markdown(f'<div class="transcript-box">📝 {r["answer"]}</div>', unsafe_allow_html=True)

            # Score columns
            c1, c2, c3, c4 = st.columns(4)
            for col, label, key, color in [
                (c1, "Communication", "communication_score", "#38bdf8"),
                (c2, "Content", "content_score", "#818cf8"),
                (c3, "Confidence", "confidence_score", "#f472b6"),
                (c4, "Total", "total_score", "#34d399"),
            ]:
                with col:
                    st.markdown(f"""
                    <div class="score-box">
                        <div class="score-label">{label}</div>
                        <div class="score-value" style="background:linear-gradient(90deg,{color},{color}aa);-webkit-background-clip:text;">
                            {r.get(key, 0)}{'/ 10' if key != 'total_score' else '/30'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Feedback / Suggestion / Motivation
            st.markdown(f'<div class="feedback-card">✅ <b>Feedback:</b> {r.get("feedback","")}</div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div class="suggestion-card">💡 <b>Suggestion:</b> {r.get("suggestion","")}</div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div class="motivation-card">🚀 <b>Motivation:</b> {r.get("motivation","")}</div>',
                        unsafe_allow_html=True)

            st.markdown("")
            if st.button("➡️ Next Question"):
                st.session_state.q_index += 1
                st.session_state.answered = False
                st.session_state.result = None
                st.rerun()

    # ── FINAL REPORT ──────────────────────────────────────
    else:
        total = st.session_state.total_score
        max_score = len(questions) * 30
        pct = int((total / max_score) * 100) if max_score else 0

        if pct >= 80:
            verdict = "🚀 Hire Ready"
            verdict_color = "#34d399"
            verdict_msg = "Outstanding performance! You're well prepared for this role."
        elif pct >= 55:
            verdict = "👍 Strong Candidate"
            verdict_color = "#818cf8"
            verdict_msg = "Solid showing. A few more specific examples and you'll stand out."
        elif pct >= 35:
            verdict = "⚠️ Needs Improvement"
            verdict_color = "#f59e0b"
            verdict_msg = "Good effort — focus on the STAR method and technical depth."
        else:
            verdict = "🔄 Keep Practicing"
            verdict_color = "#f472b6"
            verdict_msg = "Don't give up. Practice answering out loud daily and you'll improve fast."

        st.markdown(f"""
        <div class="report-card">
            <div style="font-size:2.5rem; font-weight:700; color:{verdict_color};">{verdict}</div>
            <div style="font-size:3rem; font-weight:700; margin: 10px 0;">{total} <span style="font-size:1.2rem;color:#4b5563;">/ {max_score}</span></div>
            <div style="font-size:1.8rem; color:{verdict_color};">{pct}%</div>
            <div style="color:#94a3b8; margin-top:12px;">{verdict_msg}</div>
        </div>
        """, unsafe_allow_html=True)

        # Per-question breakdown
        st.markdown("### 📋 Question Breakdown")
        for i, h in enumerate(st.session_state.history):
            with st.expander(f"Q{i+1}: {h['question'][:70]}…"):
                st.markdown(f'<div class="transcript-box">{h["answer"]}</div>', unsafe_allow_html=True)
                cols = st.columns(3)
                for col, k, label in zip(cols,
                    ["communication_score", "content_score", "confidence_score"],
                    ["Communication", "Content", "Confidence"]):
                    col.metric(label, f"{h.get(k, 0)}/10")
                st.markdown(f'<div class="feedback-card">✅ {h.get("feedback","")}</div>',
                            unsafe_allow_html=True)
                st.markdown(f'<div class="suggestion-card">💡 {h.get("suggestion","")}</div>',
                            unsafe_allow_html=True)

        st.markdown("")
        if st.button("🔄 Restart Interview"):
            for k, v in defaults.items():
                st.session_state[k] = v
            st.rerun()
