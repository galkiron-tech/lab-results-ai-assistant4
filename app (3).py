import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MedExplain AI | מערכת AI להסבר תוצאות בדיקות דם",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# DESIGN TOKENS (hardcoded — no CSS vars)
# ─────────────────────────────────────────────
C = {
    "bg_page":      "#EFF6FB",
    "bg_card":      "#FFFFFF",
    "bg_sidebar":   "#F0F7F4",
    "teal":         "#1A9882",
    "teal_l":       "#E6F4F1",
    "blue":         "#2B7BB9",
    "blue_l":       "#EAF3FB",
    "green":        "#2E9E5B",
    "green_bg":     "#E8F7EE",
    "yellow":       "#C78A00",
    "yellow_bg":    "#FFF8E1",
    "red":          "#C0392B",
    "red_bg":       "#FDECEA",
    "text":         "#1C2B39",
    "muted":        "#5D7A8A",
    "border":       "#D6E8F0",
}

# ─────────────────────────────────────────────
# GLOBAL CSS — RTL + BASE STYLES
# ─────────────────────────────────────────────
GLOBAL_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {{
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Assistant', 'Segoe UI', Arial, sans-serif !important;
    background-color: {C['bg_page']} !important;
    color: {C['text']} !important;
}}
section[data-testid="stSidebar"] {{
    direction: rtl !important;
    text-align: right !important;
    background: {C['bg_sidebar']} !important;
    border-left: 2px solid {C['border']} !important;
    border-right: none !important;
}}
section[data-testid="stSidebar"] * {{
    direction: rtl !important;
    text-align: right !important;
}}
h1, h2, h3, h4, h5, h6 {{
    direction: rtl !important;
    text-align: right !important;
    color: {C['text']} !important;
    font-family: 'Assistant', sans-serif !important;
}}
p, label, span, div, li, td, th {{
    direction: rtl !important;
    text-align: right !important;
}}
.stSelectbox label, .stRadio label, .stSlider label,
.stTextArea label, .stTextInput label, .stCheckbox label {{
    direction: rtl !important;
    text-align: right !important;
    font-weight: 600 !important;
}}
.stRadio > div {{ direction: rtl !important; }}
.stButton > button {{
    direction: rtl !important;
    background: {C['teal']} !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.4rem !important;
    font-family: 'Assistant', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
}}
.stButton > button:hover {{ background: #157A6A !important; }}
details {{ direction: rtl !important; }}
summary {{ direction: rtl !important; text-align: right !important; }}
.stTabs [data-baseweb="tab-list"] {{ direction: rtl !important; gap: 6px !important; }}
.stTabs [data-baseweb="tab"] {{
    direction: rtl !important;
    font-family: 'Assistant', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
}}
[data-testid="metric-container"] {{ direction: rtl !important; text-align: right !important; }}
.stAlert {{ direction: rtl !important; text-align: right !important; border-radius: 8px !important; }}
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
.stDeployButton {{display: none;}}

/* ── Lab table (spacious) ── */
.lab-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 8px;
    direction: rtl;
    text-align: right;
    font-family: 'Assistant', sans-serif;
}}
.lab-table th {{
    background: #EEF5FB;
    color: {C['muted']};
    font-size: 0.85rem;
    font-weight: 700;
    padding: 0.6rem 1.1rem;
    text-align: right;
    border-bottom: 2px solid {C['border']};
    letter-spacing: 0.03em;
}}
.lab-table td {{
    background: {C['bg_card']};
    padding: 0.95rem 1.1rem;
    font-size: 1rem;
    vertical-align: middle;
    text-align: right;
}}
.lab-table tr td:first-child {{ border-radius: 0 8px 8px 0; }}
.lab-table tr td:last-child  {{ border-radius: 8px 0 0 8px; }}
.lab-row-normal td {{ border-right: 4px solid {C['green']}; }}
.lab-row-border  td {{ border-right: 4px solid {C['yellow']}; background: #FFFDF2; }}
.lab-row-abnorm  td {{ border-right: 4px solid {C['red']};   background: #FFF8F7; }}
.lab-test-name {{ font-weight: 700; font-size: 1.05rem; color: {C['text']}; }}
.lab-value {{ font-weight: 700; font-size: 1.1rem; }}
.lab-range {{ color: {C['muted']}; font-size: 0.9rem; }}

/* ── Compare table ── */
.compare-table {{
    width: 100%;
    border-collapse: collapse;
    direction: rtl;
    text-align: right;
    font-size: 0.93rem;
    font-family: 'Assistant', sans-serif;
}}
.compare-table th {{
    background: {C['teal']};
    color: white;
    padding: 0.75rem 1rem;
    font-weight: 700;
    text-align: right;
}}
.compare-table td {{
    padding: 0.75rem 1rem;
    border-bottom: 1px solid {C['border']};
    text-align: right;
    vertical-align: top;
    background: white;
}}
.compare-table tr:nth-child(even) td {{ background: #F7FBFD; }}
.compare-good {{ color: {C['green']}; font-weight: 700; }}
.compare-bad  {{ color: {C['red']};   font-weight: 600; }}
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# INLINE-STYLE CARD HELPERS
# All cards use direct inline styles — no CSS class dependencies
# ─────────────────────────────────────────────

def card(content, border_color=None, bg=None, extra_style=""):
    bg = bg or C["bg_card"]
    border = f"border-right: 4px solid {border_color};" if border_color else ""
    return f"""
<div style="background:{bg};border-radius:14px;box-shadow:0 2px 12px rgba(0,0,0,0.07);
padding:1.4rem 1.6rem;margin-bottom:1rem;direction:rtl;text-align:right;{border}{extra_style}">
{content}
</div>"""

def card_teal(content):
    return f"""
<div style="background:{C['teal_l']};border-right:4px solid {C['teal']};border-radius:14px;
padding:1.2rem 1.4rem;margin-bottom:0.8rem;direction:rtl;text-align:right;">
{content}
</div>"""

def card_blue(content):
    return f"""
<div style="background:{C['blue_l']};border-right:4px solid {C['blue']};border-radius:14px;
padding:1.2rem 1.4rem;margin-bottom:0.8rem;direction:rtl;text-align:right;">
{content}
</div>"""

def disclaimer(content):
    return f"""
<div style="background:#FFF8E1;border:1.5px solid #F0C930;border-radius:8px;
padding:0.8rem 1.1rem;font-size:0.88rem;color:#7A5800;direction:rtl;text-align:right;margin-bottom:1rem;">
{content}
</div>"""

def page_hero(icon, title, subtitle, grad="135deg, #1A9882 0%, #2B7BB9 100%"):
    return f"""
<div style="background:linear-gradient({grad});border-radius:14px;padding:1.8rem 2.2rem;
color:white;margin-bottom:1.4rem;direction:rtl;text-align:right;">
<h1 style="color:white;font-size:1.9rem;margin:0 0 0.35rem 0;font-family:'Assistant',sans-serif;">{icon} {title}</h1>
<p style="color:rgba(255,255,255,0.88);margin:0;font-size:1rem;">{subtitle}</p>
</div>"""

def patient_header(icon, name, age, sex, context, label):
    return f"""
<div style="background:linear-gradient(135deg,#1A9882 0%,#2B7BB9 100%);border-radius:14px;
padding:1.6rem 2rem;color:white;margin-bottom:1.2rem;direction:rtl;text-align:right;">
<h2 style="color:white;margin:0 0 0.3rem 0;font-size:1.7rem;font-family:'Assistant',sans-serif;">{icon} {name}</h2>
<p style="color:rgba(255,255,255,0.88);margin:0;font-size:1rem;">גיל: {age} &nbsp;|&nbsp; מין: {sex} &nbsp;|&nbsp; הקשר: {context}</p>
<p style="color:rgba(255,255,255,0.75);margin:0.4rem 0 0 0;font-size:0.87rem;">תרחיש: {label}</p>
</div>"""

def badge_html(status):
    styles = {
        "תקין":  (C["green_bg"], C["green"],  "🟢 תקין"),
        "גבולי": (C["yellow_bg"],C["yellow"], "🟡 גבולי"),
        "חריג":  (C["red_bg"],   C["red"],    "🔴 חריג"),
    }
    bg, color, label = styles.get(status, (C["green_bg"], C["green"], status))
    return (f'<span style="display:inline-block;padding:0.28rem 0.85rem;border-radius:20px;'
            f'font-size:0.88rem;font-weight:700;background:{bg};color:{color};">{label}</span>')

def metric_cards(counts):
    def mc(n, label, bg, color):
        return (f'<div style="flex:1;background:white;border-radius:14px;'
                f'box-shadow:0 2px 12px rgba(0,0,0,0.07);padding:1rem 1.2rem;text-align:center;">'
                f'<div style="font-size:2.2rem;font-weight:800;color:{color};line-height:1.1;">{n}</div>'
                f'<div style="font-size:0.9rem;color:{C["muted"]};margin-top:0.2rem;">{label}</div></div>')
    return (f'<div style="display:flex;gap:1rem;margin-bottom:1.2rem;direction:rtl;">'
            f'{mc(counts["תקין"],  "🟢 תקינים",  C["green_bg"],  C["green"])}'
            f'{mc(counts["גבולי"], "🟡 גבוליים", C["yellow_bg"], C["yellow"])}'
            f'{mc(counts["חריג"],  "🔴 חריגים",  C["red_bg"],    C["red"])}'
            f'</div>')

def question_card(q):
    return (f'<div style="background:{C["blue_l"]};border-right:3px solid {C["blue"]};'
            f'border-radius:8px;padding:0.75rem 1rem;margin-bottom:0.5rem;font-size:0.97rem;'
            f'direction:rtl;text-align:right;color:{C["text"]};">❓ {q}</div>')

def contact_card(title, body):
    return (f'<div style="background:{C["teal_l"]};border-right:3px solid {C["teal"]};'
            f'border-radius:8px;padding:0.85rem 1.1rem;margin-bottom:0.5rem;'
            f'direction:rtl;text-align:right;">'
            f'<strong style="color:{C["teal"]};">{title}</strong><br>{body}</div>')

def never_item(text):
    return (f'<div style="background:{C["red_bg"]};border-right:3px solid {C["red"]};'
            f'border-radius:8px;padding:0.65rem 1rem;margin-bottom:0.4rem;font-size:0.95rem;'
            f'font-weight:600;color:{C["red"]};direction:rtl;text-align:right;">{text}</div>')

def always_item(text):
    return (f'<div style="background:{C["green_bg"]};border-right:3px solid {C["green"]};'
            f'border-radius:8px;padding:0.65rem 1rem;margin-bottom:0.4rem;font-size:0.95rem;'
            f'font-weight:600;color:{C["green"]};direction:rtl;text-align:right;">{text}</div>')

def step_card(icon, num, title, desc):
    return (f'<div style="background:white;border-radius:14px;box-shadow:0 2px 12px rgba(0,0,0,0.07);'
            f'padding:1.2rem 1.4rem;text-align:center;direction:rtl;">'
            f'<div style="font-size:2.2rem;margin-bottom:0.4rem;">{icon}</div>'
            f'<div style="font-size:0.75rem;font-weight:800;color:{C["teal"]};letter-spacing:0.1em;">{num}</div>'
            f'<div style="font-size:1rem;font-weight:700;color:{C["text"]};margin:0.3rem 0;">{title}</div>'
            f'<div style="font-size:0.88rem;color:{C["muted"]};line-height:1.5;">{desc}</div></div>')

def feature_card(icon, title, desc):
    return (f'<div style="background:white;border-radius:14px;box-shadow:0 2px 12px rgba(0,0,0,0.07);'
            f'padding:1.3rem 1.5rem;height:100%;direction:rtl;text-align:right;'
            f'border-top:3px solid {C["teal"]};">'
            f'<div style="font-size:1.8rem;margin-bottom:0.4rem;">{icon}</div>'
            f'<div style="font-size:1.05rem;font-weight:700;color:{C["text"]};margin-bottom:0.4rem;">{title}</div>'
            f'<div style="font-size:0.91rem;color:{C["muted"]};line-height:1.55;">{desc}</div></div>')

def privacy_card(icon, title, desc):
    return (f'<div style="background:white;border-radius:14px;box-shadow:0 2px 12px rgba(0,0,0,0.07);'
            f'padding:1.2rem 1.4rem;text-align:center;direction:rtl;margin-bottom:0.8rem;">'
            f'<div style="font-size:2rem;margin-bottom:0.4rem;">{icon}</div>'
            f'<div style="font-size:1rem;font-weight:700;color:{C["text"]};margin:0.3rem 0;">{title}</div>'
            f'<div style="font-size:0.88rem;color:{C["muted"]};line-height:1.5;">{desc}</div></div>')

def summary_box(text):
    return (f'<div style="background:{C["teal_l"]};border-radius:8px;padding:1rem 1.2rem;'
            f'font-size:1rem;color:{C["text"]};line-height:1.7;direction:rtl;text-align:right;'
            f'margin-bottom:0.8rem;">{text}</div>')

def divider():
    return f'<hr style="border:none;border-top:1.5px solid {C["border"]};margin:1.2rem 0;">'

def urgency_line(urgency, text):
    color = {"low": C["green"], "mid": C["yellow"], "high": C["red"]}.get(urgency, C["green"])
    icon  = {"low": "⚪", "mid": "🟡", "high": "🔴"}.get(urgency, "⚪")
    return f'<p style="color:{color};font-weight:700;margin:0.2rem 0;">{icon} {text}</p>'


# ─────────────────────────────────────────────
# LAB TABLE RENDERER
# ─────────────────────────────────────────────

def lab_row_style(status):
    styles = {
        "תקין":  (f"border-right:4px solid {C['green']};", "white"),
        "גבולי": (f"border-right:4px solid {C['yellow']};", "#FFFDF2"),
        "חריג":  (f"border-right:4px solid {C['red']};",   "#FFF8F7"),
    }
    return styles.get(status, (f"border-right:4px solid {C['green']};", "white"))

def render_lab_table(results):
    rows = ""
    for r in results:
        border, bg = lab_row_style(r["status"])
        rows += f"""
<tr>
  <td style="background:{bg};padding:0.95rem 1.1rem;{border}border-radius:0 8px 8px 0;vertical-align:middle;text-align:right;">
    <span style="font-weight:700;font-size:1.05rem;color:{C['text']};">{r['heb']}</span><br>
    <small style="color:{C['muted']};font-size:0.8rem;">{r['test']}</small>
  </td>
  <td style="background:{bg};padding:0.95rem 1.1rem;vertical-align:middle;text-align:right;">
    <span style="font-weight:700;font-size:1.1rem;">{r['value']}</span>
  </td>
  <td style="background:{bg};padding:0.95rem 1.1rem;vertical-align:middle;text-align:right;">
    <span style="color:{C['muted']};font-size:0.9rem;">{r['unit']}</span>
  </td>
  <td style="background:{bg};padding:0.95rem 1.1rem;vertical-align:middle;text-align:right;">
    <span style="color:{C['muted']};font-size:0.9rem;">{r['range']}</span>
  </td>
  <td style="background:{bg};padding:0.95rem 1.1rem;border-radius:8px 0 0 8px;vertical-align:middle;text-align:right;">
    {badge_html(r['status'])}
  </td>
</tr>"""
    return f"""
<div style="direction:rtl;overflow-x:auto;">
<table style="width:100%;border-collapse:separate;border-spacing:0 8px;direction:rtl;
text-align:right;font-family:'Assistant',sans-serif;">
<thead>
<tr>
  <th style="background:#EEF5FB;color:{C['muted']};font-size:0.85rem;font-weight:700;
  padding:0.6rem 1.1rem;text-align:right;border-bottom:2px solid {C['border']};">בדיקה</th>
  <th style="background:#EEF5FB;color:{C['muted']};font-size:0.85rem;font-weight:700;
  padding:0.6rem 1.1rem;text-align:right;border-bottom:2px solid {C['border']};">תוצאה</th>
  <th style="background:#EEF5FB;color:{C['muted']};font-size:0.85rem;font-weight:700;
  padding:0.6rem 1.1rem;text-align:right;border-bottom:2px solid {C['border']};">יחידות</th>
  <th style="background:#EEF5FB;color:{C['muted']};font-size:0.85rem;font-weight:700;
  padding:0.6rem 1.1rem;text-align:right;border-bottom:2px solid {C['border']};">טווח מקובל</th>
  <th style="background:#EEF5FB;color:{C['muted']};font-size:0.85rem;font-weight:700;
  padding:0.6rem 1.1rem;text-align:right;border-bottom:2px solid {C['border']};">סטטוס</th>
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>"""


# ─────────────────────────────────────────────
# PATIENT DATA — 12 SYNTHETIC SCENARIOS
# ─────────────────────────────────────────────
PATIENTS = [
    {
        "id": 1,
        "name": "מיכל כהן",
        "age": 34,
        "sex": "נקבה",
        "context": "בדיקת שגרה — ללא תסמינים",
        "scenario_label": "תוצאות תקינות לחלוטין",
        "results": [
            {"test": "WBC",         "heb": "ספירת לויקוציטים", "value": 6.2,  "unit": "10³/µL", "range": "4.5–11.0",  "status": "תקין"},
            {"test": "Hemoglobin",  "heb": "המוגלובין",        "value": 13.2, "unit": "g/dL",   "range": "12.0–16.0", "status": "תקין"},
            {"test": "Ferritin",    "heb": "פריטין",           "value": 42,   "unit": "ng/mL",  "range": "12–150",    "status": "תקין"},
            {"test": "HbA1c",       "heb": "HbA1c",            "value": 5.2,  "unit": "%",      "range": "< 5.7",     "status": "תקין"},
            {"test": "LDL",         "heb": "כולסטרול LDL",     "value": 88,   "unit": "mg/dL",  "range": "< 100",     "status": "תקין"},
        ],
        "summary": "כל תוצאות הבדיקות תקינות. אין ממצאים חריגים או גבוליים. ממצאים אלו תואמים לבדיקת שגרה תקינה.",
        "explanations": [],
        "contact": "ניתן להמשיך מעקב שגרתי עם רופא/ת המשפחה לפי המלצות הגיל והמצב הבריאותי.",
    },
    {
        "id": 2,
        "name": "אורי לוי",
        "age": 52,
        "sex": "זכר",
        "context": "מעקב כולסטרול — ללא טיפול תרופתי",
        "scenario_label": "LDL גבולי",
        "results": [
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 7.1,  "unit": "10³/µL", "range": "4.5–11.0",  "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 15.0, "unit": "g/dL",   "range": "13.5–17.5", "status": "תקין"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 5.4,  "unit": "%",      "range": "< 5.7",     "status": "תקין"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 118,  "unit": "mg/dL",  "range": "< 100",     "status": "גבולי"},
            {"test": "HDL",          "heb": "כולסטרול HDL",     "value": 48,   "unit": "mg/dL",  "range": "> 40",      "status": "תקין"},
            {"test": "Triglycerides","heb": "טריגליצרידים",      "value": 140,  "unit": "mg/dL",  "range": "< 150",     "status": "תקין"},
        ],
        "summary": "ערך ה-LDL נמצא מעט מעל הטווח המקובל וסווג כגבולי. שאר הבדיקות תקינות. ממצא זה ראוי לדיון עם רופא/ת המשפחה.",
        "explanations": [
            {
                "test_label": "כולסטרול LDL — 118 mg/dL",
                "badge": "גבולי",
                "badge_type": "yellow",
                "short_summary": "ערך ה-LDL גבולי מעט מעל הטווח — כדאי לדון עם רופא/ת המשפחה.",
                "what_is": "LDL הוא סוג של כולסטרול הקשור לסיכון מצטבר לבריאות כלי הדם והלב. המשמעות של הערך תלויה גם בגורמי סיכון אישיים ובבדיקות נוספות.",
                "why_different": ["תזונה עתירת שומן רווי", "גורמים גנטיים", "רמת פעילות גופנית", "גיל ומין"],
                "urgency": "low",
                "urgency_text": "לרוב לא דחוף, אך כדאי לדון עם רופא/ת המשפחה בהקדם הנוח.",
                "contact_text": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש מעקב, שינוי תזונתי, או בירור נוסף.",
                "questions": [
                    "מהו יעד ה-LDL המתאים עבורי לפי גורמי הסיכון האישיים שלי?",
                    "האם כדאי לבדוק גם HDL וטריגליצרידים בהרחבה?",
                    "האם שינוי תזונתי ופעילות גופנית עשויים להספיק בשלב זה?",
                    "מתי כדאי לחזור על פרופיל שומנים?",
                ],
            }
        ],
        "contact": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש מעקב, שינוי תזונתי, או בירור נוסף.",
    },
    {
        "id": 3,
        "name": "דנה אברהמי",
        "age": 47,
        "sex": "נקבה",
        "context": "מעקב כולסטרול — בעלת יתר לחץ דם",
        "scenario_label": "LDL מוגבר בבירור",
        "results": [
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 6.8,  "unit": "10³/µL", "range": "4.5–11.0",  "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 13.5, "unit": "g/dL",   "range": "12.0–16.0", "status": "תקין"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 5.5,  "unit": "%",      "range": "< 5.7",     "status": "תקין"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 158,  "unit": "mg/dL",  "range": "< 100",     "status": "חריג"},
            {"test": "HDL",          "heb": "כולסטרול HDL",     "value": 44,   "unit": "mg/dL",  "range": "> 50",      "status": "גבולי"},
            {"test": "Triglycerides","heb": "טריגליצרידים",      "value": 175,  "unit": "mg/dL",  "range": "< 150",     "status": "גבולי"},
        ],
        "summary": "ערך ה-LDL מוגבר בבירור מעל הטווח המקובל. גם HDL נמוך מעט וטריגליצרידים גבוליים. השילוב ראוי לדיון עם רופא/ת המשפחה בהקדם.",
        "explanations": [
            {
                "test_label": "כולסטרול LDL — 158 mg/dL",
                "badge": "חריג",
                "badge_type": "red",
                "short_summary": "ערך ה-LDL מוגבר בבירור — ממצא זה מצריך דיון עם רופא/ת המשפחה.",
                "what_is": "LDL הוא סוג של כולסטרול הקשור לסיכון מצטבר לבריאות כלי הדם והלב. המשמעות של הערך תלויה גם בגורמי סיכון אישיים כמו לחץ דם, גיל ובדיקות נוספות.",
                "why_different": ["גורמים גנטיים", "תזונה עתירת שומן רווי", "רמת פעילות גופנית נמוכה", "גורמי סיכון כלי-דמיים נוספים"],
                "urgency": "mid",
                "urgency_text": "מומלץ לדון עם רופא/ת המשפחה — ניתן לתאם תור בהקדם הנוח.",
                "contact_text": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש שינוי תזונתי, פעילות גופנית, טיפול תרופתי, או הפניה נוספת.",
                "questions": [
                    "מהו יעד ה-LDL המתאים עבורי, בהתחשב ביתר לחץ הדם?",
                    "האם השילוב של LDL, HDL וטריגליצרידים מצריך בירור נוסף?",
                    "האם שינוי תזונתי ופעילות גופנית יכולים להשפיע משמעותית בשלב זה?",
                    "מתי כדאי לחזור על פרופיל שומנים מלא?",
                    "האם יש גורמי סיכון נוספים שחשוב לקחת בחשבון יחד עם ה-LDL?",
                ],
            }
        ],
        "contact": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש שינוי תזונתי, טיפול תרופתי, או הפניה לרופא/ת לב.",
    },
    {
        "id": 4,
        "name": "יוסף מזרחי",
        "age": 58,
        "sex": "זכר",
        "context": "מעקב סוכר — HbA1c גבולי בבדיקה קודמת",
        "scenario_label": "HbA1c גבולי",
        "results": [
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 7.4,  "unit": "10³/µL", "range": "4.5–11.0",  "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 14.8, "unit": "g/dL",   "range": "13.5–17.5", "status": "תקין"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 6.1,  "unit": "%",      "range": "< 5.7",     "status": "גבולי"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 105,  "unit": "mg/dL",  "range": "< 100",     "status": "גבולי"},
            {"test": "Triglycerides","heb": "טריגליצרידים",      "value": 162,  "unit": "mg/dL",  "range": "< 150",     "status": "גבולי"},
        ],
        "summary": "ערך HbA1c גבולי בטווח המצריך מעקב. ניתן לראות גם LDL וטריגליצרידים גבוליים. השילוב ראוי לדיון עם רופא/ת המשפחה.",
        "explanations": [
            {
                "test_label": "HbA1c — 6.1%",
                "badge": "גבולי",
                "badge_type": "yellow",
                "short_summary": "ערך HbA1c גבולי — מצריך מעקב ודיון עם רופא/ת המשפחה.",
                "what_is": "HbA1c משקף את רמות הסוכר הממוצעות בדם במהלך כשלושה חודשים, ולכן הוא עוזר להבין מגמות ולא רק מדידת סוכר חד-פעמית. ערך בטווח 5.7–6.4 מסווג לרוב כגבולי ודורש מעקב.",
                "why_different": ["תזונה עשירה בפחמימות פשוטות", "ירידה ברמת הפעילות הגופנית", "גורמים גנטיים", "עלייה במשקל"],
                "urgency": "low",
                "urgency_text": "לרוב לא דחוף, אך כדאי לדון עם רופא/ת המשפחה בהקדם הנוח.",
                "contact_text": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש מעקב קרוב יותר, שינוי אורח חיים, או בירור נוסף.",
                "questions": [
                    "האם הערך השתנה לעומת הבדיקה הקודמת?",
                    "אילו שינויים באורח החיים עשויים להשפיע על הערך?",
                    "האם כדאי לבצע בדיקת מעקב בעוד מספר חודשים?",
                    "האם יש גורמי סיכון נוספים שכדאי לקחת בחשבון יחד עם ה-HbA1c?",
                    "האם השילוב של HbA1c, LDL וטריגליצרידים גבוליים מצריך בירור מרוכז יותר?",
                ],
            }
        ],
        "contact": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש מעקב קרוב יותר, שינוי אורח חיים, או הפניה לאנדוקרינולוג/ית.",
    },
    {
        "id": 5,
        "name": "רונית שפירו",
        "age": 62,
        "sex": "נקבה",
        "context": "בדיקת שגרה — היסטוריה משפחתית של סוכרת",
        "scenario_label": "HbA1c מוגבר",
        "results": [
            {"test": "WBC",        "heb": "ספירת לויקוציטים", "value": 7.9,  "unit": "10³/µL", "range": "4.5–11.0",  "status": "תקין"},
            {"test": "Hemoglobin", "heb": "המוגלובין",        "value": 12.8, "unit": "g/dL",   "range": "12.0–16.0", "status": "תקין"},
            {"test": "HbA1c",      "heb": "HbA1c",            "value": 7.2,  "unit": "%",      "range": "< 5.7",     "status": "חריג"},
            {"test": "LDL",        "heb": "כולסטרול LDL",     "value": 112,  "unit": "mg/dL",  "range": "< 100",     "status": "גבולי"},
        ],
        "summary": "ערך HbA1c מוגבר בבירור מעל הטווח המקובל. ממצא זה מצריך דיון עם רופא/ת המשפחה בהקדם. LDL גבולי.",
        "explanations": [
            {
                "test_label": "HbA1c — 7.2%",
                "badge": "חריג",
                "badge_type": "red",
                "short_summary": "ערך HbA1c מוגבר בבירור — ממצא זה מצריך דיון עם רופא/ת המשפחה.",
                "what_is": "HbA1c משקף את רמות הסוכר הממוצעות בדם במהלך כשלושה חודשים. ערך מעל 6.5 מסווג לרוב כדורש דיון עם רופא/ת המשפחה ובירור נוסף. משמעות הערך תלויה בהיסטוריה הרפואית האישית ובגורמים נוספים.",
                "why_different": ["שינויים בתזונה", "גורמים גנטיים ומשפחתיים", "רמת פעילות גופנית", "שינויים הורמונליים הקשורים לגיל"],
                "urgency": "mid",
                "urgency_text": "מומלץ לדון עם רופא/ת המשפחה — מומלץ לתאם תור בהקדם.",
                "contact_text": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרשות בדיקות נוספות, שינוי אורח חיים, או הפניה לאנדוקרינולוג/ית.",
                "questions": [
                    "כיצד הערך משתווה לבדיקות קודמות?",
                    "האם כדאי לבצע בדיקות נוספות להערכת רמות הסוכר?",
                    "אילו גורמי סיכון אישיים ומשפחתיים חשוב לקחת בחשבון?",
                    "מהו לוח הזמנים המתאים למעקב?",
                    "האם יש צורך בהפניה לרופא/ת מומחה/ית?",
                ],
            }
        ],
        "contact": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרשות בדיקות נוספות, שינוי אורח חיים, או הפניה לאנדוקרינולוג/ית.",
    },
    {
        "id": 6,
        "name": "עינב גרינברג",
        "age": 28,
        "sex": "נקבה",
        "context": "תזונה צמחונית — עייפות קלה",
        "scenario_label": "חסר ברזל קל — פריטין גבולי",
        "results": [
            {"test": "WBC",        "heb": "ספירת לויקוציטים", "value": 5.8,  "unit": "10³/µL", "range": "4.5–11.0",  "status": "תקין"},
            {"test": "Hemoglobin", "heb": "המוגלובין",        "value": 12.4, "unit": "g/dL",   "range": "12.0–16.0", "status": "תקין"},
            {"test": "Ferritin",   "heb": "פריטין",           "value": 14,   "unit": "ng/mL",  "range": "12–150",    "status": "גבולי"},
            {"test": "HbA1c",      "heb": "HbA1c",            "value": 5.1,  "unit": "%",      "range": "< 5.7",     "status": "תקין"},
        ],
        "summary": "ערך הפריטין גבולי — נמוך בתחתית הטווח התקין. שאר הבדיקות תקינות. בהקשר של תזונה צמחונית וחוויית עייפות קלה — ממצא זה ראוי לדיון עם רופא/ת המשפחה.",
        "explanations": [
            {
                "test_label": "פריטין — 14 ng/mL",
                "badge": "גבולי",
                "badge_type": "yellow",
                "short_summary": "ערך פריטין גבולי-נמוך — כדאי לדון עם רופא/ת המשפחה, במיוחד בהקשר תזונתי.",
                "what_is": "פריטין הוא חלבון שמאחסן ברזל בגוף. הערך משקף את מאגרי הברזל, ולעיתים יכול לרדת עוד לפני שמופיעה ירידה משמעותית בהמוגלובין.",
                "why_different": ["תזונה צמחונית עם ספיגת ברזל מוגבלת", "מחזוריות אצל נשים", "צורך מוגבר בברזל", "ספיגה ירודה של ברזל"],
                "urgency": "low",
                "urgency_text": "לרוב לא דחוף, אך כדאי לדון עם רופא/ת המשפחה.",
                "contact_text": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרשות בדיקות השלמה, שינוי תזונתי, או מעקב.",
                "questions": [
                    "האם התזונה הצמחונית שלי יכולה להסביר את רמת הפריטין?",
                    "האם כדאי לבדוק גם ברזל, טרנספרין או סטורציית טרנספרין?",
                    "האם יש צורך במעקב אחר המוגלובין?",
                    "מתי כדאי לחזור על הבדיקה?",
                    "האם ישנם מקורות תזונה מומלצים שיכולים לשפר את הספיגה?",
                ],
            }
        ],
        "contact": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרשות בדיקות השלמה, תוסף תזונתי, או מעקב.",
    },
    {
        "id": 7,
        "name": "תמר אלון",
        "age": 35,
        "sex": "נקבה",
        "context": "חולשה כללית וסחרחורת — בדיקת דם ראשונית",
        "scenario_label": "חסר ברזל משמעותי — פריטין ירוד והמוגלובין נמוך",
        "results": [
            {"test": "WBC",        "heb": "ספירת לויקוציטים", "value": 6.0,  "unit": "10³/µL", "range": "4.5–11.0",  "status": "תקין"},
            {"test": "Hemoglobin", "heb": "המוגלובין",        "value": 10.8, "unit": "g/dL",   "range": "12.0–16.0", "status": "חריג"},
            {"test": "Ferritin",   "heb": "פריטין",           "value": 5,    "unit": "ng/mL",  "range": "12–150",    "status": "חריג"},
            {"test": "HbA1c",      "heb": "HbA1c",            "value": 5.0,  "unit": "%",      "range": "< 5.7",     "status": "תקין"},
        ],
        "summary": "המוגלובין ירוד בבירור מתחת לטווח התקין, ופריטין ירוד מאוד. תבנית זו ראויה לדיון עם רופא/ת המשפחה בהקדם. התסמינים שצוינו — חולשה וסחרחורת — יכולים להיות קשורים לממצאים.",
        "explanations": [
            {
                "test_label": "המוגלובין — 10.8 g/dL ופריטין — 5 ng/mL",
                "badge": "חריג",
                "badge_type": "red",
                "short_summary": "המוגלובין ופריטין ירודים בבירור — ממצא זה מצריך דיון עם רופא/ת המשפחה.",
                "what_is": "המוגלובין הוא חלבון בתאי הדם האדומים שנושא חמצן מהריאות אל רקמות הגוף. ערך נמוך יכול להסביר לעיתים עייפות, חולשה או קוצר נשימה. פריטין הוא חלבון שמאחסן ברזל בגוף, והערך הנמוך מצביע על מאגרי ברזל נמוכים.",
                "why_different": ["מאגרי ברזל נמוכים (כפי שמשתקף בפריטין)", "ספיגה ירודה של ברזל", "אבדן דם", "צורך מוגבר בברזל"],
                "urgency": "mid",
                "urgency_text": "כדאי לשקול פנייה מוקדמת יותר לרופא/ת המשפחה.",
                "contact_text": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרשות בדיקות נוספות ובירור הסיבה.",
                "questions": [
                    "האם דפוס הבדיקות — המוגלובין ופריטין ירודים יחד — יכול להתאים לחסר ברזל?",
                    "האם כדאי לבדוק גורמים אפשריים לאיבוד דם או ספיגה נמוכה?",
                    "האם יש צורך בבדיקות נוספות כמו B12 או חומצה פולית?",
                    "מהו לוח הזמנים המתאים למעקב?",
                    "האם התסמינים שלי — חולשה וסחרחורת — יכולים להיות קשורים לממצאים?",
                ],
            }
        ],
        "contact": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרשות בדיקות נוספות, הפניה להמטולוג/ית, או טיפול.",
    },
    {
        "id": 8,
        "name": "גיל בן דוד",
        "age": 41,
        "sex": "זכר",
        "context": "מחלה ויראלית לאחרונה — נבדק שבועיים לאחר החלמה",
        "scenario_label": "לויקוציטוזיס קל לאחר מחלה",
        "results": [
            {"test": "WBC",        "heb": "ספירת לויקוציטים", "value": 11.4, "unit": "10³/µL", "range": "4.5–11.0",  "status": "גבולי"},
            {"test": "Hemoglobin", "heb": "המוגלובין",        "value": 15.2, "unit": "g/dL",   "range": "13.5–17.5", "status": "תקין"},
            {"test": "Ferritin",   "heb": "פריטין",           "value": 88,   "unit": "ng/mL",  "range": "12–150",    "status": "תקין"},
            {"test": "LDL",        "heb": "כולסטרול LDL",     "value": 95,   "unit": "mg/dL",  "range": "< 100",     "status": "תקין"},
        ],
        "summary": "ספירת לויקוציטים (WBC) גבולית מעט מעל הטווח. בהקשר של מחלה ויראלית לאחרונה — ייתכן שהממצא קשור להחלמה. שאר הבדיקות תקינות.",
        "explanations": [
            {
                "test_label": "WBC — 11.4 10³/µL",
                "badge": "גבולי",
                "badge_type": "yellow",
                "short_summary": "ספירת לויקוציטים גבולית — ייתכן שקשורה למחלה הויראלית האחרונה.",
                "what_is": "בדיקת WBC מודדת את מספר תאי הדם הלבנים בדם. תאים אלו הם חלק ממערכת החיסון ועוזרים לגוף להגיב לזיהומים, דלקות ומצבים נוספים.",
                "why_different": ["תגובת מערכת החיסון למחלה ויראלית לאחרונה", "שלב החלמה מזיהום", "מתח פיזי", "גורמים נוספים הדורשים הערכה רפואית"],
                "urgency": "low",
                "urgency_text": "לרוב לא דחוף, אך כדאי לעדכן את רופא/ת המשפחה.",
                "contact_text": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש מעקב או בדיקה חוזרת.",
                "questions": [
                    "האם העלייה יכולה להתאים למחלה שהייתה לי לאחרונה?",
                    "האם כדאי להשוות את התוצאה לבדיקות קודמות?",
                    "האם יש צורך לחזור על ספירת הדם בעוד מספר שבועות?",
                    "האם CRP או מדדי דלקת אחרים יכולים לעזור להבין את התמונה?",
                ],
            }
        ],
        "contact": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש מעקב, בדיקה חוזרת, או בירור נוסף.",
    },
    {
        "id": 9,
        "name": "אמיר חסן",
        "age": 45,
        "sex": "זכר",
        "context": "חום וכאבים בגוף — נבדק לצורך בירור",
        "scenario_label": "לויקוציטוזיס עם CRP מוגבר",
        "results": [
            {"test": "WBC",        "heb": "ספירת לויקוציטים", "value": 14.8, "unit": "10³/µL", "range": "4.5–11.0",  "status": "חריג"},
            {"test": "Hemoglobin", "heb": "המוגלובין",        "value": 14.0, "unit": "g/dL",   "range": "13.5–17.5", "status": "תקין"},
            {"test": "CRP",        "heb": "CRP",              "value": 38,   "unit": "mg/L",   "range": "< 5",       "status": "חריג"},
        ],
        "summary": "WBC מוגבר בבירור ו-CRP גבוה מצביעים על תגובה דלקתית. בהקשר של חום וכאבים — ממצאים אלו מצריכים דיון עם רופא/ת המשפחה בהקדם.",
        "explanations": [
            {
                "test_label": "WBC — 14.8 10³/µL ו-CRP — 38 mg/L",
                "badge": "חריג",
                "badge_type": "red",
                "short_summary": "WBC מוגבר בשילוב CRP גבוה — ממצא זה מצריך דיון עם רופא/ת המשפחה בהקדם.",
                "what_is": "בדיקת WBC מודדת את מספר תאי הדם הלבנים בדם. תאים אלו הם חלק ממערכת החיסון ועוזרים לגוף להגיב לזיהומים, דלקות ומצבים נוספים. CRP הוא חלבון שעולה בתגובה לדלקת בגוף.",
                "why_different": ["זיהום חיידקי", "זיהום ויראלי", "תגובה דלקתית", "מצבים נוספים הדורשים הערכה רפואית"],
                "urgency": "mid",
                "urgency_text": "מומלץ לדון עם רופא/ת המשפחה — מומלץ לתאם תור בהקדם.",
                "contact_text": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש בירור נוסף או טיפול.",
                "questions": [
                    "האם השילוב של WBC ו-CRP מצריך בירור נוסף?",
                    "האם התסמינים שלי — חום וכאבים — מתאימים לממצאים?",
                    "האם יש צורך בבדיקות נוספות או בטיפול מיידי?",
                    "מתי כדאי לחזור על הבדיקות?",
                    "האם מקור הדלקת ידוע, ואם לא — מה הצעד הבא?",
                ],
            }
        ],
        "contact": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש טיפול, בדיקות נוספות, או הפניה לגורם מתאים.",
    },
    {
        "id": 10,
        "name": "נועה ביטון",
        "age": 39,
        "sex": "נקבה",
        "context": "עייפות כרונית — בדיקה ראשונית",
        "scenario_label": "CRP מוגבר — מדד דלקתי",
        "results": [
            {"test": "WBC",        "heb": "ספירת לויקוציטים", "value": 8.2,  "unit": "10³/µL", "range": "4.5–11.0",  "status": "תקין"},
            {"test": "Hemoglobin", "heb": "המוגלובין",        "value": 12.6, "unit": "g/dL",   "range": "12.0–16.0", "status": "תקין"},
            {"test": "Ferritin",   "heb": "פריטין",           "value": 22,   "unit": "ng/mL",  "range": "12–150",    "status": "תקין"},
            {"test": "CRP",        "heb": "CRP",              "value": 18,   "unit": "mg/L",   "range": "< 5",       "status": "חריג"},
            {"test": "HbA1c",      "heb": "HbA1c",            "value": 5.3,  "unit": "%",      "range": "< 5.7",     "status": "תקין"},
        ],
        "summary": "ערך CRP מוגבר — מדד דלקתי. שאר הבדיקות תקינות. בהקשר של עייפות כרונית — ממצא זה ראוי לדיון עם רופא/ת המשפחה.",
        "explanations": [
            {
                "test_label": "CRP — 18 mg/L",
                "badge": "חריג",
                "badge_type": "red",
                "short_summary": "CRP מוגבר — מדד דלקתי שיכול להעיד על תגובה דלקתית בגוף.",
                "what_is": "CRP הוא חלבון המיוצר בכבד ורמתו עולה בתגובה לדלקת, זיהום, או מצבים אחרים בגוף. ערכו יכול לסייע בהערכת תהליכים שונים, אך פירושו המדויק תלוי בהקשר הקליני.",
                "why_different": ["תהליך דלקתי בגוף", "זיהום", "מצבים אוטואימוניים", "גורמים נוספים הדורשים הערכה רפואית"],
                "urgency": "mid",
                "urgency_text": "מומלץ לדון עם רופא/ת המשפחה — מומלץ לתאם תור בהקדם הנוח.",
                "contact_text": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש בירור נוסף, ואם כן — מאיזה סוג.",
                "questions": [
                    "מה יכול להסביר את העלייה ב-CRP בהקשר של העייפות שלי?",
                    "האם יש צורך בבדיקות נוספות כדי להבין את מקור הדלקת?",
                    "האם יש קשר אפשרי בין ה-CRP לתסמינים שלי?",
                    "מתי כדאי לחזור על הבדיקה?",
                    "האם יש גורמי סיכון שכדאי לבדוק?",
                ],
            }
        ],
        "contact": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרשות בדיקות נוספות לאיתור מקור הדלקת.",
    },
    {
        "id": 11,
        "name": "שרה ואנג",
        "age": 55,
        "sex": "נקבה",
        "context": "בדיקת שגרה — מעקב לאחר שינוי תזונתי",
        "scenario_label": "ממצאים גבוליים מעורבים",
        "results": [
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 9.8,  "unit": "10³/µL", "range": "4.5–11.0",  "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 11.9, "unit": "g/dL",   "range": "12.0–16.0", "status": "גבולי"},
            {"test": "Ferritin",     "heb": "פריטין",           "value": 16,   "unit": "ng/mL",  "range": "12–150",    "status": "גבולי"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 5.9,  "unit": "%",      "range": "< 5.7",     "status": "גבולי"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 122,  "unit": "mg/dL",  "range": "< 100",     "status": "גבולי"},
            {"test": "Triglycerides","heb": "טריגליצרידים",      "value": 148,  "unit": "mg/dL",  "range": "< 150",     "status": "תקין"},
        ],
        "summary": "מספר ממצאים גבוליים: המוגלובין, פריטין, HbA1c ו-LDL — כולם בתחתית הטווח הגבולי. מומלץ לדון עם רופא/ת המשפחה על כל הממצאים יחד.",
        "explanations": [
            {
                "test_label": "ממצאים גבוליים מרובים",
                "badge": "גבולי",
                "badge_type": "yellow",
                "short_summary": "מספר ממצאים גבוליים — כדאי לדון עם רופא/ת המשפחה על התמונה הכוללת.",
                "what_is": "המוגלובין הוא חלבון בתאי הדם האדומים שנושא חמצן. פריטין משקף מאגרי ברזל. HbA1c מודד ממוצע סוכר לאורך שלושה חודשים. LDL הוא כולסטרול הקשור לבריאות כלי הדם. כל אחד מהם גבולי בנפרד, אך ביחד כדאי לראות את התמונה הכוללת.",
                "why_different": ["שינוי תזונתי לאחרונה", "מאגרי ברזל נמוכים", "גורמים גנטיים", "רמת פעילות גופנית"],
                "urgency": "low",
                "urgency_text": "לרוב לא דחוף, אך כדאי לדון עם רופא/ת המשפחה.",
                "contact_text": "רופא/ת המשפחה יוכל/תוכל לראות את התמונה הכוללת ולהחליט מה הצעד הבא.",
                "questions": [
                    "האם יש קשר בין הממצאים השונים — המוגלובין, פריטין, HbA1c ו-LDL?",
                    "אילו ממצאים חשובים יותר למעקב בשלב זה?",
                    "האם כדאי לחזור על כל הבדיקות או רק על חלק מהן?",
                    "האם יש שינוי באורח החיים שיכול להשפיע על כמה מהערכים יחד?",
                    "האם השינוי התזונתי שביצעתי לאחרונה יכול להסביר חלק מהממצאים?",
                ],
            }
        ],
        "contact": "רופא/ת המשפחה יוכל/תוכל לראות את התמונה הכוללת ולהחליט מה הצעד הבא.",
    },
    {
        "id": 12,
        "name": "דוד נחמני",
        "age": 29,
        "sex": "זכר",
        "context": "בדיקת שגרה — בריא, ספורטאי חובב",
        "scenario_label": "תוצאות תקינות — צעיר בריא",
        "results": [
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 5.5,  "unit": "10³/µL", "range": "4.5–11.0",  "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 16.1, "unit": "g/dL",   "range": "13.5–17.5", "status": "תקין"},
            {"test": "Ferritin",     "heb": "פריטין",           "value": 95,   "unit": "ng/mL",  "range": "12–150",    "status": "תקין"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 4.9,  "unit": "%",      "range": "< 5.7",     "status": "תקין"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 75,   "unit": "mg/dL",  "range": "< 100",     "status": "תקין"},
            {"test": "HDL",          "heb": "כולסטרול HDL",     "value": 62,   "unit": "mg/dL",  "range": "> 40",      "status": "תקין"},
            {"test": "Triglycerides","heb": "טריגליצרידים",      "value": 85,   "unit": "mg/dL",  "range": "< 150",     "status": "תקין"},
        ],
        "summary": "כל תוצאות הבדיקות תקינות ובטווח מצוין. אין ממצאים חריגים או גבוליים. תמונה תואמת אדם צעיר ובריא.",
        "explanations": [],
        "contact": "ניתן להמשיך מעקב שגרתי עם רופא/ת המשפחה לפי המלצות הגיל.",
    },
]


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def count_statuses(results):
    counts = {"תקין": 0, "גבולי": 0, "חריג": 0}
    for r in results:
        if r["status"] in counts:
            counts[r["status"]] += 1
    return counts


# ─────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────

def page_home():
    st.markdown(page_hero("🏥", "MedExplain AI",
        "מערכת AI להסבר תוצאות בדיקות דם — שכבת הסבר חכמה בתוך אפליקציית קופת החולים"),
        unsafe_allow_html=True)

    st.markdown(disclaimer(
        "⚠️ <strong>הצהרה חשובה:</strong> מערכת זו היא הוכחת ישימות (PoC) אקדמית בלבד, "
        "המשתמשת בנתונים סינתטיים בלבד. היא אינה מאבחנת, אינה ממליצה על טיפול, ואינה מחליפה רופא/ת משפחה."),
        unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(feature_card("🔬", "הבעיה",
            "מטופלים רבים מקבלים תוצאות בדיקות דם דרך האפליקציה — ולעיתים מתקשים להבין את משמעותן, "
            "עלולים לחוות חרדה מיותרת, או לא יודעים אם הממצא דורש פנייה דחופה."),
            unsafe_allow_html=True)
    with col2:
        st.markdown(feature_card("💡", "הפתרון",
            "שכבת AI מוטמעת באפליקציית הקופה — מסבירה בשפה פשוטה, מתאימה את ההסבר להקשר האישי "
            "של המטופל, ומכינה שאלות ממוקדות לשיחה עם הרופא."),
            unsafe_allow_html=True)
    with col3:
        st.markdown(feature_card("🛡️", "הגישה הבטוחה",
            "המערכת אינה מאבחנת ואינה ממליצה על טיפול. הרופא/ה נשאר/ת הסמכות הקלינית הבלעדית. "
            "הלוגיקה מונעת ניסוחים שיכולים לגרום נזק."),
            unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5 = st.columns(2)
    with col4:
        st.markdown(card(
            f'<h4 style="color:{C["teal"]};margin-top:0;">✅ מה המערכת עושה</h4>'
            '<ul style="margin:0;padding-right:1.2rem;line-height:2;">'
            "<li>מסבירה בשפה פשוטה מה מודדת כל בדיקה</li>"
            "<li>מסבירה מדוע ערך עשוי להיות שונה מהטווח</li>"
            "<li>מציגה רמת דחיפות בצורה רגועה ולא מאיימת</li>"
            "<li>מכינה שאלות ממוקדות לשיחה עם הרופא</li>"
            "<li>מציינת למי מומלץ לפנות</li>"
            "</ul>"), unsafe_allow_html=True)
    with col5:
        st.markdown(card(
            f'<h4 style="color:{C["red"]};margin-top:0;">🚫 מה המערכת לא עושה</h4>'
            '<ul style="margin:0;padding-right:1.2rem;line-height:2;">'
            "<li>אינה מאבחנת מחלה</li>"
            "<li>אינה ממליצה על טיפול תרופתי</li>"
            "<li>אינה אומרת שאין צורך ברופא</li>"
            "<li>אינה משתמשת בשפה מאיימת</li>"
            "<li>אינה מחליפה שיקול קליני</li>"
            "</ul>"), unsafe_allow_html=True)

    st.markdown(card_teal(
        "<strong>🎓 הקשר אקדמי:</strong> מערכת זו פותחה כפרויקט הוכחת ישימות (Proof of Concept) "
        "במסגרת קורס Medical AI באוניברסיטה. כל הנתונים — שמות, ערכי מעבדה ופרטים קליניים — "
        "הם סינתטיים לחלוטין ונוצרו לצרכים חינוכיים בלבד."),
        unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: PATIENT DASHBOARD
# ─────────────────────────────────────────────

def page_dashboard():
    st.markdown(page_hero("📋", "לוח מטופל",
        "בחרו מטופל סינתטי לדוגמה לצפייה בהסבר תוצאות הבדיקות",
        "135deg, #1A9882 0%, #2B7BB9 100%"),
        unsafe_allow_html=True)

    st.markdown(disclaimer(
        "⚠️ כל הנתונים המוצגים הם סינתטיים לחלוטין. שמות, ערכים ופרטים קליניים בדויים לצרכים חינוכיים בלבד."),
        unsafe_allow_html=True)

    patient_options = {
        f"{p['id']}. {p['name']} ({p['age']}, {p['sex']}) — {p['scenario_label']}": p
        for p in PATIENTS
    }
    selected_label = st.selectbox("בחרו מטופל:", list(patient_options.keys()))
    p = patient_options[selected_label]

    st.markdown(divider(), unsafe_allow_html=True)

    # Patient header
    sex_icon = "👩" if p["sex"] == "נקבה" else "👨"
    st.markdown(patient_header(sex_icon, p["name"], p["age"], p["sex"], p["context"], p["scenario_label"]),
                unsafe_allow_html=True)

    # Metric cards
    counts = count_statuses(p["results"])
    st.markdown(metric_cards(counts), unsafe_allow_html=True)

    # Lab table
    st.markdown(f'<h3 style="direction:rtl;text-align:right;color:{C["text"]};">🔬 תוצאות הבדיקות</h3>',
                unsafe_allow_html=True)
    st.markdown(render_lab_table(p["results"]), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # Summary
    st.markdown(f'<h3 style="direction:rtl;text-align:right;color:{C["text"]};">📝 סיכום ממצאים</h3>',
                unsafe_allow_html=True)
    st.markdown(summary_box(p["summary"]), unsafe_allow_html=True)

    # Detailed explanations
    if p["explanations"]:
        st.markdown(f'<h3 style="direction:rtl;text-align:right;color:{C["text"]};">🔎 הסבר מפורט לממצאים</h3>',
                    unsafe_allow_html=True)
        for exp in p["explanations"]:
            badge_colors = {"green": (C["green_bg"], C["green"], "🟢"),
                            "yellow": (C["yellow_bg"], C["yellow"], "🟡"),
                            "red": (C["red_bg"], C["red"], "🔴")}
            bg_b, col_b, icon_b = badge_colors.get(exp["badge_type"], (C["green_bg"], C["green"], "🟢"))

            with st.expander(f"📌 {exp['test_label']}  —  סטטוס: {exp['badge']}", expanded=True):
                # Badge
                st.markdown(
                    f'<span style="display:inline-block;padding:0.28rem 0.85rem;border-radius:20px;'
                    f'font-size:0.9rem;font-weight:700;background:{bg_b};color:{col_b};">'
                    f'{icon_b} {exp["badge"]}</span>',
                    unsafe_allow_html=True)

                # Section: short summary
                st.markdown(
                    f'<h4 style="color:{C["teal"]};font-size:1rem;font-weight:700;margin:0.9rem 0 0.3rem 0;'
                    f'border-bottom:1px solid {C["teal_l"]};padding-bottom:0.3rem;direction:rtl;text-align:right;">סיכום קצר</h4>'
                    f'<p style="direction:rtl;text-align:right;color:{C["text"]};font-size:0.97rem;line-height:1.7;">{exp["short_summary"]}</p>',
                    unsafe_allow_html=True)

                # Section: what is it
                st.markdown(
                    f'<h4 style="color:{C["teal"]};font-size:1rem;font-weight:700;margin:0.8rem 0 0.3rem 0;'
                    f'border-bottom:1px solid {C["teal_l"]};padding-bottom:0.3rem;direction:rtl;text-align:right;">מה הבדיקה מודדת?</h4>'
                    f'<p style="direction:rtl;text-align:right;color:{C["text"]};font-size:0.97rem;line-height:1.7;">{exp["what_is"]}</p>',
                    unsafe_allow_html=True)

                # Section: why different
                items_html = "".join(f'<li style="margin-bottom:0.2rem;">{r}</li>' for r in exp["why_different"])
                st.markdown(
                    f'<h4 style="color:{C["teal"]};font-size:1rem;font-weight:700;margin:0.8rem 0 0.3rem 0;'
                    f'border-bottom:1px solid {C["teal_l"]};padding-bottom:0.3rem;direction:rtl;text-align:right;">למה הערך יכול להיות שונה?</h4>'
                    f'<ul style="direction:rtl;text-align:right;padding-right:1.2rem;color:{C["text"]};font-size:0.97rem;line-height:1.7;">{items_html}</ul>',
                    unsafe_allow_html=True)

                # Section: urgency
                st.markdown(
                    f'<h4 style="color:{C["teal"]};font-size:1rem;font-weight:700;margin:0.8rem 0 0.3rem 0;'
                    f'border-bottom:1px solid {C["teal_l"]};padding-bottom:0.3rem;direction:rtl;text-align:right;">כמה זה דחוף?</h4>',
                    unsafe_allow_html=True)
                st.markdown(urgency_line(exp["urgency"], exp["urgency_text"]), unsafe_allow_html=True)

                # Section: who to contact
                st.markdown(
                    f'<h4 style="color:{C["teal"]};font-size:1rem;font-weight:700;margin:0.8rem 0 0.3rem 0;'
                    f'border-bottom:1px solid {C["teal_l"]};padding-bottom:0.3rem;direction:rtl;text-align:right;">למי נכון לפנות?</h4>'
                    f'<p style="direction:rtl;text-align:right;color:{C["text"]};font-size:0.97rem;line-height:1.7;">{exp["contact_text"]}</p>',
                    unsafe_allow_html=True)

                # Physician questions
                st.markdown(
                    f'<h4 style="color:{C["blue"]};font-size:1rem;font-weight:700;margin:0.8rem 0 0.5rem 0;'
                    f'direction:rtl;text-align:right;">💬 שאלות מומלצות לרופא/ת המשפחה</h4>',
                    unsafe_allow_html=True)
                for q in exp["questions"]:
                    st.markdown(question_card(q), unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div style="background:{C["green_bg"]};border-right:3px solid {C["green"]};border-radius:8px;'
            f'padding:0.65rem 1rem;margin-bottom:0.4rem;font-size:0.95rem;font-weight:600;color:{C["green"]};'
            f'direction:rtl;text-align:right;">✅ כל תוצאות הבדיקות תקינות. לא נדרש הסבר מפורט לממצאים חריגים.</div>',
            unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # Contact
    st.markdown(f'<h3 style="direction:rtl;text-align:right;color:{C["text"]};">📞 מי מומלץ לפנות אליו?</h3>',
                unsafe_allow_html=True)
    st.markdown(contact_card("👨‍⚕️ רופא/ת משפחה", p["contact"]), unsafe_allow_html=True)
    st.markdown(contact_card("ℹ️ הערה חשובה",
        "ברוב המקרים הצעד הראשון הוא פנייה לרופא/ת המשפחה, שיוכל/תוכל להחליט "
        "האם נדרש בירור נוסף או הפניה לגורם מקצועי."), unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: HOW IT WORKS
# ─────────────────────────────────────────────

def page_how_it_works():
    st.markdown(page_hero("⚙️", "כיצד זה עובד?",
        "זרימת העבודה של שכבת ה-AI בתוך אפליקציית הקופה"),
        unsafe_allow_html=True)

    steps = [
        ("🏥", "שלב 1", "תוצאות מהמעבדה",
         "תוצאות הבדיקות מתקבלות ישירות ממערכת המעבדה של הקופה ומועברות לתיק הרפואי האלקטרוני."),
        ("📂", "שלב 2", "נתונים מובנים",
         "הערכים מגיעים כנתונים מובנים מתוך התיק הרפואי — לא כסריקה, לא כטקסט חופשי. "
         "כל ערך מוגדר, ממויין ומקושר לטווח הנורמה."),
        ("🤖", "שלב 3", "שכבת AI מסבירה",
         "מנוע ה-AI מפיק הסבר בשפה פשוטה המותאם לערך הספציפי, להקשר האישי של המטופל ולסטטוס הבדיקה."),
        ("🛡️", "שלב 4", "לוגיקת בטיחות",
         "לפני הצגת ההסבר, לוגיקת בטיחות בוחנת שאין ניסוחים אבחנתיים, המלצות טיפוליות, או שפה מאיימת."),
        ("💬", "שלב 5", "שאלות לרופא",
         "המטופל מקבל רשימת שאלות ממוקדות המותאמות לממצא ולהקשרו האישי — להכנה לשיחה עם הרופא."),
        ("👨‍⚕️", "שלב 6", "הרופא נשאר סמכות",
         "הרופא/ה נשאר/ת הסמכות הקלינית הבלעדית. המערכת משלימה — לא מחליפה — את השיקול הרפואי."),
    ]

    row1 = st.columns(3)
    for i in range(3):
        with row1[i]:
            icon, num, title, desc = steps[i]
            st.markdown(step_card(icon, num, title, desc), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    row2 = st.columns(3)
    for i in range(3):
        with row2[i]:
            icon, num, title, desc = steps[i + 3]
            st.markdown(step_card(icon, num, title, desc), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(card_teal(
        f"<strong>🔒 עיקרון המפתח:</strong> שכבת ה-AI פועלת בתוך גבולות מוגדרים מראש של מערכת בריאות מוסדרת. "
        "בשונה מ-chatbot כללי, היא אינה יכולה לסטות מהמסגרת הבטוחה שהוגדרה."),
        unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: WHY NOT CHATGPT
# ─────────────────────────────────────────────

def page_why_not_chatgpt():
    st.markdown(page_hero("🤔", "למה לא ChatGPT רגיל?",
        "השוואה בין chatbot כללי לשכבת AI מוטמעת בתוך מערכת בריאות מוסדרת",
        "135deg, #2B7BB9 0%, #1A9882 100%"),
        unsafe_allow_html=True)

    st.markdown(card(
        "<p style='direction:rtl;text-align:right;'>ייתכן ומטופלים רבים כבר פונים ל-ChatGPT כדי להבין תוצאות בדיקות — זה מובן לחלוטין. "
        "אך גישה זו מגיעה עם מגבלות משמעותיות. הטבלה הבאה מסכמת את ההבדלים המרכזיים.</p>"
        f"<p style='direction:rtl;text-align:right;color:{C['muted']};font-size:0.9rem;'>"
        "<em>הערה: המערכת הנוכחית היא PoC אקדמי. איננו טוענים שהיא מושלמת — אלא שגישה זו "
        "<strong>עשויה</strong> לשפר את הבטיחות ואת זרימת העבודה הקלינית.</em></p>"),
        unsafe_allow_html=True)

    rows = [
        ("🔒 פרטיות",
         "המטופל מעתיק תוצאות ידנית — שיתוף מידע רפואי עם ספק חיצוני",
         "הנתונים נשארים בתוך המערכת הסגורה של הקופה"),
        ("📋 נתונים מובנים",
         "טקסט חופשי שהמטופל כותב — שגיאות, השמטות אפשריות",
         "ערכי מעבדה מובנים ישירות מהתיק הרפואי"),
        ("🌐 שפה ועיצוב",
         "ממשק אנגלי בעיקר, לא מותאם לשפה ולתרבות הישראלית",
         "ממשק עברי RTL מלא, מותאם למטופל הישראלי"),
        ("🛡️ גבולות בטיחות",
         "ChatGPT עשוי לסטות לאבחון או להרגיע יתר על המידה — תלוי בניסוח",
         "גבולות שפה מוגדרים מראש — ניסוחים אבחנתיים חסומים"),
        ("⚕️ פיקוח קליני",
         "אין שילוב עם מערכת הרופא",
         "מתוכנן להשתלב בזרימת העבודה של הרופא"),
        ("📂 היסטוריה רפואית",
         "אין גישה לבדיקות קודמות להשוואה",
         "יכול להציג מגמה לאורך זמן מתוך התיק הרפואי"),
        ("⚠️ סיכון הרגעה יתר",
         "ChatGPT עשוי להרגיע מטופל ולהציע 'לא לדאוג' — ללא הקשר קליני",
         "שפה ניטרלית, תמיד מפנה לרופא/ה"),
        ("🎯 מיקוד",
         "תשובות כלליות, לא תמיד מותאמות לגיל, מין והקשר",
         "הסבר מותאם לפרופיל הספציפי של המטופל"),
    ]

    table_rows = ""
    for feature, chatgpt_col, hmo_col in rows:
        table_rows += (
            f"<tr>"
            f'<td style="padding:0.75rem 1rem;border-bottom:1px solid {C["border"]};'
            f'text-align:right;direction:rtl;"><strong>{feature}</strong></td>'
            f'<td style="padding:0.75rem 1rem;border-bottom:1px solid {C["border"]};'
            f'text-align:right;direction:rtl;color:{C["red"]};font-weight:600;">❌ {chatgpt_col}</td>'
            f'<td style="padding:0.75rem 1rem;border-bottom:1px solid {C["border"]};'
            f'text-align:right;direction:rtl;color:{C["green"]};font-weight:700;">✅ {hmo_col}</td>'
            f"</tr>"
        )

    st.markdown(
        f'<div style="overflow-x:auto;direction:rtl;">'
        f'<table style="width:100%;border-collapse:collapse;direction:rtl;text-align:right;'
        f'font-family:\'Assistant\',sans-serif;font-size:0.93rem;">'
        f'<thead><tr>'
        f'<th style="background:{C["teal"]};color:white;padding:0.75rem 1rem;text-align:right;font-weight:700;">היבט</th>'
        f'<th style="background:{C["teal"]};color:white;padding:0.75rem 1rem;text-align:right;font-weight:700;">Chatbot ציבורי (דוגמת ChatGPT)</th>'
        f'<th style="background:{C["teal"]};color:white;padding:0.75rem 1rem;text-align:right;font-weight:700;">שכבת AI מוטמעת בקופה (MedExplain)</th>'
        f'</tr></thead>'
        f'<tbody>{table_rows}</tbody>'
        f'</table></div>',
        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(card_blue(
        f"<strong>⚖️ הצהרת אמינות:</strong> אנו לא טוענים שהמערכת הנוכחית מושלמת. כמו כל כלי AI, "
        "היא חשופה לטעויות, הרגעה יתרה, ועמימות. היתרון המרכזי הוא "
        "<em>פעולה בתוך גבולות מוגדרים של מערכת בריאות מוסדרת</em> — "
        "ולא כ-chatbot כללי ללא גבולות."),
        unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: SAFETY & ETHICS
# ─────────────────────────────────────────────

def page_safety():
    st.markdown(page_hero("🛡️", "בטיחות ואתיקה",
        "עקרונות הבטיחות, האתיקה והפרטיות של המערכת"),
        unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["⚖️ עקרונות בסיסיים", "🚫 מה המערכת לעולם לא תאמר", "🔒 פרטיות ואבטחה"])

    with tab1:
        col1, col2 = st.columns(2)
        principles = [
            ("🎓", "כלי חינוכי בלבד",
             "המערכת מיועדת להסבר ולהכנת שאלות בלבד. היא אינה חלק מזרימת טיפול קלינית."),
            ("🩺", "הרופא הוא הסמכות",
             "הרופא/ת המשפחה נשאר/ת הסמכות הקלינית הבלעדית. ההמלצה תמיד היא לשוחח עם הרופא."),
            ("🔬", "נתונים סינתטיים",
             "כל הנתונים בגרסת ה-PoC הם סינתטיים לחלוטין. אין שימוש בנתוני מטופלים אמיתיים."),
            ("🧠", "פיקוח אנושי",
             "המערכת אינה עצמאית. היא פועלת בתוך מסגרת שנקבעה על ידי אנשי מקצוע רפואיים."),
            ("⚠️", "סיכון הזיה (Hallucination)",
             "כמו כל מערכת AI, קיים סיכון לתשובות לא מדויקות. לכן השפה מוגדרת מראש ולא נוצרת באופן חופשי."),
            ("😌", "סיכון הרגעה יתר",
             "הרגעה לא מבוססת עלולה להזיק. המערכת תמיד ממליצה על פנייה לרופא ואינה אומרת 'אין מה לדאוג'."),
            ("♿", "נגישות ושוויון",
             "יש לוודא שהמערכת נגישה לאוכלוסיות מגוונות — כולל אוכלוסיות מבוגרות, דוברות שפות שונות, ובעלות מגבלויות."),
            ("📊", "הטיית נתונים",
             "מודלי AI עלולים לשקף הטיות הקיימות בנתוני האימון. יש לנטר ולבחון את הפלטים לאורך זמן."),
        ]
        for i, (icon, title, desc) in enumerate(principles):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(card(
                    f'<div style="font-size:1.5rem;margin-bottom:0.3rem;">{icon}</div>'
                    f'<strong style="color:{C["teal"]};">{title}</strong>'
                    f'<p style="margin:0.4rem 0 0 0;font-size:0.92rem;color:{C["muted"]};">{desc}</p>'),
                    unsafe_allow_html=True)

    with tab2:
        st.markdown(card(
            f"<p style='direction:rtl;text-align:right;'>המערכת מיועדת לעולם <strong>לא לשלוח</strong> ניסוחים אלה — "
            "גם אם הם עשויים להיות נכונים קלינית. השפה נקבעת מראש ומוגדרת בלוגיקת הבטיחות.</p>"),
            unsafe_allow_html=True)

        never_list = [
            '"יש לך סוכרת"', '"יש לך אנמיה"', '"אתה חייב תרופה"',
            '"עליך לקחת X"', '"אין צורך לפנות לרופא"', '"הממצא מסוכן"',
            '"זה חמור"', '"זה ממאיר"', '"אין מה לדאוג"',
            '"הכל בסדר, אינך צריך רופא"',
        ]
        always_list = [
            '"ממצא זה מצריך דיון עם רופא/ת המשפחה"',
            '"ייתכן שהערך קשור ל..."',
            '"יכול להתאים ל... אך ההקשר הקליני חשוב"',
            '"כדאי להשוות לבדיקות קודמות"',
            '"רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש בירור"',
            '"בהקשר הקליני המתאים"',
        ]

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f'<h4 style="direction:rtl;text-align:right;color:{C["red"]};">🚫 לעולם לא תאמר</h4>',
                unsafe_allow_html=True)
            for s in never_list:
                st.markdown(never_item(s), unsafe_allow_html=True)
        with c2:
            st.markdown(
                f'<h4 style="direction:rtl;text-align:right;color:{C["green"]};">✅ תמיד תשתמש בניסוח כזה</h4>',
                unsafe_allow_html=True)
            for s in always_list:
                st.markdown(always_item(s), unsafe_allow_html=True)

    with tab3:
        considerations = [
            ("🔐", "סגירות הנתונים",   "הנתונים נשארים בתוך מערכת הקופה הסגורה. לא מועברים לשרת חיצוני."),
            ("🗑️", "מינימיזציית נתונים", "המערכת משתמשת אך ורק בנתונים הנחוצים לתפקודה — ללא איסוף מידע עודף."),
            ("👁️", "שקיפות",            "המטופל יודע שהוא מקבל הסבר אוטומטי ממוחשב, ולא פסיקה קלינית."),
            ("✅", "הסכמה מדעת",        "בגרסה מלאה, המטופל יאשר הסכמתו לשימוש בכלי הסברה ממוחשב."),
            ("📋", "רגולציה",           "מערכת כזו תדרוש אישור רגולטורי ממשרד הבריאות ומהגורמים המוסמכים."),
            ("🔍", "מעקב ואיכות",       "יש לנטר את פלטי המערכת לאורך זמן ולבחון אותם מול מומחים קליניים."),
        ]
        cols = st.columns(3)
        for i, (icon, title, desc) in enumerate(considerations):
            with cols[i % 3]:
                st.markdown(privacy_card(icon, title, desc), unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: PATIENT FEEDBACK
# ─────────────────────────────────────────────

def page_feedback():
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#2B7BB9 0%,#1A9882 100%);border-radius:14px;'
        f'padding:1.8rem 2.2rem;color:white;margin-bottom:1.4rem;direction:rtl;text-align:right;">'
        f'<h2 style="color:white;margin:0 0 0.3rem 0;font-family:\'Assistant\',sans-serif;">💬 משוב מהמטופל</h2>'
        f'<p style="color:rgba(255,255,255,0.88);margin:0;font-size:0.97rem;">'
        f'האם ההסבר עזר לך? המשוב שלך עוזר לשפר את המערכת בעתיד</p></div>',
        unsafe_allow_html=True)

    st.markdown(disclaimer(
        "⚠️ זהו טופס משוב לדוגמה בלבד. הנתונים אינם נשמרים. נועד להדגמת מנגנון הערכה מבוסס-מטופל."),
        unsafe_allow_html=True)

    with st.form("feedback_form"):
        st.markdown(f'<h4 style="direction:rtl;text-align:right;color:{C["text"]};">1️⃣ עד כמה ההסבר היה ברור?</h4>',
                    unsafe_allow_html=True)
        clarity = st.slider("בהירות ההסבר", 1, 5, 3, key="clarity",
                            label_visibility="collapsed")
        clarity_labels = {1: "לא ברור כלל", 2: "לא ממש ברור", 3: "ברור חלקית", 4: "ברור", 5: "ברור מאוד"}
        st.markdown(
            f'<p style="color:{C["teal"]};font-weight:700;margin-top:-0.5rem;direction:rtl;text-align:right;">'
            f'{clarity_labels[clarity]}</p>', unsafe_allow_html=True)

        st.markdown(divider(), unsafe_allow_html=True)
        st.markdown(f'<h4 style="direction:rtl;text-align:right;color:{C["text"]};">2️⃣ האם ההסבר עזר לך להבין את משמעות התוצאה?</h4>',
                    unsafe_allow_html=True)
        understanding = st.slider("עזרה בהבנה", 1, 5, 3, key="understanding",
                                  label_visibility="collapsed")
        understanding_labels = {1: "לא עזר בכלל", 2: "עזר מעט", 3: "עזר חלקית", 4: "עזר", 5: "עזר מאוד"}
        st.markdown(
            f'<p style="color:{C["teal"]};font-weight:700;margin-top:-0.5rem;direction:rtl;text-align:right;">'
            f'{understanding_labels[understanding]}</p>', unsafe_allow_html=True)

        st.markdown(divider(), unsafe_allow_html=True)
        st.markdown(f'<h4 style="direction:rtl;text-align:right;color:{C["text"]};">3️⃣ האם ברור לך יותר מה כדאי לשאול את הרופא?</h4>',
                    unsafe_allow_html=True)
        questions_clear = st.radio("שאלות לרופא", ["כן", "חלקית", "לא"],
                                   key="questions_clear", horizontal=True,
                                   label_visibility="collapsed")

        st.markdown(divider(), unsafe_allow_html=True)
        st.markdown(f'<h4 style="direction:rtl;text-align:right;color:{C["text"]};">4️⃣ האם ההסבר הפחית את רמת החשש שלך?</h4>',
                    unsafe_allow_html=True)
        anxiety = st.radio("הפחתת חשש", ["כן מאוד", "במידה מסוימת", "לא", "לא רלוונטי"],
                           key="anxiety", horizontal=True, label_visibility="collapsed")

        st.markdown(divider(), unsafe_allow_html=True)
        st.markdown(f'<h4 style="direction:rtl;text-align:right;color:{C["text"]};">5️⃣ האם היית משתמש/ת בכלי כזה באפליקציית קופת החולים?</h4>',
                    unsafe_allow_html=True)
        would_use = st.radio("שימוש בכלי", ["כן", "אולי", "לא"],
                             key="would_use", horizontal=True, label_visibility="collapsed")

        st.markdown(divider(), unsafe_allow_html=True)
        st.markdown(f'<h4 style="direction:rtl;text-align:right;color:{C["text"]};">6️⃣ מה עדיין לא היה ברור?</h4>',
                    unsafe_allow_html=True)
        open_feedback = st.text_area("משוב פתוח", placeholder="כתב/י כאן בחופשיות...",
                                     height=100, key="open_feedback",
                                     label_visibility="collapsed")

        submitted = st.form_submit_button("📤 שליחת משוב")

    if submitted:
        st.success("✅ תודה על המשוב!")
        st.markdown(card_teal(
            "<strong>תודה על המשוב.</strong> בגרסה עתידית ניתן יהיה להשתמש במשובים מסוג זה "
            "כדי לשפר את בהירות ההסברים, לזהות ניסוחים מבלבלים, ולוודא שהמערכת באמת "
            "מסייעת למטופלים להבין את תוצאות הבדיקות."),
            unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)
    st.markdown(card_blue(
        f"<strong>🎓 מנגנון הערכה מבוסס-מטופל</strong><br><br>"
        "מנגנון המשוב מאפשר להעריך את הצלחת המערכת מנקודת מבט של המטופל: "
        "האם ההסבר היה ברור? האם הופחתה חרדה? האם המטופל יודע טוב יותר מה לשאול את הרופא?<br><br>"
        "בשונה ממדדים טכניים (דיוק, Recall וכו'), הערכה זו מכוונת לתוצאה הקלינית המשמעותית: "
        "<em>האם הכלי עזר למטופל לפעול נכון?</em>"),
        unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR & NAVIGATION
# ─────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown(
            f'<div style="text-align:center;padding:0.5rem 0 1rem 0;direction:rtl;">'
            f'<div style="font-size:2.5rem;">🏥</div>'
            f'<div style="font-size:1.1rem;font-weight:800;color:{C["teal"]};">MedExplain AI</div>'
            f'<div style="font-size:0.75rem;color:{C["muted"]};margin-top:0.1rem;">מערכת הסבר בדיקות דם</div>'
            f'</div>'
            f'<hr style="border:1px solid {C["border"]};margin:0.5rem 0 1rem 0;">',
            unsafe_allow_html=True)

        nav_options = {
            "🏠 עמוד הבית":      "home",
            "📋 לוח מטופל":      "dashboard",
            "⚙️ כיצד זה עובד":   "how",
            "🤔 למה לא ChatGPT?": "chatgpt",
            "🛡️ בטיחות ואתיקה":  "safety",
            "💬 משוב מהמטופל":   "feedback",
        }

        selected = st.radio(
            "ניווט:", list(nav_options.keys()),
            key="nav", label_visibility="collapsed")

        st.markdown(
            f'<hr style="border:1px solid {C["border"]};margin:1rem 0;">'
            f'<div style="font-size:0.78rem;color:{C["muted"]};text-align:right;line-height:1.6;direction:rtl;">'
            f'<span style="background:{C["red_bg"]};color:{C["red"]};font-size:0.72rem;font-weight:700;'
            f'border-radius:10px;padding:0.15rem 0.5rem;margin-left:0.3rem;">PoC</span>'
            f'גרסת הדגמה בלבד<br>'
            f'נתונים סינתטיים לחלוטין<br>'
            f'לא לשימוש קליני<br><br>'
            f'<strong>MedExplain AI</strong><br>'
            f'פרויקט קורס Medical AI<br>'
            f'© 2024 Academic PoC'
            f'</div>',
            unsafe_allow_html=True)

        return nav_options[selected]


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    page = render_sidebar()
    if page == "home":
        page_home()
    elif page == "dashboard":
        page_dashboard()
    elif page == "how":
        page_how_it_works()
    elif page == "chatgpt":
        page_why_not_chatgpt()
    elif page == "safety":
        page_safety()
    elif page == "feedback":
        page_feedback()


if __name__ == "__main__":
    main()
