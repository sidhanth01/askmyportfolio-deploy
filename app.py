import streamlit as st
import os
from dotenv import load_dotenv
import base64
import io # Import io for BytesIO
from fpdf import FPDF


# LangChain and LLM imports
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain_huggingface.llms import HuggingFaceInferenceAPI



# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Portfolio Explorer",
    layout="wide",
    initial_sidebar_state="expanded"  # Keeps the sidebar open
)


# --- Custom CSS for Gemini-like Dark Theme and Advanced UI ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Montserrat:wght@700&display=swap');

/* Overall App Background and Text */
.stApp {
    background-color: #121212 !important; /* Deeper black/dark grey */
    color: #e0e0e0 !important; /* Light grey for general text */
    font-family: 'Inter', sans-serif; /* Modern, clean font */
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #1c1c1c !important; /* Slightly lighter dark grey for sidebar */
    color: #e0e0e0 !important;
    min-width: 330px;
    border-right: 1px solid #333333; /* Darker border for separation */
    box-shadow: 4px 0px 24px rgba(0, 0, 0, 0.2); /* More pronounced shadow */
    transition: margin-left 0.3s ease-in-out; /* Smooth transition for expand/collapse */
}
            
/* Sidebar expand/collapse button (hamburger menu) */
/* This targets the actual button container for the hamburger menu */
button[data-testid="stSidebarNav] {
    position: fixed; /* Keep it fixed */
    top: 10px; /* Adjust top padding */
    left: 10px; /* Adjust left padding */
    z-index: 1001; /* Ensure it's above other elements */
    background-color: transparent !important; /* Make button background transparent */
    border: none !important; /* Remove border */
    box-shadow: none !important; /* Remove shadow */
}

/* Sidebar expand/collapse button (hamburger menu) */
/* This targets the actual button container for the hamburger menu */
button[data-testid="stSidebarNav"] {
    display: none !important; /* Add this line to hide the button */
}

/* This targets the SVG icon inside the hamburger menu button */
/* You can now remove this entire block since the button is hidden */
button[data-testid="stSidebarNav"] svg {
    color: #4CAF50;
    font-size: 1.8em;
    transition: color 0.2s;
}
button[data-testid="stSidebarNav"]:hover svg {
    color: #66BB6A;
}

/* Sidebar Buttons */
.sidebar-items .stButton>button {
    border-radius: 9px;
    margin-bottom: 8px;
    padding: 0.5em 1em; /* Increased padding */
    color: #e3eded;
    background: #2a2a2a; /* Darker background for buttons */
    border: none;
    font-size: 1.05em; /* Slightly larger font */
    width: 100%; /* Make sidebar buttons full width */
    text-align: left;
    transition: background 0.2s, color 0.2s, transform 0.1s; /* Smooth transitions */
    box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Subtle button shadow */
}
.stButton>button:hover {
    background: #3a3a3a !important; /* Lighter on hover */
    color: #62edc9 !important; /* Accent color on hover */
    transform: translateY(-1px); /* Slight lift effect */
    box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* More pronounced shadow on hover */
}

/* Adjust top padding for main content area */
.st-emotion-cache-18ni7ap { /* This class targets the main content block */
    padding-top: 0.1rem;
}
.st-emotion-cache-6qob1r { /* This class targets the sidebar content wrapper */
    min-width: 330px;
}

/* Main Heading and Tagline */
.center-title {
    text-align: center;
    font-family: 'Montserrat', sans-serif; /* Distinct font for heading */
    font-size: 3.2em; /* Larger heading */
    font-weight: 700;
    letter-spacing: 3px; /* More spacing */
    color: #62edc9; /* Accent color for main title */
    text-shadow: 0 0 10px rgba(98, 237, 201, 0.3); /* Subtle glow */
    margin: 0.7em 0 0.1em 0;
}
.tagline {
    text-align: center;
    color: #b0b0b0; /* Softer grey for tagline */
    font-size: 1.1em; /* Slightly larger tagline */
    margin-bottom: 2.5em; /* More space below tagline */
}

