import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(
    page_title="NEET UG State Quota Eligibility Predictor",
    page_icon="🎓",
    layout="centered"
)

# Application title
st.title("🎓 NEET UG State Quota Eligibility Predictor")
st.markdown("Check if you meet the Domicile or Schooling requirements for 85% State Quota counselling across different Indian states and UTs.")
st.markdown("---")

# Function to load data
@st.cache_data
def load_data():
    # Use relative path so it works on Streamlit Cloud!
    excel_path = 'neet ug state quota eligibility.xlsx'
    
    if not os.path.exists(excel_path):
        st.error(f"Error: Could not find Excel file at '{excel_path}'. Ensure it is in the same folder as this script!")
        return None

    try:
        # The main header starts at row 3 (index 2 in pandas but passing header=2)
        df = pd.read_excel(excel_path, header=2)
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

    # Normalize column names by replacing newlines with spaces
    df.columns = df.columns.str.replace('\n', ' ')

    # Drop rows where 'Eligibility Type' is missing
    df = df.dropna(subset=['Eligibility Type'])
    
    # Strip whitespace from string columns to avoid mismatches
    df['State'] = df['State / UT'].str.strip()
    df['Eligibility Type'] = df['Eligibility Type'].str.strip()
    df['Key Rule Summary'] = df['Key Rule Summary'].str.strip()
    
    return df

df = load_data()

if df is not None:
    available_states = df['State'].tolist()
    
    # 1. State Selection
    st.subheader("1. Select Your Target State")
    selected_state = st.selectbox("Which State or UT are you aiming for?", ["-- Select a State --"] + available_states)
    
    if selected_state != "-- Select a State --":
        # 2. Input Criteria
        st.subheader("2. Your Academic & Residential Background")
        col1, col2 = st.columns(2)
        
        with col1:
            has_domicile = st.radio(f"Do you have a **Domicile** for {selected_state}?", ["No", "Yes"]) == "Yes"
            
        with col2:
            has_schooling = st.radio(f"Did you complete your **Schooling** (Class 10/12) in {selected_state}?", ["No", "Yes"]) == "Yes"
            
        # Add a submit button
        if st.button("Check Eligibility", type="primary"):
            st.divider()
            st.subheader("3. Eligibility Result")
            
            # Fetch rule for selected state
            state_row = df[df['State'] == selected_state].iloc[0]
            eligibility_type = state_row['Eligibility Type']
            rule_summary = state_row['Key Rule Summary']
            
            is_eligible = False
            details = ""
            status_color = "red"
            
            # Logic implementation
            if eligibility_type == 'Domicile Only':
                if has_domicile:
                    is_eligible = True
                    details = "You are **eligible** because this state requires Domicile only, and you have it."
                else:
                    is_eligible = False
                    details = "You are **NOT eligible** because this state strictly requires Domicile, which you don't have."
                    
            elif eligibility_type == 'Schooling Only':
                if has_schooling:
                    is_eligible = True
                    details = "You are **eligible** because this state requires Schooling only, and you meet the requirement."
                else:
                    is_eligible = False
                    details = "You are **NOT eligible** because this state strictly requires Schooling, which you haven't completed there."
                    
            elif eligibility_type == 'Either / Or':
                if has_domicile or has_schooling:
                    is_eligible = True
                    details = "You are **eligible** because this state requires either Domicile OR Schooling, and you meet at least one condition."
                else:
                    is_eligible = False
                    details = "You are **NOT eligible** because this state requires at least one (Domicile OR Schooling), and you have neither."
                    
            elif eligibility_type == 'Both Required':
                if has_domicile and has_schooling:
                    is_eligible = True
                    details = "You are **eligible** because you have both Domicile AND Schooling in this state."
                else:
                    is_eligible = False
                    details = "You are **NOT eligible**. This state requires BOTH Domicile AND Schooling, which you do not fully meet."
                    
            elif eligibility_type == 'Special':
                st.warning("⚠️ **DEPENDS ON SPECIAL CONDITIONS**")
                st.info("This state has special mixed frameworks. The simple yes/no prediction cannot give a definitive answer.")
                st.markdown(f"**The precise rule is:**\n> {rule_summary}")
                st.stop()
                
            # Display Final Results
            if is_eligible:
                st.success("✅ **STATUS: ELIGIBLE**")
                st.markdown(details)
            else:
                st.error("❌ **STATUS: NOT ELIGIBLE**")
                st.markdown(details)
                
            with st.expander("View the exact rule for this state"):
                st.info(f"**State Requirement Type:** {eligibility_type}\n\n**Official Rule Summary:**\n{rule_summary}")

st.markdown("---")
st.caption("A tool built with Streamlit. Note: Make sure to double-check official counseling brochures for exceptions before final submission.")
