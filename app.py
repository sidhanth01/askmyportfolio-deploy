import streamlit as st
import os
from dotenv import load_dotenv
import base64
import io  # for BytesIO
from fpdf import FPDF

# SQLite version fix for ChromaDB on Streamlit Cloud with Python 3.11
# MUST be before importing langchain_chroma or chromadb
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except Exception:
    # Fallback to default sqlite3, might cause sqlite version error
    pass

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate

import requests  # For Together AI API calls


# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Portfolio Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (Paste your full CSS here) ---
st.markdown("""
<style>
/* Your full Gemini dark theme CSS goes here */
</style>
""", unsafe_allow_html=True)

# --- HEADING AND TAGLINE ---
st.markdown('''
<h1 style="text-align:center; font-size:2.8em; font-weight:800; color:#FFFFFF; margin-bottom:0.1em;">
    Ask-My-Portfolio
</h1>
<div style="text-align:center; font-size:1.2em; font-weight:400; color:#90a0e6; margin-bottom:1.8em;">
    Discover my capabilities and project impact instantly with AI-powered interaction.
</div>
''', unsafe_allow_html=True)

# --- ENV & DB SETUP ---
load_dotenv()
DATA_PATH = "data/"
CHROMA_DB_PATH = "chroma_db/"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

if not os.path.exists(CHROMA_DB_PATH) or not os.listdir(CHROMA_DB_PATH):
    st.error(
        "Error: The ChromaDB knowledge base was not found. "
        "Please pre-ingest your data locally and push the 'chroma_db' directory to your repository."
    )
    st.stop()

@st.cache_resource
def get_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    return db

vectorstore = get_vector_store()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY") or st.secrets.get("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    st.error("Together AI API key (TOGETHER_API_KEY) not found. Please add it to Streamlit secrets.")
    st.stop()

# Choose a Together AI serverless chat model (free-tier):
TOGETHER_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

def call_together_llm(prompt: str) -> str:
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": TOGETHER_MODEL,
        "messages": [
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 256,
        "temperature": 0.0
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        if response.status_code != 200:
            try:
                err_json = response.json()
                return f"Together AI error {response.status_code}: {err_json.get('error', err_json)}"
            except Exception:
                return f"Together AI error {response.status_code}: {response.text}"
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, no response from Together AI.")
    except Exception as e:
        return f"Error calling Together AI LLM: {e}"

# --- RAG prompt template ---
PROMPT = """
You are an AI assistant designed to answer questions about a user's professional portfolio and projects.
Use ONLY the provided context to answer. If you cannot find the answer in the context, clearly state: "Sorry, I could not find that information in the current portfolio documentation."
Format structured answers using markdown (bullets, headings, tables) when helpful.
When referencing a project or section, start your answer with its name for clarity.
Never invent beyond the context provided, but you can improvise the answer based on the context.
Keep every answer concise, precise, professional, and focused on the question asked.
When asked to elaborate, explain the relevant point in your own words using only what is present in the context. Do not supplement with outside information.
Never include any source document IDs or references in the final answer.

Context:
{context}

Question: {question}

Answer:"""

prompt_template = ChatPromptTemplate.from_template(PROMPT)

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "voice_query" not in st.session_state:
    st.session_state.voice_query = ""

# --- Display chat messages ---
chat_display_area = st.container()
with chat_display_area:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🧑‍💼"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(msg["content"])

user_question = st.chat_input("Ask me about my projects, skills, or career journey...", key="chat_input_main_box")



# --- Unified chat input processing (typed or sidebar) ---
if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""
if "awaiting_response" not in st.session_state:
    st.session_state.awaiting_response = False


# If user types a question
if user_question and user_question.strip():
    if not st.session_state.pending_question and not st.session_state.awaiting_response:
        st.session_state.messages.append({"role": "user", "content": user_question.strip()})
        st.session_state.pending_question = user_question.strip()
        st.session_state.voice_query = ""
        st.session_state.awaiting_response = True
        st.experimental_rerun()

# If a sidebar question is pending
if st.session_state.pending_question and not st.session_state.awaiting_response:
    st.session_state.messages.append({"role": "user", "content": st.session_state.pending_question})
    st.session_state.voice_query = ""
    st.session_state.awaiting_response = True
    st.experimental_rerun()

# If awaiting response, process the answer
if st.session_state.awaiting_response and st.session_state.pending_question:
    user_input = st.session_state.pending_question
    with st.spinner("Thinking..."):
        try:
            docs = retriever.get_relevant_documents(user_input)
            context_text = "\n\n".join([doc.page_content for doc in docs])
            final_prompt = PROMPT.format(context=context_text, question=user_input)
            response = call_together_llm(final_prompt)
        except Exception as e:
            response = f"Sorry, there was an error processing your request: {e}. Please try again."

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.pending_question = ""
    st.session_state.awaiting_response = False


# --- Download chat transcripts ---
if st.session_state.messages:

    def transcript_content():
        return "\n".join([f"{'USER:' if m['role']=='user' else 'AI:'} {m['content']}" for m in st.session_state.messages])

    def safe_text(text):
        replacements = {'—': '-', '–': '-', '’': "'", '“': '"', '”': '"', '…': '...'}
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text.encode("ascii", "ignore").decode("ascii")

    def transcript_to_pdf():
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=11)

        for msg in st.session_state.messages:
            role_label = "USER:" if msg["role"] == "user" else "AI:"
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 8, safe_text(role_label), ln=1)
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 8, safe_text(msg["content"]))
            pdf.ln(2)

        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        return pdf_output

    st.markdown("---")
    download_cols = st.columns([0.4, 0.1, 0.1, 0.4])

    with download_cols[1]:
        st.download_button(
            "⭳ Text",
            data=transcript_content(),
            file_name="chat_transcript.txt",
            mime="text/plain",
            key="download_txt_chat",
            use_container_width=True,
        )
    with download_cols[2]:
        pdf_buffer = transcript_to_pdf()
        st.download_button(
            "⭳ PDF",
            data=pdf_buffer,
            file_name="chat_transcript.pdf",
            mime="application/pdf",
            key="download_pdf_chat",
            use_container_width=True,
        )