/* Chat Message Containers (st.chat_message) */
[data-testid="stChatMessage"] {
    padding: 15px 20px; /* More padding */
    margin-bottom: 12px; /* More space between messages */
    border-radius: 22px; /* More rounded corners */
    font-size: 1.05em;
    line-height: 1.6;
    max-width: 770px; /* Limit width of chat bubbles */
    box-shadow: 0 2px 8px rgba(0,0,0,0.1); /* Subtle shadow for bubbles */
    display: flex; /* Enable flexbox for internal alignment (avatar/content) */
    align-items: flex-start; /* Align items to the top (for avatars) */
}

/* User Message Bubble (Left aligned) */
[data-testid="stChatMessage"][data-st-chat-message-type="user"] {
    background: #2a2a2a; /* Darker grey for user, consistent with AI's previous background */
    color: #f8f9ff; /* Very light text */
    margin-left: 15px; /* Spacing from left edge */
    margin-right: auto; /* Align user messages to the left */
    text-align: left; /* Keep text left-aligned within the bubble */
}

/* Assistant Message Bubble (Right aligned) */
[data-testid="stChatMessage"][data-st-chat-message-type="assistant"] {
    background: #33334d; /* Dark blue-purple for AI, consistent with user's previous background */
    color: #e8ecff; /* Light text */
    margin-right: 15px; /* Spacing from right edge */
    margin-left: auto; /* Align assistant messages to the right */
    text-align: left; /* Keep text left-aligned within the bubble */
}

/* Avatar Styling within chat messages */
/* Adjust avatar position for user messages to be on the left */
[data-testid="stChatMessage"][data-st-chat-message-type="user"] .st-emotion-cache-1c7gnj6 { /* User avatar container */
    order: 0; /* Keep avatar on the left */
    margin-right: 12px; /* Space after avatar */
    margin-left: 0;
    align-self: flex-start; /* Align avatar to top of message */
}
/* Adjust avatar position for assistant messages to be on the right */
[data-testid="stChatMessage"][data-st-chat-message-type="assistant"] .st-emotion-cache-1c7gnj6 { /* Assistant avatar container */
    order: 1; /* Move avatar to the right */
    margin-left: 12px; /* Space after avatar */
    margin-right: 0;
    align-self: flex-start; /* Align avatar to top of message */
}

/* Ensure message content takes full width within its bubble */
[data-testid="stChatMessage"] .st-emotion-cache-1ae02w6 { /* Message content wrapper */
    flex-grow: 1;
}

/* Streamlit chat_input (Gemini-like) */
[data-testid="stChatInput"] {
    background: #121212; /* Match app background */
    padding: 15px 0; /* More padding around the input */
    position: fixed; /* Keep input at the bottom */
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 1000; /* Ensure it stays on top */
    border-top: 1px solid #333333; /* Darker separator line */
    box-shadow: 0 -5px 15px rgba(0,0,0,0.3); /* Shadow to lift it from content */
}

/* This targets the actual input box within st.chat_input */
[data-testid="stChatInput"] > div > div {
    background: #2a2a2a !important; /* Input box background */
    border-radius: 30px !important; /* Even more rounded */
    border: 1px solid #444444 !important; /* Darker, subtle border */
    color: #e0e0e0 !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25); /* More pronounced shadow */
    min-height: 60px; /* Taller input box */
    padding: 15px 25px; /* More padding inside the input */
    margin: 0 auto; /* Center the input box */
    max-width: 800px; /* Slightly wider input box */
    width: calc(100% - 40px); /* Adjust width considering margins */
    display: flex; /* Use flexbox for internal alignment */
    align-items: center; /* Vertically align content */
}
[data-testid="stChatInput"] textarea {
    color: #e0e0e0 !important; /* Text color inside input */
    background: transparent !important; /* Ensure transparent background for text area */
    resize: none !important; /* Disable manual resize */
    padding: 0; /* Remove default textarea padding */
    flex-grow: 1; /* Allow textarea to take available space */
    height: auto !important; /* Allow height to adjust to content */
    min-height: 24px; /* Minimum height for one line */
    line-height: 1.5; /* Consistent line height */
}
[data-testid="stChatInput"] ::placeholder { /* Placeholder text color */
    color: #888888 !important;
    opacity: 1;
}

