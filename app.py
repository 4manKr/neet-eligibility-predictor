import streamlit as st
import pandas as pd
import os
from rules_engine import get_state_info

# Set page configuration
st.set_page_config(
    page_title="NEET UG State Quota Discovery",
    page_icon="🎓",
    layout="wide"
)

# Application title
st.title("🎓 NEET UG State Quota Discovery Engine")
st.markdown("Discover exactly which Indian States and UTs you qualify for under the 85% regional quota.")
st.markdown("---")

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
    
    st.subheader("Your Academic & Residential Background")
    
    col1, col2 = st.columns(2)
    
    # Store dynamic answers
    domicile_answers = {}
    schooling_answers = {}
    
    with col1:
        st.markdown("**📍 Domicile Linkage**")
        domicile_state = st.selectbox(
            "Which state holds your Domicile?", 
            ["-- Select State --", "None"] + available_states
        )
        
        if domicile_state not in ["-- Select State --", "None"]:
            state_info = get_state_info(domicile_state)
            if state_info:
                st.info(f"Please affirm conditions for **{domicile_state}**:")
                for q_id, q_text in state_info["questions"]:
                    domicile_answers[q_id] = st.checkbox(q_text, key=f"dom_{domicile_state}_{q_id}")
            else:
                st.warning("Deep logic mapping pending for this state.")
                
    with col2:
        st.markdown("**🏫 Schooling Linkage**")
        schooling_state = st.selectbox(
            "In which state did you complete your Schooling (Class 10/12)?", 
            ["-- Select State --", "None"] + available_states
        )
        
        if schooling_state not in ["-- Select State --", "None"]:
            if schooling_state == domicile_state:
                st.success(f"Questions for **{schooling_state}** match your Domicile and are successfully unified. Answer them on the left.")
            else:
                state_info = get_state_info(schooling_state)
                if state_info:
                    st.info(f"Please affirm conditions for **{schooling_state}**:")
                    for q_id, q_text in state_info["questions"]:
                        schooling_answers[q_id] = st.checkbox(q_text, key=f"sch_{schooling_state}_{q_id}")
                else:
                    st.warning("Deep logic mapping pending for this state.")

    if st.button("Discover My Eligible States", type="primary"):
        if domicile_state == "-- Select State --" or schooling_state == "-- Select State --":
            st.warning("Please select both your Domicile and Schooling states (or choose 'None').")
        else:
            st.divider()
            st.subheader("Your Verified Eligibility Results")
            
            eligible_states = []
            not_eligible_states = []
            
            for _, row in df.iterrows():
                target_state = row['State']
                eligibility_type = row['Eligibility Type']
                rule = row['Key Rule Summary']
                
                is_eligible = False
                
                # Check target against strictly mapped Domicile rules
                if target_state == domicile_state:
                    state_info = get_state_info(target_state)
                    if state_info:
                        is_eligible = state_info["eval_logic"](domicile_answers)
                
                # Check target against strictly mapped Schooling rules (if it didn't pass via Domicile)
                if not is_eligible and target_state == schooling_state:
                    state_info = get_state_info(target_state)
                    eval_answers = domicile_answers if domicile_state == schooling_state else schooling_answers
                    if state_info:
                        is_eligible = state_info["eval_logic"](eval_answers)
                            
                # If target state is unconnected structurally (not selected by candidate at all)
                if target_state != domicile_state and target_state != schooling_state:
                    has_domicile = (domicile_state == target_state)  # Will be False
                    has_schooling = (schooling_state == target_state) # Will be False
                    
                    if eligibility_type == 'Domicile Only':
                        is_eligible = has_domicile
                    elif eligibility_type == 'Schooling Only':
                        is_eligible = has_schooling
                    elif eligibility_type == 'Either / Or':
                        is_eligible = has_domicile or has_schooling
                    elif eligibility_type == 'Both Required':
                        is_eligible = has_domicile and has_schooling
                    elif eligibility_type == 'Special':
                        is_eligible = False 
                
                if is_eligible:
                    eligible_states.append((target_state, rule, eligibility_type))
                else:
                    not_eligible_states.append(target_state)
            
            if eligible_states:
                st.success(f"🎉 **You form legal eligibility for {len(eligible_states)} state(s)!**")
                for state_name, rule, eth_type in eligible_states:
                    with st.expander(f"✅ {state_name}"):
                        st.write(f"**Basis for eligibility:** {eth_type}")
                        st.info(f"**Official Rule Passed:** {rule}")
            else:
                st.error("You do not meet the stringent criteria for any state quotas based on your exact answers.")

st.markdown("---")
st.caption("A tool built with Streamlit. Note: Predictive mapping checks complex frameworks locally. Always cross-check official counseling brochures.")
