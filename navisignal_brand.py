"""
Navisignal Brand Kit
====================
Single source of truth for Navisignal product branding.
Import into any Python project to keep colors, typography,
and copy consistent across all tools and reports.

Usage:
    from navisignal_brand import Brand, ReportLabColors, CSS

    # Streamlit / HTML
    st.markdown(f'<div style="background:{Brand.BG};color:{Brand.TEXT};">')

    # ReportLab PDF
    from reportlab.lib import colors
    GOLD = colors.HexColor(Brand.GOLD)

    # Inject full CSS block
    st.markdown(f"<style>{CSS.full_stylesheet()}</style>", unsafe_allow_html=True)
"""

# ── Core palette ──────────────────────────────────────────────────────────────

class Brand:
    # Backgrounds
    BG          = "#0F1829"   # page / app background
    SURFACE     = "#182238"   # card / panel surface
    SURFACE_2   = "#1C2844"   # elevated surface (hover states, nested cards)
    SIDEBAR     = "#09111F"   # sidebar / nav background

    # Borders
    BORDER      = "#1E2D48"   # default border
    BORDER_HOVER= "#2A3D60"   # hover / focus border

    # Accent — gold
    GOLD        = "#C9A84C"   # primary accent (headlines, CTAs, icons)
    GOLD_HOVER  = "#A8893C"   # gold on hover / pressed
    GOLD_SUBTLE = "rgba(201,168,76,0.12)"  # gold tint for backgrounds

    # Text
    TEXT        = "#FFFFFF"   # primary text
    TEXT_2      = "#B0C4DE"   # secondary / body text
    TEXT_3      = "#8094B4"   # muted / captions
    TEXT_ON_DARK= "#FFFFFF"   # text placed on dark navy surfaces

    # Semantic — risk bands
    GREEN       = "#10b981"   # low risk
    AMBER       = "#f59e0b"   # moderate risk
    RED         = "#ef4444"   # high risk

    # Typography
    FONT_DISPLAY = "'Space Grotesk', sans-serif"
    FONT_BODY    = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    FONT_IMPORT  = (
        "https://fonts.googleapis.com/css2?"
        "family=Space+Grotesk:wght@300;400;500;600;700"
        "&family=Inter:wght@400;500;600;700"
        "&display=swap"
    )

    # Copy
    PRODUCT_NAME   = "Navisignal"
    TAGLINE        = "Evidence. Structure. Action."
    SUB_TAGLINE    = "AI-enabled tech tools for complex environments."
    EMAIL          = "hello@navisignal.app"
    WEBSITE        = "https://navisignal.app"

    # Logo mark — SVG paths (56×36 viewBox)
    # Three signal-source dots converging through lines to a 4-pointed star, then an arrow.
    LOGO_SVG = """<svg width="{w}" height="{h}" viewBox="0 0 56 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="4" cy="9"  r="2.2" fill="{gold}" opacity="0.45"/>
  <circle cx="4" cy="18" r="2.2" fill="{gold}" opacity="0.75"/>
  <circle cx="4" cy="27" r="2.2" fill="{gold}" opacity="0.45"/>
  <line x1="6.2" y1="9"  x2="34" y2="18" stroke="{gold}" stroke-width="1"   stroke-linecap="round" opacity="0.45"/>
  <line x1="6.2" y1="18" x2="34" y2="18" stroke="{gold}" stroke-width="1.3" stroke-linecap="round" opacity="0.85"/>
  <line x1="6.2" y1="27" x2="34" y2="18" stroke="{gold}" stroke-width="1"   stroke-linecap="round" opacity="0.45"/>
  <path d="M34 12 L35.4 17.2 L34 18 L35.4 18.8 L34 24 L32.6 18.8 L34 18 L32.6 17.2 Z" fill="{gold}"/>
  <path d="M28 18 L32.6 17.2 L34 18 L32.6 18.8 L28 18 Z" fill="{gold}"/>
  <path d="M40 18 L35.4 17.2 L34 18 L35.4 18.8 L40 18 Z" fill="{gold}"/>
  <line x1="40" y1="18" x2="52" y2="18" stroke="{gold}" stroke-width="1.4" stroke-linecap="round"/>
  <polyline points="47,13.5 52,18 47,22.5" stroke="{gold}" stroke-width="1.4"
            stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>"""

    @classmethod
    def logo_svg(cls, width=56, height=36, gold=None):
        """Return the Navisignal logo mark as an SVG string."""
        return cls.LOGO_SVG.format(w=width, h=height, gold=gold or cls.GOLD)


