import streamlit as st

st.set_page_config(
    page_title="NEET UG Centralized Counselling Portal",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 NEET UG Centralized Counselling Portal")
st.markdown("Welcome to the smartest NEET counselling intelligence hub.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏛️ 85% State Quota Predictor")
    st.markdown(
        """
        Discover which states you are legally eligible for under the **85% regional quota**.
        
        - Answer dynamic state-specific questions
        - Covers Domicile, Schooling, and Special eligibility types
        - Backed by official 2024-25 counselling rulebooks
        """
    )
    st.page_link("pages/1_State_Quota_Predictor.py", label="Open State Quota Predictor →", icon="🏛️")

with col2:
    st.subheader("🏥 Deemed College Predictor")
    st.markdown(
        """
        Predict your chances at **Deemed Medical Colleges** using historical cutoff data.
        
        - Intelligent 10% rank variance for borderline matches
        - Filter by Category (OPEN, Minority quotas, etc.)
        - Filter by Fee range to find affordable options
        """
    )
    st.page_link("pages/2_Deemed_College_Predictor.py", label="Open Deemed College Predictor →", icon="🏥")

st.markdown("---")
st.caption("Developed securely By Aman Kumar. Note: AI evaluations are predictive guides based on 2024-2025 data architectures.")
