# Ask-My-Portfolio

### An AI-powered chatbot that intelligently answers questions about my professional portfolio and projects.

---

## 🚀 Live Demo

**[Live Demo Link](https://huggingface.co/spaces/sidhanthL/ask-my-portfolio)**

This project is deployed as a live, interactive demo on Hugging Face Spaces, showcasing a seamless end-to-end RAG application.

## ✨ Key Features

* **Interactive Q&A:** A user-friendly Streamlit chatbot interface for natural language queries.
* **Context-Aware Responses:** The model provides answers based solely on my resume and other professional documents, preventing fabrication of information.
* **Advanced RAG Pipeline:** Employs a Retrieval-Augmented Generation (RAG) architecture to ensure responses are accurate and relevant.
* **Dual LLM Architecture:** Utilizes a local LLM (Ollama's Mistral) for development with a cloud-based fallback (Hugging Face Hub) for reliable deployment.
* **Resume Integration:** A sidebar displays my resume directly within the application, allowing for simultaneous viewing and interaction.
* **Chat History Download:** Users can download a full transcript of the conversation in both PDF and plain text formats.
* **Modular Data Ingestion:** The project's knowledge base can be easily updated by adding new documents to the `data/` folder.

## 🛠️ Technical Stack

-   **Framework:** [Streamlit](https://streamlit.io/)
-   **Core LLM Library:** [LangChain](https://www.langchain.com/)
-   **Vector Database:** [ChromaDB](https://www.trychroma.com/)
-   **Embedding Model:** `all-MiniLM-L6-v2` (from Hugging Face)
-   **Language Models:**
    -   Local Development: [Ollama](https://ollama.ai/) (Mistral 7B)
    -   Cloud Deployment: [HuggingFaceHub](https://huggingface.co/docs/hub/spaces-sdks-integrations) (Flan-T5-Base)
-   **Deployment:** [Hugging Face Spaces](https://huggingface.co/spaces)
-   **Version Control:** [Git](https://git-scm.com/) and [Git LFS](https://git-lfs.github.com/) for handling large files.

## 📂 File Structure

```
├── app.py                     # Main Streamlit application
├── ingest_data.py             # Script for data ingestion and vector DB creation
├── requirements.txt           # Project dependencies
├── .gitignore                 # Specifies files and folders to ignore (e.g., .env, venv)
├── .gitattributes             # Git LFS configuration for binary files
├── data/                      # Folder for resume and other portfolio documents
│   └── Resume.pdf
└── .env                       # Environment variables (secret)
```

## 💻 Local Setup & Installation

To run this project on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[your-username]/[your-repo-name].git
    cd [your-repo-name]
    ```
2.  **Initialize Git LFS and pull the data files:**
    ```bash
    git lfs install
    git pull
    ```
3.  **Set up the virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    # For Windows:
    .\venv\Scripts\activate
    # For macOS/Linux:
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    -   Create a `.env` file in the root directory.
    -   Fill it with your token and LLM details:
        ```
        OLLAMA_BASE_URL="http://localhost:11434"
        OLLAMA_MODEL="mistral"
        HF_TOKEN="<your_hugging_face_token>"
        ```
5.  **Run the data ingestion script:**
    -   Ensure your Ollama server is running locally and the `mistral` model is pulled.
    -   This will create the `chroma_db` vector database.
    ```bash
    python ingest_data.py
    ```
6.  **Launch the Streamlit application:**
    -   Since your `requirements.txt` does not include `ollama`, your application will automatically fall back to using the `HuggingFaceHub` LLM when you run it locally.
    ```bash
    streamlit run app.py
    ```

## 📄 Usage

-   Ask the chatbot questions about my projects, skills, and professional experience.
-   Use the pre-filled questions in the sidebar for quick examples.

## 🤝 Contact

-   **Name:** Sidhanth L
-   **GitHub:** [view](https://github.com/sidhanth01)
-   **LinkedIn:** [view](https://www.linkedin.com/in/sidhanth-l-60667b311/?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

Feel free to connect and ask any questions about my work! 