# ── ReportLab color objects ───────────────────────────────────────────────────

class ReportLabColors:
    """
    Pre-built ReportLab HexColor objects.
    Requires: from reportlab.lib import colors
    """
    @staticmethod
    def _c(hex_str):
        from reportlab.lib import colors as _colors
        return _colors.HexColor(hex_str)

    @classmethod
    def palette(cls):
        """Return a dict of all brand colors as ReportLab HexColor objects."""
        return {
            "GOLD":         cls._c(Brand.GOLD),
            "DARK":         cls._c(Brand.BG),
            "SURFACE":      cls._c(Brand.SURFACE),
            "MUTED":        cls._c(Brand.TEXT_3),
            "TEXT_2":       cls._c(Brand.TEXT_2),
            "BORDER":       cls._c(Brand.BORDER),
            "NEAR_WHITE":   cls._c("#F4F7FB"),
            "AMBER_BG":     cls._c("#FDF8EE"),
            "BLUE_BG":      cls._c("#EDF1F8"),
            "GREEN":        cls._c(Brand.GREEN),
            "AMBER":        cls._c(Brand.AMBER),
            "RED":          cls._c(Brand.RED),
        }


# ── Streamlit CSS ─────────────────────────────────────────────────────────────

class CSS:
    """
    Ready-to-inject Streamlit CSS blocks.
    Call CSS.full_stylesheet() to get the complete CSS string,
    then inject with st.markdown(f"<style>{css}</style>", unsafe_allow_html=True).
    """

    @staticmethod
    def font_import():
        return f"@import url('{Brand.FONT_IMPORT}');"

    @staticmethod
    def base():
        return f"""
*, html, body {{
  font-family: {Brand.FONT_BODY} !important;
}}
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, section.main {{
  background-color: {Brand.BG} !important;
}}
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
header[data-testid="stHeader"],
#MainMenu, footer {{
  display: none !important;
  visibility: hidden !important;
}}
[data-testid="stMainBlockContainer"],
.block-container {{
  padding-top: 0 !important;
  max-width: 720px !important;
}}"""

    @staticmethod
    def widgets():
        return f"""
[data-testid="stWidgetLabel"] p {{
  color: {Brand.TEXT} !important;
  font-size: 13px !important;
  font-weight: 500 !important;
}}
[data-baseweb="select"] > div:first-child {{
  background-color: {Brand.SURFACE} !important;
  border: 1px solid {Brand.BORDER} !important;
  border-radius: 6px !important;
}}
[data-baseweb="select"] > div:first-child:hover {{
  border-color: {Brand.BORDER_HOVER} !important;
}}
[data-baseweb="select"] span,
[data-baseweb="select"] > div > div > div {{
  color: {Brand.TEXT} !important;
  font-size: 13px !important;
}}
[data-baseweb="select"] svg {{ fill: {Brand.TEXT_3} !important; }}
[data-baseweb="popover"],
[data-baseweb="popover"] > div {{
  background-color: {Brand.SURFACE} !important;
  border: 1px solid {Brand.BORDER} !important;
  border-radius: 6px !important;
  box-shadow: 0 8px 32px rgba(0,0,0,0.6) !important;
}}
[data-baseweb="menu"] {{ background-color: {Brand.SURFACE} !important; }}
[data-baseweb="menu"] li {{
  background-color: {Brand.SURFACE} !important;
  color: {Brand.TEXT} !important;
  font-size: 13px !important;
}}
[data-baseweb="menu"] li:hover {{ background-color: {Brand.BORDER} !important; }}
[data-baseweb="menu"] [aria-selected="true"] {{
  background-color: {Brand.GOLD_SUBTLE} !important;
  color: {Brand.GOLD} !important;
}}
[data-testid="stTextInput"] input,
input[type="password"] {{
  background-color: {Brand.SURFACE} !important;
  border: 1px solid {Brand.BORDER} !important;
  border-radius: 6px !important;
  color: {Brand.TEXT} !important;
  font-size: 13px !important;
  padding: 10px 14px !important;
}}
[data-testid="stTextInput"] input:focus {{
  border-color: {Brand.GOLD} !important;
  box-shadow: 0 0 0 3px rgba(201,168,76,0.25) !important;
}}"""

    @staticmethod
    def buttons():
        return f"""
.stButton > button {{
  background: {Brand.GOLD} !important;
  color: #fff !important;
  border: 1px solid {Brand.GOLD} !important;
  border-radius: 6px !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  letter-spacing: 0.02em !important;
  padding: 10px 22px !important;
  transition: background 150ms ease !important;
}}
.stButton > button:hover:not(:disabled) {{
  background: {Brand.GOLD_HOVER} !important;
  border-color: {Brand.GOLD_HOVER} !important;
}}
.stButton > button:disabled {{
  background: transparent !important;
  color: {Brand.TEXT_3} !important;
  border-color: {Brand.BORDER} !important;
}}
[data-testid="stDownloadButton"] > button {{
  background: {Brand.GOLD} !important;
  color: #fff !important;
  border: 1px solid {Brand.GOLD} !important;
  border-radius: 6px !important;
  font-weight: 700 !important;
}}
[data-testid="stDownloadButton"] > button:hover {{
  background: {Brand.GOLD_HOVER} !important;
  border-color: {Brand.GOLD_HOVER} !important;
}}"""

    @staticmethod
    def sidebar():
        return f"""
[data-testid="stSidebar"] {{
  background-color: {Brand.SIDEBAR} !important;
  border-right: 1px solid {Brand.BORDER} !important;
}}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] span {{
  color: {Brand.TEXT_2} !important;
  font-size: 12px !important;
  line-height: 1.7 !important;
}}
[data-testid="stSidebar"] strong {{ color: {Brand.TEXT} !important; }}
[data-testid="stSidebar"] a {{
  color: {Brand.GOLD} !important;
  text-decoration: none !important;
  font-weight: 600 !important;
}}
[data-testid="stSidebar"] hr {{ border-color: {Brand.BORDER} !important; }}"""

    @staticmethod
    def misc():
        return f"""
[data-testid="stCheckbox"] label p,
[data-testid="stCheckbox"] label span {{
  color: {Brand.TEXT_2} !important;
  font-size: 13px !important;
}}
[data-testid="stExpander"] {{
  border: 1px solid {Brand.BORDER} !important;
  border-radius: 6px !important;
  background: {Brand.SURFACE} !important;
}}
[data-testid="stExpander"] details > summary {{
  background-color: {Brand.SURFACE} !important;
  color: {Brand.TEXT_2} !important;
  font-size: 12px !important;
  font-weight: 600 !important;
}}
[data-testid="stExpander"] > div > div {{
  background-color: {Brand.BG} !important;
  border-top: 1px solid {Brand.BORDER} !important;
}}
[data-testid="stExpander"] p,
[data-testid="stExpander"] li {{
  color: {Brand.TEXT_2} !important;
  font-size: 12px !important;
}}
hr {{ border: none !important; border-top: 1px solid {Brand.BORDER} !important; }}
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {Brand.BG}; }}
::-webkit-scrollbar-thumb {{ background: {Brand.BORDER}; border-radius: 3px; }}"""

    @classmethod
    def full_stylesheet(cls):
        """Return the complete CSS string ready for injection."""
        return "\n".join([
            cls.font_import(),
            cls.base(),
            cls.widgets(),
            cls.buttons(),
            cls.sidebar(),
            cls.misc(),
        ])


