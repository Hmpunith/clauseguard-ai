"""
ClauseGuard AI — Autonomous Contract Intelligence Agent Pipeline
Five specialized Gemini agents that analyze contracts autonomously.
"""

import json
import asyncio
import base64
import re
from pathlib import Path

import google.generativeai as genai


class ContractAgentPipeline:
    """Orchestrates 5 autonomous agents to analyze a contract end-to-end."""

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    # ── SSE helper ──────────────────────────────────────────────
    @staticmethod
    def _evt(agent: str, status: str, data):
        return {"type": "agent_update", "agent": agent, "status": status, "data": data}

    # ── Gemini call wrapper ─────────────────────────────────────
    async def _ask(self, prompt: str, *, file_data=None, json_mode: bool = True):
        """Call Gemini and optionally parse JSON from the response."""
        parts = []
        if file_data:
            parts.append(file_data)
        parts.append(prompt)

        config = {}
        if json_mode:
            config["response_mime_type"] = "application/json"

        response = await asyncio.to_thread(
            self.model.generate_content,
            parts,
            generation_config=config if config else None,
        )
        text = response.text.strip()

        if json_mode:
            # Strip markdown code fences if present
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
            return json.loads(text)
        return text

    # ── Pipeline entry point (async generator → SSE) ───────────
    async def run(self, file_path: str, content_type: str):
        results = {}

        # ─── AGENT 1 — Document Ingestion ──────────────────────
        yield self._evt("ingestion", "working", "Reading document with Gemini Vision...")
        try:
            with open(file_path, "rb") as f:
                raw = f.read()
            file_blob = {"mime_type": content_type, "data": base64.b64encode(raw).decode()}

            doc_text = await self._ask(
                "Extract ALL text from this document verbatim. "
                "Preserve section numbers, headings, bullet points, and paragraph structure. "
                "Return only the raw extracted text.",
                file_data=file_blob,
                json_mode=False,
            )
            results["text"] = doc_text
            char_count = len(doc_text)
            yield self._evt("ingestion", "complete", f"Extracted {char_count:,} characters")
        except Exception as e:
            yield self._evt("ingestion", "error", str(e))
            return

        # ─── AGENT 2 — Document Understanding ──────────────────
        yield self._evt("understanding", "working", "Identifying parties, dates, and structure...")
        try:
            understanding = await self._ask(PROMPT_UNDERSTANDING.format(text=doc_text[:12000]))
            results["understanding"] = understanding
            parties = understanding.get("parties", [])
            sections = understanding.get("structure", [])
            yield self._evt(
                "understanding",
                "complete",
                {
                    "summary": f"{understanding.get('document_type','Document')} — "
                    f"{len(parties)} parties, {len(sections)} sections",
                    "detail": understanding,
                },
            )
        except Exception as e:
            yield self._evt("understanding", "error", str(e))
            return

        # ─── AGENT 3 — Clause Extraction ───────────────────────
        yield self._evt("extraction", "working", "Extracting and categorizing clauses...")
        try:
            clauses = await self._ask(PROMPT_CLAUSES.format(text=doc_text[:15000]))
            results["clauses"] = clauses
            clause_list = clauses.get("clauses", [])
            yield self._evt(
                "extraction",
                "complete",
                {
                    "summary": f"Extracted {len(clause_list)} clauses across "
                    f"{len(set(c.get('category','') for c in clause_list))} categories",
                    "detail": clauses,
                },
            )
        except Exception as e:
            yield self._evt("extraction", "error", str(e))
            return

        # ─── AGENT 4 — Risk Analysis ──────────────────────────
        yield self._evt("risk", "working", "Analyzing risk factors in every clause...")
        try:
            risks = await self._ask(
                PROMPT_RISK.format(
                    text=doc_text[:10000],
                    clauses_json=json.dumps(clauses.get("clauses", [])[:20], indent=2),
                )
            )
            results["risks"] = risks
            risk_items = risks.get("risks", [])
            score = risks.get("overall_risk_score", "?")
            yield self._evt(
                "risk",
                "complete",
                {
                    "summary": f"{len(risk_items)} risk factors — Risk Score: {score}/100",
                    "detail": risks,
                },
            )
        except Exception as e:
            yield self._evt("risk", "error", str(e))
            return

        # ─── AGENT 5 — Executive Summary ──────────────────────
        yield self._evt("summary", "working", "Generating executive briefing...")
        try:
            summary = await self._ask(
                PROMPT_SUMMARY.format(
                    understanding_json=json.dumps(understanding, indent=2)[:3000],
                    clauses_json=json.dumps(clauses.get("clauses", [])[:15], indent=2)[:4000],
                    risks_json=json.dumps(risks, indent=2)[:4000],
                )
            )
            results["summary"] = summary
            yield self._evt(
                "summary",
                "complete",
                {"summary": "Executive briefing ready", "detail": summary},
            )
        except Exception as e:
            yield self._evt("summary", "error", str(e))
            return

        # ─── DONE ──────────────────────────────────────────────
        yield {"type": "pipeline_complete", "data": results}


