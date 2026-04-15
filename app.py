import streamlit as st
import pandas as pd
import os
from rules_engine import get_state_info

# Set page configuration
st.set_page_config(
    page_title="NEET UG State Quota Predictor",
    page_icon="🎓",
    layout="wide"
)

# Application title
st.title("🎓 NEET UG State Quota Eligibility Suite")
st.markdown("---")

# Function to load data
@st.cache_data
def load_data():
    excel_path = 'neet ug state quota eligibility.xlsx'
    
    if not os.path.exists(excel_path):
        st.error(f"Error: Could not find Excel file at '{excel_path}'. Ensure it is in the same folder!")
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
    
    # Create Tabs
    tab1, tab2 = st.tabs(["🌎 Global Discovery Engine", "🔬 Advanced State Specific Filter"])
    
    # ---------------- TAB 1: GLOBAL DISCOVERY ----------------
    with tab1:
        st.header("🌎 Global Discovery Engine")
        st.markdown("Input your broad Domicile and Schooling states below to discover all the Indian States where you hold basic eligibility.")
        
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
                st.subheader("Your General Eligibility Results")
                
                eligible_states = []
                not_eligible_states = []
                
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
                        is_eligible = False  # Special excluded from broad match
                    
                    if is_eligible:
                        eligible_states.append((target_state, rule, eligibility_type))
                    else:
                        not_eligible_states.append(target_state)
                
                if eligible_states:
                    st.success(f"🎉 **You broadly meet the criteria for {len(eligible_states)} state(s)!**")
                    for state_name, rule, eth_type in eligible_states:
                        with st.expander(f"✅ {state_name}"):
                            st.write(f"**Basis:** {eth_type}")
                            st.info(f"**Rule Snippet:** {rule}")
                else:
                    st.error("You are not broadly eligible for standard state quotas based purely on general matching.")
                    
    # ---------------- TAB 2: ADVANCED FILTER ----------------
    with tab2:
        st.header("🔬 Deep State-Specific Sub-Filter")
        st.markdown("Select a specific State to answer precise qualifying questions based on its exact legal framework. This is crucial for **Either/Or**, **Both Required**, and **Special Case** states.")
        
        target_state = st.selectbox(
            "Select the Target State you wish to apply for:",
            ["-- Select State --"] + available_states
        )
        
        if target_state != "-- Select State --":
            state_info = get_state_info(target_state)
            
            # Fetch rule for UI context
            ref_rule = df[df['State'] == target_state].iloc[0]['Key Rule Summary']
            st.info(f"**Official Rule Context:**\n> {ref_rule}")
            
            if state_info:
                st.write("### Please answer the following specific clauses:")
                
                # Checkbox dictionary
                answers = {}
                for q_id, q_text in state_info["questions"]:
                    # Create a toggle checkbox for each specific rule question
                    answers[q_id] = st.checkbox(q_text, key=f"{target_state}_{q_id}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Evaluate Specific Eligibility", type="primary", key="eval_btn"):
                    # Pass the answers to the custom lambda logic function
                    is_pass = state_info["eval_logic"](answers)
                    
                    if is_pass:
                        st.success(f"✅ **STATUS: ELIGIBLE** for {target_state}")
                        st.balloons()
                        st.markdown(f"You have confirmed meeting the necessary clauses defined by {target_state}.")
                    else:
                        st.error(f"❌ **STATUS: NOT EXPLICITLY ELIGIBLE** for {target_state}")
                        st.markdown("You have not selected the combination of clauses required to fulfill the State quota rules.")
            else:
                st.warning("Advanced mapped questionnaire formulation is pending for this specific State in the system update.")

st.markdown("---")
st.caption("A tool built with Streamlit. Note: Deep rules are logically translated from Excel summaries. Always verify with full official counseling brochures.")
