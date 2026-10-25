# Multimodal Construction Intelligence Platform

**Skill Wallet Capstone Project 1** — Streamlit app for construction safety triage, crack diagnostics, project planning, and weather-aware site guidance.

## Features
- **Site Safety & PPE Audit:** JPG/PNG upload, structured JSON, PPE checklist, safety score, hazards, severity and corrective actions.
- **Crack Diagnostics:** Defect classification, cautious crack-width estimate only when a scale is visible, possible causes, urgency and engineer follow-up.
- **Planning & Valuation:** Interactive structure, area, location tier, completion, cost and material assumptions; indicative budget, CapEx, asset-value proxy, steel and cement estimates.
- **Daily Site Assistant:** Weather-specific checklists and multi-turn Gemini chat.
- **Demo mode:** Works without an API key using explicitly labelled sample outputs.
- No external database; results and chat remain in Streamlit session state.

## Local setup
Python 3.10+ recommended.

    git clone https://github.com/Devansh51111/Multimodal-Construction-Intelligence-Platform.git
    cd Multimodal-Construction-Intelligence-Platform
    python -m venv .venv
    pip install -r requirements.txt
    streamlit run app.py

For live AI, paste a Google Gemini API key into the sidebar or set GEMINI_API_KEY in your environment. Local Streamlit secrets can be configured in .streamlit/secrets.toml. Never commit a real key. Default model: gemini-2.5-flash.

## Deploy on Streamlit Community Cloud
1. Create a new app and select this repository, branch main, and app.py.
2. In app settings → Secrets, add a valid TOML entry for GEMINI_API_KEY (a quoted API key value).
3. Deploy. Without a key the app uses demonstration mode.

## Important limitations
- AI outputs are advisory, not a certified OSHA audit, legal compliance determination, structural diagnosis, or engineering sign-off. Photos cannot reliably establish hidden PPE, crack width without scale, structural capacity, or site-wide conditions.
- IS 456 is a concrete design code, not a PPE standard.
- Costs, asset values and quantities are rough planning proxies. Validate using local quotes, approved drawings, BOQs and qualified professional advice.
- Concept rendering uses an external Pollinations service; availability and data practices are outside this app's control.
- Gemini usage may incur charges and is subject to Google's terms and quotas.
