import streamlit as st
import os
import sys
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle)

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Sustainability Supplier Readiness",
    page_icon="🌍",
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
        <h1>🌱 Sustainability Supplier Diagnostic </h1>
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
        "Micro",
        "Small",
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
st.markdown("## 🌱 Sustainability Supplier Readiness (CSRD Friendly)")
st.caption("CSRD-aligned readiness diagnostic for SME and supply chain suppliers · Beta")

with st.expander("ℹ️ About this tool", expanded=False):
    st.markdown(""" This Sustainability Readiness tool is a fast, decision-grade diagnostic designed to help SME and supplier companies understand whether
they are prepared for current sustainability, human rights, and climate-related reporting expectations — especially under the EU Corporate
Sustainability Reporting Directive (CSRD).

Rather than asking suppliers to "do everything," the tool focuses on what actually matters: data availability, governance maturity, risk exposure, and the ability to meet near-term disclosure and due-[...]

The output is a clear, comparable readiness profile that highlights gaps, flags material risks, and distinguishes between suppliers who need support, monitoring, or escalation.

Built for real supply chains (not idealized ones), the tool is practical, proportionate, and globally usable.

This product can also serve to screen supplier readiness to be onboarded to buyer platforms, identify weak points for triage before risk is metabolized, and prioritize next steps for investment of res[...]  

Additional Notes:
- No legal interpretation required from the supplier  
- Aligned to what buyers actually screen for first under CSRD / HRDD  
- Safe for Global South and SME suppliers  

Disclaimer: This is a decision support tool. It is not meant to be legal advice, or a final compliance/reporting determination.

""")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ════════════════════════════════════════════════
#  INTAKE FORM
# ════════════════════════════════════════════════
st.markdown("### Supplier Intake")

