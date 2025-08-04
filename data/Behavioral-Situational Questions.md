### Q: Describe a difficult situation at work and how you handled it.

During the development and deployment of my **Ask-My-Portfolio** chatbot, I encountered a high-pressure situation when the Hugging Face Spaces demo broke right before a scheduled pitch—because the ChromaDB vector store wasn’t initialized. With less than an hour to spare, I calmly analyzed the logs, identified the missing ingestion trigger, and refactored my Streamlit frontend to automatically rebuild embeddings if needed. This not only got the demo back online but also improved product reliability for future users. I learned that composure, rapid root cause analysis, and building self-healing systems are crucial in production deployments.

---

### Q: Tell me about a time you worked on a team to solve a problem.

While leading the development of the **Auto Service System**, our team faced a major roadblock: our initial database schema design led to conflicts when simultaneous updates occurred for jobs assigned to different mechanics. I organized an ad-hoc team standup to openly discuss the challenge, then proposed and coordinated a database migration to implement row-level locking and better transaction handling. I delegated implementation tasks aligned to teammates’ strengths, provided mentorship where needed, and ensured we incorporated comprehensive test cases. Together, we delivered a more robust system before release—and the collaborative effort grew team morale and trust.

---

### Q: How do you handle conflicts or disagreements with colleagues?

I believe in proactive communication and empathic listening. For example, once while collaborating on the **FinGenius** AI assistant, a teammate strongly disagreed on using a Random Forest over a Neural Network for fraud detection. Instead of dismissing the suggestion, I proposed a side-by-side experiment, documented the technical pros and cons, and facilitated a transparent review with actual dataset metrics. In the end, we chose a hybrid model, and the experience built mutual respect and clarified our shared project priorities.

---

### Q: What would you do if you were assigned a project in an unfamiliar technology?

I’m always excited to tackle new technologies. When first building my RAG chatbot, **Ask-My-Portfolio**, I hadn’t previously used LangChain or ChromaDB. I started by reviewing core docs and tutorials, quickly prototyped minimal test cases, and leveraged discussions in the open-source community to clarify best patterns. I typically set up a small “sandbox” project, incrementally integrate components, and document lessons learned—all while communicating progress and blockers to stakeholders. This approach accelerates my learning curve and ensures high-quality delivery even in new stacks.

---

### Q: Give an example of how you adapted to change at work.

While working on **Bill & Receipt Insight Extractor**, user testing revealed that most real-world receipts had far more variability in format and quality than my initial synthetic test set. To adapt, I expanded my testing pipeline to cover a broader sample of receipts, implemented a user-editable correction interface in the dashboard, and re-engineered the OCR and parsing logic to be more fault-tolerant. This shift in priorities—from assuming static input to accounting for noisy, unpredictable data—made the product more resilient and user-friendly.

---

### Project-Specific Behavioral Narratives

**Ask-My-Portfolio – Narrative:**  
During the early rollout, a recruiter flagged that the chatbot would sometimes "hallucinate" if project sections were missing. I responded by refining my prompt engineering—adding instructions for the model to state “I don’t know” when context is insufficient, and by ensuring that my document chunking included negative and “not available” cases for edge queries. This direct feedback loop improved both the transparency of the model and recruiter satisfaction.

**Auto Service System – Narrative:**  
Our client requested a real-time analytics dashboard one week before go-live—a major scope change. Instead of resisting the late request, I led a rapid requirements session, reprioritized sprint tasks, and delegated rapid prototyping to teammates according to strengths. We delivered a functional analytics MVP on time, and the client was impressed by our agility and focus.

---

### Q: Describe a time you mentored or helped a peer/team member.

In the **ChestX-AI-Classifier** project, a new teammate struggled with model evaluation scripts and PyTorch syntax. I scheduled regular check-ins, pair programmed sample validation routines, and shared annotated code walkthroughs. Seeing their confidence and output quality improve was deeply rewarding and reinforced my commitment to mentorship and knowledge sharing.

---
