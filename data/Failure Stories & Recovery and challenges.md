# Failure Stories & Recovery — Project Resilience Narratives

## Ask-My-Portfolio

### Biggest Failure
**Failure:** During an important demo for a potential collaborator, the app failed to answer any questions because the ChromaDB vector store wasn’t initialized after a codebase deploy. The auto-ingestion trigger silently failed due to a minor path typo, leading to a “dead bot” just as the session began.

**Recovery:** I quickly diagnosed the ingestion block, traced it to a missing try-except for DirectoryLoader errors, and immediately patched the code to surface ingestion issues on the UI—and to re-trigger ingestion if ChromaDB was empty. After hotfixing and redeploying in under 20 minutes, the next user session was seamless. This incident solidified my approach: always expose recovery feedback in the UI and never leave ingestion as a silent failure.

---

## Bill & Receipt Insight Extractor

### Biggest Failure
**Failure:** My initial deployment used a set of “ideal” OCR parameters and parsing regexes, which worked in staged tests but completely broke down in real user uploads—many receipts were blurry or had new layouts, resulting in mislabeled fields and empty vendor/amount columns in the database.

**Recovery:** I rapidly added a manual review step with user-editable fields in the UI, flagging suspect extractions for correction. I then adjusted the pipeline to log failed parses, enabling iterative tuning with real user data. By closing the feedback loop and prioritizing user correction pathways, the system transitioned from brittle to resilient—and user trust and data coverage improved dramatically.

---

## ChestX-AI-Classifier

### Biggest Failure
**Failure:** Early in development, I neglected to use cross-institutional validation datasets and, as a result, my model achieved excellent metrics on local test splits but performed poorly on data from a new hospital partner—precision dropped by 20%, and the radiologists flagged obvious misclassifications.

**Recovery:** I introduced a better cross-validation setup, collected more heterogeneous data, and implemented extensive data augmentation. I also added per-class metric tracking to catch future issues. This “failure” reinforced the importance of realistic, diversity-aware validation and building for robustness beyond my own data.

---

## Auto Service System

### Biggest Failure
**Failure:** The first full deployment resulted in the admin dashboard crashing during peak hours as concurrent service updates conflicted (race condition in DB writes). Multiple users experienced lost job records, creating a stressful situation during rollout.

**Recovery:** I quickly rolled back to a stable version, then rewrote the service update logic to use row-level database locking and implemented atomic transactions. Additionally, I introduced regular backend health checks and comprehensive integration tests. The system stabilized, and user confidence surged.

---

## FinGenius

### Biggest Failure
**Failure:** My fraud detection module, when demoed live, missed several adversarial synthetic transactions inserted by a reviewer, undermining trust in the model’s claimed accuracy.

**Recovery:** I rebuilt the test suite with synthesized edge-case data and implemented adversarial validation routines. I also moved to a hybrid ensemble model (Random Forest + rules) and added explainable outputs so users could see why a flag or miss occurred. This experience taught me to never trust “single-metric” model claims at face value.

---

## QuoraInsight-Scraper

### Biggest Failure
**Failure:** The scraper was blocked by anti-bot measures after just 10 minutes of scraping, making large-scale corpus building impossible and forcing me to re-think the entire automation plan.

**Recovery:** I redesigned it to include randomized user agents, dynamic wait times, and robust session/cookie handling. I also implemented error retries and batch progress logging. While anti-bot blocks can never be fully eliminated, my new scraper now reliably collects data at scale while respecting rate limits.

---

# Challenges & Edge Cases — Advanced Scenario Narratives

## Ask-My-Portfolio

### Edge Case
**Challenge:** After a major document structure update, the bot started surfacing out-of-context snippets that misaligned with the section the user asked about.

**Solution:** I implemented smarter, context-aware chunk splitting and enriched chunk metadata with section headers and project names. Retrieval logic was updated to bias answers towards chunks with closely matching headings. This dramatically improved answer relevance in multi-topic documents.

---

## Bill & Receipt Insight Extractor

### Edge Case
**Challenge:** An uploaded batch of receipts mixed English and non-English vendors, confusing both OCR and parser; the system output nonsensical strings or crashed.

**Solution:** I added language detection and explicit error catching around the OCR pipeline. When non-English or low-confidence text is detected, the UI now flags it for manual entry, avoiding crashes and alerting users to data limitations.

---

## ChestX-AI-Classifier

### Edge Case
**Challenge:** Certain chest X-ray images had rare artifacts (like embedded hospital seals or machine noise) that led to model misclassification and misled GradCAM activations.

**Solution:** I employed an artifact detection pre-filter and excluded these images from training/validation. Visual review tools were built to surface edge cases and improve model explainability for real-world clinicians.

---

## Auto Service System

### Edge Case
**Challenge:** Edge case when two admins updated the same service record nearly simultaneously, leading to a “lost update” in the database and customer confusion over booking status.

**Solution:** I introduced row-level locking and optimistic concurrency controls. UI warns if an update race is detected, prompting a refresh and retry for the admin.

---

## FinGenius

### Edge Case
**Challenge:** Sudden, massive data spikes (test scenario: thousands of new transactions in one minute) overloaded the ingestion module and transactions were missed.

**Solution:** I refactored the ingestion to be batch-processed with queuing and retries, and added circuit breaker logic to prevent data loss during surges.

---

## QuoraInsight-Scraper

### Edge Case
**Challenge:** After Quora UI updates, the "load more answers" button changed dynamically, breaking all previous scraping selectors and halting data collection.

**Solution:** I moved to robust, regex-based selector logic, programmed the scraper to detect selector changes mid-run, and log “UI breakage” for manual intervention. I also versioned parsers to make hot-patching new selectors quick.