/* Specific styling for the submit button inside chat_input */
[data-testid="stChatInput"] button {
    background-color: #4CAF50 !important; /* Green send button */
    color: white !important;
    border-radius: 50% !important; /* Circular button */
    width: 48px !important; /* Larger button */
    height: 48px !important; /* Larger button */
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative; /* Position relative to the flex container */
    flex-shrink: 0; /* Prevent shrinking */
    margin-left: 15px; /* Space from text area */
    box-shadow: 0 2px 8px rgba(0,0,0,0.3); /* Button shadow */
    transition: background-color 0.2s, transform 0.1s, box-shadow 0.2s;
}
[data-testid="stChatInput"] button:hover {
    background-color: #66BB6A !important; /* Lighter green on hover */
    transform: translateY(-1px); /* Slight lift effect */
    box-shadow: 0 4px 12px rgba(0,0,0,0.4); /* More pronounced shadow on hover */
}
/* Ensure the send icon is visible and centered */
[data-testid="stChatInput"] button svg {
    font-size: 1.2em; /* Adjust icon size */
}

/* File uploader */
.stFileUploader>label {
    color: #e9e9f5 !important;
}
.resume-link {
    background: #234c53;
    border-radius: 7px;
    color: #e7faef;
    padding: 0.32em 0.82em;
    font-size: 1em;
    text-decoration: none; /* Remove underline */
    display: inline-block; /* Allow padding */
    margin-top: 10px;
    transition: background 0.2s, color 0.2s;
}
.resume-link:hover {
    background: #2c5a62;
    color: #ffffff;
}

/* Scrollbar styling */
::-webkit-scrollbar-thumb {
    background: #444444 !important; /* Darker thumb */
    border-radius: 14px;
}
::-webkit-scrollbar {
    background: #222222 !important; /* Darker track */
    width: 9px;
}

/* Adjust Streamlit's default margins for main content to make space for fixed input */
.st-emotion-cache-1ghvgyx { /* Main content block padding */
    padding-bottom: 100px; /* Add space at the bottom for the fixed input */
}

/* Hide the default microphone input if using custom button */
[data-testid="stMicrophoneInput"] {
    display: none;
}

