# MedExplain AI — מערכת AI להסבר תוצאות בדיקות דם

A polished, patient-facing Medical AI proof-of-concept built with Streamlit, designed as a realistic simulation of an AI explanation layer integrated into an Israeli HMO application.

---

## Project Overview

**MedExplain AI** is an academic course proof-of-concept that demonstrates how AI can serve as an *explanation layer* inside a healthcare app — helping patients understand their blood test results, reducing anxiety around borderline findings, and preparing more informed questions for their physician.

> ⚠️ This application uses **fully synthetic data only**. It does not provide diagnosis, treatment recommendations, or real medical advice. All patient scenarios are fictional and created solely for educational purposes.

---

## Features

- 🏥 **6 navigation pages** — Home, Patient Dashboard, How It Works, Why Not ChatGPT?, Safety & Ethics, Patient Feedback  
- 🧑‍⚕️ **12 realistic synthetic patient scenarios** with varied lab findings  
- 📊 **Visual lab result cards** with green/yellow/red status badges  
- 💬 **Patient-specific physician questions** tailored to each scenario  
- 🔒 **Safety-first language** — no diagnosis, no treatment instructions  
- 🇮🇱 **Full Hebrew RTL interface** — right-to-left layout throughout  
- 📱 **Healthcare app aesthetic** inspired by Israeli HMO portals (Clalit Online / Maccabi / Meuhedet style — original design, no copyrighted assets used)  

---

## Supported Lab Tests

| Test | Hebrew |
|------|--------|
| WBC | ספירת לויקוציטים |
| Hemoglobin | המוגלובין |
| Ferritin | פריטין |
| HbA1c | המוגלובין מסוכר |
| LDL | כולסטרול LDL |
| HDL | כולסטרול HDL |
| Triglycerides | טריגליצרידים |
| CRP | חלבון C-reactive |

---

## How to Run

### Prerequisites

- Python 3.9 or higher  
- pip

### Installation

```bash
# Clone or download the project
cd medexplain_ai

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## Deploy to Streamlit Cloud

1. Push the project to a GitHub repository (both `app.py` and `requirements.txt`)  
2. Go to [share.streamlit.io](https://share.streamlit.io)  
3. Connect your GitHub repository  
4. Set the main file to `app.py`  
5. Click **Deploy**

No additional secrets or environment variables are required.

---

## Project Structure

```
medexplain_ai/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Academic Context

This proof-of-concept was developed as part of a university Medical AI course. It demonstrates:

- **Clinical understanding** — realistic lab value ranges and patient contexts  
- **Healthcare workflow integration** — simulates HMO app integration  
- **Patient-centered design** — plain-language explanations, RTL Hebrew  
- **AI safety** — safety-first language, no diagnostic claims  
- **Privacy awareness** — synthetic data only, no real patient data  
- **PoC evaluation** — patient feedback mechanism for measuring explanation quality  

---

## Ethical Disclaimer

> This system is an **educational tool only**. It does not replace clinical judgment. The physician remains the sole clinical authority. No diagnosis, prognosis, or treatment recommendation is provided or implied. All data in this application is entirely synthetic and fictional.

---

## Design Inspiration

The UI is inspired by the clean, soft pastel, rounded-card aesthetic of Israeli HMO apps (Clalit Online, Maccabi Digital, Meuhedet). All design elements are original — no logos, trademarks, or copyrighted assets from those organizations are used.

---

*MedExplain AI — Medical AI Course Project | Academic PoC | Synthetic Data Only*
