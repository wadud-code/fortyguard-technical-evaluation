
# FortyGuard Technical Product Evaluation (Dashboard, API & MCP)

**Evaluator:** Abdul Wadud  
**Test Case:** Urban Heat Island (UHI) Analysis — Hialeah / Miami, FL (`25.873, -80.252`)  
**Environment:** WSL2 (Ubuntu), Python 3 (`requests`), Cursor IDE (`fortyguard-mcp`)

---

## 1. Executive Summary
This repository documents an end-to-end technical evaluation across FortyGuard's three core interfaces: the **Web Dashboard + Selesious**, the **REST Heatmap API**, and the **Model Context Protocol (MCP) Server**. All three layers successfully returned high-resolution thermal and environmental data for the Hialeah/Miami corridor, with specific developer-experience (DX) and UI observations noted below.

---

## 2. Product Findings & Friction Log

### A. FortyGuard Dashboard & Selesious
* **What Worked Well:** Rapid spatial rendering of localized thermal hotspots across industrial and residential blocks in Hialeah/Miami (`25.873, -80.252`), paired with natural-language querying via Selesious.
* **UI/UX Observations:**
  1. **Active Date Visibility:** The selected historical/forecast timestamp is not persistently pinned in the primary map header, making it easy to lose temporal context while zooming.
  2. **Export Workflow:** Exporting raw tabular/GeoJSON slices directly from an active polygon selection requires extra navigation steps compared to an inline one-click export action.

![Dashboard Heatmap](screenshots/01_dashboard.png)

### B. REST Heatmap API (`test_fortyguard_api.py`)
* **Integration Flow:** Authenticated via `FORTYGUARD_API_KEY`, submitted a polygon request for Hialeah/Miami, polled the asynchronous `activity_id` until completion, and persisted the output to `miami_heatmap_result.json` (area average: `18.6°C`).
* **Developer Experience (DX) Finding:**
  * Initial requests using `filter_type: 3` returned an `HTTP 422 Unprocessable Entity` error when `date_time` was omitted. Making `date_time` validation explicit in the quickstart payload examples for `filter_type: 3` will prevent integration friction.

![API Terminal Run](screenshots/02_api_terminal.png)

### C. Model Context Protocol (`fortyguard-mcp` in Cursor)
* **Integration Flow:** Configured `fortyguard` inside Cursor (`WSL: Ubuntu`), verified authentication and credit balance (`995,780` credits via `credit_balance`), and tested `env_params` tool schema discovery and execution.
* **Developer Experience (DX) Finding:**
  * Remote HTTP MCP connections inside WSL2 occasionally encounter `fetch failed` / client transport errors; running the local `fortyguard-mcp` stdio binary resolves transport drops cleanly. Including a copy-paste WSL/Linux `stdio` snippet in the MCP setup docs will streamline onboarding.

![Cursor MCP Integration](screenshots/03_mcp_cursor.png)

---

## 3. Reproducibility
```bash
export FORTYGUARD_API_KEY="your_api_key_here"
python3 test_fortyguard_api.py
