# 💼 Ask-My-Portfolio Dataset Entry: Bill & Receipt Insight Extractor

## Project Title
Bill & Receipt Insight Extractor

## Short Description / Tagline
AI-powered application for automated extraction, validation, visualization, and management of receipt and bill financial data to simplify personal expense tracking.

## Problem Statement / Real-World Challenge
Manual management of receipts and bills is cumbersome, inefficient, and prone to errors. Most users struggle to keep accurate records and gain actionable insights from fragmented, unstructured financial documents, limiting effective budgeting and spending control.

## Project Goal / Objectives
- Automate ingestion and parsing of diverse receipt and bill formats (images, PDFs, text).
- Extract structured, reliable financial information (vendor, date, amount, category).
- Store data in an efficient, queryable database that supports user-driven refinement.
- Provide interactive dashboards and visual analytics to reveal spending patterns and trends.
- Enable manual corrections and flexible data export for downstream use.

## Your Specific Role & Contributions
- Designed and developed the full-stack application architecture and workflow.
- Implemented OCR integration using Tesseract with customized parsing rules for robust data extraction.
- Developed backend REST API with FastAPI coupled with SQLite via SQLModel ORM.
- Defined precise data validation schemas using Pydantic for maintaining data integrity.
- Created Streamlit-based interactive frontend with dynamic visualizations using Plotly Express.
- Developed features for multi-format file ingestion, manual data editing, and CSV export.
- Conducted performance tuning to handle batch processing of 100+ files.
- Tested and iteratively improved OCR accuracy and UI usability.
- Documented the project comprehensively and deployed a live demo for user testing.

## Key Technologies & Techniques Used
- **Languages:** Python
- **Frameworks:** FastAPI (backend), Streamlit (frontend)
- **OCR:** Tesseract-OCR (via pytesseract)
- **Databases:** SQLite (managed with SQLModel ORM)
- **Validation:** Pydantic for schema enforcement and data validation
- **Data Handling:** Pandas, NumPy
- **Image & PDF Processing:** Pillow (PIL), PyPDF2
- **Visualization:** Plotly Express
- **Other Tools:** Git & GitHub (version control), Requests (HTTP client)

## Workflow / Architecture Summary
- **Data Flow:** User uploads files (images/PDFs/text) → files processed with OCR to extract text → parsed to extract structured fields → validated against Pydantic models → stored in SQLite database with indexing.
- **Modular Design:** 
  - OCR and parsing module isolates text extraction.
  - API layer (FastAPI) handles data operations.
  - Frontend (Streamlit) presents data and visualizations.
  - Export module enables CSV downloads.
- This separation enhances maintainability, extensibility, and scalability.

## Key Features
- Multi-format file ingestion: supports .jpg, .png, .pdf, .txt files.
- Intelligent text extraction with OCR combined with rule-based parsing.
- Automatic identification of key financial fields: vendor, amount, date, category.
- Data validation and schema enforcement with Pydantic to ensure accuracy.
- Persistent, indexed SQLite database for efficient storage and retrieval.
- Interactive dashboard for filtering, sorting, and examining transaction data.
- Multiple visualization types: bar charts (vendor frequency), pie/donut charts (category breakdown), line graphs (monthly trends), summary stats.
- Manual correction interface allowing users to edit extracted data.
- Ability to delete incorrect or unwanted entries.
- CSV export capability supporting customized datasets by filters.
- Scalable batch processing supporting 100+ files per session.

## Quantifiable Results / Impact
- OCR parsing accuracy consistently ≥ 85% on clear scans, reducing manual data entry effort significantly.
- Batch processing optimized for handling over 100 receipts without degradation in performance.
- Estimated >90% reduction in manual receipt data logging time compared to traditional spreadsheet methods.
- Improved expenditure insights helped users identify saving opportunities and usage trends.
- User feedback from early testers indicated enhanced budgeting confidence.

## Sample Usage / Example Scenario
1. A user uploads a batch of receipts from a recent shopping trip in .jpg format.
2. The system automatically extracts key financial details and populates the database.
3. User reviews parsed entries in the dashboard, manually correcting one vendor name and a misread date.
4. Visual charts reveal the largest spending category and monthly expenditure trends.
5. User exports the filtered receipts data for integration into their personal finance software.

## Known Limitations & Future Enhancements
- **Limitations:**
  - OCR struggles somewhat with poor-quality scans or handwritten receipts.
  - Currently limited to English-language documents.
  - No multi-user authentication or privacy controls yet implemented.
- **Future Enhancements:**
  - Add multi-user support with secure authentication and data separation.
  - Integrate AI/ML models for smarter auto-categorization and improved OCR accuracy.
  - Expand language support including non-Latin scripts.
  - Upgrade backend to cloud-based scalable databases for collaborative usage.
  - Mobile app extension for on-the-go receipt capture and processing.

## Live Demo Link, Repo Link
- **Live Demo:** https://bill-receipt-insight-extractor.streamlit.app/
- **GitHub Repository:** https://github.com/sidhanth01/bill-receipt-insight-extractor
