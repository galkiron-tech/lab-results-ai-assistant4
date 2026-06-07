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
# GLOBAL CSS — RTL + HEALTHCARE DESIGN SYSTEM
# ─────────────────────────────────────────────
GLOBAL_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;500;600;700;800&display=swap');

/* ── Root Design Tokens ── */
:root {
    --bg-page:       #EFF6FB;
    --bg-card:       #FFFFFF;
    --bg-sidebar:    #F0F7F4;
    --accent-teal:   #1A9882;
    --accent-teal-l: #E6F4F1;
    --accent-blue:   #2B7BB9;
    --accent-blue-l: #EAF3FB;
    --green:         #2E9E5B;
    --green-bg:      #E8F7EE;
    --yellow:        #C78A00;
    --yellow-bg:     #FFF8E1;
    --red:           #C0392B;
    --red-bg:        #FDECEA;
    --text-main:     #1C2B39;
    --text-muted:    #5D7A8A;
    --border:        #D6E8F0;
    --shadow:        0 2px 12px rgba(0,0,0,0.07);
    --radius:        14px;
    --radius-sm:     8px;
}

/* ── Base RTL ── */
html, body, [class*="css"], .stApp {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Assistant', 'Segoe UI', Arial, sans-serif !important;
    background-color: var(--bg-page) !important;
    color: var(--text-main) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    direction: rtl !important;
    text-align: right !important;
    background: var(--bg-sidebar) !important;
    border-left: 2px solid var(--border) !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] * {
    direction: rtl !important;
    text-align: right !important;
}

/* ── Headings ── */
h1, h2, h3, h4, h5, h6 {
    direction: rtl !important;
    text-align: right !important;
    color: var(--text-main) !important;
    font-family: 'Assistant', sans-serif !important;
}

/* ── Paragraphs & labels ── */
p, label, span, div, li, td, th {
    direction: rtl !important;
    text-align: right !important;
}

/* ── Streamlit selectbox / radio ── */
.stSelectbox label, .stRadio label, .stSlider label,
.stTextArea label, .stTextInput label, .stCheckbox label {
    direction: rtl !important;
    text-align: right !important;
    font-weight: 600 !important;
}
.stRadio > div {
    direction: rtl !important;
}

/* ── Streamlit buttons ── */
.stButton > button {
    direction: rtl !important;
    background: var(--accent-teal) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.55rem 1.4rem !important;
    font-family: 'Assistant', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background: #157A6A !important;
}

/* ── Streamlit expander ── */
details {
    direction: rtl !important;
}
summary {
    direction: rtl !important;
    text-align: right !important;
}

/* ── Streamlit tabs ── */
.stTabs [data-baseweb="tab-list"] {
    direction: rtl !important;
    gap: 6px !important;
}
.stTabs [data-baseweb="tab"] {
    direction: rtl !important;
    font-family: 'Assistant', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
}

/* ── Streamlit metric ── */
[data-testid="metric-container"] {
    direction: rtl !important;
    text-align: right !important;
}

/* ── Streamlit alerts / info boxes ── */
.stAlert {
    direction: rtl !important;
    text-align: right !important;
    border-radius: var(--radius-sm) !important;
}

/* ── Streamlit dataframe ── */
.stDataFrame {
    direction: rtl !important;
}

/* ── Hide Streamlit branding ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-page); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
"""

# ─────────────────────────────────────────────
# COMPONENT CSS HELPERS
# ─────────────────────────────────────────────
CARD_CSS = """
<style>
.med-card {
    background: var(--bg-card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    direction: rtl;
    text-align: right;
}
.med-card-teal {
    background: var(--accent-teal-l);
    border-right: 4px solid var(--accent-teal);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    direction: rtl;
    text-align: right;
}
.med-card-blue {
    background: var(--accent-blue-l);
    border-right: 4px solid var(--accent-blue);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    direction: rtl;
    text-align: right;
}
.patient-header {
    background: linear-gradient(135deg, #1A9882 0%, #2B7BB9 100%);
    border-radius: var(--radius);
    padding: 1.6rem 2rem;
    color: white;
    margin-bottom: 1.4rem;
    direction: rtl;
    text-align: right;
}
.patient-header h2 { color: white !important; margin: 0 0 0.3rem 0; font-size: 1.7rem; }
.patient-header p  { color: rgba(255,255,255,0.88); margin: 0; font-size: 1rem; }

/* ── Status badges ── */
.badge {
    display: inline-block;
    padding: 0.28rem 0.85rem;
    border-radius: 20px;
    font-size: 0.88rem;
    font-weight: 700;
    letter-spacing: 0.02em;
}
.badge-green  { background: var(--green-bg);  color: var(--green); }
.badge-yellow { background: var(--yellow-bg); color: var(--yellow); }
.badge-red    { background: var(--red-bg);    color: var(--red); }