/* Adjust for the Streamlit's default padding around the main block container */
.st-emotion-cache-z5fcl4 {
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Download buttons at the bottom of the chat */
.stDownloadButton>button {
    background-color: #3a3a3a !important; /* Darker grey, consistent with sidebar buttons */
    color: #62edc9 !important; /* Accent color */
    border: 1px solid #555555 !important;
    border-radius: 8px !important;
    padding: 0.4em 0.8em !important; /* Minimized padding */
    font-size: 0.9em !important; /* Smaller font size */
    transition: background-color 0.2s, color 0.2s, border-color 0.2s;
    display: inline-flex; /* Allows icon and text to align */
    align-items: center;
    gap: 5px; /* Space between icon and text */
    margin-right: 10px; /* Space between buttons */
}
.stDownloadButton>button:hover {
    background-color: #4a4a4a !important;
    color: #ffffff !important;
    border-color: #62edc9 !important;
}
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


# Ensure data directory exists
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

# Check for existing Chroma DB or ingest data
if not os.path.exists(CHROMA_DB_PATH) or not os.listdir(CHROMA_DB_PATH):
    with st.spinner("Setting up knowledge base... This might take a moment."):
        try:
            # Dynamically import ingest_data to avoid circular dependencies if it's in a separate file
            from ingest_data import load_documents, split_documents, create_embeddings_and_store
            docs = load_documents()
            if docs:
                chunks = split_documents(docs)
                create_embeddings_and_store(chunks)
                st.success("Knowledge base ready! You can now ask questions.")
            else:
                st.error("No documents found in 'data/'. Please upload your resume/portfolio files and restart the application.")
                st.stop() # Stop execution if no documents are found
        except ImportError:
            st.error("Error: 'ingest_data.py' not found. Please ensure it's in the same directory as 'app.py'.")
            st.stop()
        except Exception as e:
            st.error(f"Error during knowledge base setup: {e}. Please check your documents and environment.")
            st.stop()

@st.cache_resource
def get_vector_store():
    """Caches and returns the Chroma vector store with HuggingFace embeddings."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    return db

@st.cache_resource
def get_llm():
    """Caches and returns the Language Model (Ollama or HuggingFaceHub fallback)."""
    ollama_model = os.getenv("OLLAMA_MODEL")
    ollama_url = os.getenv("OLLAMA_BASE_URL")
    if ollama_model and ollama_url:
        try:
            # Attempt to connect to Ollama and make a small test call
            test_llm = Ollama(model=ollama_model, base_url=ollama_url, temperature=0.0, num_predict=384)
            test_llm.invoke("Hello") # Quick test to check connectivity
            st.success(f"Successfully connected to Ollama model: {ollama_model}")
            return test_llm
        except Exception as e:
            st.warning(f"Ollama unavailable ({e}). Using HuggingFaceHub fallback. "
                       "Ensure Ollama server is running and model '{ollama_model}' is pulled.")
    
    st.info("Using cloud-based LLM (HuggingFaceHub). Performance may vary.")
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        st.error("HuggingFace API Token (HF_TOKEN) not found in your .env file. "
                 "Please set it up for cloud LLM fallback, or ensure Ollama is configured.")
        st.stop() # Stop if no LLM can be initialized
    return HuggingFaceInferenceAPI(
        repo_id="google/flan-t5-base", # Consider a more capable model if needed
        model_kwargs={"temperature": 0.0, "max_length": 256},
        huggingfacehub_api_token=hf_token
    )

# Initialize vector store and LLM
vectorstore = get_vector_store()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 relevant documents
llm = get_llm()


# Define the RAG prompt template
PROMPT = """
You are an AI assistant designed to answer questions about a user's professional portfolio and projects.
Use ONLY the provided context to answer. If you cannot find the answer in the context, clearly state: "Sorry, I could not find that information in the current portfolio documentation."
Format structured answers using markdown (bullets, headings, tables) when helpful.
When referencing a project or section, start your answer with its name for clarity.
Never invent beyond the context provided, But you can improvise the answer based on the context.
Keep every answer concise, precise, professional and focused on the question asked.
When asked to elaborate, explain the relevant point in your own words using only what is present in the context. Do not supplement with outside information.
Never include any source document IDs or references in the final answer.

Context:
{context}

Question: {question}

Answer:"""
prompt = ChatPromptTemplate.from_template(PROMPT)

# Create the RAG chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)

# Initialize chat messages and voice query in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "voice_query" not in st.session_state: # Kept voice_query for potential future use, but not actively used for pre-fill
    st.session_state.voice_query = ""

# --- CHAT BUBBLES DISPLAY ---
# Use a container to hold chat messages, allowing it to scroll independently
chat_display_area = st.container()

with chat_display_area:
    for idx, msg in enumerate(st.session_state.messages):
        # User messages on the left, AI on the right
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🧑‍💼"): # User avatar
                st.write(msg["content"])
        else: # role is "assistant"
            with st.chat_message("assistant", avatar="🤖"): # AI avatar
                st.write(msg["content"])
                # Removed individual download/copy buttons as requested

# --- MAIN CHAT INPUT ---
# The main chat input box, fixed at the bottom
# Removed 'value' parameter to avoid TypeError
user_question = st.chat_input(
    "Ask me about my projects, skills, or career journey...",
    key="chat_input_main_box", # Unique key for the chat input widget
)

# Process user question when submitted
if user_question and user_question.strip() != "":
    # Prevent duplicate messages if user hits enter multiple times or reruns
    if not st.session_state.messages or user_question.strip() != st.session_state.messages[-1]["content"]:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_question.strip()})
        st.session_state.voice_query = "" # Clear voice query after it's been used

        # Get AI response
        with st.spinner("Thinking..."):
            try:
                response = rag_chain.invoke(user_question.strip())
            except Exception as e:
                response = f"Sorry, there was an error processing your request: {e}. Please try again."
            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun() # Rerun to display new messages and clear the input box

# --- DOWNLOAD FULL CHAT BUTTONS ---
# Only show download options if there are messages in the chat
if st.session_state.messages:
    def transcript_content():
        """Generates a plain text transcript of the chat."""
        return "\n".join([f"{'USER:' if m['role']=='user' else 'AI:'} {m['content']}" for m in st.session_state.messages])

    def safe_text(text):
        """Removes non-ASCII characters for PDF compatibility."""
        replacements = {'—': '-', '–': '-', '’': "'", '“': '"', '”': '"', '…': '...'}
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text.encode('ascii', 'ignore').decode('ascii')

    def transcript_to_pdf():
        """Generates a PDF transcript of the chat."""
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        
        for msg in st.session_state.messages:
            role_label = "USER:" if msg["role"] == "user" else "AI:"
            pdf.set_font("Arial", 'B', 11) # Bold for role
            pdf.cell(0, 8, safe_text(role_label), ln=1)
            pdf.set_font("Arial", '', 11) # Regular for content
            # Ensure multi_cell handles line breaks and special characters
            pdf.multi_cell(0, 8, safe_text(msg["content"]))
            pdf.ln(2) # Small line break between messages
        
        # Output PDF to BytesIO buffer
        pdf_output = io.BytesIO()
        pdf_bytes = pdf.output(dest='S').encode('latin-1') # Get PDF content as bytes
        pdf_output.write(pdf_bytes)
        pdf_output.seek(0) # Rewind to the beginning
        return pdf_output

    st.markdown("---") # Separator before download buttons
    # Use columns to place buttons next to each other
    download_cols = st.columns([0.4, 0.1, 0.1, 0.4]) # Adjusted column ratios for centering
    with download_cols[1]: # Place TXT button in the second column
        st.download_button(
            "⭳ Text", # Shorter label
            data=transcript_content(),
            file_name="chat_transcript.txt",
            mime="text/plain",
            key="download_txt_chat",
            use_container_width=True # Make button full width of its column
        )
    with download_cols[2]: # Place PDF button in the third column
        pdf_file_buffer = transcript_to_pdf() # Get the BytesIO object
        st.download_button(
            "⭳ PDF", # Shorter label
            data=pdf_file_buffer,
            file_name="chat_transcript.pdf",
            mime="application/pdf",
            key="download_pdf_chat",
            use_container_width=True # Make button full width of its column
        )

# --- SIDEBAR DESIGN ---
with st.sidebar:
    st.markdown("""<div style="font-weight:600; font-size:1.21em;margin-top:-0.7em;">💬 Interview Prompts</div>""", unsafe_allow_html=True)
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
            # When an example question is clicked, add it to messages and trigger response
            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.voice_query = "" # Clear any pending voice input
            # Automatically invoke RAG chain for example questions
            with st.spinner("Thinking..."):
                try:
                    response = rag_chain.invoke(q)
                except Exception as e:
                    response = f"Sorry, there was an error processing this example: {e}"
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun() # Rerun to display the new messages

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:1.03em;color:#94b0be;line-height:1.43;">
    <b>AIML engineering graduate.</b><br>
    <span style="font-size:0.978em;">Ask about my projects, skills, or career journey—select from above or start typing!</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<h5 style='margin-bottom:0.65em;margin-top:1.65em;'><b>My Resume</b></h5>", unsafe_allow_html=True)

# Make sure to use the direct download/view link for Google Drive
resume_url = "https://drive.google.com/uc?export=view&id=1lf5SzSEzrMkj93_8ko_rVVQ03mdnUcHu"

# Embed PDF viewer
pdf_display = f'<iframe src="{resume_url}" width="100%" height="350px" type="application/pdf"></iframe>'
st.markdown(pdf_display, unsafe_allow_html=True)

# Download link
st.markdown(
    f'<a href="{resume_url}" download class="resume-link">⬇️ Download Resume</a>',
    unsafe_allow_html=True
)


# Footer section with structured markdown
st.markdown("""
 <div style="margin-top:45px; color:#8998a7; font-size:0.9em; text-align:center;">
    <p style="margin-bottom: 5px;">© 2025 <b>Sidhanth L</b></p>
    <p style="margin-bottom: 5px;">Built with 
        <span style='color:#68d6e3;'>LangChain</span>,
        <span style='color:#3cbfbe;'>ChromaDB</span>, 
        <span style='color:#c5ba6a;'>Streamlit</span>,
        <span style='color:#b836bf;'>Mistral 7B LLM</span>
    </p>
    <p style="margin-bottom: 5px;">Powered by RAG · Deployed on Hugging Face Spaces</p>
    <p>
        <a href="https://github.com/sidhanth01" style="color:#8baaff;text-decoration:none;">GitHub</a>
    </p>
</div>
""", unsafe_allow_html=True)
