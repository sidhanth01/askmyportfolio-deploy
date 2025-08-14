import streamlit as st
import os
from dotenv import load_dotenv
import io  # For BytesIO
import base64
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from groq import Groq

# SQLite version fix for ChromaDB on Streamlit Cloud (important to do before LangChain/Chroma imports)
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except Exception:
    pass

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate

import requests  # For Together AI API calls
import re
# Function to reduce heading levels in markdown
def reduce_heading_levels(md: str, max_level=2) -> str:
    """
    Downgrade all markdown headings (#) and HTML headings (<h1>-<h6>)
    to at most the given max_level.
    """
    # Fix markdown-style headings
    def md_replacer(match):
        level = min(len(match.group(1)), max_level)
        return "#" * level + " "
    text = re.sub(r"^(#{1,6})\s+", md_replacer, md, flags=re.MULTILINE)

    # Fix HTML headings
    def html_replacer(match):
        return f"<h{max_level}>{match.group(2)}</h{max_level}>"
    text = re.sub(r"<h([1-6])>(.*?)</h\1>", html_replacer, text, flags=re.IGNORECASE | re.DOTALL)

    return text


# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Portfolio Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
/* Paste your complete Gemini dark theme CSS here */
</style>
""", unsafe_allow_html=True)

# --- Heading and Tagline ---
st.markdown('''
<h1 style="text-align:center; font-size:2.8em; font-weight:800; color:#FFFFFF; margin-bottom:0.1em;">
    Ask-My-Portfolio
</h1>
<div style="text-align:center; font-size:1.2em; font-weight:400; color:#90a0e6; margin-bottom:1.8em;">
    Discover my capabilities and project impact instantly with AI-powered interaction.
</div>
''', unsafe_allow_html=True)

# --- Load Environment Variables ---
load_dotenv()

DATA_PATH = "data/"
CHROMA_DB_PATH = "chroma_db/"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Ensure data dir exists
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

# Check Chroma DB exists
if not os.path.exists(CHROMA_DB_PATH) or not os.listdir(CHROMA_DB_PATH):
    st.error("Error: The ChromaDB knowledge base was not found. Please ingest your data locally and push 'chroma_db' directory.")
    st.stop()

@st.cache_resource
def get_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    return Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)

vectorstore = get_vector_store()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Load API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("Groq API key (GROQ_API_KEY) not found. Please add it to Streamlit secrets.")
    st.stop()

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

def call_groq_llm(prompt: str) -> str:
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=768,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling Groq LLM: {e}"

# --- Prompt Template ---
PROMPT = """
You are an AI assistant designed to answer questions about a user's professional portfolio and projects.
Use ONLY the provided context to answer. If you cannot find the answer in the context, clearly state: "Sorry, I could not find that information in the current portfolio documentation."
Format structured answers using markdown (bullets, headings, tables) when helpful.
When referencing a project or section, start your answer with its name for clarity.
Never invent beyond the context provided, but you can improvise the answer based on the context.
Keep every answer concise, precise, professional, and focused on the question asked.
When asked to elaborate, explain the relevant point in your own words using only what is present in the context. Do not supplement with outside information.
Never include any source document IDs or references in the final answer.
When outputting headings, use at most '##' markdown. Do not use <h1> HTML tags.

Context:
{context}

Question: {question}