# ── HTML snippet helpers ──────────────────────────────────────────────────────

class HTML:
    """
    Reusable branded HTML snippets for Streamlit markdown injection.
    All methods return strings safe for st.markdown(..., unsafe_allow_html=True).
    """

    @staticmethod
    def section_label(text: str) -> str:
        """Gold uppercase label — e.g. 'ASSESSMENT COMPLETE'"""
        return (
            f'<div style="font-size:11px;font-weight:600;letter-spacing:0.18em;'
            f'text-transform:uppercase;color:{Brand.GOLD};margin-bottom:6px;">'
            f'{text}</div>'
        )

    @staticmethod
    def page_title(text: str) -> str:
        """Large Space Grotesk display heading."""
        return (
            f'<h1 style="font-family:{Brand.FONT_DISPLAY};font-size:28px;'
            f'color:{Brand.TEXT};line-height:1.2;margin-bottom:6px;font-weight:400;">'
            f'{text}</h1>'
        )

    @staticmethod
    def subtitle(text: str) -> str:
        """Muted body subtitle."""
        return (
            f'<p style="font-size:13px;color:{Brand.TEXT_2};'
            f'line-height:1.6;margin-bottom:24px;">{text}</p>'
        )

    @staticmethod
    def card(content: str, border_left_color: str = None) -> str:
        """Surface card with optional left accent border."""
        border = (
            f'border-left:3px solid {border_left_color};'
            if border_left_color else f'border:1px solid {Brand.BORDER};'
        )
        return (
            f'<div style="background:{Brand.SURFACE};{border}'
            f'border-radius:6px;padding:16px 18px;">'
            f'{content}</div>'
        )

    @staticmethod
    def pill(text: str) -> str:
        """Gold-tinted pill / tag chip."""
        return (
            f'<span style="display:inline-block;padding:3px 10px;border-radius:9999px;'
            f'font-size:10px;font-weight:600;letter-spacing:0.05em;'
            f'background:{Brand.GOLD_SUBTLE};color:{Brand.GOLD};margin:2px 4px 2px 0;">'
            f'{text}</span>'
        )

    @staticmethod
    def app_header(tool_name: str, subtitle: str = "") -> str:
        """Full branded app header bar matching the Navisignal nav style."""
        logo = Brand.logo_svg(width=42, height=26)
        sub_html = (
            f'<div style="font-size:10px;color:{Brand.TEXT_3};margin-top:2px;'
            f'letter-spacing:0.04em;">{subtitle}</div>'
            if subtitle else ""
        )
        return (
            f'<div style="border-bottom:1px solid {Brand.BORDER};padding:14px 0;'
            f'display:flex;align-items:center;justify-content:space-between;">'
            f'<div style="display:flex;align-items:center;gap:10px;">'
            f'{logo}'
            f'<span style="font-family:{Brand.FONT_DISPLAY};font-size:14px;font-weight:600;'
            f'letter-spacing:0.12em;text-transform:uppercase;color:{Brand.TEXT};">'
            f'{Brand.PRODUCT_NAME}</span>'
            f'<span style="font-size:10px;font-weight:600;letter-spacing:0.1em;'
            f'text-transform:uppercase;color:{Brand.GOLD};'
            f'border:1px solid rgba(201,168,76,0.4);border-radius:9999px;padding:2px 8px;">Beta</span>'
            f'</div>'
            f'<div style="text-align:right;">'
            f'<div style="font-family:{Brand.FONT_DISPLAY};font-size:13px;color:{Brand.TEXT};">'
            f'{tool_name}</div>'
            f'{sub_html}'
            f'</div></div>'
        )

    @staticmethod
    def footer() -> str:
        """Branded page footer with tagline and contact links."""
        return (
            f'<div style="border-top:1px solid {Brand.BORDER};padding:28px 0 40px;'
            f'text-align:center;line-height:1.7;">'
            f'<div style="font-size:12px;color:{Brand.TEXT_3};margin-bottom:4px;">'
            f'A product of <strong style="color:{Brand.TEXT_2};">{Brand.PRODUCT_NAME}</strong>'
            f' — {Brand.SUB_TAGLINE}</div>'
            f'<div style="display:flex;align-items:center;justify-content:center;'
            f'gap:12px;margin-top:8px;flex-wrap:wrap;">'
            f'<a href="{Brand.WEBSITE}" target="_blank" '
            f'style="color:{Brand.GOLD};text-decoration:none;font-weight:600;font-size:12px;">'
            f'navisignal.app</a>'
            f'<span style="color:{Brand.TEXT_3};font-size:12px;">&middot;</span>'
            f'<a href="mailto:{Brand.EMAIL}" '
            f'style="color:{Brand.GOLD};text-decoration:none;font-weight:600;font-size:12px;">'
            f'{Brand.EMAIL}</a></div>'
            f'<div style="margin-top:12px;font-size:10px;color:{Brand.TEXT_3};'
            f'letter-spacing:0.12em;text-transform:uppercase;">{Brand.TAGLINE}</div>'
            f'</div>'
        )
