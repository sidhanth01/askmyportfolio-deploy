### Q: Tell me about a recent project you worked on.

One of my most impactful recent projects is **Ask-My-Portfolio**, an AI-powered Retrieval-Augmented Generation (RAG) chatbot designed to answer natural language queries about my project portfolio. I built the entire pipeline—from ingestion scripts that process PDFs, markdowns, and text files using LangChain loaders, to semantic chunking and embedding with all-MiniLM-L6-v2, to deploying a Streamlit Q&A interface on Hugging Face Spaces powered by Mistral 7B LLM. This project showcases my hands-on expertise in vector search, LLM orchestration, and user-centric full-stack engineering.

---

### Q: Which of your projects are you most proud of and why?

I’m especially proud of **Bill & Receipt Insight Extractor** because it solves a tangible pain point—turning messy receipts into structured, actionable financial insights for everyday users. I engineered an OCR-powered (using Tesseract) workflow, built a FastAPI backend, and designed an interactive Streamlit dashboard for analytics. Down the line, this project taught me how to balance AI automation with user editability, and how to push out robust, cloud-friendly deployments for real-world use.

---

### Q: What role did you play in [Project X]? (Example: ChestX-AI-Classifier)

In **ChestX-AI-Classifier**, I served as the lead developer and architect. I designed the dataset preprocessing pipeline, implemented transfer learning on DenseNet121 for multi-class X-ray image classification, wrote evaluation scripts for medical metrics like ROC-AUC, and integrated GradCAM for interpretability. I also documented the codebase for reproducibility, handled data augmentation, and validated performance on open datasets, ensuring the results were both accurate and explainable.

---

### Q: Can you explain the technical stack and choices for one of your key projects?

In **Ask-My-Portfolio**, I chose:
- **all-MiniLM-L6-v2** for semantic embedding because of its speed and high recall in document retrieval scenarios.
- **ChromaDB** as the vector store for lightweight, persistent, and scalable chunk storage.
- **LangChain** for its modular retrieval and RAG chain capabilities.
- **Mistral 7B** LLM (via Ollama/HuggingFaceHub) for precise, context-aware answer synthesis.
- **Streamlit** frontend for interactive chat and cross-platform deployment.
This stack allowed for fast ingestion, robust chunked retrieval, and easy, scalable deployment—essential for handling a growing, evolving portfolio.

---

### Q: What was the quantifiable impact/results of your projects?

- **Bill & Receipt Insight Extractor**: Reduced manual expense tracking time by 90% and achieved >85% OCR accuracy on clear scans.
- **ChestX-AI-Classifier**: Delivered >90% validation accuracy and >0.95 ROC-AUC on open chest X-ray datasets.
- **FinGenius**: Fraud detection model achieved 94.2% accuracy and processed 1,000+ transactions/sec under load tests.
- **Ask-My-Portfolio**: Supported recruiters in obtaining detailed answers to portfolio questions with >95% accuracy, slashing manual review time by over 90%.

---

### Q: Tell me about a challenging project and what you learned from it.

**Ask-My-Portfolio** was a uniquely challenging project because it required blending multiple advanced components—document loaders for various file types (PDF, markdown, text), robust chunking logic, semantic vector search with ChromaDB, the integration of a state-of-the-art LLM (Mistral 7B), and a Streamlit chat interface—all while ensuring user privacy and scalable deployment. One lesson was the importance of *context-aware chunking*: getting retrieval right meant experimenting with chunk sizes and overlaps to maximize both answer accuracy and latency. I also had to design the ingestion script to be self-healing for Hugging Face Spaces deployment, triggering data processing automatically when the vector store was missing. This project pushed me to orchestrate cloud-native workflows, optimize retrieval pipelines under quota constraints, and develop clear user feedback mechanisms for a seamless experience.

---

### Q: Give an example of teamwork or leadership in your project experience.

In the development of **Auto Service System**, I led a small team through the entire SDLC—partitioning responsibilities for backend logic, frontend UX, and database design. I facilitated sprint standups, mentored teammates in implementing Flask/Django best practices, and ensured our admin dashboard and service workflow reflected real user needs. This project taught me how clarity of communication and shared vision are critical to both progress and morale.

---

### Q: How do you ensure your project results are reliable and robust?

I emphasize end-to-end testing, validation against real and synthetic data, and comprehensive documentation. For all major projects, I wrote unit and integration tests (e.g., for NLP pipelines in FinGenius and model inference in ChestX-AI-Classifier), performed cross-validation, and set up logging/monitoring to catch anomalies early. User feedback, manual error analysis, and open-sourcing for collaborative review are also core parts of my robustness strategy.

---

### Project Narrative Stories

**Ask-My-Portfolio (RAG Chatbot) – Narrative: “RAG Under Pressure”**

Late one night before my demo, I discovered that the Hugging Face Spaces instance was failing due to a missing ChromaDB vector store—something undetectable in local runs. Drawing on what I’d built, I rapidly refactored the frontend to auto-ingest supported files and self-heal without manual intervention, ensuring uptime and a frictionless recruiter experience. This iterative, edge-case-driven debugging honed my cloud deployment skills and reinforced the importance of full pipeline observability.

---

**Bill & Receipt Insight Extractor – Narrative: “Automation Meets Reality”**

Building the bill extractor, I thought OCR and simple parsing would be enough—until I tested on real-world receipts with blurry images and irregular formats. My initial models flagged errors and filled the dashboard with noise. Instead of hiding the flaws, I built a user feedback loop: editable fields, error flagging, and visual cues, so users could correct and improve the extraction over time. This transformed the project from a static tool into a living system that gets smarter with use—demonstrating my commitment to bridging AI with human-centric design.
