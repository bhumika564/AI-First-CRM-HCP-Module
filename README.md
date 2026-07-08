# AI-First CRM HCP Module

This project implements an AI-First Customer Relationship Management (CRM) module tailored for Healthcare Professionals (HCPs). It features a "Log Interaction Screen" with both a structured form and a conversational AI chat interface.

## Tech Stack
- **Frontend**: React (TypeScript), Vite, Redux Toolkit, Vanilla CSS (Premium Glassmorphism Design)
- **Backend**: Python, FastAPI, SQLAlchemy
- **AI Agent**: LangGraph, ChatGroq (`gemma2-9b-it`)
- **Database**: SQLite (Configured to easily switch to PostgreSQL/MySQL via `.env`)

## Project Structure
- `/frontend`: The React UI application.
- `/backend`: The FastAPI and LangGraph backend server.

## Prerequisites
- Node.js (v18+)
- Python 3.10+
- A Groq API Key

## Setup Instructions

### 1. Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend` directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   DATABASE_URL=sqlite:///./crm.db
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### 2. Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the Vite development server:
   ```bash
   npm run dev
   ```

## LangGraph AI Agent & Tools
The LangGraph agent acts as an intelligent assistant for life science field representatives. It manages state and executes tools to automate the logging of interactions.

**Configured Tools:**
1. **Log Interaction**: Extracts data from conversational input and saves a new interaction record to the database.
2. **Edit Interaction**: Updates an existing interaction record based on user corrections.
3. **Get Past Interactions**: Retrieves recent history for an HCP to provide context to the agent.
4. **Search Materials**: Recommends marketing PDFs/brochures based on topics discussed.
5. **Schedule Follow-up**: Sets up actionable follow-up tasks for specific HCPs.
