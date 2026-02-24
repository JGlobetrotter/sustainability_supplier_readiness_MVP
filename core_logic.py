# ─────────────────────────────────────────────
#  ESG / CSRD Supplier Readiness Scorer
# ─────────────────────────────────────────────

# ── 1. Question → answer-key mapping ─────────
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

# ── 2. Sector baseline assumptions ───────────
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

# ── 3. Sample answers ─────────────────────────
answers_by_question = {
    "Where is your company primarily operating?": "Non-EU",
    "Do you sell directly or indirectly to EU-based companies or investors?": "Yes, indirectly",
    "What best describes your company size?": "Medium",
    "Which sector best fits your operations?": "Manufacturing (components / sub-assemblies)",
    "Which best describes your role in the value chain today?": "Primarily a supplier to other companies",
    "How complex is your supply chain?": "Highly multi-tiered",
    "Do your operations or sourcing occur in regions commonly considered higher risk for labor or human-rights issues?": "Yes",
    "Are labor conditions a material issue in your operations or sourcing?": "Somewhat",
    "Have buyers or partners asked you about environmental or climate-related topics?": "Yes",
    "Which environmental topics have buyers mentioned or asked about? (Select all that apply)?": "Not specified / unclear",
    "Have buyers or partners recently requested ESG, sustainability, or human-rights information?": "Yes",
    "Have you been asked to complete questionnaires or provide information that feels new or more detailed than in the past?": "Yes, significantly more detailed",
    "What do you think prompted these requests?": "Unclear / not explained",
    "Have any buyers or partners mentioned CSRD, EU sustainability reporting, or new EU sustainability laws when requesting information from you?": "Yes, indirectly (e.g. \"new EU requirements\")",
    "Who is primarily responsible for sustainability or social impact topics internally?": "No clear owner",
    "Do you have written policies related to the environment, sustainability and labor?": "No",
    "Do you currently track any sustainability or social data?": "Informal / ad hoc",
    "How confident do you feel responding to buyer ESG, sustainability or human rights requests?": "Not confident",
}

# ── 4. Normalize answers ──────────────────────
def normalize_answers(answers: dict) -> dict:
    result = {}
    for question, answer in answers.items():
        key = QUESTION_TO_KEY.get(question)
        if key:
            result[key] = answer
    return result

# ── 5. Tag derivation logic ───────────────────
def derive_tags(a: dict) -> list:
    tags = []

    # BUYER_OPACITY_RISK — buyer requests exist but reasons are unclear
    if a.get("env_topics") in ("Not specified / unclear",):
        tags.append("BUYER_OPACITY_RISK")
    if a.get("request_driver") in ("Unclear / not explained",):
        tags.append("BUYER_OPACITY_RISK")
    if a.get("csrd_mentioned") and "indirectly" in a.get("csrd_mentioned", "").lower():
        tags.append("BUYER_OPACITY_RISK")
    if a.get("more_detailed_requests") in ("Yes, significantly more detailed",):
        tags.append("BUYER_OPACITY_RISK")

    # HRDD_RELEVANCE_HIGH — human rights / labor risk indicators
    if a.get("hr_risk_region") in ("Yes",):
        tags.append("HRDD_RELEVANCE_HIGH")
    if a.get("labor_material") in ("Yes", "Somewhat"):
        tags.append("HRDD_RELEVANCE_HIGH")
    if a.get("supply_chain_complexity") in ("Highly multi-tiered",):
        tags.append("HRDD_RELEVANCE_HIGH")

    # SUPPLIER_CONFIDENCE_LOW — low internal confidence / capability
    if a.get("confidence") in ("Not confident",):
        tags.append("SUPPLIER_CONFIDENCE_LOW")
    if a.get("internal_owner") in ("No clear owner",):
        tags.append("SUPPLIER_CONFIDENCE_LOW")
    if a.get("policy_status") in ("No",):
        tags.append("SUPPLIER_CONFIDENCE_LOW")
    if a.get("data_tracking") in ("Informal / ad hoc", "No",):
        tags.append("SUPPLIER_CONFIDENCE_LOW")

    # CSRD_CASCADE_SIGNAL — downstream CSRD pressure
    if a.get("csrd_mentioned") and "yes" in a.get("csrd_mentioned", "").lower():
        tags.append("CSRD_CASCADE_SIGNAL")

    # DOCUMENTATION_LIGHT — weak written documentation
    if a.get("policy_status") in ("No",):
        tags.append("DOCUMENTATION_LIGHT")

    # ENVIRONMENTAL_BASELINE_GAP — gaps in environmental tracking / awareness
    if a.get("env_asked") in ("Yes",) and a.get("data_tracking") in ("Informal / ad hoc", "No"):
        tags.append("ENVIRONMENTAL_BASELINE_GAP")
    if a.get("env_topics") in ("Not specified / unclear",):
        tags.append("ENVIRONMENTAL_BASELINE_GAP")

    # OWNER_GAP — no internal sustainability owner
    if a.get("internal_owner") in ("No clear owner",):
        tags.append("OWNER_GAP")
    if a.get("policy_status") in ("No",):
        tags.append("OWNER_GAP")

    return tags