# ═══════════════════════════════════════════════════════════════
# AGENT PROMPTS
# ═══════════════════════════════════════════════════════════════

PROMPT_UNDERSTANDING = """You are a senior legal analyst AI agent. Analyze this contract text and extract structured metadata.

CONTRACT TEXT:
\"\"\"
{text}
\"\"\"

Return a JSON object with exactly these keys:
{{
  "document_type": "string — e.g. NDA, SaaS Agreement, Employment Contract",
  "title": "string — document title if present",
  "parties": [
    {{"name": "string", "role": "string — e.g. Provider, Client, Employee"}}
  ],
  "effective_date": "string or null",
  "expiration_date": "string or null",
  "governing_law": "string — jurisdiction, or null",
  "structure": [
    {{"section": "string — section number", "title": "string — section heading"}}
  ]
}}
"""

PROMPT_CLAUSES = """You are a clause extraction AI agent. Extract every significant clause from this contract.

CONTRACT TEXT:
\"\"\"
{text}
\"\"\"

Return JSON:
{{
  "clauses": [
    {{
      "id": "number — sequential",
      "section": "string — section reference e.g. 4.2",
      "title": "string — clause heading",
      "category": "string — one of: payment, liability, termination, confidentiality, ip_ownership, non_compete, indemnification, warranty, dispute_resolution, data_protection, force_majeure, renewal, other",
      "summary": "string — 1-2 sentence summary of what this clause does",
      "key_terms": ["string — important terms, amounts, or durations mentioned"]
    }}
  ]
}}

Extract ALL clauses. Be thorough.
"""

PROMPT_RISK = """You are a contract risk assessment AI agent. Analyze these clauses for legal and business risks.

CONTRACT TEXT (for reference):
\"\"\"
{text}
\"\"\"

EXTRACTED CLAUSES:
{clauses_json}

For each risky clause, assess the severity. Then provide an overall risk score from 0 (safe) to 100 (extremely risky).

Return JSON:
{{
  "overall_risk_score": "number 0-100",
  "overall_rating": "string — LOW, MEDIUM, HIGH, or CRITICAL",
  "risks": [
    {{
      "clause_id": "number — references clause id",
      "clause_title": "string",
      "severity": "string — low, medium, high, critical",
      "issue": "string — what the risk is",
      "explanation": "string — why this is risky",
      "recommendation": "string — how to mitigate"
    }}
  ]
}}

Focus on: unlimited liability, one-sided termination, IP assignment traps, broad non-competes, auto-renewal lock-ins, weak data protection, missing limitation of liability caps, broad indemnification, unfavorable dispute resolution.
"""

PROMPT_SUMMARY = """You are an executive briefing AI agent. Synthesize all analysis into a clear executive summary.

DOCUMENT UNDERSTANDING:
{understanding_json}

KEY CLAUSES:
{clauses_json}

RISK ANALYSIS:
{risks_json}

Return JSON:
{{
  "executive_summary": "string — 3-5 paragraph executive summary of the contract and its risks",
  "risk_score": "number 0-100",
  "risk_rating": "string — LOW, MEDIUM, HIGH, or CRITICAL",
  "top_concerns": [
    {{"concern": "string", "severity": "string", "action": "string"}}
  ],
  "recommended_actions": ["string — specific action items before signing"],
  "negotiation_points": ["string — clauses that should be renegotiated"],
  "approval_recommendation": "string — APPROVE, APPROVE WITH CHANGES, or DO NOT SIGN"
}}
"""
