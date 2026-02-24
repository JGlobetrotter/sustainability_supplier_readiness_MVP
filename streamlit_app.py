import streamlit as st
import os
import sys

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Supplier Sustainability Screener",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: #f4f1ec;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Password screen */
.password-card {
    background: #fff;
    border-radius: 16px;
    padding: 3rem 2.5rem;
    max-width: 420px;
    margin: 8vh auto 0;
    box-shadow: 0 4px 32px rgba(0,0,0,0.08);
    text-align: center;
}
.password-card h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #1a1a2e;
    margin-bottom: 0.25rem;
}
.password-card p {
    color: #6b7280;
    font-size: 0.92rem;
    margin-bottom: 2rem;
}

/* Section headers */
h1, h2, h3 {
    font-family: 'DM Serif Display', serif !important;
    color: #1a1a2e !important;
}

/* Metric cards */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-card {
    flex: 1;
    background: #fff;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.metric-card .label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 0.4rem;
}
.metric-card .value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #1a1a2e;
    line-height: 1;
}

/* Band badge */
.band-low    { background: #d1fae5; color: #065f46; }
.band-medium { background: #fef3c7; color: #92400e; }
.band-high   { background: #fee2e2; color: #991b1b; }
.band-badge {
    display: inline-block;
    padding: 0.45rem 1.1rem;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

/* Tag pills */
.tag-pill {
    display: inline-block;
    background: #e0e7ff;
    color: #3730a3;
    border-radius: 999px;
    padding: 0.25rem 0.75rem;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 0.2rem 0.2rem 0.2rem 0;
}

/* Why list */
.why-item {
    background: #fff;
    border-left: 3px solid #6366f1;
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.93rem;
    color: #374151;
}

/* Assumption box */
.assumption-box {
    background: #fff;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    border: 1px solid #e5e7eb;
    font-size: 0.88rem;
    color: #4b5563;
    margin-top: 0.5rem;
}
.assumption-box li { margin-bottom: 0.4rem; }

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 2rem 0;
}

/* Selectbox label override */
.stSelectbox label {
    font-weight: 500 !important;
    color: #374151 !important;
}

/* Button */
.stButton > button {
    background: #1a1a2e !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
#  PASSWORD GATE
# ════════════════════════════════════════════════
PASSWORD = "betastream"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <div class="password-card">
        <h1>🌿 ESG Screener</h1>
        <p>Supplier Sustainability Readiness Tool — Beta</p>
    </div>
    """, unsafe_allow_html=True)
    pwd = st.text_input("Enter access password", type="password", label_visibility="collapsed",
                        placeholder="Enter password…")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Enter →", use_container_width=True):
            if pwd == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    st.stop()

# ════════════════════════════════════════════════
#  DATA — embedded so the app is fully standalone
# ════════════════════════════════════════════════

QUESTION_TO_KEY = {
    "Where is your company primarily operating?": "operates_in_eu",
    "Do you sell directly or indirectly to EU-based companies or investors?": "sells_to_eu_buyers",
    "What best describes your company size?": "company_size",
    "Which sector best fits your operations?": "sector",
    "Which best describes your role in the value chain today?": "value_chain_role",
    "How complex is your supply chain?": "supply_chain_complexity",
    "Do your operations or sourcing occur in regions commonly considered higher risk for labor or human-rights issues?": "hr_risk_region",
    "Are labor conditions a material issue in your operations or sourcing?": "labor_material",
    "Have buyers or partners asked you about environmental or climate-related topics?": "env_asked",
    "Which environmental topics have buyers mentioned or asked about? (Select all that apply)?": "env_topics",
    "Have buyers or partners recently requested ESG, sustainability, or human-rights information?": "recent_esg_requests",
    "Have you been asked to complete questionnaires or provide information that feels new or more detailed than in the past?": "more_detailed_requests",
    "What do you think prompted these requests?": "request_driver",
    "Have any buyers or partners mentioned CSRD, EU sustainability reporting, or new EU sustainability laws when requesting information from you?": "csrd_mentioned",
    "Who is primarily responsible for sustainability or social impact topics internally?": "internal_owner",
    "Do you have written policies related to the environment, sustainability and labor?": "policy_status",
    "Do you currently track any sustainability or social data?": "data_tracking",
    "How confident do you feel responding to buyer ESG, sustainability or human rights requests?": "confidence",
}

INTAKE_QUESTIONS = {
    "Where is your company primarily operating?": [
        "— select —",
        "EU",
        "Non-EU",
        "Both EU and Non-EU",
    ],
    "Do you sell directly or indirectly to EU-based companies or investors?": [
        "— select —",
        "Yes, directly",
        "Yes, indirectly",
        "No",
        "Unsure",
    ],
    "What best describes your company size?": [
        "— select —",
        "Micro (< 10 employees)",
        "Small (10–49)",
        "Medium",
        "Large",
    ],
    "Which sector best fits your operations?": [
        "— select —",
        "Manufacturing (components / sub-assemblies)",
        "Processing / transformation (e.g. food, materials)",
        "Agriculture / farming",
        "Forestry / timber",
        "Fisheries / aquaculture",
        "Mining / extractives",
        "Construction / infrastructure",
        "Logistics / transport (road, sea, air)",
        "Warehousing / distribution",
        "Energy production or supply",
        "Waste management / recycling",
        "Chemicals / industrial inputs",
        "Textiles / apparel / footwear",
        "Electronics / electrical equipment",
        "Packaging / materials",
        "IT / digital services",
        "Professional services",
        "Facilities management / cleaning / security",
        "Other services",
    ],
    "Which best describes your role in the value chain today?": [
        "— select —",
        "Primarily a supplier to other companies",
        "Primarily a manufacturer selling finished goods",
        "Both supplier and direct-to-market",
        "Service provider",
    ],
    "How complex is your supply chain?": [
        "— select —",
        "Simple / direct sourcing",
        "Some multi-tiering",
        "Highly multi-tiered",
        "Unsure",
    ],
    "Do your operations or sourcing occur in regions commonly considered higher risk for labor or human-rights issues?": [
        "— select —",
        "Yes",
        "No",
        "Partially",
        "Unsure",
    ],
    "Are labor conditions a material issue in your operations or sourcing?": [
        "— select —",
        "Yes",
        "No",
        "Somewhat",
        "Unsure",
    ],
    "Have buyers or partners asked you about environmental or climate-related topics?": [
        "— select —",
        "Yes",
        "No",
        "Unsure",
    ],
    "Which environmental topics have buyers mentioned or asked about? (Select all that apply)?": [
        "— select —",
        "Carbon / GHG emissions",
        "Energy use",
        "Water use",
        "Biodiversity",
        "Waste",
        "Not specified / unclear",
        "None asked",
    ],
    "Have buyers or partners recently requested ESG, sustainability, or human-rights information?": [
        "— select —",
        "Yes",
        "No",
        "Unsure",
    ],
    "Have you been asked to complete questionnaires or provide information that feels new or more detailed than in the past?": [
        "— select —",
        "Yes, significantly more detailed",
        "Yes, somewhat",
        "No",
        "Not applicable",
    ],
    "What do you think prompted these requests?": [
        "— select —",
        "New EU regulations (e.g. CSRD)",
        "Buyer internal policy",
        "Unclear / not explained",
        "Customer ESG programme",
        "Other",
    ],
    "Have any buyers or partners mentioned CSRD, EU sustainability reporting, or new EU sustainability laws when requesting information from you?": [
        "— select —",
        "Yes, explicitly",
        'Yes, indirectly (e.g. "new EU requirements")',
        "No",
        "Unsure",
    ],
    "Who is primarily responsible for sustainability or social impact topics internally?": [
        "— select —",
        "Dedicated sustainability / ESG role",
        "Shared / part-time responsibility",
        "Senior leadership only",
        "No clear owner",
    ],
    "Do you have written policies related to the environment, sustainability and labor?": [
        "— select —",
        "Yes, comprehensive",
        "Yes, partial",
        "In development",
        "No",
    ],
    "Do you currently track any sustainability or social data?": [
        "— select —",
        "Yes, systematically",
        "Yes, partially",
        "Informal / ad hoc",
        "No",
    ],
    "How confident do you feel responding to buyer ESG, sustainability or human rights requests?": [
        "— select —",
        "Very confident",
        "Somewhat confident",
        "Not very confident",
        "Not confident",
    ],
}

SECTOR_BASELINE_ASSUMPTIONS = {
    "Manufacturing (components / sub-assemblies)": [
        "Environmental data often exists (energy, waste) but is inconsistent and not audit-ready.",
        "Human rights due diligence is typically weak beyond Tier 1 labor.",
        "Climate transition planning is uncommon unless driven by major customers.",
    ],
    "Processing / transformation (e.g. food, materials)": [
        "Traceability is partial and upstream risks are not fully understood.",
        "Certifications may exist but are not aligned to CSRD materiality.",
        "High exposure to water, waste, and labor risks.",
    ],
    "Agriculture / farming": [
        "Formal sustainability reporting is generally very limited.",
        "Data is seasonal, estimated, or proxy-based.",
        "High biodiversity and labor risks with weak documentation.",
    ],
    "Forestry / timber": [
        "Chain-of-custody claims may exist but are unevenly verified.",
        "Biodiversity impacts are under-measured.",
        "Land tenure and Indigenous rights risks are often weakly governed.",
    ],
    "Fisheries / aquaculture": [
        "Traceability and data maturity are low.",
        "Labor risks can be significant and poorly documented.",
        "Environmental impacts are rarely evidenced.",
    ],
    "Mining / extractives": [
        "Environmental and safety reporting is usually strong internally.",
        "Community and grievance systems are uneven.",
        "Downstream and contractor risks are poorly controlled.",
    ],
    "Construction / infrastructure": [
        "Safety data exists, but environmental data is fragmented.",
        "Subcontractor oversight is weak.",
        "Temporary labor complicates due diligence.",
    ],
    "Logistics / transport (road, sea, air)": [
        "Fuel and emissions data exists at a high level only.",
        "Data granularity is often insufficient for CSRD.",
        "Labor risk varies widely by subcontracting depth.",
    ],
    "Warehousing / distribution": [
        "Basic energy data may exist.",
        "Labor standards vary widely.",
        "Temporary workforce risks are often overlooked.",
    ],
    "Energy production or supply": [
        "Strong regulatory and climate reporting exists.",
        "Transition risk is material.",
        "Social and biodiversity risks are under-integrated.",
    ],
    "Waste management / recycling": [
        "Environmental metrics are tracked.",
        "Downstream leakage is difficult to verify.",
        "Circularity claims often exceed evidence.",
    ],
    "Chemicals / industrial inputs": [
        "Strong compliance culture exists.",
        "Transparency rarely extends beyond minimum requirements.",
        "Downstream impacts are weakly assessed.",
    ],
    "Textiles / apparel / footwear": [
        "High audit familiarity but persistent labor risks.",
        "Traceability beyond Tier 1 is weak.",
        "Audit fatigue is common.",
    ],
    "Electronics / electrical equipment": [
        "Product compliance is strong.",
        "Supply chain traceability beyond Tier 1 is weak.",
        "Mineral sourcing risks persist.",
    ],
    "Packaging / materials": [
        "Material data exists.",
        "Circularity performance is often overstated.",
        "End-of-life outcomes are poorly evidenced.",
    ],
    "IT / digital services": [
        "Low awareness of CSRD relevance.",
        "Environmental impact is treated as indirect.",
        "Energy use from data centers is often overlooked.",
    ],
    "Professional services": [
        "Sustainability maturity is low.",
        "Workforce metrics are under-measured.",
        "Often excluded from supplier programs.",
    ],
    "Facilities management / cleaning / security": [
        "High labor risk and thin margins.",
        "Documentation is weak.",
        "Subcontracting is common.",
    ],
    "Other services": [
        "Very limited sustainability readiness.",
        "CSRD relevance is unclear to the supplier.",
        "Data is often absent.",
    ],
}

# ════════════════════════════════════════════════
#  LOGIC (self-contained, no external imports)
# ════════════════════════════════════════════════

def normalize_answers(answers: dict) -> dict:
    result = {}
    for question, answer in answers.items():
        key = QUESTION_TO_KEY.get(question)
        if key:
            result[key] = answer
    return result


def derive_tags(a: dict) -> list:
    tags = []

    if a.get("env_topics") == "Not specified / unclear":
        tags.append("BUYER_OPACITY_RISK")
    if a.get("request_driver") == "Unclear / not explained":
        tags.append("BUYER_OPACITY_RISK")
    if "indirectly" in (a.get("csrd_mentioned") or "").lower():
        tags.append("BUYER_OPACITY_RISK")
    if a.get("more_detailed_requests") == "Yes, significantly more detailed":
        tags.append("BUYER_OPACITY_RISK")

    if a.get("hr_risk_region") == "Yes":
        tags.append("HRDD_RELEVANCE_HIGH")
    if a.get("labor_material") in ("Yes", "Somewhat"):
        tags.append("HRDD_RELEVANCE_HIGH")
    if a.get("supply_chain_complexity") == "Highly multi-tiered":
        tags.append("HRDD_RELEVANCE_HIGH")

    if a.get("confidence") == "Not confident":
        tags.append("SUPPLIER_CONFIDENCE_LOW")
    if a.get("internal_owner") == "No clear owner":
        tags.append("SUPPLIER_CONFIDENCE_LOW")
    if a.get("policy_status") == "No":
        tags.append("SUPPLIER_CONFIDENCE_LOW")
    if a.get("data_tracking") in ("Informal / ad hoc", "No"):
        tags.append("SUPPLIER_CONFIDENCE_LOW")

    if "yes" in (a.get("csrd_mentioned") or "").lower():
        tags.append("CSRD_CASCADE_SIGNAL")

    if a.get("policy_status") == "No":
        tags.append("DOCUMENTATION_LIGHT")

    if a.get("env_asked") == "Yes" and a.get("data_tracking") in ("Informal / ad hoc", "No"):
        tags.append("ENVIRONMENTAL_BASELINE_GAP")
    if a.get("env_topics") == "Not specified / unclear":
        tags.append("ENVIRONMENTAL_BASELINE_GAP")

    if a.get("internal_owner") == "No clear owner":
        tags.append("OWNER_GAP")
    if a.get("policy_status") == "No":
        tags.append("OWNER_GAP")

    return tags


SCORE_RULES = [
    ("sells_to_eu_buyers",     ["Yes", "Yes, directly", "Yes, indirectly"],             1),
    ("supply_chain_complexity",["Highly multi-tiered", "Multi-tiered"],                 1),
    ("hr_risk_region",         ["Yes", "Partially"],                                    1),
    ("recent_esg_requests",    ["Yes"],                                                 1),
    ("more_detailed_requests", ["Yes, significantly more detailed", "Yes, somewhat"],   1),
    ("csrd_mentioned",         ["Yes, explicitly",
                                'Yes, indirectly (e.g. "new EU requirements")'],        1),
    ("policy_status",          ["No"],                                                  1),
    ("data_tracking",          ["Informal / ad hoc", "No"],                             1),
    ("internal_owner",         ["No clear owner"],                                      1),
    ("confidence",             ["Not confident", "Not very confident"],                 1),
]

SCORE_BANDS = [
    (0, 3,  "LOW",    "Limited sustainability-driven pressure at this stage."),
    (4, 6,  "MEDIUM", "Some sustainability-driven pressure likely."),
    (7, 10, "HIGH",   "Significant sustainability-driven pressure — action required."),
]

RECOMMENDATION_MAP = {
    "CSRD_CASCADE_SIGNAL":       "CSRD readiness activities strongly recommended.",
    "BUYER_OPACITY_RISK":        "Clients or buyers are expressing conflicting or confusing requests.",
    "HRDD_RELEVANCE_HIGH":       "Human Rights and Labor activity strengthening recommended.",
    "OWNER_GAP":                 "Strengthen responsibility linkages to reporting and compliance.",
    "ENVIRONMENTAL_BASELINE_GAP":"Draft environmental compliance processes to create a baseline.",
    "SUPPLIER_CONFIDENCE_LOW":   "Confidence is low — strongly suggest external advisory or support.",
    "DOCUMENTATION_LIGHT":       "Develop written policies for environment, sustainability and labor.",
}


def run_screening(tags_dict: dict) -> dict:
    # Reconstruct tag list from dict
    tags = [t for t, v in tags_dict.items() if v]

    # Score from normalized answers stored in session state
    a = st.session_state.get("normalized", {})
    score = 0
    for key, matching, pts in SCORE_RULES:
        if a.get(key) in matching:
            score += pts

    band, band_desc = "UNKNOWN", ""
    for lo, hi, b, d in SCORE_BANDS:
        if lo <= score <= hi:
            band, band_desc = b, d

    unique_tags = list(dict.fromkeys(tags))
    why = [RECOMMENDATION_MAP[t] for t in unique_tags if t in RECOMMENDATION_MAP]

    return {
        "score": score,
        "band": band,
        "band_desc": band_desc,
        "why": why,
        "tags": unique_tags,
    }

# ════════════════════════════════════════════════
#  SESSION STATE INIT
# ════════════════════════════════════════════════
for key in ("answers", "results", "applied_tags", "normalized"):
    if key not in st.session_state:
        st.session_state[key] = {} if key in ("answers", "normalized") else ([] if key == "applied_tags" else None)

# ════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════
st.markdown("## 🌿 Supplier Sustainability Screener")
st.caption("CSRD-aligned readiness diagnostic for SME and supply chain suppliers · Beta")

with st.expander("ℹ️ About this tool", expanded=False):
    st.markdown("""
This tool is a fast, decision-grade diagnostic designed to help SME and supplier companies understand
whether they are prepared for current sustainability, human rights, and climate-related reporting
expectations — especially under the EU **Corporate Sustainability Reporting Directive (CSRD)**.

The output is a clear readiness profile that highlights gaps, flags material risks, and distinguishes
between suppliers who need support, monitoring, or escalation.

**Disclaimer:** This is a decision support tool. It is not legal advice or a final compliance determination.
""")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ════════════════════════════════════════════════
#  INTAKE FORM
# ════════════════════════════════════════════════
st.markdown("### Supplier Intake")

SECTIONS = {
    "🏢 Company Profile": list(INTAKE_QUESTIONS.items())[:5],
    "⛓️ Supply Chain & Risk": list(INTAKE_QUESTIONS.items())[5:10],
    "📬 Buyer Signals": list(INTAKE_QUESTIONS.items())[10:14],
    "📋 Internal Readiness": list(INTAKE_QUESTIONS.items())[14:],
}

for section_title, questions in SECTIONS.items():
    st.markdown(f"**{section_title}**")
    for question_text, options in questions:
        answer = st.selectbox(
            question_text,
            options,
            key=f"q::{question_text}",
            index=0,
        )
        st.session_state.answers[question_text] = answer

        # Inline sector assumptions
        if question_text.strip() == "Which sector best fits your operations?" and answer and answer != "— select —":
            assumptions = SECTOR_BASELINE_ASSUMPTIONS.get(answer)
            if assumptions:
                bullet_html = "".join(f"<li>{a}</li>" for a in assumptions)
                st.markdown(
                    f'<div class="assumption-box"><strong>Sector baseline:</strong><ul>{bullet_html}</ul></div>',
                    unsafe_allow_html=True,
                )
    st.markdown("")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ════════════════════════════════════════════════
#  RUN BUTTON
# ════════════════════════════════════════════════
col_btn, _ = st.columns([1, 3])
with col_btn:
    run = st.button("▶ Run screening", use_container_width=True)

if run:
    # Validate: no unanswered questions
    unanswered = [q for q, a in st.session_state.answers.items() if a == "— select —"]
    if unanswered:
        st.warning(f"Please answer all questions before running. ({len(unanswered)} remaining)")
    else:
        normalized = normalize_answers(st.session_state.answers)
        st.session_state.normalized = normalized

        applied_tags = derive_tags(normalized)
        applied_tags = list(dict.fromkeys(applied_tags))
        st.session_state.applied_tags = applied_tags

        tags_dict = {t: True for t in applied_tags}

        try:
            st.session_state.results = run_screening(tags_dict)
        except Exception as e:
            st.session_state.results = None
            st.error("Screening failed.")
            st.exception(e)

# ════════════════════════════════════════════════
#  RESULTS
# ════════════════════════════════════════════════
st.markdown("### Results")

if st.session_state.results is None:
    st.info("Complete the intake form above and click **▶ Run screening** to generate your readiness profile.")
else:
    r = st.session_state.results
    score     = r.get("score", "—")
    band      = r.get("band", "")
    band_desc = r.get("band_desc", "")
    why       = r.get("why", [])
    tags      = r.get("tags", [])

    # Score + Band cards
    band_class = f"band-{band.lower()}" if band in ("LOW", "MEDIUM", "HIGH") else ""
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="label">Readiness Score</div>
            <div class="value">{score}<span style="font-size:1rem;color:#9ca3af"> / 10</span></div>
        </div>
        <div class="metric-card">
            <div class="label">Risk Band</div>
            <div class="value" style="font-size:1.4rem;">{band}</div>
            <span class="band-badge {band_class}">{band_desc}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tags
    if tags:
        st.markdown("**Applied diagnostic tags:**")
        pills = "".join(f'<span class="tag-pill">{t}</span>' for t in tags)
        st.markdown(f'<div style="margin-bottom:1rem">{pills}</div>', unsafe_allow_html=True)

    # Why / recommendations
    if why:
        st.markdown("**Recommendations:**")
        for item in why:
            st.markdown(f'<div class="why-item">💡 {item}</div>', unsafe_allow_html=True)

    # Sector assumptions in results
    sector = st.session_state.normalized.get("sector")
    if sector and sector in SECTOR_BASELINE_ASSUMPTIONS:
        with st.expander(f"📂 Sector baseline: {sector}", expanded=False):
            for assumption in SECTOR_BASELINE_ASSUMPTIONS[sector]:
                st.markdown(f"- {assumption}")

    # Raw JSON for debugging
    with st.expander("🔍 Raw output (debug)", expanded=False):
        st.json(r)
        st.write("Normalized answers:", st.session_state.normalized)