# ── 6. Scoring logic ──────────────────────────
SCORE_BANDS = [
    (0,  3,  "LOW",    "Limited sustainability-driven pressure at this stage."),
    (4,  6,  "MEDIUM", "Some Sustainability-driven pressure likely"),
    (7,  10, "HIGH",   "Significant sustainability-driven pressure — action required."),
]

SCORE_RULES = [
    # (answer_key, matching_values, points)
    ("sells_to_eu_buyers",     ["Yes", "Yes, indirectly"],                              1),
    ("supply_chain_complexity",["Highly multi-tiered", "Multi-tiered"],                 1),
    ("hr_risk_region",         ["Yes"],                                                 1),
    ("recent_esg_requests",    ["Yes"],                                                 1),
    ("more_detailed_requests", ["Yes, significantly more detailed", "Yes, somewhat"],   1),
    ("csrd_mentioned",         ["Yes", "Yes, indirectly (e.g. \"new EU requirements\")"], 1),
    ("policy_status",          ["No"],                                                  1),
    ("data_tracking",          ["Informal / ad hoc", "No"],                             1),
    ("internal_owner",         ["No clear owner"],                                      1),
    ("confidence",             ["Not confident"],                                       1),
]

def calculate_score(a: dict) -> int:
    score = 0
    for key, matching_values, points in SCORE_RULES:
        if a.get(key) in matching_values:
            score += points
    return score

def get_band(score: int) -> tuple:
    for low, high, band, description in SCORE_BANDS:
        if low <= score <= high:
            return band, description
    return "UNKNOWN", "Score out of range."

# ── 7. Recommendation logic ───────────────────
def get_recommendations(tags: list, a: dict) -> list:
    recs = []
    unique_tags = set(tags)

    if "CSRD_CASCADE_SIGNAL" in unique_tags:
        recs.append("CSRD readiness activities strongly recommended.")
    if "BUYER_OPACITY_RISK" in unique_tags:
        recs.append("Clients or buyers are expressing conflicting or confusing requests.")
    if "HRDD_RELEVANCE_HIGH" in unique_tags:
        recs.append("Human Rights and Labor activity strengthening recommended")
    if "OWNER_GAP" in unique_tags:
        recs.append("Strengthen responsibility linkages to reporting and compliance")
    if "ENVIRONMENTAL_BASELINE_GAP" in unique_tags:
        recs.append("Suggest to draft environmental compliance processes to create a baseline")
    if "SUPPLIER_CONFIDENCE_LOW" in unique_tags:
        recs.append("You don't have a lot of confidence at present - strongly suggest external advisory or support.")

    return recs

# ── 8. Main execution ─────────────────────────
def main():
    # Normalize
    a = normalize_answers(answers_by_question)
    print("Normalized answers keys:", list(a.keys()))

    # Tags
    tags = derive_tags(a)
    for tag in tags:
        print(tag)
    print("\nApplied tags list:", tags)

    # Score
    score = calculate_score(a)
    band, band_desc = get_band(score)
    recommendations = get_recommendations(tags, a)

    print(f"\nScore: {score}")
    print(f"Band: {band}: {band_desc}")
    print("Why:")
    for rec in recommendations:
        print(f"-  {rec}")

    # Sector baseline assumptions
    sector = a.get("sector")
    if sector and sector in SECTOR_BASELINE_ASSUMPTIONS:
        print(f"\nBaseline assumptions for '{sector}':")
        for assumption in SECTOR_BASELINE_ASSUMPTIONS[sector]:
            print("-", assumption)
    else:
        print(f"\nNo specific baseline assumptions found for sector: {sector}")

if __name__ == "__main__":
    main()