/* ── Metric summary cards ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.2rem;
    direction: rtl;
}
.metric-card {
    flex: 1;
    background: var(--bg-card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-card .metric-number { font-size: 2.2rem; font-weight: 800; line-height: 1.1; }
.metric-card .metric-label  { font-size: 0.9rem; color: var(--text-muted); margin-top: 0.2rem; }
.metric-green  .metric-number { color: var(--green); }
.metric-yellow .metric-number { color: var(--yellow); }
.metric-red    .metric-number { color: var(--red); }

/* ── Lab results table (spacious) ── */
.lab-table-wrap { direction: rtl; }
.lab-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 8px;
    direction: rtl;
    text-align: right;
}
.lab-table th {
    background: #EEF5FB;
    color: var(--text-muted);
    font-size: 0.85rem;
    font-weight: 700;
    padding: 0.6rem 1.1rem;
    text-align: right;
    border-bottom: 2px solid var(--border);
    letter-spacing: 0.03em;
}
.lab-table td {
    background: var(--bg-card);
    padding: 0.95rem 1.1rem;
    font-size: 1rem;
    vertical-align: middle;
    text-align: right;
}
.lab-table tr td:first-child { border-radius: 0 var(--radius-sm) var(--radius-sm) 0; }
.lab-table tr td:last-child  { border-radius: var(--radius-sm) 0 0 var(--radius-sm); }
.lab-row-normal  td { border-right: 4px solid var(--green); }
.lab-row-border  td { border-right: 4px solid var(--yellow); background: #FFFDF2; }
.lab-row-abnorm  td { border-right: 4px solid var(--red);   background: #FFF8F7; }
.lab-test-name { font-weight: 700; font-size: 1.05rem; color: var(--text-main); }
.lab-value     { font-weight: 700; font-size: 1.1rem; }
.lab-range     { color: var(--text-muted); font-size: 0.9rem; }

/* ── Explanation panel ── */
.explain-section {
    background: var(--bg-card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    direction: rtl;
    text-align: right;
}
.explain-section h4 {
    color: var(--accent-teal);
    font-size: 1rem;
    font-weight: 700;
    margin: 0.8rem 0 0.3rem 0;
    border-bottom: 1px solid var(--accent-teal-l);
    padding-bottom: 0.3rem;
}
.explain-section h3 {
    color: var(--text-main);
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0 0 0.8rem 0;
}
.explain-section p, .explain-section li {
    color: var(--text-main);
    font-size: 0.97rem;
    line-height: 1.7;
    margin: 0.2rem 0;
}
.urgency-low    { color: var(--green);  font-weight: 700; }
.urgency-mid    { color: var(--yellow); font-weight: 700; }
.urgency-high   { color: var(--red);    font-weight: 700; }

/* ── Questions list ── */
.question-card {
    background: var(--accent-blue-l);
    border-right: 3px solid var(--accent-blue);
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.97rem;
    direction: rtl;
    text-align: right;
    color: var(--text-main);
}

/* ── Workflow step cards ── */
.step-card {
    background: var(--bg-card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 1.2rem 1.4rem;
    text-align: center;
    direction: rtl;
}
.step-icon  { font-size: 2.2rem; margin-bottom: 0.4rem; }
.step-num   { font-size: 0.75rem; font-weight: 800; color: var(--accent-teal); letter-spacing: 0.1em; text-transform: uppercase; }
.step-title { font-size: 1rem; font-weight: 700; color: var(--text-main); margin: 0.3rem 0; }
.step-desc  { font-size: 0.88rem; color: var(--text-muted); line-height: 1.5; }

/* ── Home feature cards ── */
.feature-card {
    background: var(--bg-card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 1.3rem 1.5rem;
    height: 100%;
    direction: rtl;
    text-align: right;
    border-top: 3px solid var(--accent-teal);
}
.feature-icon { font-size: 1.8rem; margin-bottom: 0.4rem; }
.feature-title { font-size: 1.05rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.4rem; }
.feature-desc  { font-size: 0.91rem; color: var(--text-muted); line-height: 1.55; }

/* ── Safety items ── */
.never-item {
    background: var(--red-bg);
    border-right: 3px solid var(--red);
    border-radius: var(--radius-sm);
    padding: 0.65rem 1rem;
    margin-bottom: 0.4rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--red);
    direction: rtl;
    text-align: right;
}
.always-item {
    background: var(--green-bg);
    border-right: 3px solid var(--green);
    border-radius: var(--radius-sm);
    padding: 0.65rem 1rem;
    margin-bottom: 0.4rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--green);
    direction: rtl;
    text-align: right;
}

/* ── Comparison table ── */
.compare-table {
    width: 100%;
    border-collapse: collapse;
    direction: rtl;
    text-align: right;
    font-size: 0.93rem;
}
.compare-table th {
    background: var(--accent-teal);
    color: white;
    padding: 0.75rem 1rem;
    font-weight: 700;
    text-align: right;
}
.compare-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border);
    text-align: right;
    vertical-align: top;
}
.compare-table tr:nth-child(even) td { background: #F7FBFD; }
.compare-good { color: var(--green); font-weight: 700; }
.compare-bad  { color: var(--red);   font-weight: 600; }

/* ── Sidebar nav ── */
.sidebar-logo {
    text-align: center;
    padding: 0.5rem 0 1rem 0;
    direction: rtl;
}
.sidebar-logo .logo-icon { font-size: 2.5rem; }
.sidebar-logo .logo-name { font-size: 1.1rem; font-weight: 800; color: var(--accent-teal); }
.sidebar-logo .logo-sub  { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.1rem; }
.sidebar-badge {
    background: var(--red-bg);
    color: var(--red);
    font-size: 0.72rem;
    font-weight: 700;
    border-radius: 10px;
    padding: 0.15rem 0.5rem;
    margin-right: 0.4rem;
}

/* ── Page hero banner ── */
.page-hero {
    background: linear-gradient(135deg, #1A9882 0%, #2B7BB9 100%);
    border-radius: var(--radius);
    padding: 2rem 2.4rem;
    color: white;
    margin-bottom: 1.6rem;
    direction: rtl;
    text-align: right;
}
.page-hero h1 { color: white !important; font-size: 2rem; margin: 0 0 0.4rem 0; }
.page-hero p  { color: rgba(255,255,255,0.88); font-size: 1.05rem; margin: 0; }

/* ── Disclaimer banner ── */
.disclaimer {
    background: #FFF8E1;
    border: 1.5px solid #F0C930;
    border-radius: var(--radius-sm);
    padding: 0.8rem 1.1rem;
    font-size: 0.88rem;
    color: #7A5800;
    direction: rtl;
    text-align: right;
    margin-bottom: 1rem;
}

/* ── Contact card ── */
.contact-card {
    background: var(--accent-teal-l);
    border-right: 3px solid var(--accent-teal);
    border-radius: var(--radius-sm);
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.5rem;
    direction: rtl;
    text-align: right;
}
.contact-card strong { color: var(--accent-teal); }

/* ── Feedback form ── */
.feedback-hero {
    background: linear-gradient(135deg, #2B7BB9 0%, #1A9882 100%);
    border-radius: var(--radius);
    padding: 1.8rem 2.2rem;
    color: white;
    margin-bottom: 1.4rem;
    direction: rtl;
    text-align: right;
}
.feedback-hero h2 { color: white !important; margin: 0 0 0.3rem 0; }
.feedback-hero p  { color: rgba(255,255,255,0.88); margin: 0; font-size: 0.97rem; }

/* ── Section divider ── */
.section-divider {
    border: none;
    border-top: 1.5px solid var(--border);
    margin: 1.2rem 0;
}

/* ── Summary box ── */
.summary-box {
    background: var(--accent-teal-l);
    border-radius: var(--radius-sm);
    padding: 1rem 1.2rem;
    font-size: 1rem;
    color: var(--text-main);
    line-height: 1.7;
    direction: rtl;
    text-align: right;
    margin-bottom: 0.8rem;
}
</style>
"""


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
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 6.2,  "unit": "10³/µL",  "range": "4.5–11.0",   "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 13.2, "unit": "g/dL",    "range": "12.0–16.0",  "status": "תקין"},
            {"test": "Ferritin",     "heb": "פריטין",           "value": 42,   "unit": "ng/mL",   "range": "12–150",     "status": "תקין"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 5.2,  "unit": "%",       "range": "< 5.7",      "status": "תקין"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 88,   "unit": "mg/dL",   "range": "< 100",      "status": "תקין"},
        ],
        "summary": "כל תוצאות הבדיקות תקינות. אין ממצאים חריגים או גבוליים. ממצאים אלו תואמים לבדיקת שגרה תקינה.",
        "explanations": [],
        "questions": [],
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
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 7.1,  "unit": "10³/µL",  "range": "4.5–11.0",   "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 15.0, "unit": "g/dL",    "range": "13.5–17.5",  "status": "תקין"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 5.4,  "unit": "%",       "range": "< 5.7",      "status": "תקין"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 118,  "unit": "mg/dL",   "range": "< 100",      "status": "גבולי"},
            {"test": "HDL",          "heb": "כולסטרול HDL",     "value": 48,   "unit": "mg/dL",   "range": "> 40",       "status": "תקין"},
            {"test": "Triglycerides","heb": "טריגליצרידים",      "value": 140,  "unit": "mg/dL",   "range": "< 150",      "status": "תקין"},
        ],
        "summary": "ערך ה-LDL נמצא מעט מעל הטווח המקובל וסווג כגבולי. שאר הבדיקות תקינות. ממצא זה ראוי לדיון עם רופא/ת המשפחה.",
        "explanations": [
            {
                "test_label": "כולסטרול LDL — 118 mg/dL",
                "badge": "גבולי",
                "badge_type": "yellow",
                "short_summary": "ערך ה-LDL גבולי מעט מעל הטווח — כדאי לדון עם רופא/ת המשפחה.",
                "what_is": "LDL הוא סוג של כולסטרול הקשור לסיכון מצטבר לבריאות כלי הדם והלב. המשמעות של הערך תלויה גם בגורמי סיכון אישיים ובבדיקות נוספות.",
                "why_different": [
                    "תזונה עתירת שומן רווי",
                    "גורמים גנטיים",
                    "רמת פעילות גופנית",
                    "גיל ומין",
                ],
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
        "questions": [],
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
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 6.8,  "unit": "10³/µL",  "range": "4.5–11.0",   "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 13.5, "unit": "g/dL",    "range": "12.0–16.0",  "status": "תקין"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 5.5,  "unit": "%",       "range": "< 5.7",      "status": "תקין"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 158,  "unit": "mg/dL",   "range": "< 100",      "status": "חריג"},
            {"test": "HDL",          "heb": "כולסטרול HDL",     "value": 44,   "unit": "mg/dL",   "range": "> 50",       "status": "גבולי"},
            {"test": "Triglycerides","heb": "טריגליצרידים",      "value": 175,  "unit": "mg/dL",   "range": "< 150",      "status": "גבולי"},
        ],
        "summary": "ערך ה-LDL מוגבר בבירור מעל הטווח המקובל. גם HDL נמוך מעט וטריגליצרידים גבוליים. השילוב ראוי לדיון עם רופא/ת המשפחה בהקדם.",
        "explanations": [
            {
                "test_label": "כולסטרול LDL — 158 mg/dL",
                "badge": "חריג",
                "badge_type": "red",
                "short_summary": "ערך ה-LDL מוגבר בבירור — ממצא זה מצריך דיון עם רופא/ת המשפחה.",
                "what_is": "LDL הוא סוג של כולסטרול הקשור לסיכון מצטבר לבריאות כלי הדם והלב. המשמעות של הערך תלויה גם בגורמי סיכון אישיים כמו לחץ דם, גיל ובדיקות נוספות.",
                "why_different": [
                    "גורמים גנטיים",
                    "תזונה עתירת שומן רווי",
                    "רמת פעילות גופנית נמוכה",
                    "גורמי סיכון כלי-דמיים נוספים",
                ],
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
        "questions": [],
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
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 7.4,  "unit": "10³/µL",  "range": "4.5–11.0",   "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 14.8, "unit": "g/dL",    "range": "13.5–17.5",  "status": "תקין"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 6.1,  "unit": "%",       "range": "< 5.7",      "status": "גבולי"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 105,  "unit": "mg/dL",   "range": "< 100",      "status": "גבולי"},
            {"test": "Triglycerides","heb": "טריגליצרידים",      "value": 162,  "unit": "mg/dL",   "range": "< 150",      "status": "גבולי"},
        ],
        "summary": "ערך HbA1c גבולי בטווח המצריך מעקב. ניתן לראות גם LDL וטריגליצרידים גבוליים. השילוב ראוי לדיון עם רופא/ת המשפחה.",
        "explanations": [
            {
                "test_label": "HbA1c — 6.1%",
                "badge": "גבולי",
                "badge_type": "yellow",
                "short_summary": "ערך HbA1c גבולי — מצריך מעקב ודיון עם רופא/ת המשפחה.",
                "what_is": "HbA1c משקף את רמות הסוכר הממוצעות בדם במהלך כשלושה חודשים, ולכן הוא עוזר להבין מגמות ולא רק מדידת סוכר חד-פעמית. ערך בטווח 5.7–6.4 מסווג לרוב כגבולי ודורש מעקב.",
                "why_different": [
                    "תזונה עשירה בפחמימות פשוטות",
                    "ירידה ברמת הפעילות הגופנית",
                    "גורמים גנטיים",
                    "עלייה במשקל",
                ],
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
        "questions": [],
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
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 7.9,  "unit": "10³/µL",  "range": "4.5–11.0",   "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 12.8, "unit": "g/dL",    "range": "12.0–16.0",  "status": "תקין"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 7.2,  "unit": "%",       "range": "< 5.7",      "status": "חריג"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 112,  "unit": "mg/dL",   "range": "< 100",      "status": "גבולי"},
        ],
        "summary": "ערך HbA1c מוגבר בבירור מעל הטווח המקובל. ממצא זה מצריך דיון עם רופא/ת המשפחה בהקדם. LDL גבולי.",
        "explanations": [
            {
                "test_label": "HbA1c — 7.2%",
                "badge": "חריג",
                "badge_type": "red",
                "short_summary": "ערך HbA1c מוגבר בבירור — ממצא זה מצריך דיון עם רופא/ת המשפחה.",
                "what_is": "HbA1c משקף את רמות הסוכר הממוצעות בדם במהלך כשלושה חודשים. ערך מעל 6.5 מסווג לרוב כדורש דיון עם רופא/ת המשפחה ובירור נוסף. משמעות הערך תלויה בהיסטוריה הרפואית האישית ובגורמים נוספים.",
                "why_different": [
                    "שינויים בתזונה",
                    "גורמים גנטיים ומשפחתיים",
                    "רמת פעילות גופנית",
                    "שינויים הורמונליים הקשורים לגיל",
                ],
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
        "questions": [],
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
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 5.8,  "unit": "10³/µL",  "range": "4.5–11.0",   "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 12.4, "unit": "g/dL",    "range": "12.0–16.0",  "status": "תקין"},
            {"test": "Ferritin",     "heb": "פריטין",           "value": 14,   "unit": "ng/mL",   "range": "12–150",     "status": "גבולי"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 5.1,  "unit": "%",       "range": "< 5.7",      "status": "תקין"},
        ],
        "summary": "ערך הפריטין גבולי — נמוך בתחתית הטווח התקין. שאר הבדיקות תקינות. בהקשר של תזונה צמחונית וחוויית עייפות קלה — ממצא זה ראוי לדיון עם רופא/ת המשפחה.",
        "explanations": [
            {
                "test_label": "פריטין — 14 ng/mL",
                "badge": "גבולי",
                "badge_type": "yellow",
                "short_summary": "ערך פריטין גבולי-נמוך — כדאי לדון עם רופא/ת המשפחה, במיוחד בהקשר תזונתי.",
                "what_is": "פריטין הוא חלבון שמאחסן ברזל בגוף. הערך משקף את מאגרי הברזל, ולעיתים יכול לרדת עוד לפני שמופיעה ירידה משמעותית בהמוגלובין.",
                "why_different": [
                    "תזונה צמחונית עם ספיגת ברזל מוגבלת",
                    "מחזוריות אצל נשים",
                    "צורך מוגבר בברזל",
                    "ספיגה ירודה של ברזל",
                ],
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
        "questions": [],
        "contact": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרשות בדיקות השלמה, תוסף תזונתי, או מעקב.",
    },
    {
        "id": 7,
        "name": "תמר אלון",
        "age": 35,
        "sex": "נקבה",
        "context": "חולשה כללית וסחרחורת — בדיקת דם ראשונית",
        "scenario_label": "חסר ברזל משמעותי — פריטין ירוד וMCP נמוך",
        "results": [
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 6.0,  "unit": "10³/µL",  "range": "4.5–11.0",   "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 10.8, "unit": "g/dL",    "range": "12.0–16.0",  "status": "חריג"},
            {"test": "Ferritin",     "heb": "פריטין",           "value": 5,    "unit": "ng/mL",   "range": "12–150",     "status": "חריג"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 5.0,  "unit": "%",       "range": "< 5.7",      "status": "תקין"},
        ],
        "summary": "המוגלובין ירוד בבירור מתחת לטווח התקין, ופריטין ירוד מאוד. תבנית זו ראויה לדיון עם רופא/ת המשפחה בהקדם. התסמינים שצוינו — חולשה וסחרחורת — יכולים להיות קשורים לממצאים.",
        "explanations": [
            {
                "test_label": "המוגלובין — 10.8 g/dL",
                "badge": "חריג",
                "badge_type": "red",
                "short_summary": "המוגלובין ירוד בבירור — ממצא זה מצריך דיון עם רופא/ת המשפחה.",
                "what_is": "המוגלובין הוא חלבון בתאי הדם האדומים שנושא חמצן מהריאות אל רקמות הגוף. ערך נמוך יכול להסביר לעיתים עייפות, חולשה או קוצר נשימה.",
                "why_different": [
                    "מאגרי ברזל נמוכים (כפי שמשתקף בפריטין)",
                    "ספיגה ירודה של ברזל",
                    "אבדן דם",
                    "צורך מוגבר בברזל",
                ],
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
        "questions": [],
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
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 11.4, "unit": "10³/µL",  "range": "4.5–11.0",   "status": "גבולי"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 15.2, "unit": "g/dL",    "range": "13.5–17.5",  "status": "תקין"},
            {"test": "Ferritin",     "heb": "פריטין",           "value": 88,   "unit": "ng/mL",   "range": "12–150",     "status": "תקין"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 95,   "unit": "mg/dL",   "range": "< 100",      "status": "תקין"},
        ],
        "summary": "ספירת לויקוציטים (WBC) גבולית מעט מעל הטווח. בהקשר של מחלה ויראלית לאחרונה — ייתכן שהממצא קשור להחלמה. שאר הבדיקות תקינות.",
        "explanations": [
            {
                "test_label": "WBC — 11.4 10³/µL",
                "badge": "גבולי",
                "badge_type": "yellow",
                "short_summary": "ספירת לויקוציטים גבולית — ייתכן שקשורה למחלה הויראלית האחרונה.",
                "what_is": "בדיקת WBC מודדת את מספר תאי הדם הלבנים בדם. תאים אלו הם חלק ממערכת החיסון ועוזרים לגוף להגיב לזיהומים, דלקות ומצבים נוספים.",
                "why_different": [
                    "תגובת מערכת החיסון למחלה ויראלית לאחרונה",
                    "שלב החלמה מזיהום",
                    "מתח פיזי",
                    "גורמים נוספים הדורשים הערכה רפואית",
                ],
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
        "questions": [],
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
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 14.8, "unit": "10³/µL",  "range": "4.5–11.0",   "status": "חריג"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 14.0, "unit": "g/dL",    "range": "13.5–17.5",  "status": "תקין"},
            {"test": "CRP",          "heb": "CRP",              "value": 38,   "unit": "mg/L",    "range": "< 5",        "status": "חריג"},
        ],
        "summary": "WBC מוגבר בבירור ו-CRP גבוה מצביעים על תגובה דלקתית. בהקשר של חום וכאבים — ממצאים אלו מצריכים דיון עם רופא/ת המשפחה בהקדם.",
        "explanations": [
            {
                "test_label": "WBC — 14.8 10³/µL",
                "badge": "חריג",
                "badge_type": "red",
                "short_summary": "WBC מוגבר בשילוב CRP גבוה — ממצא זה מצריך דיון עם רופא/ת המשפחה בהקדם.",
                "what_is": "בדיקת WBC מודדת את מספר תאי הדם הלבנים בדם. תאים אלו הם חלק ממערכת החיסון ועוזרים לגוף להגיב לזיהומים, דלקות ומצבים נוספים. CRP הוא חלבון שעולה בתגובה לדלקת בגוף.",
                "why_different": [
                    "זיהום חיידקי",
                    "זיהום ויראלי",
                    "תגובה דלקתית",
                    "מצבים נוספים הדורשים הערכה רפואית",
                ],
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
        "questions": [],
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
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 8.2,  "unit": "10³/µL",  "range": "4.5–11.0",   "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 12.6, "unit": "g/dL",    "range": "12.0–16.0",  "status": "תקין"},
            {"test": "Ferritin",     "heb": "פריטין",           "value": 22,   "unit": "ng/mL",   "range": "12–150",     "status": "תקין"},
            {"test": "CRP",          "heb": "CRP",              "value": 18,   "unit": "mg/L",    "range": "< 5",        "status": "חריג"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 5.3,  "unit": "%",       "range": "< 5.7",      "status": "תקין"},
        ],
        "summary": "ערך CRP מוגבר — מדד דלקתי. שאר הבדיקות תקינות. בהקשר של עייפות כרונית — ממצא זה ראוי לדיון עם רופא/ת המשפחה.",
        "explanations": [
            {
                "test_label": "CRP — 18 mg/L",
                "badge": "חריג",
                "badge_type": "red",
                "short_summary": "CRP מוגבר — מדד דלקתי שיכול להעיד על תגובה דלקתית בגוף.",
                "what_is": "CRP הוא חלבון המיוצר בכבד ורמתו עולה בתגובה לדלקת, זיהום, או מצבים אחרים בגוף. ערכו יכול לסייע בהערכת תהליכים שונים, אך פירושו המדויק תלוי בהקשר הקליני.",
                "why_different": [
                    "תהליך דלקתי בגוף",
                    "זיהום",
                    "מצבים אוטואימוניים",
                    "גורמים נוספים הדורשים הערכה רפואית",
                ],
                "urgency": "mid",
                "urgency_text": "מומלץ לדון עם רופא/ת המשפחה — מומלץ לתאם תור בהקדם הנוח.",
                "contact_text": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש בירור נוסף, ואם כן — מאיזה סוג.",
                "questions": [
                    "מה יכול להסביר את העלייה ב-CRP בהקשר של העייפות שלי?",
                    "האם יש צורך בבדיקות נוספות כדי להבין את מקור הדלקת?",
                    "האם יש קשר אפשרי בין הERP לתסמינים שלי?",
                    "מתי כדאי לחזור על הבדיקה?",
                    "האם יש גורמי סיכון שכדאי לבדוק?",
                ],
            }
        ],
        "questions": [],
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
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 9.8,  "unit": "10³/µL",  "range": "4.5–11.0",   "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 11.9, "unit": "g/dL",    "range": "12.0–16.0",  "status": "גבולי"},
            {"test": "Ferritin",     "heb": "פריטין",           "value": 16,   "unit": "ng/mL",   "range": "12–150",     "status": "גבולי"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 5.9,  "unit": "%",       "range": "< 5.7",      "status": "גבולי"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 122,  "unit": "mg/dL",   "range": "< 100",      "status": "גבולי"},
            {"test": "Triglycerides","heb": "טריגליצרידים",      "value": 148,  "unit": "mg/dL",   "range": "< 150",      "status": "תקין"},
        ],
        "summary": "מספר ממצאים גבוליים: המוגלובין, פריטין, HbA1c ו-LDL — כולם בתחתית הטווח הגבולי. מומלץ לדון עם רופא/ת המשפחה על כל הממצאים יחד.",
        "explanations": [
            {
                "test_label": "המוגלובין — 11.9 g/dL",
                "badge": "גבולי",
                "badge_type": "yellow",
                "short_summary": "המוגלובין מעט מתחת לטווח — כדאי לדון עם רופא/ת המשפחה.",
                "what_is": "המוגלובין הוא חלבון בתאי הדם האדומים שנושא חמצן. ערך מעט נמוך יכול לנוע ממשמעותי פחות ועד ממצא שדורש מעקב — ההקשר הקליני חשוב.",
                "why_different": [
                    "מאגרי ברזל נמוכים (כפי שמשתקף בפריטין)",
                    "תזונה",
                    "גורמים נוספים",
                ],
                "urgency": "low",
                "urgency_text": "לרוב לא דחוף, אך כדאי לדון עם רופא/ת המשפחה.",
                "contact_text": "רופא/ת המשפחה יוכל/תוכל להחליט האם נדרשות בדיקות נוספות.",
                "questions": [
                    "האם יש קשר בין הממצאים השונים — המוגלובין, פריטין, HbA1c ו-LDL?",
                    "אילו ממצאים חשובים יותר למעקב בשלב זה?",
                    "האם כדאי לחזור על כל הבדיקות או רק על חלק מהן?",
                    "האם יש שינוי באורח החיים שיכול להשפיע על כמה מהערכים יחד?",
                    "האם השינוי התזונתי שביצעתי לאחרונה יכול להסביר חלק מהממצאים?",
                ],
            }
        ],
        "questions": [],
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
            {"test": "WBC",          "heb": "ספירת לויקוציטים", "value": 5.5,  "unit": "10³/µL",  "range": "4.5–11.0",   "status": "תקין"},
            {"test": "Hemoglobin",   "heb": "המוגלובין",        "value": 16.1, "unit": "g/dL",    "range": "13.5–17.5",  "status": "תקין"},
            {"test": "Ferritin",     "heb": "פריטין",           "value": 95,   "unit": "ng/mL",   "range": "12–150",     "status": "תקין"},
            {"test": "HbA1c",        "heb": "HbA1c",            "value": 4.9,  "unit": "%",       "range": "< 5.7",      "status": "תקין"},
            {"test": "LDL",          "heb": "כולסטרול LDL",     "value": 75,   "unit": "mg/dL",   "range": "< 100",      "status": "תקין"},
            {"test": "HDL",          "heb": "כולסטרול HDL",     "value": 62,   "unit": "mg/dL",   "range": "> 40",       "status": "תקין"},
            {"test": "Triglycerides","heb": "טריגליצרידים",      "value": 85,   "unit": "mg/dL",   "range": "< 150",      "status": "תקין"},
        ],
        "summary": "כל תוצאות הבדיקות תקינות ובטווח מצוין. אין ממצאים חריגים או גבוליים. תמונה תואמת אדם צעיר ובריא.",
        "explanations": [],
        "questions": [],
        "contact": "ניתן להמשיך מעקב שגרתי עם רופא/ת המשפחה לפי המלצות הגיל.",
    },
]


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def badge_html(status: str) -> str:
    mapping = {
        "תקין":  ("badge-green",  "🟢 תקין"),
        "גבולי": ("badge-yellow", "🟡 גבולי"),
        "חריג":  ("badge-red",    "🔴 חריג"),
    }
    cls, label = mapping.get(status, ("badge-green", status))
    return f'<span class="badge {cls}">{label}</span>'


def count_statuses(results):
    counts = {"תקין": 0, "גבולי": 0, "חריג": 0}
    for r in results:
        s = r["status"]
        if s in counts:
            counts[s] += 1
    return counts


def lab_row_class(status: str) -> str:
    return {"תקין": "lab-row-normal", "גבולי": "lab-row-border", "חריג": "lab-row-abnorm"}.get(status, "lab-row-normal")


def urgency_class(urgency: str) -> str:
    return {"low": "urgency-low", "mid": "urgency-mid", "high": "urgency-high"}.get(urgency, "urgency-low")


def render_lab_table(results):
    rows_html = ""
    for r in results:
        rc = lab_row_class(r["status"])
        rows_html += f"""
        <tr class="{rc}">
            <td><span class="lab-test-name">{r['heb']}</span><br><small style="color:#888;font-size:0.8rem">{r['test']}</small></td>
            <td><span class="lab-value">{r['value']}</span></td>
            <td><span class="lab-range">{r['unit']}</span></td>
            <td><span class="lab-range">{r['range']}</span></td>
            <td>{badge_html(r['status'])}</td>
        </tr>"""
    return f"""
    <div class="lab-table-wrap">
        <table class="lab-table">
            <thead>
                <tr>
                    <th>בדיקה</th>
                    <th>תוצאה</th>
                    <th>יחידות</th>
                    <th>טווח מקובל</th>
                    <th>סטטוס</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>"""


def render_metric_cards(counts):
    return f"""
    <div class="metric-row">
        <div class="metric-card metric-green">
            <div class="metric-number">{counts['תקין']}</div>
            <div class="metric-label">🟢 תקינים</div>
        </div>
        <div class="metric-card metric-yellow">
            <div class="metric-number">{counts['גבולי']}</div>
            <div class="metric-label">🟡 גבוליים</div>
        </div>
        <div class="metric-card metric-red">
            <div class="metric-number">{counts['חריג']}</div>
            <div class="metric-label">🔴 חריגים</div>
        </div>
    </div>"""


# ─────────────────────────────────────────────
# PAGE RENDERERS
# ─────────────────────────────────────────────

def page_home():
    st.markdown("""
    <div class="page-hero">
        <h1>🏥 MedExplain AI</h1>
        <p>מערכת AI להסבר תוצאות בדיקות דם — שכבת הסבר חכמה בתוך אפליקציית קופת החולים</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>הצהרה חשובה:</strong> מערכת זו היא הוכחת ישימות (PoC) אקדמית בלבד, המשתמשת בנתונים סינתטיים בלבד.
        היא אינה מאובחנת, אינה ממליצה על טיפול, ואינה מחליפה רופא/ת משפחה.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔬</div>
            <div class="feature-title">הבעיה</div>
            <div class="feature-desc">מטופלים רבים מקבלים תוצאות בדיקות דם דרך האפליקציה — ולעיתים מתקשים להבין את משמעותן, עלולים לחוות חרדה מיותרת, או לא יודעים אם הממצא דורש פנייה דחופה.</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">הפתרון</div>
            <div class="feature-desc">שכבת AI מוטמעת באפליקציית הקופה — מסבירה בשפה פשוטה, מתאימה את ההסבר להקשר האישי של המטופל, ומכינה שאלות ממוקדות לשיחה עם הרופא.</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">הגישה הבטוחה</div>
            <div class="feature-desc">המערכת אינה מאבחנת ואינה ממליצה על טיפול. הרופא/ה נשאר/ת הסמכות הקלינית הבלעדית. הלוגיקה מונעת ניסוחים שיכולים לגרום נזק.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col4, col5 = st.columns(2)
    with col4:
        st.markdown("""
        <div class="med-card">
            <h4 style="color:var(--accent-teal);margin-top:0">✅ מה המערכת עושה</h4>
            <ul style="margin:0;padding-right:1.2rem;line-height:2">
                <li>מסבירה בשפה פשוטה מה מודדת כל בדיקה</li>
                <li>מסבירה מדוע ערך עשוי להיות שונה מהטווח</li>
                <li>מציגה רמת דחיפות בצורה רגועה ולא מאיימת</li>
                <li>מכינה שאלות ממוקדות לשיחה עם הרופא</li>
                <li>מציינת למי מומלץ לפנות</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div class="med-card">
            <h4 style="color:var(--red);margin-top:0">🚫 מה המערכת לא עושה</h4>
            <ul style="margin:0;padding-right:1.2rem;line-height:2">
                <li>אינה מאבחנת מחלה</li>
                <li>אינה ממליצה על טיפול תרופתי</li>
                <li>אינה אומרת שאין צורך ברופא</li>
                <li>אינה משתמשת בשפה מאיימת</li>
                <li>אינה מחליפה שיקול קליני</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="med-card-teal" style="margin-top:1rem">
        <strong>🎓 הקשר אקדמי:</strong> מערכת זו פותחה כפרויקט הוכחת ישימות (Proof of Concept) במסגרת קורס Medical AI באוניברסיטה.
        כל הנתונים — שמות, ערכי מעבדה ופרטים קליניים — הם סינתטיים לחלוטין ונוצרו לצרכים חינוכיים בלבד.
    </div>
    """, unsafe_allow_html=True)


def page_dashboard():
    st.markdown("""
    <div class="page-hero" style="padding:1.4rem 2rem;">
        <h1 style="font-size:1.6rem">📋 לוח מטופל</h1>
        <p>בחרו מטופל סינתטי לדוגמה לצפייה בהסבר תוצאות הבדיקות</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        ⚠️ כל הנתונים המוצגים הם סינתטיים לחלוטין. שמות, ערכים ופרטים קליניים בדויים לצרכים חינוכיים בלבד.
    </div>
    """, unsafe_allow_html=True)

    # Patient selector
    patient_options = {
        f"{p['id']}. {p['name']} ({p['age']}, {p['sex']}) — {p['scenario_label']}": p
        for p in PATIENTS
    }
    selected_label = st.selectbox("בחרו מטופל:", list(patient_options.keys()), label_visibility="visible")
    p = patient_options[selected_label]

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # A. Patient header card
    sex_icon = "👩" if p["sex"] == "נקבה" else "👨"
    st.markdown(f"""
    <div class="patient-header">
        <h2>{sex_icon} {p['name']}</h2>
        <p>גיל: {p['age']} &nbsp;|&nbsp; מין: {p['sex']} &nbsp;|&nbsp; הקשר: {p['context']}</p>
        <p style="margin-top:0.5rem;font-size:0.88rem;opacity:0.85">תרחיש: {p['scenario_label']}</p>
    </div>
    """, unsafe_allow_html=True)

    # B. Metric cards
    counts = count_statuses(p["results"])
    st.markdown(render_metric_cards(counts), unsafe_allow_html=True)

    # C. Lab results table
    st.markdown("### 🔬 תוצאות הבדיקות", unsafe_allow_html=False)
    st.markdown(render_lab_table(p["results"]), unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # D. Summary
    st.markdown("### 📝 סיכום ממצאים")
    st.markdown(f'<div class="summary-box">{p["summary"]}</div>', unsafe_allow_html=True)

    # E. Detailed explanations
    if p["explanations"]:
        st.markdown("### 🔎 הסבר מפורט לממצאים")
        for exp in p["explanations"]:
            badge_cls = {"green": "badge-green", "yellow": "badge-yellow", "red": "badge-red"}.get(exp["badge_type"], "badge-green")
            with st.expander(f"📌 {exp['test_label']}  —  סטטוס: {exp['badge']}", expanded=True):
                st.markdown(f"""
                <div class="explain-section">
                    <span class="badge {badge_cls}">{('🟢' if exp['badge_type']=='green' else '🟡' if exp['badge_type']=='yellow' else '🔴')} {exp['badge']}</span>
                    <h4 style="margin-top:0.9rem">סיכום קצר</h4>
                    <p>{exp['short_summary']}</p>
                    <h4>מה הבדיקה מודדת?</h4>
                    <p>{exp['what_is']}</p>
                    <h4>למה הערך יכול להיות שונה?</h4>
                    <ul>{''.join(f'<li>{r}</li>' for r in exp['why_different'])}</ul>
                    <h4>כמה זה דחוף?</h4>
                    <p class="{urgency_class(exp['urgency'])}">{'⚪' if exp['urgency']=='low' else '🟡' if exp['urgency']=='mid' else '🔴'} {exp['urgency_text']}</p>
                    <h4>למי נכון לפנות?</h4>
                    <p>{exp['contact_text']}</p>
                </div>
                """, unsafe_allow_html=True)

                # F. Physician questions
                st.markdown("#### 💬 שאלות מומלצות לרופא/ת המשפחה")
                for q in exp["questions"]:
                    st.markdown(f'<div class="question-card">❓ {q}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="always-item">
            ✅ כל תוצאות הבדיקות תקינות. לא נדרש הסבר מפורט לממצאים חריגים.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # G. Contact section
    st.markdown("### 📞 מי מומלץ לפנות אליו?")
    st.markdown(f"""
    <div class="contact-card">
        <strong>👨‍⚕️ רופא/ת משפחה</strong><br>
        {p['contact']}
    </div>
    <div class="contact-card">
        <strong>ℹ️ הערה חשובה</strong><br>
        ברוב המקרים הצעד הראשון הוא פנייה לרופא/ת המשפחה, שיוכל/תוכל להחליט האם נדרש בירור נוסף או הפניה לגורם מקצועי.
    </div>
    """, unsafe_allow_html=True)


def page_how_it_works():
    st.markdown("""
    <div class="page-hero">
        <h1>⚙️ כיצד זה עובד?</h1>
        <p>זרימת העבודה של שכבת ה-AI בתוך אפליקציית הקופה</p>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("🏥", "שלב 1", "תוצאות מהמעבדה", "תוצאות הבדיקות מתקבלות ישירות ממערכת המעבדה של הקופה ומועברות לתיק הרפואי האלקטרוני."),
        ("📂", "שלב 2", "נתונים מובנים", "הערכים מגיעים כנתונים מובנים מתוך התיק הרפואי — לא כסריקה, לא כטקסט חופשי. כל ערך מוגדר, ממויין ומקושר לטווח הנורמה."),
        ("🤖", "שלב 3", "שכבת AI מסבירה", "מנוע ה-AI מפיק הסבר בשפה פשוטה המותאם לערך הספציפי, להקשר האישי של המטופל ולסטטוס הבדיקה."),
        ("🛡️", "שלב 4", "לוגיקת בטיחות", "לפני הצגת ההסבר, לוגיקת בטיחות בוחנת שאין ניסוחים אבחנתיים, המלצות טיפוליות, או שפה מאיימת."),
        ("💬", "שלב 5", "שאלות לרופא", "המטופל מקבל רשימת שאלות ממוקדות המותאמות לממצא ולהקשרו האישי — להכנה לשיחה עם הרופא."),
        ("👨‍⚕️", "שלב 6", "הרופא נשאר סמכות", "הרופא/ה נשאר/ת הסמכות הקלינית הבלעדית. המערכת משלימה — לא מחליפה — את השיקול הרפואי."),
    ]

    cols = st.columns(3)
    for i, (icon, num, title, desc) in enumerate(steps):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="step-card">
                <div class="step-icon">{icon}</div>
                <div class="step-num">{num}</div>
                <div class="step-title">{title}</div>
                <div class="step-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        if i == 2:
            st.markdown("")
            cols = st.columns(3)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="med-card-teal">
        <strong>🔒 עיקרון המפתח:</strong> שכבת ה-AI פועלת בתוך גבולות מוגדרים מראש של מערכת בריאות מוסדרת.
        בשונה מ-chatbot כללי, היא אינה יכולה לסטות מהמסגרת הבטוחה שהוגדרה.
    </div>
    """, unsafe_allow_html=True)


def page_why_not_chatgpt():
    st.markdown("""
    <div class="page-hero">
        <h1>🤔 למה לא ChatGPT רגיל?</h1>
        <p>השוואה בין chatbot כללי לשכבת AI מוטמעת בתוך מערכת בריאות מוסדרת</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="med-card">
        <p>ייתכן ומטופלים רבים כבר פונים ל-ChatGPT כדי להבין תוצאות בדיקות — זה מובן לחלוטין.
        אך גישה זו מגיעה עם מגבלות משמעותיות. הטבלה הבאה מסכמת את ההבדלים המרכזיים.</p>
        <p><em>הערה: המערכת הנוכחית היא PoC אקדמי. איננו טוענים שהיא מושלמת — אלא שגישה זו
        <strong>עשויה</strong> לשפר את הבטיחות ואת זרימת העבודה הקלינית.</em></p>
    </div>
    """, unsafe_allow_html=True)

    rows = [
        ("🔒 פרטיות", "המטופל מעתיק תוצאות ידנית — שיתוף מידע רפואי עם ספק חיצוני", "הנתונים נשארים בתוך המערכת הסגורה של הקופה"),
        ("📋 נתונים מובנים", "טקסט חופשי שהמטופל כותב — שגיאות, השמטות אפשריות", "ערכי מעבדה מובנים ישירות מהתיק הרפואי"),
        ("🌐 שפה ועיצוב", "ממשק אנגלי בעיקר, לא מותאם לשפה ולתרבות הישראלית", "ממשק עברי RTL מלא, מותאם למטופל הישראלי"),
        ("🛡️ גבולות בטיחות", "ChatGPT עשוי לסטות לאבחון או להרגיע יתר על המידה — תלוי בניסוח", "גבולות שפה מוגדרים מראש — ניסוחים אבחנתיים חסומים"),
        ("⚕️ פיקוח קליני", "אין שילוב עם מערכת הרופא", "מתוכנן להשתלב בזרימת העבודה של הרופא"),
        ("📂 היסטוריה רפואית", "אין גישה לבדיקות קודמות להשוואה", "יכול להציג מגמה לאורך זמן מתוך התיק הרפואי"),
        ("⚠️ סיכון הרגעה יתר", "ChatGPT עשוי להרגיע מטופל ולהציע 'לא לדאוג' — ללא הקשר קליני", "שפה ניטרלית, תמיד מפנה לרופא/ה"),
        ("🎯 מיקוד", "תשובות כלליות, לא תמיד מותאמות לגיל, מין והקשר", "הסבר מותאם לפרופיל הספציפי של המטופל"),
    ]

    table_rows = ""
    for feature, chatgpt, hmo in rows:
        table_rows += f"""
        <tr>
            <td><strong>{feature}</strong></td>
            <td class="compare-bad">❌ {chatgpt}</td>
            <td class="compare-good">✅ {hmo}</td>
        </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto;">
        <table class="compare-table">
            <thead>
                <tr>
                    <th>היבט</th>
                    <th>Chatbot ציבורי (דוגמת ChatGPT)</th>
                    <th>שכבת AI מוטמעת בקופה (MedExplain)</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="med-card-blue" style="margin-top:1rem">
        <strong>⚖️ הצהרת אמינות:</strong> אנו לא טוענים שהמערכת הנוכחית מושלמת. כמו כל כלי AI, היא חשופה לטעויות,
        הרגעה יתרה, ועמימות. היתרון המרכזי הוא <em>פעולה בתוך גבולות מוגדרים של מערכת בריאות מוסדרת</em> —
        ולא כ-chatbot כללי ללא גבולות.
    </div>
    """, unsafe_allow_html=True)


def page_safety():
    st.markdown("""
    <div class="page-hero">
        <h1>🛡️ בטיחות ואתיקה</h1>
        <p>עקרונות הבטיחות, האתיקה והפרטיות של המערכת</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["⚖️ עקרונות בסיסיים", "🚫 מה המערכת לעולם לא תאמר", "🔒 פרטיות ואבטחה"])

    with tab1:
        col1, col2 = st.columns(2)
        principles = [
            ("🎓", "כלי חינוכי בלבד", "המערכת מיועדת להסבר ולהכנת שאלות בלבד. היא אינה חלק מזרימת טיפול קלינית."),
            ("🩺", "הרופא הוא הסמכות", "הרופא/ת המשפחה נשאר/ת הסמכות הקלינית הבלעדית. ההמלצה תמיד היא לשוחח עם הרופא."),
            ("🔬", "נתונים סינתטיים", "כל הנתונים בגרסת ה-PoC הם סינתטיים לחלוטין. אין שימוש בנתוני מטופלים אמיתיים."),
            ("🧠", "פיקוח אנושי", "המערכת אינה עצמאית. היא פועלת בתוך מסגרת שנקבעה על ידי אנשי מקצוע רפואיים."),
            ("⚠️", "סיכון הזיה (Hallucination)", "כמו כל מערכת AI, קיים סיכון לתשובות לא מדויקות. לכן השפה מוגדרת מראש ולא נוצרת באופן חופשי."),
            ("😌", "סיכון הרגעה יתר", "הרגעה לא מבוססת עלולה להזיק. המערכת תמיד ממליצה על פנייה לרופא ואינה אומרת 'אין מה לדאוג'."),
            ("♿", "נגישות ושוויון", "יש לוודא שהמערכת נגישה לאוכלוסיות מגוונות — כולל אוכלוסיות מבוגרות, דוברות שפות שונות, ובעלות מגבלויות."),
            ("📊", "הטיית נתונים", "מודלי AI עלולים לשקף הטיות הקיימות בנתוני האימון. יש לנטר ולבחון את הפלטים לאורך זמן."),
        ]
        for i, (icon, title, desc) in enumerate(principles):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"""
                <div class="med-card" style="margin-bottom:0.8rem">
                    <div style="font-size:1.5rem;margin-bottom:0.3rem">{icon}</div>
                    <strong style="color:var(--accent-teal)">{title}</strong>
                    <p style="margin:0.4rem 0 0 0;font-size:0.92rem;color:var(--text-muted)">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="med-card">
            <p>המערכת מיועדת לעולם <strong>לא לשלוח</strong> ניסוחים אלה — גם אם הם עשויים להיות נכונים קלינית.
            השפה נקבעת מראש ומוגדרת בלוגיקת הבטיחות.</p>
        </div>
        """, unsafe_allow_html=True)

        never_says = [
            '"יש לך סוכרת"',
            '"יש לך אנמיה"',
            '"אתה חייב תרופה"',
            '"עליך לקחת X"',
            '"אין צורך לפנות לרופא"',
            '"הממצא מסוכן"',
            '"זה חמור"',
            '"זה ממאיר"',
            '"אין מה לדאוג"',
            '"הכל בסדר, אינך צריך רופא"',
        ]
        always_says = [
            '"ממצא זה מצריך דיון עם רופא/ת המשפחה"',
            '"ייתכן שהערך קשור ל..."',
            '"יכול להתאים ל... אך ההקשר הקליני חשוב"',
            '"כדאי להשוות לבדיקות קודמות"',
            '"רופא/ת המשפחה יוכל/תוכל להחליט האם נדרש בירור"',
            '"בהקשר הקליני המתאים"',
        ]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🚫 לעולם לא תאמר")
            for s in never_says:
                st.markdown(f'<div class="never-item">{s}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown("#### ✅ תמיד תשתמש בניסוח כזה")
            for s in always_says:
                st.markdown(f'<div class="always-item">{s}</div>', unsafe_allow_html=True)

    with tab3:
        considerations = [
            ("🔐", "סגירות הנתונים", "הנתונים נשארים בתוך מערכת הקופה הסגורה. לא מועברים לשרת חיצוני."),
            ("🗑️", "מינימיזציית נתונים", "המערכת משתמשת אך ורק בנתונים הנחוצים לתפקודה — ללא איסוף מידע עודף."),
            ("👁️", "שקיפות", "המטופל יודע שהוא מקבל הסבר אוטומטי ממוחשב, ולא פסיקה קלינית."),
            ("✅", "הסכמה מדעת", "בגרסה מלאה, המטופל יאשר הסכמתו לשימוש בכלי הסברה ממוחשב."),
            ("📋", "רגולציה", "מערכת כזו תדרוש אישור רגולטורי ממשרד הבריאות ומהגורמים המוסמכים."),
            ("🔍", "מעקב ואיכות", "יש לנטר את פלטי המערכת לאורך זמן ולבחון אותם מול מומחים קליניים."),
        ]
        cols = st.columns(3)
        for i, (icon, title, desc) in enumerate(considerations):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="step-card" style="margin-bottom:0.8rem">
                    <div class="step-icon">{icon}</div>
                    <div class="step-title">{title}</div>
                    <div class="step-desc">{desc}</div>
                </div>
                """, unsafe_allow_html=True)


def page_feedback():
    st.markdown("""
    <div class="feedback-hero">
        <h2>💬 משוב מהמטופל</h2>
        <p>האם ההסבר עזר לך? המשוב שלך עוזר לשפר את המערכת בעתיד</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        ⚠️ זהו טופס משוב לדוגמה בלבד. הנתונים אינם נשמרים. נועד להדגמת מנגנון הערכה מבוסס-מטופל.
    </div>
    """, unsafe_allow_html=True)

    with st.form("feedback_form"):
        st.markdown('<div class="med-card">', unsafe_allow_html=True)

        st.markdown("#### 1️⃣ עד כמה ההסבר היה ברור?")
        clarity = st.slider("", 1, 5, 3, key="clarity",
                            help="1 = לא ברור כלל, 5 = ברור מאוד")
        clarity_labels = {1: "לא ברור כלל", 2: "לא ממש ברור", 3: "ברור חלקית", 4: "ברור", 5: "ברור מאוד"}
        st.markdown(f'<p style="color:var(--accent-teal);font-weight:700;margin-top:-0.5rem">{clarity_labels[clarity]}</p>', unsafe_allow_html=True)

        st.markdown("#### 2️⃣ האם ההסבר עזר לך להבין את משמעות התוצאה?")
        understanding = st.slider("", 1, 5, 3, key="understanding",
                                  help="1 = לא עזר בכלל, 5 = עזר מאוד")
        understanding_labels = {1: "לא עזר בכלל", 2: "עזר מעט", 3: "עזר חלקית", 4: "עזר", 5: "עזר מאוד"}
        st.markdown(f'<p style="color:var(--accent-teal);font-weight:700;margin-top:-0.5rem">{understanding_labels[understanding]}</p>', unsafe_allow_html=True)

        st.markdown("#### 3️⃣ האם ברור לך יותר מה כדאי לשאול את הרופא?")
        questions_clear = st.radio("", ["כן", "חלקית", "לא"], key="questions_clear", horizontal=True)

        st.markdown("#### 4️⃣ האם ההסבר הפחית את רמת החשש שלך?")
        anxiety = st.radio("", ["כן מאוד", "במידה מסוימת", "לא", "לא רלוונטי"], key="anxiety", horizontal=True)

        st.markdown("#### 5️⃣ האם היית משתמש/ת בכלי כזה באפליקציית קופת החולים?")
        would_use = st.radio("", ["כן", "אולי", "לא"], key="would_use", horizontal=True)

        st.markdown("#### 6️⃣ מה עדיין לא היה ברור?")
        open_feedback = st.text_area("", placeholder="כתב/י כאן בחופשיות...", height=100, key="open_feedback")

        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("📤 שליחת משוב")

    if submitted:
        st.success("✅ תודה על המשוב!")
        st.markdown("""
        <div class="med-card-teal">
            <strong>תודה על המשוב.</strong> בגרסה עתידית ניתן יהיה להשתמש במשובים מסוג זה כדי לשפר את בהירות ההסברים,
            לזהות ניסוחים מבלבלים, ולוודא שהמערכת באמת מסייעת למטופלים להבין את תוצאות הבדיקות.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="med-card-blue">
        <strong>🎓 מנגנון הערכה מבוסס-מטופל</strong><br><br>
        מנגנון המשוב מאפשר להעריך את הצלחת המערכת מנקודת מבט של המטופל:
        האם ההסבר היה ברור? האם הופחתה חרדה? האם המטופל יודע טוב יותר מה לשאול את הרופא?<br><br>
        בשונה ממדדים טכניים (דיוק, Recall וכו'), הערכה זו מכוונת לתוצאה הקלינית המשמעותית:
        <em>האם הכלי עזר למטופל לפעול נכון?</em>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR & NAVIGATION
# ─────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div class="logo-icon">🏥</div>
            <div class="logo-name">MedExplain AI</div>
            <div class="logo-sub">מערכת הסבר בדיקות דם</div>
        </div>
        <hr style="border:1px solid var(--border);margin:0.5rem 0 1rem 0">
        """, unsafe_allow_html=True)

        nav_options = {
            "🏠 עמוד הבית": "home",
            "📋 לוח מטופל": "dashboard",
            "⚙️ כיצד זה עובד": "how",
            "🤔 למה לא ChatGPT?": "chatgpt",
            "🛡️ בטיחות ואתיקה": "safety",
            "💬 משוב מהמטופל": "feedback",
        }

        selected = st.radio(
            "ניווט:",
            list(nav_options.keys()),
            key="nav",
            label_visibility="collapsed"
        )

        st.markdown("<hr style='border:1px solid var(--border);margin:1rem 0'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.78rem;color:var(--text-muted);text-align:right;line-height:1.6">
            <span class="sidebar-badge">PoC</span> גרסת הדגמה בלבד<br>
            נתונים סינתטיים לחלוטין<br>
            לא לשימוש קליני<br><br>
            <strong>MedExplain AI</strong><br>
            פרויקט קורס Medical AI<br>
            © 2024 Academic PoC
        </div>
        """, unsafe_allow_html=True)

        return nav_options[selected]


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    # Inject CSS
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(CARD_CSS, unsafe_allow_html=True)

    # Sidebar navigation
    page = render_sidebar()

    # Route
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
