# BitHealth RAG App Refactoring

This repository contains my refactored version of the RAG application as part of the technical test for the Associate Software Engineer position.

## Project Structure
- `app/`: Main application logic (API, Services, Workflow, Schemas).
- `notes.md`: Detailed explanation of design decisions and trade-offs.
- `requirements.txt`: Project dependencies.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the server: `uvicorn app.main:app --reload`