# --- Sidebar with example prompts and resume ---
with st.sidebar:
    st.markdown('<div style="font-weight:600; font-size:1.21em;margin-top:-0.7em;">💬 Interview Prompts</div>', unsafe_allow_html=True)
    example_questions = [
        "Can you summarize your main technical skills and core strengths?",
        "Walk me through your resume profile and most notable achievements.",
        "What is Retrieval-Augmented Generation (RAG) and how does Ask-My-Portfolio use it?",
        "Which of your projects best showcases AI and LLM integration?",
        "Tell me about the end-to-end workflow of Ask-My-Portfolio.",
        "What unique challenges did you overcome with Bill & Receipt Insight Extractor?",
        "How does ChestX-AI-Classifier achieve explainability and high accuracy?",
        "What role did you play in the design and deployment of Auto Service System?",
        "Share quantifiable results from your top projects.",
        "What was your approach to handling edge cases in ChestX-AI-Classifier?",
        "Which project required the most robust validation and why?",
        "Describe your approach to automating document ingestion and retrieval.",
        "Explain the tech stack and LLM choices you made for your portfolio chatbot.",
        "Describe a time you led a team or mentored a peer during a complex project.",
        "How do you ensure code, models, and products are reliable and production-ready?",
        "What did you learn from user or recruiter feedback in any of your applications?",
        "Give an example of how you adapted to change during development.",
        "How did you recover from a major technical setback in a project demo?",
        "Describe a unique or unforeseen edge case you solved in any project.",
        "What motivates you in your professional work?",
        "How do you handle conflicts or disagreements in a team setting?",
        "What are your career goals, and how do your portfolio projects support them?",
        "If assigned to work in a new technology stack, how would you proceed?",
        "What’s your approach to continuous learning in AI and software engineering?",
        "Can you provide a narrative of how a user or recruiter might interact with your systems?",
        "How would you compare your solution for Bill & Receipt Insight Extractor to ChestX-AI-Classifier?",
        "Which project’s results have had the most real-world impact for users or stakeholders?"
    ]
    for q in example_questions:
        if st.button(q, key=q):
            if not st.session_state.pending_question:
                st.session_state.pending_question = q

    st.markdown("---")
    st.markdown("""
        <div style="font-size:1.03em;color:#94b0be;line-height:1.43;">
            <b>AIML engineering graduate.</b><br>
            <span style="font-size:0.978em;">Ask about my projects, skills, or career journey—select from above or start typing!</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h5 style='margin-bottom:0.65em;margin-top:1.65em;'><b>My Resume</b></h5>", unsafe_allow_html=True)

    resume_url = "https://drive.google.com/uc?export=view&id=1lf5SzSEzrMkj93_8ko_rVVQ03mdnUcHu"
    pdf_display = f'<iframe src="{resume_url}" width="100%" height="350px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

    st.markdown(
        f'<a href="{resume_url}" download class="resume-link">⬇️ Download Resume</a>',
        unsafe_allow_html=True
    )

    st.markdown("""
        <div style="margin-top:45px; color:#8998a7; font-size:0.9em; text-align:center;">
            <p style="margin-bottom: 5px;">© 2025 <b>Sidhanth L</b></p>
            <p style="margin-bottom: 5px;">Built with 
                <span style='color:#68d6e3;'>LangChain</span>,
                <span style='color:#3cbfbe;'>ChromaDB</span>, 
                <span style='color:#c5ba6a;'>Streamlit</span>,
                <span style='color:#b836bf;'>Custom LLM via Replicate</span>
            </p>
            <p style="margin-bottom: 5px;">Powered by RAG · Deployed on Streamlit Community Cloud</p>
            <p>
                <a href="https://github.com/sidhanth01" style="color:#8baaff;text-decoration:none;">GitHub</a>
            </p>
        </div>
    """, unsafe_allow_html=True)
