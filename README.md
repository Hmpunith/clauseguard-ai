# 🛡️ ClauseGuard AI — Autonomous Contract Intelligence Agent

> **AI Agent Olympics Hackathon · Milan AI Week 2026**
> Powered by **Gemini** · Deployed on **Vultr**

## What It Does

ClauseGuard AI is an autonomous multi-agent system that analyzes contracts end-to-end without human intervention. Upload any contract (PDF, scan, or photo), and **five specialized AI agents** work in sequence to deliver a complete risk assessment and executive briefing.

### The 5 Autonomous Agents

| # | Agent | Role |
|---|-------|------|
| 1 | 📥 **Ingestion** | Reads and extracts text from PDFs, scans, and photos using Gemini Vision |
| 2 | 🧠 **Understanding** | Identifies document type, parties, dates, governing law, and structure |
| 3 | 📋 **Extraction** | Extracts and categorizes every clause (payment, liability, IP, etc.) |
| 4 | ⚠️ **Risk Analysis** | Scores each clause for risk — flags dangerous terms and provides mitigation advice |
| 5 | 📝 **Executive Summary** | Generates a board-ready briefing with risk score, top concerns, and recommended actions |

### Key Features

- **Fully Autonomous** — Upload a contract and the agents handle everything, no prompts needed
- **Real-Time Agent Trace** — Watch each agent work in real time via streaming updates
- **Multimodal Input** — Handles PDFs, scanned documents, and photos of contracts
- **Risk Scoring** — 0–100 risk score with severity ratings for every clause
- **Actionable Output** — Executive summary, negotiation points, and approval recommendation

## Tech Stack

- **AI Model:** Google Gemini 2.0 Flash (via Gemini API)
- **Backend:** Python, FastAPI, Server-Sent Events
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Deployment:** Docker → Vultr VM

## Quick Start

### 1. Get a Gemini API Key

Go to [Google AI Studio](https://aistudio.google.com/) → Get API Key

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Install & Run

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000

### Docker

```bash
docker build -t clauseguard .
docker run -p 8000:8000 --env-file .env clauseguard
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (HTML/JS)                    │
│  Upload Zone → Agent Pipeline Viz → Results Dashboard   │
├─────────────────────────────────────────────────────────┤
│                  FastAPI Server (SSE)                    │
│  /api/upload → /api/analyze/{id} → /api/results/{id}   │
├─────────────────────────────────────────────────────────┤
│              Agent Pipeline (Sequential)                │
│  Ingestion → Understanding → Extraction → Risk → Summary│
├─────────────────────────────────────────────────────────┤
│               Google Gemini 2.0 Flash                   │
│         Multimodal Vision + JSON Structured Output      │
└─────────────────────────────────────────────────────────┘
```

## Hackathon Tracks

- **🟢 Google Gemini Track** — Gemini powers all 5 agents (vision + reasoning + structured output)
- **🔵 Vultr Track** — Full-stack containerized deployment on Vultr VM

## License

MIT
