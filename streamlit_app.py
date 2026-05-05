import streamlit as st
import io
from datetime import datetime
from pathlib import Path
# from jinja2 import Template
# from weasyprint import HTML

── ReportLab 
 from reportlab.lib.pagesizes import A4
 from reportlab.lib.units import cm
 from reportlab.lib import colors
 from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
 from reportlab.platypus import (
     SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
 )

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Supplier Readiness Diagnostic — Navisignal",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap');

/* ── Global fonts & background ────────────────────────────────────────── */
*, html, body {
  font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, section.main {
  background-color: #09090b !important;
}

/* ── Hide Streamlit chrome ──────────────────────────────────────────────── */
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
header[data-testid="stHeader"],
#MainMenu, footer {
  display: none !important;
  visibility: hidden !important;
}

/* ── Block container ────────────────────────────────────────────────────── */
[data-testid="stMainBlockContainer"],
.block-container {
  padding-top: 0 !important;
  padding-bottom: 140px !important;
  max-width: 720px !important;
}

/* ── Widget labels ──────────────────────────────────────────────────────── */
[data-testid="stWidgetLabel"] p,
label[data-testid="stWidgetLabel"] {
  color: #fafafa !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  margin-bottom: 4px !important;
}

/* ── BaseWeb Select — dark ──────────────────────────────────────────────── */
[data-baseweb="select"] > div:first-child {
  background-color: #18181b !important;
  border: 1px solid #27272a !important;
  border-radius: 6px !important;
  box-shadow: none !important;
  transition: border-color 150ms ease;
}
[data-baseweb="select"] > div:first-child:hover {
  border-color: #52525b !important;
}
[data-baseweb="select"] span,
[data-baseweb="select"] div[role="button"] span,
[data-baseweb="select"] > div > div > div {
  color: #fafafa !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 13px !important;
}
[data-baseweb="select"] svg { fill: #71717a !important; }
[data-baseweb="popover"],
[data-baseweb="popover"] > div {
  background-color: #18181b !important;
  border: 1px solid #27272a !important;
  border-radius: 6px !important;
  box-shadow: 0 8px 32px rgba(0,0,0,0.6) !important;
}
[data-baseweb="menu"] { background-color: #18181b !important; }
[data-baseweb="menu"] li,
[data-baseweb="menu"] [role="option"] {
  background-color: #18181b !important;
  color: #fafafa !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 13px !important;
}
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] [role="option"]:hover { background-color: #27272a !important; }
[data-baseweb="menu"] [aria-selected="true"] {
  background-color: rgba(59,130,246,0.12) !important;
  color: #3b82f6 !important;
}

/* ── Text / password input ──────────────────────────────────────────────── */
[data-testid="stTextInput"] input,
input[type="password"] {
  background-color: #18181b !important;
  border: 1px solid #27272a !important;
  border-radius: 6px !important;
  color: #fafafa !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 13px !important;
  padding: 10px 14px !important;
  box-shadow: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #71717a !important; }
[data-testid="stTextInput"] input:focus {
  border-color: #3b82f6 !important;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.25) !important;
  outline: none;
}

/* ── Buttons ────────────────────────────────────────────────────────────── */
.stButton > button {
  background: #3b82f6 !important;
  color: #fff !important;
  border: 1px solid #3b82f6 !important;
  border-radius: 6px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  letter-spacing: 0.02em !important;
  padding: 10px 22px !important;
  cursor: pointer !important;
  transition: background 150ms ease, border-color 150ms ease !important;
}
.stButton > button:hover:not(:disabled) {
  background: #2563eb !important;
  border-color: #2563eb !important;
}
.stButton > button:disabled {
  background: transparent !important;
  color: #71717a !important;
  border-color: #27272a !important;
  cursor: default !important;
}

/* ── Download button ────────────────────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {
  background: #3b82f6 !important;
  color: #fff !important;
  border: 1px solid #3b82f6 !important;
  border-radius: 6px !important;
  font-weight: 700 !important;
  font-size: 13px !important;
}
[data-testid="stDownloadButton"] > button:hover {
  background: #2563eb !important;
  border-color: #2563eb !important;
}

/* ── Checkbox ───────────────────────────────────────────────────────────── */
[data-testid="stCheckbox"] label p,
[data-testid="stCheckbox"] label span {
  color: #a1a1aa !important;
  font-size: 13px !important;
  line-height: 1.5 !important;
}

/* ── Expander ───────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
  border: 1px solid #27272a !important;
  border-radius: 6px !important;
  overflow: hidden;
  background: #18181b !important;
}
[data-testid="stExpander"] details > summary {
  background-color: #18181b !important;
  color: #a1a1aa !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  padding: 10px 14px;
  list-style: none;
}
[data-testid="stExpander"] details[open] > summary { border-radius: 6px 6px 0 0; }
[data-testid="stExpander"] > div > div {
  background-color: #111113 !important;
  border-top: 1px solid #27272a !important;
  padding: 12px 14px;
}
[data-testid="stExpander"] p, [data-testid="stExpander"] li {
  color: #a1a1aa !important;
  font-size: 12px !important;
  line-height: 1.7 !important;
}

/* ── Sidebar ────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background-color: #0d0d0f !important;
  border-right: 1px solid #27272a !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] span {
  color: #a1a1aa !important;
  font-size: 12px !important;
  line-height: 1.7 !important;
}
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] b { color: #fafafa !important; }
[data-testid="stSidebar"] a {
  color: #3b82f6 !important;
  text-decoration: none !important;
  font-weight: 600 !important;
}
[data-testid="stSidebar"] hr { border-color: #27272a !important; }

/* ── HR ─────────────────────────────────────────────────────────────────── */
hr { border: none !important; border-top: 1px solid #27272a !important; margin: 0 !important; }

/* ── Scrollbar ──────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #09090b; }
::-webkit-scrollbar-thumb { background: #27272a; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Constants ─────────────────────────────────────────────────────────────────
SECTIONS = [
    {"id": "company",  "label": "Company Profile",    "subtitle": "Basic details about your organisation."},
    {"id": "supply",   "label": "Supply Chain & Risk", "subtitle": "Your supply chain exposure and human rights risk."},
    {"id": "buyer",    "label": "Buyer Signals",        "subtitle": "What your buyers and partners are asking for."},
    {"id": "internal", "label": "Internal Readiness",  "subtitle": "Governance maturity and data confidence."},
]

QUESTIONS = [
    {"key": "operates_in_eu", "section": 0,
     "text": "Where is your company primarily operating?",
     "options": ["EU", "Non-EU", "Both EU and Non-EU"]},
    {"key": "sells_to_eu_buyers", "section": 0,
     "text": "Do you sell directly or indirectly to EU-based companies or investors?",
     "options": ["Yes, directly", "Yes, indirectly", "No", "Unsure"]},
    {"key": "company_size", "section": 0,
     "text": "What best describes your company size?",
     "options": ["Micro (< 10 employees)", "Small (10–49)", "Medium", "Large"]},
    {"key": "sector", "section": 0,
     "text": "Which sector best fits your operations?",
     "options": [
         "Manufacturing (components / sub-assemblies)",
         "Processing / transformation (e.g. food, materials)",
         "Agriculture / farming", "Forestry / timber", "Fisheries / aquaculture",
         "Mining / extractives", "Construction / infrastructure",
         "Logistics / transport (road, sea, air)", "Warehousing / distribution",
         "Energy production or supply", "Waste management / recycling",
         "Chemicals / industrial inputs", "Textiles / apparel / footwear",
         "Electronics / electrical equipment", "Packaging / materials",
         "IT / digital services", "Professional services",
         "Facilities management / cleaning / security", "Other services",
     ]},
    {"key": "value_chain_role", "section": 0,
     "text": "Which best describes your role in the value chain today?",
     "options": [
         "Primarily a supplier to other companies",
         "Primarily a manufacturer selling finished goods",
         "Both supplier and direct-to-market", "Service provider",
     ]},
    {"key": "supply_chain_complexity", "section": 1,
     "text": "How complex is your supply chain?",
     "options": ["Simple / direct sourcing", "Some multi-tiering", "Highly multi-tiered", "Unsure"]},
    {"key": "hr_risk_region", "section": 1,
     "text": "Do your operations or sourcing occur in regions commonly considered higher risk for labor or human-rights issues?",
     "options": ["Yes", "No", "Partially", "Unsure"]},
    {"key": "labor_material", "section": 1,
     "text": "Are labor conditions a material issue in your operations or sourcing?",
     "options": ["Yes", "No", "Somewhat", "Unsure"]},
    {"key": "env_asked", "section": 1,
     "text": "Have buyers or partners asked you about environmental or climate-related topics?",
     "options": ["Yes", "No", "Unsure"]},
    {"key": "env_topics", "section": 1,
     "text": "Which environmental topics have buyers mentioned or asked about?",
     "options": ["Carbon / GHG emissions", "Energy use", "Water use", "Biodiversity",
                  "Waste", "Not specified / unclear", "None asked"]},
    {"key": "recent_esg_requests", "section": 2,
     "text": "Have buyers or partners recently requested ESG, sustainability, or human-rights information?",
     "options": ["Yes", "No", "Unsure"]},
    {"key": "more_detailed_requests", "section": 2,
     "text": "Have you been asked to complete questionnaires that feel more detailed than before?",
     "options": ["Yes, significantly more detailed", "Yes, somewhat", "No", "Not applicable"]},
    {"key": "request_driver", "section": 2,
     "text": "What do you think prompted these requests?",
     "options": ["New EU regulations (e.g. CSRD)", "Buyer internal policy",
                  "Unclear / not explained", "Customer ESG programme", "Other"]},
    {"key": "csrd_mentioned", "section": 2,
     "text": "Have buyers mentioned CSRD, EU sustainability reporting, or new EU sustainability laws?",
     "options": ["Yes, explicitly", 'Yes, indirectly (e.g. "new EU requirements")', "No", "Unsure"]},
    {"key": "internal_owner", "section": 3,
     "text": "Who is primarily responsible for sustainability or social impact topics internally?",
     "options": ["Dedicated sustainability / ESG role", "Shared / part-time responsibility",
                  "Senior leadership only", "No clear owner"]},
    {"key": "policy_status", "section": 3,
     "text": "Do you have written policies related to environment, sustainability and labor?",
     "options": ["Yes, comprehensive", "Yes, partial", "In development", "No"]},
    {"key": "data_tracking", "section": 3,
     "text": "Do you currently track any sustainability or social data?",
     "options": ["Yes, systematically", "Yes, partially", "Informal / ad hoc", "No"]},
    {"key": "confidence", "section": 3,
     "text": "How confident do you feel responding to buyer ESG, sustainability or human rights requests?",
     "options": ["Very confident", "Somewhat confident", "Not very confident", "Not confident"]},
]

SECTOR_ASSUMPTIONS = {
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

TAG_WEIGHTS = {
    "CSRD_CASCADE_SIGNAL":        1,
    "EU_EXPOSURE_NON_EU":         1,
    "POLICY_LIGHT":               2,
    "HRDD_RELEVANCE_HIGH":        2,
    "BUYER_OPACITY_RISK":         1,
    "ENVIRONMENTAL_BASELINE_GAP": 1,
    "DOCUMENTATION_LIGHT":        1,
    "SUPPLIER_CONFIDENCE_LOW":    1,
    "OWNER_GAP":                  2,
}

TAG_LABELS = {
    "CSRD_CASCADE_SIGNAL":        "CSRD cascade signal",
    "EU_EXPOSURE_NON_EU":         "EU exposure",
    "POLICY_LIGHT":               "Policy gaps",
    "HRDD_RELEVANCE_HIGH":        "HRDD relevance high",
    "BUYER_OPACITY_RISK":         "Buyer opacity risk",
    "ENVIRONMENTAL_BASELINE_GAP": "Environmental baseline gap",
    "DOCUMENTATION_LIGHT":        "Documentation light",
    "SUPPLIER_CONFIDENCE_LOW":    "Low confidence",
    "OWNER_GAP":                  "Owner gap",
}

MAX_SCORE = 12


# ── Logic ─────────────────────────────────────────────────────────────────────
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
    if (a.get("operates_in_eu") == "Non-EU"
            and a.get("sells_to_eu_buyers") in ("Yes, directly", "Yes, indirectly")):
        tags.append("EU_EXPOSURE_NON_EU")
    if a.get("policy_status") in ("In development", "No"):
        tags.append("POLICY_LIGHT")
    return list(dict.fromkeys(tags))


def run_screening(tags: list) -> dict:
    score = sum(TAG_WEIGHTS.get(t, 0) for t in tags)
    if score <= 2:
        band, band_label = "GREEN", "Low risk"
        interpretation = (
            "Limited immediate pressure signals and minor capability gaps. "
            "Focus on documentation hygiene and staying ahead of buyer requests."
        )
    elif score <= 6:
        band, band_label = "AMBER", "Moderate risk"
        interpretation = (
            "Buyer and regulatory pressure signals detected alongside internal gaps. "
            "Prioritize ownership, policy basics, and minimum viable data tracking."
        )
    else:
        band, band_label = "RED", "High risk"
        interpretation = (
            "Multiple pressure signals and capability gaps detected. This is where suppliers "
            "get caught flat-footed during buyer requests, audits, or tender processes. "
            "Move quickly to establish ownership, baseline policies, and auditable evidence."
        )
    steps = []
    if "OWNER_GAP" in tags:
        steps.append("Assign a single accountable owner for sustainability and compliance requests — by name and role.")
    if "POLICY_LIGHT" in tags:
        steps.append("Draft a minimum policy set covering environment and labor/human rights, with version control and sign-off.")
    if "DOCUMENTATION_LIGHT" in tags:
        steps.append("Start a basic data baseline: energy, emissions assumptions, water, and waste in a simple tracker.")
    if "HRDD_RELEVANCE_HIGH" in tags:
        steps.append("Map human rights and labor risk in sourcing countries and set up a lightweight due diligence checklist.")
    if "CSRD_CASCADE_SIGNAL" in tags or "BUYER_OPACITY_RISK" in tags:
        steps.append("Create a buyer-response pack: 1-page overview + evidence folder + standard Q&A for incoming requests.")
    if "EU_EXPOSURE_NON_EU" in tags:
        steps.append("Identify EU-linked customers and expected reporting asks. Align your evidence to what they request most.")
    steps.append("Package all outputs into a reusable Readiness Folder — policies, tracker, evidence, Q&A — for future requests.")
    return {"score": score, "band": band, "band_label": band_label,
            "interpretation": interpretation, "next_steps": steps, "tags": tags}


# ── build_pdf (ReportLab) — replaced by generate_pdf_from_html ─────────────
# def build_pdf(results: dict, answers: dict) -> bytes:
#     buf = io.BytesIO()
#     doc = SimpleDocTemplate(buf, pagesize=A4,
#                             leftMargin=2*cm, rightMargin=2*cm,
#                             topMargin=2*cm, bottomMargin=2*cm)
#     ns_surface   = colors.HexColor("#111113")
#     ns_fg        = colors.HexColor("#fafafa")
#     ns_fg_muted  = colors.HexColor("#a1a1aa")
#     ns_fg_subtle = colors.HexColor("#71717a")
#     ns_primary   = colors.HexColor("#3b82f6")
#     ns_border    = colors.HexColor("#27272a")
#     band_clr = {"GREEN": colors.HexColor("#10b981"),
#                 "AMBER": colors.HexColor("#f59e0b"),
#                 "RED":   colors.HexColor("#ef4444")}
# 
#     styles  = getSampleStyleSheet()
#     title_s = ParagraphStyle("T",  parent=styles["Title"],   textColor=ns_fg,        fontSize=20, spaceAfter=4,  fontName="Helvetica-Bold")
#     sub_s   = ParagraphStyle("Su", parent=styles["Normal"],  textColor=ns_fg_subtle, fontSize=9,  spaceAfter=12)
#     body_s  = ParagraphStyle("B",  parent=styles["Normal"],  textColor=ns_fg_muted,  fontSize=10, spaceAfter=4)
#     label_s = ParagraphStyle("L",  parent=styles["Normal"],  textColor=ns_fg_subtle, fontSize=8,  spaceAfter=2)
#     big_s   = ParagraphStyle("BV", parent=styles["Normal"],  textColor=ns_fg,        fontSize=22, spaceAfter=4,  fontName="Helvetica-Bold")
#     note_s  = ParagraphStyle("N",  parent=styles["Normal"],  textColor=ns_fg_subtle, fontSize=8,  spaceAfter=2)
#     step_s  = ParagraphStyle("ST", parent=styles["Normal"],  textColor=ns_fg_muted,  fontSize=9,  leading=14)
#     interp_s= ParagraphStyle("IT", parent=styles["Normal"],  textColor=ns_fg_muted,  fontSize=10, leading=15)
#     assump_s= ParagraphStyle("AS", parent=styles["Normal"],  textColor=ns_fg_muted,  fontSize=9,  leftIndent=10, spaceAfter=3)
# 
#     score       = results.get("score", 0)
#     band        = results.get("band", "")
#     band_label  = results.get("band_label", "")
#     interpretation = results.get("interpretation", "")
#     next_steps  = results.get("next_steps", [])
#     tags        = results.get("tags", [])
#     bc          = band_clr.get(band, ns_fg_muted)
# 
#     story = []
#     story.append(Paragraph("Supplier Readiness Diagnostic Report", title_s))
#     story.append(Paragraph("Navisignal · CSRD-aligned diagnostic for SME and supply chain suppliers", sub_s))
#     story.append(Spacer(1, 0.3*cm))
# 
#     div = Table([[""]], colWidths=[17*cm], rowHeights=[1])
#     div.setStyle(TableStyle([("LINEABOVE",(0,0),(-1,0),1,ns_primary),("TOPPADDING",(0,0),(-1,0),0),("BOTTOMPADDING",(0,0),(-1,0),0)]))
#     story += [div, Spacer(1, 0.4*cm)]
# 
#     meta = [["Operating region:", answers.get("operates_in_eu","—")],
#             ["EU buyer relationship:", answers.get("sells_to_eu_buyers","—")],
#             ["Company size:", answers.get("company_size","—")],
#             ["Sector:", answers.get("sector","—")],
#             ["Value chain role:", answers.get("value_chain_role","—")],
#             ["Report date:", datetime.today().strftime("%Y-%m-%d")]]
#     mt = Table(meta, colWidths=[5*cm,12*cm])
#     mt.setStyle(TableStyle([("TEXTCOLOR",(0,0),(0,-1),ns_fg_subtle),("TEXTCOLOR",(1,0),(1,-1),ns_fg),
#                              ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),("FONTNAME",(1,0),(1,-1),"Helvetica"),
#                              ("FONTSIZE",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),2)]))
#     story += [mt, Spacer(1,0.5*cm)]
# 
#     bv_s = ParagraphStyle("bv",parent=styles["Normal"],textColor=bc,fontSize=18,spaceAfter=4,fontName="Helvetica-Bold")
#     score_cell = [Paragraph("SCORE",label_s), Paragraph(f'{score} <font size="12" color="#71717a">/ {MAX_SCORE}</font>',big_s)]
#     band_cell  = [Paragraph("RISK BAND",label_s), Paragraph(band,bv_s),
#                   Paragraph(band_label,ParagraphStyle("bl",parent=styles["Normal"],textColor=ns_fg_subtle,fontSize=9))]
#     cards = Table([[score_cell,band_cell]],colWidths=[8*cm,9*cm])
#     cards.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),ns_surface),("BOX",(0,0),(0,0),1,ns_border),
#                                ("BOX",(1,0),(1,0),1,ns_border),("TOPPADDING",(0,0),(-1,-1),12),
#                                ("BOTTOMPADDING",(0,0),(-1,-1),12),("LEFTPADDING",(0,0),(-1,-1),14),
#                                ("RIGHTPADDING",(0,0),(-1,-1),14),("VALIGN",(0,0),(-1,-1),"TOP")]))
#     story += [cards, Spacer(1,0.5*cm)]
# 
#     story.append(Paragraph("<b>Interpretation</b>", body_s))
#     it = Table([[Paragraph(interpretation,interp_s)]],colWidths=[16.5*cm])
#     it.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),ns_surface),("BOX",(0,0),(-1,-1),0.5,ns_border),
#                              ("LINEBEFORE",(0,0),(0,-1),2,bc),("TOPPADDING",(0,0),(-1,-1),10),
#                              ("BOTTOMPADDING",(0,0),(-1,-1),10),("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12)]))
#     story += [it, Spacer(1,0.5*cm)]
# 
#     if tags:
#         story.append(Paragraph("<b>Flags triggered</b>", body_s))
#         story.append(Paragraph("  ·  ".join(TAG_LABELS.get(t,t) for t in tags),
#                                ParagraphStyle("tg",fontSize=9,textColor=ns_primary,spaceAfter=8)))
#         story.append(Spacer(1,0.3*cm))
# 
#     if next_steps:
#         story.append(Paragraph("<b>Recommended next steps</b>", body_s))
#         story.append(Spacer(1,0.15*cm))
#         for i, txt in enumerate(next_steps):
#             row = Table([[Paragraph(f"{i+1}.  {txt}",step_s)]],colWidths=[16.5*cm])
#             row.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),ns_surface),("BOX",(0,0),(-1,-1),0.5,ns_border),
#                                      ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
#                                      ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12)]))
#             story += [row, Spacer(1,0.1*cm)]
#         story.append(Spacer(1,0.3*cm))
# 
#     sector = answers.get("sector")
#     if sector and sector in SECTOR_ASSUMPTIONS:
#         story.append(Paragraph(f"<b>Sector baseline: {sector}</b>", body_s))
#         for a in SECTOR_ASSUMPTIONS[sector]:
#             story.append(Paragraph(f"•  {a}", assump_s))
#         story.append(Spacer(1,0.4*cm))
# 
#     story += [div, Spacer(1,0.3*cm)]
#     story.append(Paragraph("<b>Disclaimer:</b> This is a decision support tool. It is not legal advice or a final compliance determination.", note_s))
#     story.append(Spacer(1,0.15*cm))
#     story.append(Paragraph(f"Generated by Navisignal Supplier Readiness Diagnostic · {datetime.today().strftime('%Y-%m-%d')}",
#                            ParagraphStyle("gen",fontSize=7,textColor=ns_fg_subtle)))
#     doc.build(story)
#     buf.seek(0)
#     return buf.read()
# 



# ── HTML → PDF via WeasyPrint ─────────────────────────────────────────────────
TEMPLATE_PATH = Path(__file__).parent / "templates" / "pdf_report_template_clean.html"


def generate_pdf_from_html(report_data: dict) -> bytes:
    r   = report_data["results"]
    ans = report_data["answers"]

    html_template = TEMPLATE_PATH.read_text(encoding="utf-8")

    score  = r.get("score", 0)
    sector = ans.get("sector", "")
    assumptions = SECTOR_ASSUMPTIONS.get(sector, ["—", "—", "—"])

    intake_answers = [
        {"question": q["text"], "answer": ans.get(q["key"], "—")}
        for q in QUESTIONS
    ]

    context = {
        "score":                  score,
        "max_score":              MAX_SCORE,
        "band":                   r.get("band", ""),
        "band_subtitle":          r.get("band_label", ""),
        "band_needle_percent":    min(int(score / MAX_SCORE * 100), 100),
        "generated_date_display": datetime.today().strftime("%d %B %Y"),
        "report_date_iso":        datetime.today().strftime("%Y-%m-%d"),
        "operating_region":       ans.get("operates_in_eu", "—"),
        "eu_buyer_relationship":  ans.get("sells_to_eu_buyers", "—"),
        "company_size":           ans.get("company_size", "—"),
        "sector":                 sector,
        "value_chain_role":       ans.get("value_chain_role", "—"),
        "interpretation":         r.get("interpretation", ""),
        "tags":                   r.get("tags", []),
        "recommendations":        r.get("next_steps", []),
        "sector_assumption_1":    assumptions[0] if len(assumptions) > 0 else "—",
        "sector_assumption_2":    assumptions[1] if len(assumptions) > 1 else "—",
        "sector_assumption_3":    assumptions[2] if len(assumptions) > 2 else "—",
        "intake_answers":         intake_answers,
    }

    rendered_html = Template(html_template).render(**context)
    pdf_bytes = HTML(
        string=rendered_html,
        base_url=str(TEMPLATE_PATH.parent)
    ).write_pdf()
    return pdf_bytes

# ── Session state ─────────────────────────────────────────────────────────────
for _k, _v in {"authed": False, "step": 0, "answers": {},
               "show_validation": False, "results": None}.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── Secrets ───────────────────────────────────────────────────────────────────
try:
    APP_PASSWORD = st.secrets["APP_PASSWORD"]
except Exception:
    APP_PASSWORD = "betastream"
try:
    BETA_EMAIL = st.secrets["BETA_EMAIL"]
except Exception:
    BETA_EMAIL = "hello@navisignal.app"


# ═══════════════════════════════════════════════════════════════════════════════
# PASSWORD GATE
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state.authed:
    st.markdown('<div style="height:8vh;"></div>', unsafe_allow_html=True)
    _, pw_col, _ = st.columns([1, 2.2, 1])
    with pw_col:
        st.markdown("""
        <div style="background:#111113;border:1px solid #27272a;border-radius:10px;
                    padding:40px 36px 28px;text-align:center;">
          <div style="margin-bottom:20px;">
            <svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="22" cy="22" r="20" stroke="#3b82f6" stroke-width="2" opacity="0.3"/>
              <circle cx="22" cy="22" r="3" fill="#3b82f6"/>
              <line x1="22" y1="2" x2="22" y2="10" stroke="#c9a84c" stroke-width="2" stroke-linecap="round"/>
              <line x1="22" y1="34" x2="22" y2="42" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
              <line x1="2" y1="22" x2="10" y2="22" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
              <line x1="34" y1="22" x2="42" y2="22" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
            </svg>
          </div>
          <div style="font-family:'DM Serif Display',Georgia,serif;font-size:24px;
                      color:#fafafa;margin-bottom:6px;">Supplier Readiness</div>
          <div style="font-size:12px;color:#71717a;line-height:1.6;margin-bottom:28px;">
            CSRD-aligned diagnostic for SME and supply chain suppliers<br>
            <em>Beta access only</em>
          </div>
        </div>
        """, unsafe_allow_html=True)

        pwd = st.text_input("", type="password", placeholder="Enter access password…",
                            label_visibility="collapsed")
        if st.button("Enter →", use_container_width=True):
            if pwd == APP_PASSWORD:
                st.session_state.authed = True
                st.rerun()
            else:
                st.error("Incorrect password. Contact your administrator.")
        st.markdown(
            f'<div style="text-align:center;margin-top:16px;font-size:12px;color:#71717a;">'
            f'<a href="mailto:{BETA_EMAIL}?subject=Beta access request" '
            f'style="color:#3b82f6;font-weight:600;text-decoration:none;">Request beta access</a></div>',
            unsafe_allow_html=True,
        )
    st.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — About this tool + progress nav (collapsible via Streamlit toggle)
# ═══════════════════════════════════════════════════════════════════════════════
cur_step   = st.session_state.step
is_results = cur_step == len(SECTIONS)

with st.sidebar:
    st.markdown(
        '<p style="font-family:\'DM Serif Display\',Georgia,serif;font-size:16px;'
        'color:#fafafa;margin-bottom:12px;">About this tool</p>',
        unsafe_allow_html=True,
    )
    st.markdown("""
This is a fast, decision-grade diagnostic designed to help SME and supply chain suppliers
understand whether they are prepared for current sustainability, human rights, and
climate-related reporting expectations — especially under the EU **Corporate Sustainability
Reporting Directive (CSRD)**.

Rather than asking suppliers to "do everything," the tool focuses on what actually matters:
data availability, governance maturity, risk exposure, and the ability to meet near-term
disclosure and due-diligence expectations.

The output is a clear, comparable readiness profile that highlights gaps, flags material
risks, and distinguishes between suppliers who need support, monitoring, or escalation.

**Additional notes:**
- No legal interpretation required from the supplier
- Aligned to what buyers actually screen for first under CSRD / HRDD
- Safe for Global South and SME suppliers
- Built for real supply chains (not idealized ones)
""")
    st.markdown("---")
    if not is_results:
        st.markdown('<p style="font-size:10px;font-weight:600;letter-spacing:0.15em;'
                    'text-transform:uppercase;color:#71717a;margin-bottom:4px;">Your progress</p>',
                    unsafe_allow_html=True)
        for i, s in enumerate(SECTIONS):
            if i < cur_step:
                dot, clr, fw = "●", "#10b981", "400"
            elif i == cur_step:
                dot, clr, fw = "●", "#3b82f6", "600"
            else:
                dot, clr, fw = "○", "#71717a", "400"
            st.markdown(
                f'<div style="font-size:13px;color:{clr};font-weight:{fw};padding:4px 0;">'
                f'{dot}&nbsp;&nbsp;{s["label"]}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("---")
    else:
        st.markdown('<p style="color:#10b981;font-size:12px;">✓ All sections complete</p>',
                    unsafe_allow_html=True)
        st.markdown("---")
    st.markdown('<p style="font-size:10px;font-weight:600;letter-spacing:0.15em;'
                'text-transform:uppercase;color:#71717a;margin-bottom:4px;">Contact</p>',
                unsafe_allow_html=True)
    st.markdown("[navisignal.app](https://navisignal.app)  \n[hello@navisignal.app](mailto:hello@navisignal.app)")
    st.markdown("---")
    st.markdown('<p style="font-size:11px;color:#71717a;font-style:italic;line-height:1.6;">'
                'This is a decision support tool. It is not legal advice or a final compliance determination.</p>',
                unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="border-bottom:1px solid #27272a;padding:14px 0 14px;
            display:flex;align-items:center;justify-content:space-between;
            margin-bottom:4px;">
  <div style="font-family:'DM Serif Display',Georgia,serif;font-size:18px;color:#fafafa;">
    Navisignal
    <span style="font-family:'DM Sans',sans-serif;font-size:10px;font-weight:600;
                 letter-spacing:0.1em;text-transform:uppercase;color:#c9a84c;
                 border:1px solid #c9a84c;border-radius:9999px;
                 padding:2px 8px;margin-left:8px;">Beta</span>
  </div>
  <div style="text-align:right;">
    <div style="font-family:'DM Serif Display',Georgia,serif;font-size:15px;color:#fafafa;">Supplier Readiness Diagnostic</div>
    <div style="font-size:11px;color:#71717a;margin-top:1px;">CSRD-aligned &middot; SME &amp; supply chain</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRESS TRACK (intake only)
# ═══════════════════════════════════════════════════════════════════════════════
if not is_results:
    total_q    = len(QUESTIONS)
    answered_q = sum(1 for q in QUESTIONS if st.session_state.answers.get(q["key"]))
    pct        = int((answered_q / total_q) * 100)

    st.markdown(
        f'<div style="padding:10px 0 14px;border-bottom:1px solid #1f1f23;margin-bottom:20px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">'
        f'<span style="font-size:11px;color:#71717a;">{SECTIONS[cur_step]["label"]} — step {cur_step+1} of {len(SECTIONS)}</span>'
        f'<span style="font-size:11px;color:#3b82f6;font-weight:600;">{pct}% complete</span>'
        f'</div>'
        f'<div style="height:3px;background:#27272a;border-radius:9999px;overflow:hidden;">'
        f'<div style="height:3px;background:#3b82f6;border-radius:9999px;'
        f'width:{pct}%;transition:width 0.4s ease;"></div></div></div>',
        unsafe_allow_html=True,
    )

    dots = '<div style="display:flex;gap:6px;margin-bottom:28px;">'
    for i in range(len(SECTIONS)):
        c = "#10b981" if i < cur_step else ("#3b82f6" if i == cur_step else "#27272a")
        dots += f'<div style="flex:1;height:3px;border-radius:9999px;background:{c};"></div>'
    dots += '</div>'
    st.markdown(dots, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# INTAKE STEPS
# ═══════════════════════════════════════════════════════════════════════════════
if not is_results:
    section    = SECTIONS[cur_step]
    section_qs = [q for q in QUESTIONS if q["section"] == cur_step]

    st.markdown(
        f'<div style="font-size:11px;font-weight:600;letter-spacing:0.18em;'
        f'text-transform:uppercase;color:#3b82f6;margin-bottom:6px;">'
        f'Section {cur_step+1} of {len(SECTIONS)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<h1 style="font-family:\'DM Serif Display\',Georgia,serif;font-size:28px;'
        f'color:#fafafa;line-height:1.2;margin-bottom:6px;font-weight:400;">{section["label"]}</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p style="font-size:13px;color:#a1a1aa;line-height:1.6;margin-bottom:24px;">{section["subtitle"]}</p>',
        unsafe_allow_html=True,
    )

    if st.session_state.show_validation:
        st.markdown("""
        <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);
                    border-radius:6px;padding:10px 14px;font-size:12px;color:#ef4444;
                    margin-bottom:18px;">
          Please answer all questions in this section before continuing.
        </div>
        """, unsafe_allow_html=True)

    unanswered_keys = (
        {q["key"] for q in section_qs if not st.session_state.answers.get(q["key"])}
        if st.session_state.show_validation else set()
    )

    for q in section_qs:
        is_req   = q["key"] in unanswered_keys
        cur_val  = st.session_state.answers.get(q["key"]) or ""
        opts     = [""] + q["options"]
        try:
            idx = opts.index(cur_val)
        except ValueError:
            idx = 0

        lbl_color = "#ef4444" if is_req else "#fafafa"
        st.markdown(
            f'<div style="font-size:13px;font-weight:500;color:{lbl_color};'
            f'margin-bottom:4px;margin-top:4px;">'
            f'{q["text"]} <span style="color:#3b82f6;">⁎</span></div>',
            unsafe_allow_html=True,
        )

        selected = st.selectbox(
            q["text"],
            opts,
            index=idx,
            format_func=lambda x: "— select —" if x == "" else x,
            key=f"s{cur_step}_{q['key']}",
            label_visibility="collapsed",
        )

        if is_req and not selected:
            st.markdown(
                '<div style="font-size:11px;color:#ef4444;margin-top:-6px;margin-bottom:6px;">'
                'This field is required.</div>',
                unsafe_allow_html=True,
            )

        st.session_state.answers[q["key"]] = selected or None

        if q["key"] == "sector" and selected:
            assumptions = SECTOR_ASSUMPTIONS.get(selected)
            if assumptions:
                bullets = "".join(
                    f'<li style="font-size:12px;color:#a1a1aa;line-height:1.65;'
                    f'margin-bottom:3px;">{a}</li>'
                    for a in assumptions
                )
                st.markdown(
                    f'<div style="background:rgba(59,130,246,0.06);'
                    f'border-left:2px solid #3b82f6;border-radius:0 6px 6px 0;'
                    f'padding:10px 14px;margin-top:4px;margin-bottom:4px;">'
                    f'<div style="font-size:10px;font-weight:600;letter-spacing:0.1em;'
                    f'text-transform:uppercase;color:#3b82f6;margin-bottom:6px;">'
                    f'Sector baseline</div>'
                    f'<ul style="padding-left:14px;margin:0;">{bullets}</ul></div>',
                    unsafe_allow_html=True,
                )

        st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

    st.markdown(
        '<hr style="border:none;border-top:1px solid #27272a;margin:24px 0 16px;">',
        unsafe_allow_html=True,
    )
    answered_sec = sum(1 for q in section_qs if st.session_state.answers.get(q["key"]))
    st.markdown(
        f'<div style="text-align:center;font-size:11px;color:#71717a;margin-bottom:14px;">'
        f'{answered_sec} / {len(section_qs)} answered in this section</div>',
        unsafe_allow_html=True,
    )

    is_last = cur_step == len(SECTIONS) - 1
    col_back, _, col_next = st.columns([1, 2, 1])

    with col_back:
        if st.button("← Back", disabled=(cur_step == 0), use_container_width=True):
            st.session_state.step -= 1
            st.session_state.show_validation = False
            st.rerun()

    with col_next:
        lbl = "Run screening →" if is_last else "Next →"
        if st.button(lbl, type="primary", use_container_width=True):
            missing = [q for q in section_qs if not st.session_state.answers.get(q["key"])]
            if missing:
                st.session_state.show_validation = True
                st.rerun()
            elif is_last:
                tags    = derive_tags(st.session_state.answers)
                res     = run_screening(tags)
                st.session_state.results         = res
                st.session_state.step            = len(SECTIONS)
                st.session_state.show_validation = False
                st.rerun()
            else:
                st.session_state.step           += 1
                st.session_state.show_validation = False
                st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
else:
    r          = st.session_state.results
    score      = r["score"]
    band       = r["band"]
    band_label = r["band_label"]
    interp     = r["interpretation"]
    steps      = r["next_steps"]
    tags       = r["tags"]
    ans        = st.session_state.answers

    BAND_C = {"GREEN": "#10b981", "AMBER": "#f59e0b", "RED": "#ef4444"}
    bc          = BAND_C.get(band, "#a1a1aa")
    needle_pct  = min(int((score / MAX_SCORE) * 100), 100)
    meta_parts  = [p for p in [ans.get("sector",""), ans.get("company_size",""), ans.get("operates_in_eu","")] if p]

    st.markdown(
        '<div style="font-size:11px;font-weight:600;letter-spacing:0.18em;'
        'text-transform:uppercase;color:#3b82f6;margin-bottom:6px;">Assessment complete</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<h1 style="font-family:\'DM Serif Display\',Georgia,serif;font-size:28px;'
        'color:#fafafa;line-height:1.2;margin-bottom:6px;font-weight:400;">Your readiness profile</h1>',
        unsafe_allow_html=True,
    )
    if meta_parts:
        st.markdown(
            f'<p style="font-size:13px;color:#a1a1aa;margin-bottom:24px;">{ " · ".join(meta_parts) }</p>',
            unsafe_allow_html=True,
        )

    col_s, col_b = st.columns([1, 2])
    with col_s:
        st.markdown(
            f'<div style="background:#18181b;border:1px solid #27272a;border-radius:6px;padding:16px 18px;">'
            f'<div style="font-size:10px;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;'
            f'color:#71717a;margin-bottom:8px;">Score</div>'
            f'<div style="font-family:\'DM Serif Display\',Georgia,serif;font-size:42px;'
            f'color:#fafafa;line-height:1;">'
            f'{score}<span style="font-size:16px;color:#71717a;"> / {MAX_SCORE}</span></div></div>',
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            f'<div style="background:#18181b;border:1px solid #27272a;border-radius:6px;padding:16px 18px;">'
            f'<div style="font-size:10px;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;'
            f'color:#71717a;margin-bottom:8px;">Risk band</div>'
            f'<div style="font-family:\'DM Serif Display\',Georgia,serif;font-size:28px;'
            f'color:{bc};line-height:1;margin-bottom:4px;">{band}</div>'
            f'<div style="font-size:11px;color:#71717a;margin-bottom:10px;">{band_label}</div>'
            f'<div style="height:6px;border-radius:9999px;position:relative;margin-bottom:6px;'
            f'background:linear-gradient(to right,#10b981 0%,#10b981 30%,#f59e0b 30%,#f59e0b 65%,#ef4444 65%);">'
            f'<div style="position:absolute;top:50%;left:{needle_pct}%;transform:translate(-50%,-50%);'
            f'width:14px;height:14px;border-radius:50%;background:#fafafa;border:2px solid #09090b;"></div></div>'
            f'<div style="display:flex;justify-content:space-between;font-size:9px;font-weight:600;letter-spacing:0.08em;">'
            f'<span style="color:#10b981;">Green</span>'
            f'<span style="color:#f59e0b;">Amber</span>'
            f'<span style="color:#ef4444;">Red</span></div></div>',
            unsafe_allow_html=True,
        )

    if tags:
        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:11px;font-weight:600;color:#71717a;margin-bottom:8px;'
            'letter-spacing:0.05em;text-transform:uppercase;">Flags triggered</div>',
            unsafe_allow_html=True,
        )
        pills = "".join(
            f'<span style="display:inline-block;padding:3px 10px;border-radius:9999px;'
            f'font-size:10px;font-weight:600;letter-spacing:0.05em;'
            f'background:rgba(59,130,246,0.12);color:#3b82f6;margin:2px 4px 2px 0;">'
            f'{TAG_LABELS.get(t,t)}</span>'
            for t in tags
        )
        st.markdown(f'<div style="display:flex;flex-wrap:wrap;">{pills}</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div style="background:#18181b;border-left:2px solid {bc};'
        f'border-radius:0 6px 6px 0;padding:14px 16px;margin-top:16px;margin-bottom:24px;">'
        f'<div style="font-size:10px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;'
        f'color:#71717a;margin-bottom:6px;">Interpretation</div>'
        f'<p style="font-size:13px;color:#a1a1aa;line-height:1.65;margin:0;">{interp}</p></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<hr style="border:none;border-top:1px solid #27272a;margin:28px 0;">', unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:11px;font-weight:600;letter-spacing:0.18em;'
        'text-transform:uppercase;color:#3b82f6;margin-bottom:4px;">Action checklist</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<h2 style="font-family:\'DM Serif Display\',Georgia,serif;font-size:20px;'
        'font-weight:400;color:#fafafa;margin-bottom:16px;">Recommended next steps</h2>',
        unsafe_allow_html=True,
    )
    for i, step_text in enumerate(steps):
        st.checkbox(step_text, key=f"chk_{i}", value=False)

    sector_val = ans.get("sector", "")
    if sector_val and sector_val in SECTOR_ASSUMPTIONS:
        with st.expander(f"Sector baseline: {sector_val}"):
            for assumption in SECTOR_ASSUMPTIONS[sector_val]:
                st.markdown(
                    f'<li style="font-size:12px;color:#a1a1aa;line-height:1.7;'
                    f'list-style:disc;margin-left:16px;margin-bottom:3px;">{assumption}</li>',
                    unsafe_allow_html=True,
                )

    st.markdown('<hr style="border:none;border-top:1px solid #27272a;margin:28px 0;">', unsafe_allow_html=True)

    col_dl, col_rs = st.columns([2, 1])
    with col_dl:
        pdf_bytes = generate_pdf_from_html({"results": r, "answers": ans})
        fname = (
            f"Navisignal_Readiness_"
            f"{sector_val.replace(' ','_').replace('/','_')[:25]}_"
            f"{datetime.today().strftime('%Y%m%d')}.pdf"
        )
        st.download_button("↓ Download report (PDF)", data=pdf_bytes,
                           file_name=fname, mime="application/pdf")
    with col_rs:
        if st.button("Restart screening"):
            st.session_state.answers          = {}
            st.session_state.results          = None
            st.session_state.step             = 0
            st.session_state.show_validation  = False
            st.rerun()

    st.markdown(
        '<div style="font-size:11px;color:#71717a;line-height:1.6;margin:24px 0 8px;font-style:italic;">'
        'This is a decision support tool. It is not legal advice or a final compliance determination. '
        'Generated by Navisignal Supplier Readiness Diagnostic.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div style="border-top:1px solid #27272a;padding:28px 0 40px;text-align:center;line-height:1.7;">
      <div style="font-size:12px;color:#71717a;margin-bottom:4px;">
        Supplier Readiness Diagnostic is a product of
        <strong style="color:#a1a1aa;">Navisignal</strong> — practical tools for complex decisions.
      </div>
      <div style="display:flex;align-items:center;justify-content:center;gap:12px;margin-top:8px;flex-wrap:wrap;">
        <a href="https://navisignal.app" target="_blank"
           style="color:#3b82f6;text-decoration:none;font-weight:600;font-size:12px;">navisignal.app</a>
        <span style="color:#27272a;font-size:12px;">&middot;</span>
        <a href="mailto:hello@navisignal.app"
           style="color:#3b82f6;text-decoration:none;font-weight:600;font-size:12px;">hello@navisignal.app</a>
      </div>
      <div style="margin-top:12px;font-size:10px;color:#71717a;opacity:0.5;letter-spacing:0.1em;">
        Evidence. Structure. Action.
      </div>
    </div>
    """, unsafe_allow_html=True)