SECTIONS = {
    "👥 Company Profile": list(INTAKE_QUESTIONS.items())[:5],
    "⛓️ Supply Chain & Risk": list(INTAKE_QUESTIONS.items())[5:10],
    "🔍 Buyer Signals": list(INTAKE_QUESTIONS.items())[10:14],
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

    # ── PDF Export ─────────────────────────────────────────────────────────
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("### Export Report")

    def build_pdf():
        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=2 * cm, rightMargin=2 * cm,
            topMargin=2 * cm, bottomMargin=2 * cm,
        )

        # ── Colour palette (yellow & grey on white) ─────────────────────
        yellow    = colors.HexColor("#f5c518")
        dark_grey = colors.HexColor("#1a1a1a")
        mid_grey  = colors.HexColor("#4b5563")
        grey_text = colors.HexColor("#6b7280")
        light_grey = colors.HexColor("#9ca3af")
        grey_line = colors.HexColor("#e5e7eb")
        white     = colors.white
        off_white = colors.HexColor("#f9f9f7")
        tag_bg    = colors.HexColor("#fef9e7")
        tag_fg    = colors.HexColor("#92400e")

        band_colors = {
            "LOW":    (colors.HexColor("#d1fae5"), colors.HexColor("#065f46")),
            "MEDIUM": (colors.HexColor("#fef3c7"), colors.HexColor("#92400e")),
            "HIGH":   (colors.HexColor("#fee2e2"), colors.HexColor("#991b1b")),
        }

        styles = getSampleStyleSheet()
        story  = []

        title_style = ParagraphStyle(
            "T", parent=styles["Title"],
            textColor=dark_grey, fontSize=20, spaceAfter=4,
            fontName="Helvetica-Bold",
        )
        subtitle_style = ParagraphStyle(
            "Sub", parent=styles["Normal"],
            textColor=grey_text, fontSize=9, spaceAfter=12,
        )
        h2_style = ParagraphStyle(
            "H2", parent=styles["Heading2"],
            textColor=dark_grey, fontSize=13, spaceAfter=6,
            fontName="Helvetica-Bold",
        )
        body_style = ParagraphStyle(
            "B", parent=styles["Normal"],
            textColor=mid_grey, fontSize=10, spaceAfter=4,
        )
        label_style = ParagraphStyle(
            "L", parent=styles["Normal"],
            textColor=light_grey, fontSize=8,
            spaceAfter=2,
        )
        big_value_style = ParagraphStyle(
            "BV", parent=styles["Normal"],
            textColor=dark_grey, fontSize=22, spaceAfter=4,
            fontName="Helvetica-Bold",
        )

        # ── Title ─────────────────────────────────────────────────────────
        story.append(Paragraph(
            "Sustainability Supplier Readiness Report", title_style))
        story.append(Paragraph(
            "CSRD-aligned readiness diagnostic for SME and supply chain suppliers",
            subtitle_style))

        # ── Divider ───────────────────────────────────────────────────────
        divider = Table([[""]],
            colWidths=[17 * cm], rowHeights=[1])
        divider.setStyle(TableStyle([
            ("LINEABOVE", (0, 0), (-1, 0), 1, yellow),
            ("TOPPADDING", (0, 0), (-1, 0), 0),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
        ]))
        story.append(Spacer(1, 0.3 * cm))
        story.append(divider)
        story.append(Spacer(1, 0.4 * cm))

        # ── Company profile metadata ──────────────────────────────────────
        n = st.session_state.normalized
        meta = [
            ["Operating region:", n.get("operates_in_eu", "—")],
            ["EU buyer relationship:", n.get("sells_to_eu_buyers", "—")],
            ["Company size:", n.get("company_size", "—")],
            ["Sector:", n.get("sector", "—")],
            ["Value chain role:", n.get("value_chain_role", "—")],
            ["Report date:", datetime.today().strftime("%Y-%m-%d")],
        ]
        mt = Table(meta, colWidths=[5 * cm, 12 * cm])
        mt.setStyle(TableStyle([
            ("TEXTCOLOR",     (0, 0), (0, -1), grey_text),
            ("TEXTCOLOR",     (1, 0), (1, -1), dark_grey),
            ("FONTNAME",      (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME",      (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE",      (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ]))
        story.append(mt)
        story.append(Spacer(1, 0.5 * cm))

        # ── Score & Band cards (side by side) ─────────────────────────────
        band_bg, band_fg = band_colors.get(band, (grey_line, dark_grey))

        score_cell = [
            Paragraph("READINESS SCORE", label_style),
            Paragraph(f'{score} <font size="12" color="#9ca3af">/ 10</font>',
                      big_value_style),
        ]

        band_cell_content = [
            Paragraph("RISK BAND", label_style),
            Paragraph(band, ParagraphStyle(
                "bandval", parent=styles["Normal"],
                textColor=dark_grey, fontSize=18, spaceAfter=4,
                fontName="Helvetica-Bold",
            )),
        ]
        # Band badge as a small colored table
        badge_table = Table(
            [[Paragraph(band_desc, ParagraphStyle(
                "badge", fontSize=8, textColor=band_fg,
                fontName="Helvetica-Bold",
            ))]],
            colWidths=[7.5 * cm],
        )
        badge_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), band_bg),
            ("ROUNDEDCORNERS", [6, 6, 6, 6]),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ]))
        band_cell_content.append(badge_table)

        cards = Table(
            [[score_cell, band_cell_content]],
            colWidths=[8 * cm, 9 * cm],
        )
        cards.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), off_white),
            ("BOX",           (0, 0), (0, 0),   1, yellow),
            ("BOX",           (1, 0), (1, 0),   1, yellow),
            ("ROUNDEDCORNERS", [8, 8, 8, 8]),
            ("TOPPADDING",    (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("LEFTPADDING",   (0, 0), (-1, -1), 14),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(cards)
        story.append(Spacer(1, 0.5 * cm))

        # ── Diagnostic Tags ───────────────────────────────────────────────
        if tags:
            story.append(Paragraph(
                "<b>Applied diagnostic tags:</b>", body_style))
            tag_cells = []
            for t in tags:
                tag_cells.append(Paragraph(
                    t, ParagraphStyle(
                        "tag", fontSize=8, textColor=tag_fg,
                        fontName="Helvetica-Bold",
                    )))
            tag_table = Table(
                [tag_cells],
                colWidths=[len(t) * 0.18 * cm + 1.2 * cm for t in tags],
            )
            tag_style_cmds = [
                ("BACKGROUND",    (0, 0), (-1, -1), tag_bg),
                ("TOPPADDING",    (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING",   (0, 0), (-1, -1), 8),
                ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
                ("ROUNDEDCORNERS", [10, 10, 10, 10]),
                ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ]
            tag_table.setStyle(TableStyle(tag_style_cmds))
            story.append(Spacer(1, 0.15 * cm))
            story.append(tag_table)
            story.append(Spacer(1, 0.5 * cm))

        # ── Recommendations ───────────────────────────────────────────────
        if why:
            story.append(Paragraph("<b>Recommendations:</b>", body_style))
            story.append(Spacer(1, 0.15 * cm))
            for item in why:
                rec_table = Table(
                    [[Paragraph(
                        f"\u0020\u0020{item}",
                        ParagraphStyle("rec", fontSize=9,
                                       textColor=mid_grey),
                    )]],
                    colWidths=[16.5 * cm],
                )
                rec_table.setStyle(TableStyle([
                    ("BACKGROUND",    (0, 0), (-1, -1), off_white),
                    ("BOX",           (0, 0), (-1, -1), 0.5, grey_line),
                    ("LINEBEFOREDECOR", (0, 0), (0, -1), 3, yellow),
                    ("TOPPADDING",    (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING",   (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
                ]))
                story.append(rec_table)
                story.append(Spacer(1, 0.15 * cm))
            story.append(Spacer(1, 0.3 * cm))

        # ── Sector baseline assumptions ───────────────────────────────────
        sector_val = n.get("sector")
        if sector_val and sector_val in SECTOR_BASELINE_ASSUMPTIONS:
            story.append(Paragraph(
                f"<b>Sector baseline: {sector_val}</b>", body_style))
            story.append(Spacer(1, 0.1 * cm))
            for assumption in SECTOR_BASELINE_ASSUMPTIONS[sector_val]:
                story.append(Paragraph(
                    f"\u2022  {assumption}",
                    ParagraphStyle("assumption", fontSize=9,
                                   textColor=colors.HexColor("#4b5563"),
                                   leftIndent=10, spaceAfter=3),
                ))
            story.append(Spacer(1, 0.4 * cm))

        # ── Intake answers breakdown ──────────────────────────────────────
        story.append(Paragraph("Intake Response Summary", h2_style))
        story.append(Spacer(1, 0.1 * cm))
        ans_data = [["Question", "Answer"]]
        for question_text, answer in st.session_state.answers.items():
            q_short = (question_text[:70] + "\u2026") if len(question_text) > 70 else question_text
            ans_data.append([
                Paragraph(q_short, ParagraphStyle("qcell", fontSize=8,
                          textColor=mid_grey)),
                Paragraph(str(answer), ParagraphStyle("acell", fontSize=8,
                          textColor=dark_grey, fontName="Helvetica-Bold")),
            ])
        ans_table = Table(ans_data, colWidths=[9.5 * cm, 7.5 * cm])
        ans_table.setStyle(TableStyle([
            ("BACKGROUND",     (0, 0), (-1, 0),  yellow),
            ("TEXTCOLOR",      (0, 0), (-1, 0),  dark_grey),
            ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",       (0, 0), (-1, 0),  9),
            ("BACKGROUND",     (0, 1), (-1, -1), white),
            ("GRID",           (0, 0), (-1, -1), 0.5, grey_line),
            ("VALIGN",         (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",     (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, off_white]),
        ]))
        story.append(ans_table)
        story.append(Spacer(1, 0.5 * cm))

        # ── Divider before footer ─────────────────────────────────────────
        story.append(divider)
        story.append(Spacer(1, 0.3 * cm))

        # ── Disclaimer / Footer ───────────────────────────────────────────
        disclaimer_style = ParagraphStyle(
            "FT", parent=styles["Normal"],
            textColor=grey_text,
            fontSize=8, spaceAfter=2,
        )
        story.append(Paragraph(
            "<b>Disclaimer:</b> This is a decision support tool. "
            "It is not meant to be legal advice, or a final "
            "compliance/reporting determination.",
            disclaimer_style,
        ))
        story.append(Spacer(1, 0.15 * cm))
        story.append(Paragraph(
            f"Generated by Sustainability Supplier Readiness Tool "
            f"\u2022 {datetime.today().strftime('%Y-%m-%d')}",
            ParagraphStyle("gen", fontSize=7,
                           textColor=colors.HexColor("#9ca3af")),
        ))

        doc.build(story)
        buf.seek(0)
        return buf

    pdf_data = build_pdf()
    sector_val = st.session_state.normalized.get("sector", "report")
    fname = (
        f"Sustainability_Readiness_"
        f"{sector_val.replace(' ', '_').replace('/', '_')[:30]}_"
        f"{datetime.today().strftime('%Y%m%d')}.pdf"
    )
    st.download_button(
        "📄 Download PDF Report",
        data=pdf_data,
        file_name=fname,
        mime="application/pdf",
    )
