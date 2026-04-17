# 🎓 NEET UG Centralized Counselling Portal

A smart, multi-tab **NEET UG counselling prediction tool** built with [Streamlit](https://streamlit.io/). Helps medical aspirants discover their eligibility and predict realistic college admissions across multiple counselling pathways.

---

## ✨ Features

### 🏛️ 85% State Quota Predictor
- Discover which states you are legally eligible for under the **85% regional quota**
- Answer dynamic, state-specific eligibility questions (Domicile, Schooling, Special criteria)
- Backed by official 2024-25 counselling rulebooks covering **30+ States/UTs**

### 🏥 Deemed Medical College Predictor
- Predict your chances at **Deemed Medical Colleges** using historical cutoff data
- Intelligent **10% rank variance** for borderline safety predictions
- Filter by Category (OPEN, Minority quotas, etc.) and Fee range

### 🇮🇳 All India Quota (MCC) College Predictor
- Predict your chances at **Government Medical Colleges** under the **15% All India Quota**
- Category-wise filtering (UR, OBC, SC, ST, EWS, PwD)
- Round-wise prediction (Round 1, Round 2, Mop-up, Stray)
- Fee range slider for budget-conscious decisions
- **10% rank safety buffer** to avoid overly optimistic predictions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/neet-eligibility-predictor.git
cd neet-eligibility-predictor

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
TABINDIA/
├── app.py                          # Home page with navigation
├── pages/
│   ├── 1_State_Quota_Predictor.py  # 85% State Quota eligibility engine
│   ├── 2_Deemed_College_Predictor.py # Deemed college rank predictor
│   └── 3_AIQ_College_Predictor.py  # All India Quota (MCC) predictor
├── utils/
│   ├── __init__.py
│   └── data_loader.py             # Cached data loading functions
├── rules_engine.py                # State-wise eligibility rules & logic
├── eligibility_predictor.py       # CLI-based eligibility checker
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📊 Data Sources

| File | Description |
|------|-------------|
| `neet ug state quota eligibility.xlsx` | State-wise eligibility rules (Domicile, Schooling, etc.) |
| `Aman_TAB_India_Deemed_MBBS_Cutoff_2025.xlsx` | Deemed university cutoff data with fees |
| `Aman_TAB_India_MCC_AIQ_MBBS_Cutoff_2025.xlsx` | MCC All India Quota cutoff data (7000+ records) |

---

## 🔧 How Prediction Works

1. **Input**: Candidate enters their NEET rank, category, and counselling round
2. **Safety Buffer**: Rank is internally increased by **10%** (`adjusted_rank = rank × 1.10`)
3. **Filtering**: Dataset is filtered where `Cutoff Rank ≥ adjusted_rank` and category matches exactly
4. **Anti-Overshoot**: Removes colleges where cutoff is unrealistically far from the candidate's rank
5. **Sorting**: Results sorted by Cutoff Rank (ascending) — best chances shown first
6. **Display**: Clean table with Institute Name, Fee, Cutoff Rank, and Round

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Data Processing**: [Pandas](https://pandas.pydata.org/)
- **Excel Parsing**: [OpenPyXL](https://openpyxl.readthedocs.io/)

---

## 👤 Author

**Aman Kumar**

---

## ⚠️ Disclaimer

This tool provides **predictive guidance** based on 2024-2025 historical counselling data. Actual admissions depend on official cutoffs released by MCC/State authorities. Always verify with official sources before making counselling decisions.
