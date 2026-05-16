/* ClauseGuard AI — App Logic */
(function () {
  "use strict";

  const $ = (s) => document.querySelector(s);
  const $$ = (s) => document.querySelectorAll(s);

  // DOM refs
  const uploadZone = $("#upload-zone");
  const fileInput = $("#file-input");
  const btnBrowse = $("#btn-browse");
  const fileInfo = $("#file-info");
  const fileName = $("#file-name");
  const btnAnalyze = $("#btn-analyze");
  const pipelineSec = $("#pipeline-section");
  const resultsSec = $("#results-section");
  const agentLog = $("#agent-log");
  const navStatus = $("#nav-status");
  const btnNew = $("#btn-new");

  let selectedFile = null;

  // ── Upload handlers ──────────────────────────────────────
  uploadZone.addEventListener("click", () => fileInput.click());
  btnBrowse.addEventListener("click", (e) => { e.stopPropagation(); fileInput.click(); });

  uploadZone.addEventListener("dragover", (e) => { e.preventDefault(); uploadZone.classList.add("drag-over"); });
  uploadZone.addEventListener("dragleave", () => uploadZone.classList.remove("drag-over"));
  uploadZone.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadZone.classList.remove("drag-over");
    if (e.dataTransfer.files.length) pickFile(e.dataTransfer.files[0]);
  });

  fileInput.addEventListener("change", () => { if (fileInput.files.length) pickFile(fileInput.files[0]); });

  function pickFile(file) {
    selectedFile = file;
    fileName.textContent = file.name;
    fileInfo.style.display = "flex";
  }

  // ── Analyze ──────────────────────────────────────────────
  btnAnalyze.addEventListener("click", async () => {
    if (!selectedFile) return;

    // Upload
    btnAnalyze.disabled = true;
    btnAnalyze.textContent = "Uploading...";
    setNav("Uploading...", true);

    const form = new FormData();
    form.append("file", selectedFile);

    let contractId;
    try {
      const res = await fetch("/api/upload", { method: "POST", body: form });
      if (!res.ok) { const e = await res.json(); throw new Error(e.detail || "Upload failed"); }
      const data = await res.json();
      contractId = data.contract_id;
    } catch (err) {
      alert("Upload error: " + err.message);
      btnAnalyze.disabled = false;
      btnAnalyze.textContent = "🚀 Analyze Contract";
      setNav("Ready", false);
      return;
    }

    // Show pipeline
    $("#upload-section").style.display = "none";
    pipelineSec.style.display = "block";
    pipelineSec.classList.add("fade-in");
    resetPipeline();
    setNav("Analyzing...", true);

    // SSE
    const source = new EventSource(`/api/analyze/${contractId}`);
    let finalData = null;

    source.onmessage = (e) => {
      const evt = JSON.parse(e.data);

      if (evt.type === "agent_update") {
        updateAgent(evt.agent, evt.status, evt.data);
      } else if (evt.type === "pipeline_complete") {
        finalData = evt.data;
      } else if (evt.type === "error") {
        addLog("system", "error", evt.message);
      } else if (evt.type === "stream_end") {
        source.close();
        if (finalData) showResults(finalData);
        setNav("Complete", false);
      }
    };

    source.onerror = () => {
      source.close();
      if (finalData) showResults(finalData);
      else setNav("Connection lost", false);
    };
  });

  // ── Pipeline helpers ─────────────────────────────────────
  function resetPipeline() {
    $$(".agent-node").forEach((n) => {
      n.className = "agent-node";
      n.querySelector(".agent-status").textContent = "Pending";
    });
    $$(".pipeline-connector").forEach((c) => c.classList.remove("active"));
    agentLog.innerHTML = "";
  }

  const AGENT_NAMES = {
    ingestion: "Ingestion",
    understanding: "Understanding",
    extraction: "Extraction",
    risk: "Risk Analysis",
    summary: "Summary",
  };

  const AGENT_ORDER = ["ingestion", "understanding", "extraction", "risk", "summary"];

  function updateAgent(agent, status, data) {
    const node = $(`.agent-node[data-agent="${agent}"]`);
    if (!node) return;

    node.className = `agent-node ${status}`;
    const statusEl = node.querySelector(".agent-status");

    if (status === "working") {
      statusEl.textContent = "Working...";
      addLog(agent, "working", typeof data === "string" ? data : "Processing...");
    } else if (status === "complete") {
      statusEl.textContent = "Done ✓";
      const msg = typeof data === "object" ? data.summary || "Complete" : data;
      addLog(agent, "complete", msg);
      // Activate connector after this agent
      const idx = AGENT_ORDER.indexOf(agent);
      if (idx >= 0) {
        const connectors = $$(".pipeline-connector");
        if (connectors[idx]) connectors[idx].classList.add("active");
      }
    } else if (status === "error") {
      statusEl.textContent = "Error ✗";
      addLog(agent, "error", typeof data === "string" ? data : "Error");
    }
  }

  function addLog(agent, status, msg) {
    const time = new Date().toLocaleTimeString("en-US", { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" });
    const name = AGENT_NAMES[agent] || agent;
    const div = document.createElement("div");
    div.className = `log-entry ${status}`;
    div.innerHTML = `<span class="log-time">${time}</span><span class="log-agent">${name}</span><span class="log-msg">${escapeHtml(msg)}</span>`;
    agentLog.appendChild(div);
    agentLog.scrollTop = agentLog.scrollHeight;
  }

  function setNav(text, active) {
    navStatus.textContent = text;
    navStatus.className = active ? "nav-status active" : "nav-status";
  }

  // ── Render Results ───────────────────────────────────────
  function showResults(data) {
    resultsSec.style.display = "block";
    resultsSec.classList.add("fade-in");

    const summary = data.summary || {};
    const risks = data.risks || {};
    const clauses = data.clauses || {};
    const understanding = data.understanding || {};

    // KPIs
    const score = summary.risk_score ?? risks.overall_risk_score ?? "—";
    const rating = (summary.risk_rating || risks.overall_rating || "—").toUpperCase();
    $("#kpi-risk-value").textContent = score;
    const badge = $("#kpi-risk-badge");
    badge.textContent = rating;
    badge.className = `kpi-badge ${rating.toLowerCase()}`;

    $("#kpi-clauses").textContent = (clauses.clauses || []).length;
    $("#kpi-risks").textContent = (risks.risks || []).length;
    const rec = summary.approval_recommendation || "—";
    const recEl = $("#kpi-recommendation");
    recEl.textContent = rec.replace(/_/g, " ");
    if (rec.includes("NOT")) recEl.style.color = "var(--red)";
    else if (rec.includes("CHANGE")) recEl.style.color = "var(--amber)";
    else recEl.style.color = "var(--green)";

    // Color the risk KPI card border
    const riskCard = $("#kpi-risk");
    if (score >= 70) riskCard.style.borderColor = "var(--red)";
    else if (score >= 40) riskCard.style.borderColor = "var(--amber)";
    else riskCard.style.borderColor = "var(--green)";

    // Executive Summary
    $("#summary-body").innerHTML = `<p>${escapeHtml(summary.executive_summary || "No summary available.")}</p>`;

    // Top Concerns
    const concerns = summary.top_concerns || [];
    $("#concerns-body").innerHTML = concerns.length
      ? concerns.map((c) => `<div class="concern-item"><div class="concern-severity ${(c.severity || "medium").toLowerCase()}"></div><div><div class="concern-text">${escapeHtml(c.concern)}</div><div class="concern-action">→ ${escapeHtml(c.action || "")}</div></div></div>`).join("")
      : "<p>No major concerns identified.</p>";

    // Risk breakdown
    const riskItems = risks.risks || [];
    $("#risks-body").innerHTML = riskItems.length
      ? riskItems.map((r) => `<div class="risk-item"><div class="risk-severity ${(r.severity || "medium").toLowerCase()}">${escapeHtml(r.severity || "?")}</div><div class="risk-details"><h4>${escapeHtml(r.clause_title || "Clause")}</h4><p>${escapeHtml(r.issue || "")}</p><p>${escapeHtml(r.explanation || "")}</p><p class="rec">💡 ${escapeHtml(r.recommendation || "")}</p></div></div>`).join("")
      : "<p>No risks identified.</p>";

    // Clauses
    const clauseList = clauses.clauses || [];
    $("#clauses-body").innerHTML = clauseList.length
      ? clauseList.map((c) => `<div class="clause-item"><div class="clause-header"><span class="clause-section">§ ${escapeHtml(c.section || "?")}</span><span class="clause-category">${escapeHtml(c.category || "")}</span><span class="clause-title">${escapeHtml(c.title || "")}</span></div><div class="clause-summary">${escapeHtml(c.summary || "")}</div></div>`).join("")
      : "<p>No clauses extracted.</p>";

    // Actions
    const actions = summary.recommended_actions || [];
    const nego = summary.negotiation_points || [];
    let actionsHtml = "";
    if (actions.length) {
      actionsHtml += "<h4 style='margin-bottom:0.5rem;color:var(--text-primary)'>Action Items</h4>";
      actionsHtml += actions.map((a) => `<div class="action-item"><span class="action-bullet">→</span><span>${escapeHtml(a)}</span></div>`).join("");
    }
    if (nego.length) {
      actionsHtml += "<h4 style='margin:1rem 0 0.5rem;color:var(--text-primary)'>Negotiation Points</h4>";
      actionsHtml += nego.map((n) => `<div class="action-item"><span class="action-bullet">⚡</span><span>${escapeHtml(n)}</span></div>`).join("");
    }
    $("#actions-body").innerHTML = actionsHtml || "<p>No actions recommended.</p>";

    // Document info
    const parties = understanding.parties || [];
    const sections = understanding.structure || [];
    $("#doc-body").innerHTML = `<dl class="doc-meta">
      <dt>Type</dt><dd>${escapeHtml(understanding.document_type || "—")}</dd>
      <dt>Title</dt><dd>${escapeHtml(understanding.title || "—")}</dd>
      <dt>Parties</dt><dd>${parties.map((p) => escapeHtml(p.name + " (" + p.role + ")")).join(", ") || "—"}</dd>
      <dt>Effective Date</dt><dd>${escapeHtml(understanding.effective_date || "—")}</dd>
      <dt>Expiration</dt><dd>${escapeHtml(understanding.expiration_date || "—")}</dd>
      <dt>Governing Law</dt><dd>${escapeHtml(understanding.governing_law || "—")}</dd>
      <dt>Sections</dt><dd>${sections.length} sections identified</dd>
    </dl>`;
  }

  // ── New analysis ─────────────────────────────────────────
  btnNew.addEventListener("click", () => {
    resultsSec.style.display = "none";
    pipelineSec.style.display = "none";
    $("#upload-section").style.display = "block";
    fileInfo.style.display = "none";
    btnAnalyze.disabled = false;
    btnAnalyze.textContent = "🚀 Analyze Contract";
    selectedFile = null;
    fileInput.value = "";
    setNav("Ready", false);
  });

  // ── Utils ────────────────────────────────────────────────
  function escapeHtml(s) {
    if (typeof s !== "string") s = String(s);
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }
})();