Answer:"""
prompt_template = ChatPromptTemplate.from_template(PROMPT)

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "awaiting_response" not in st.session_state:
    st.session_state.awaiting_response = False
if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""

# --- Display chat messages ---
chat_display_area = st.container()
with chat_display_area:
    for msg in st.session_state.messages:
        avatar = "🧑‍💼" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            content = msg["content"]
            if msg["role"] == "assistant":  # Only fix headings for assistant
                content = reduce_heading_levels(content, max_level=2)
                st.markdown(content, unsafe_allow_html=True)
            else:
                st.write(content)

# --- User input ---
user_question = st.chat_input("Ask me about my projects, skills, or career journey...", key="chat_input_main_box")

# Handle typed input
if user_question:
    # Add question immediately
    st.session_state.messages.append({"role": "user", "content": user_question})
    # Set pending question and awaiting response flag
    st.session_state.pending_question = user_question
    st.session_state.awaiting_response = True
    st.rerun()

# -- If waiting response, generate it now --
if st.session_state.awaiting_response and st.session_state.pending_question:
    with st.spinner("Thinking..."):
        try:
            docs = retriever.get_relevant_documents(st.session_state.pending_question)
            context_text = "\n\n".join([doc.page_content for doc in docs])
            final_prompt = PROMPT.format(context=context_text, question=st.session_state.pending_question)
            response = call_groq_llm(final_prompt)
        except Exception as e:
            response = f"Sorry, there was an error processing your request: {e}"

    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.pending_question = ""
    st.session_state.awaiting_response = False
    st.rerun()

# --- Download chat transcripts ---
if st.session_state.messages:

    def transcript_content():
        return "\n".join([f"{'USER:' if m['role']=='user' else 'AI:'} {m['content']}" for m in st.session_state.messages])

    def safe_text(text):
        replacements = {'—': '-', '–': '-', '’': "'", '“': '"', '”': '"', '…': '...'}
        for k,v in replacements.items():
            text = text.replace(k, v)
        return text.encode("ascii", "ignore").decode("ascii")

    def transcript_to_pdf():
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", size=11)

        for msg in st.session_state.messages:
            role_label = "USER:" if msg["role"] == "user" else "AI:"
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, safe_text(role_label), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 8, safe_text(msg["content"]))
            pdf.ln(2)

        pdf_output = io.BytesIO()
        pdf_bytes = pdf.output(dest='S')
        pdf_output.write(pdf_bytes)
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

# --- Sidebar with example questions and resume embed ---
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
            if not st.session_state.awaiting_response:
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.pending_question = q
                st.session_state.awaiting_response = True
                st.rerun()

    st.markdown("---")
    st.markdown("""
        <div style="font-size:1.03em;color:#94b0be;line-height:1.43;">
            <b>AIML engineering graduate.</b><br>
            <span style="font-size:0.978em;">Ask about my projects, skills, or career journey—select from above or start typing!</span>
        </div>
    """, unsafe_allow_html=True)

    try:
        # File path to your local resume
        # ⚠️ Make sure this matches your file name exactly
        resume_file_path = "Sidhanth_Resume.pdf"
        
        # Check if the resume file exists
        if os.path.exists(resume_file_path):
            with open(resume_file_path, "rb") as f:
                pdf_bytes = f.read()
            
            st.markdown("---") # Add a separator for better UI

            st.download_button(
                label="⬇️ View or Download Resume",
                data=pdf_bytes,
                file_name="my_resume.pdf",
                mime="application/pdf",
                key="download_resume_button",
                use_container_width=True
            )
        else:
            st.warning(f"Resume file '{resume_file_path}' not found. Please add it to the project directory.")
            
    except Exception as e:
        st.error(f"Error loading resume: {e}")

    st.markdown("""
        <div style="margin-top:45px; color:#8998a7; font-size:0.9em; text-align:center;">
            <p style="margin-bottom: 5px;">© 2025 <b>Sidhanth L</b></p>
            <p style="margin-bottom: 5px;">Built with
                <span style='color:#68d6e3;'>LangChain</span>,
                <span style='color:#3cbfbe;'>ChromaDB</span>,
                <span style='color:#c5ba6a;'>Streamlit</span>,
                <span style='color:#b836bf;'>Custom LLM via Groq</span>
            </p>
            <p style="margin-bottom: 5px;">Powered by RAG · Deployed on Streamlit Community Cloud</p>
            <p>
                <a href="https://github.com/sidhanth01" style="color:#8baaff;text-decoration:none;">GitHub</a>
            </p>
        </div>
    """, unsafe_allow_html=True)