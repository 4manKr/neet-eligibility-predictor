import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(
    page_title="NEET UG State Quota Discovery",
    page_icon="🎓",
    layout="wide"
)

# Application title
st.title("🎓 NEET UG State Quota Discovery Engine")
st.markdown("Input your Domicile and Schooling states below to instantly discover **all** the Indian States and UTs where you are eligible for the 85% State Quota!")
st.markdown("---")

# Function to load data
@st.cache_data
def load_data():
    excel_path = 'neet ug state quota eligibility.xlsx'
    
    if not os.path.exists(excel_path):
        st.error(f"Error: Could not find Excel file at '{excel_path}'. Ensure it is in the same folder as this script!")
        return None

    try:
        df = pd.read_excel(excel_path, header=2)
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

    df.columns = df.columns.str.replace('\n', ' ')
    df = df.dropna(subset=['Eligibility Type'])
    
    df['State'] = df['State / UT'].str.strip()
    df['Eligibility Type'] = df['Eligibility Type'].str.strip()
    df['Key Rule Summary'] = df['Key Rule Summary'].str.strip()
    
    return df

df = load_data()

if df is not None:
    available_states = sorted(df['State'].tolist())
    
    st.subheader("1. Your Academic & Residential Background")
    
    col1, col2 = st.columns(2)
    with col1:
        domicile_state = st.selectbox(
            "📍 Which state holds your Domicile?", 
            ["-- Select State --", "None"] + available_states
        )
        
    with col2:
        schooling_state = st.selectbox(
            "🏫 In which state did you complete your Schooling (Class 10/12)?", 
            ["-- Select State --", "None"] + available_states
        )
        
    st.markdown("---")
    st.subheader("2. Special Exceptions (Optional)")
    st.caption("These apply to special frameworks in state rules.")
    
    spec_col1, spec_col2 = st.columns(2)
    with spec_col1:
        is_apst = st.checkbox("I am an APST (Arunachal Pradesh Scheduled Tribe) Candidate")
    with spec_col2:
        is_govt_employee_ward = st.checkbox("My parents are long-term Central/State Govt Employees posted in Chandigarh or Dadra & Nagar Haveli")
        
    st.markdown("---")
        
    if st.button("Discover My Eligible States", type="primary"):
        if domicile_state == "-- Select State --" or schooling_state == "-- Select State --":
            st.warning("Please select both your Domicile and Schooling states (or choose 'None').")
        else:
            st.subheader("3. Your Eligibility Results")
            
            eligible_states = []
            not_eligible_states = []
            
            # Analyze every state
            for _, row in df.iterrows():
                target_state = row['State']
                eligibility_type = row['Eligibility Type']
                rule = row['Key Rule Summary']
                
                has_domicile = (domicile_state == target_state)
                has_schooling = (schooling_state == target_state)
                
                is_eligible = False
                
                if eligibility_type == 'Domicile Only':
                    is_eligible = has_domicile
                elif eligibility_type == 'Schooling Only':
                    is_eligible = has_schooling
                elif eligibility_type == 'Either / Or':
                    is_eligible = has_domicile or has_schooling
                elif eligibility_type == 'Both Required':
                    is_eligible = has_domicile and has_schooling
                elif eligibility_type == 'Special':
                    # Handle the 3 Special States
                    if 'Arunachal Pradesh' in target_state:
                        # APST has 80% reservation. Non-APST needs residence AND schooling
                        is_eligible = is_apst or (has_domicile and has_schooling)
                        
                    elif 'Chandigarh' in target_state:
                        # Schooling OR parents residence/govt service
                        is_eligible = has_schooling or has_domicile or is_govt_employee_ward
                        
                    elif 'Dadra' in target_state or 'Daman' in target_state:
                        # Priority list (domicile or schooling or parental posting)
                        is_eligible = has_domicile or has_schooling or is_govt_employee_ward
                
                if is_eligible:
                    # Provide clearer context for special states inside the UI
                    if eligibility_type == 'Special':
                        eth_type = "Special/Mixed (Condition Met)"
                    else:
                        eth_type = eligibility_type
                        
                    eligible_states.append((target_state, rule, eth_type))
                else:
                    not_eligible_states.append(target_state)
            
            # --- Display Results ---
            
            # Display Eligible States
            if eligible_states:
                st.success(f"🎉 **You are eligible for {len(eligible_states)} state(s) quotas!**")
                for state_name, rule, eth_type in eligible_states:
                    with st.expander(f"✅ {state_name}"):
                        st.write(f"**Basis for eligibility:** {eth_type}")
                        st.info(f"**Official Rule snippet:** {rule}")
            else:
                st.error("You do not clearly meet the primary rules for any state's 85% quota based on your inputs.")
                
st.markdown("---")
st.caption("A tool built with Streamlit. Note: This predicts purely off general 85% regional quota rules. Always cross-check official counseling brochures.")
