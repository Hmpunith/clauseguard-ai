# ClauseGuard AI — Hackathon Submission

## 📋 Basic Information

**Project Title:** ClauseGuard AI — Autonomous Contract Intelligence Agent

**Short Description:** Six autonomous AI agents analyze any contract end-to-end — extracting clauses, scoring risks, generating executive briefings, and self-auditing their findings — all powered by Gemini 2.5 Flash, with zero human prompting.

**Long Description:**

### The Problem
Contract review is broken. Legal review costs $500–$1,000/hour, takes weeks, and still misses critical risks buried in dense language. Small businesses sign dangerous contracts because they can't afford legal counsel. Even enterprise teams lack consistent risk scoring across deals.

### Our Solution
ClauseGuard AI is a fully autonomous multi-agent system that analyzes contracts end-to-end without human intervention. Upload any contract — PDF, scan, or photo — and six specialized AI agents deliver a complete risk assessment in under 90 seconds.

### The 6 Autonomous Agents
1. **📥 Ingestion Agent** — Reads PDFs, scans, and photos using Gemini's multimodal vision
2. **🧠 Understanding Agent** — Identifies document type, parties, dates, governing law, and structure
3. **📋 Extraction Agent** — Extracts and categorizes every clause (payment, liability, IP, termination, etc.)
4. **⚠️ Risk Analysis Agent** — Scores each clause for risk severity with detailed mitigation recommendations
5. **📝 Summary Agent** — Generates a board-ready executive briefing with approval recommendation
6. **🔍 Audit Agent** — Cross-validates all other agents' findings for consistency and missed risks

### Key Technical Highlights
- **Fully Autonomous Pipeline** — Upload once, agents handle everything sequentially with zero prompts
- **Real-Time Agent Trace** — Watch each agent work via Server-Sent Events streaming
- **Self-Auditing Architecture** — The 6th agent validates the other 5, checking for missed risks and logical inconsistencies
- **Multimodal Input** — Gemini Vision processes PDFs, scanned contracts, and photos directly
- **Structured JSON Output** — Every agent returns clean, structured data enabling rich visualizations
- **Risk Scoring** — 0–100 quantified risk score with CRITICAL/HIGH/MEDIUM/LOW severity ratings
- **Actionable Output** — Specific negotiation points, action items, and approval recommendations
- **PDF Export** — One-click downloadable report for stakeholders

### How Gemini Powers ClauseGuard
| Capability | Usage |
|---|---|
| Multimodal Vision | Direct document reading — PDFs, scans, photos without OCR |
| Advanced Reasoning | Legal risk identification and cross-clause analysis |
| Structured JSON Output | Clean data for every agent enabling programmatic processing |
| Speed (Flash) | Full 6-agent pipeline in ~90 seconds |

### Architecture
```
Frontend (HTML/JS)          Backend (FastAPI + SSE)
─────────────────           ──────────────────────
Upload Zone          →      /api/upload
Pipeline Viz         ←      /api/analyze/{id} (SSE stream)
Results Dashboard    ←      Agent Pipeline:
PDF Export                   Ingest → Understand → Extract → Risk → Summary → Audit
                            ↕
                     Google Gemini 2.5 Flash (Multimodal + JSON mode)
```

### Business Value
- **50x faster** than manual legal review
- **$0 per review** vs $500+/hour for legal counsel
- **100% consistent** risk scoring across all contracts
- **Target markets:** SMBs, enterprise legal teams, M&A due diligence, procurement

### Tech Stack
- **AI Model:** Google Gemini 2.5 Flash via Gemini API
- **Backend:** Python, FastAPI, Server-Sent Events
- **Frontend:** HTML5, CSS3 (glassmorphism), Vanilla JavaScript
- **Deployment:** Docker → Render

**Technology Tags:** Gemini AI, AI Studio, Google Cloud, FastAPI, Python

**Category Tags:** Enterprise, Legal Tech, Autonomous Agents, Multi-Agent Systems

---

## 💻 Links

- **GitHub:** https://github.com/Hmpunith/clauseguard-ai
- **Live App:** https://clauseguard-ai-onx1.onrender.com
- **Pitch Deck:** (open pitch-deck.html locally or screenshot for slides)

---

## 🎥 Demo Video Script (3-4 minutes)

### INTRO (30 seconds)
"Hi, I'm [Name], and this is ClauseGuard AI — an autonomous contract intelligence agent built for the AI Agent Olympics Hackathon.

Contract review is broken. It costs $500 an hour, takes weeks, and still misses critical risks. What if six AI agents could do it in 90 seconds?

That's exactly what ClauseGuard does."

### THE ARCHITECTURE (30 seconds)
"ClauseGuard uses six specialized Gemini-powered agents that work in sequence — completely autonomously. 

First, the Ingestion agent reads your document using Gemini's multimodal vision. Then the Understanding agent identifies parties and structure. The Extraction agent pulls every clause. The Risk agent scores each one. The Summary agent generates an executive briefing. And finally — the Audit agent cross-validates everything the other five did.

No human prompts. No manual steps. Fully autonomous."

### LIVE DEMO (90 seconds)
"Let me show you. I'll upload this SaaS agreement..."

[Upload contract → show pipeline animation → agents lighting up one by one]

"Watch the agents work in real time. Each one streams its progress as it analyzes the contract.

[Scroll through results]

"Risk score: 95 out of 100 — Critical. The agents found 20 clauses, 12 risk factors, and recommend 'Approve with Significant Changes.'

Look at what it caught — a perpetual data license, one-sided termination rights, an 18% late payment penalty, and a 3-year non-compete on a SaaS client. These are exactly the traps that cost companies millions.

And here's the Audit agent — it cross-validated everything and confirmed the risk score is accurate with 92% confidence."

### BUSINESS VALUE (30 seconds)
"ClauseGuard isn't just a demo — it's a real enterprise tool. SMBs can review vendor contracts before signing. Legal teams can process high volumes consistently. M&A teams can due-diligence contract portfolios.

50x faster than manual review. Zero cost per analysis. 100% consistent scoring."

### TECH & CLOSING (30 seconds)
"Built with Gemini 2.5 Flash for all six agents, FastAPI for real-time SSE streaming, and deployed as a single Docker container.

The key innovation is the self-auditing architecture — agent 6 validates agents 1 through 5, making this a truly autonomous system that checks its own work.

ClauseGuard AI — autonomous contract intelligence. Thank you."

---

## Recording Tips
1. Use screen recording software (OBS or built-in screen recorder)
2. Record at 1920x1080
3. Speak clearly and at a steady pace
4. Show the live deployed URL (not localhost)
5. Have the sample contract ready to upload
6. Let the pipeline animation play in full — it's visually impressive
7. Scroll slowly through results so judges can read
