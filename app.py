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
        
    if st.button("Discover My Eligible States", type="primary"):
        if domicile_state == "-- Select State --" or schooling_state == "-- Select State --":
            st.warning("Please select both your Domicile and Schooling states (or choose 'None').")
        else:
            st.divider()
            st.subheader("2. Your Eligibility Results")
            
            eligible_states = []
            special_states = []
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
                    special_states.append((target_state, rule))
                    continue # handled separately
                
                if is_eligible:
                    eligible_states.append((target_state, rule, eligibility_type))
                else:
                    not_eligible_states.append(target_state)
            
            # --- Display Results ---
            
            # Display Eligible States
            if eligible_states:
                st.success(f"🎉 **You are strongly eligible for {len(eligible_states)} state(s)!**")
                for state_name, rule, eth_type in eligible_states:
                    with st.expander(f"✅ {state_name}"):
                        st.write(f"**Basis for eligibility:** {eth_type}")
                        st.info(f"**Rule snippet:** {rule}")
            else:
                st.error("You are not broadly eligible for any standard state quotas based on these primary rules alone.")
                
            # Display Special Frameworks
            if special_states:
                st.markdown("---")
                st.warning(f"⚠️ **{len(special_states)} state(s) have Special / Mixed conditions.**")
                st.markdown("Your eligibility depends on specific exceptions (like APST vs Non-APST, parent long-term service, etc.)")
                for state_name, rule in special_states:
                    with st.expander(f"🔍 {state_name} (Requires Review)"):
                        st.info(f"**Rule snippet:** {rule}")

st.markdown("---")
st.caption("A tool built with Streamlit. Note: This predicts purely off general 85% regional quota rules. Always cross-check official counseling brochures.")
