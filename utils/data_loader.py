import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_state_data():
    """Load and clean the State Quota Eligibility Excel file."""
    excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'neet ug state quota eligibility.xlsx')

    if not os.path.exists(excel_path):
        return None

    try:
        df = pd.read_excel(excel_path, header=2)
        df.columns = df.columns.str.replace('\n', ' ')
        df = df.dropna(subset=['Eligibility Type'])
        df['State'] = df['State / UT'].str.strip()
        df['Eligibility Type'] = df['Eligibility Type'].str.strip()
        df['Key Rule Summary'] = df['Key Rule Summary'].str.strip()
        return df
    except Exception as e:
        return None

@st.cache_data
def load_deemed_data():
    """Load the Aman TAB India Deemed MBBS Cutoff Excel file with Fee & Category columns."""
    excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Aman_TAB_India_Deemed_MBBS_Cutoff_2025.xlsx')
    if not os.path.exists(excel_path):
        return None
    try:
        df = pd.read_excel(excel_path, header=3)
        return df
    except Exception as e:
        return None

@st.cache_data
def load_aiq_data():
    """Load the Aman TAB India MCC AIQ MBBS Cutoff Excel file."""
    excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Aman_TAB_India_MCC_AIQ_MBBS_Cutoff_2025.xlsx')
    if not os.path.exists(excel_path):
        return None
    try:
        df = pd.read_excel(excel_path)
        return df
    except Exception as e:
        return None
