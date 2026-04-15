import streamlit as st
import pandas as pd
import os
from rules_engine import get_state_info

# Set page configuration
st.set_page_config(
    page_title="NEET UG Centralized Counselling",
    page_icon="🎓",
    layout="wide"
)

# Application title
st.title("🎓 NEET UG Centralized Counselling Portal")
st.markdown("Discover your 85% regional quota eligibility and predict your Deemed College chances using intelligent historical variance.")
st.markdown("---")

@st.cache_data
def load_state_data():
    excel_path = 'neet ug state quota eligibility.xlsx'
    
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
    excel_path = 'TAB_India_Deemed_MBBS_Cutoff_2025.xlsx'
    if not os.path.exists(excel_path):
        return None
    try:
        df = pd.read_excel(excel_path, header=3)
        return df
    except Exception as e:
        return None

state_df = load_state_data()
deemed_df = load_deemed_data()

tab1, tab2 = st.tabs(["🏛️ 85% State Quota Predictor", "🏥 Deemed College Predictor"])

# ---------------- TAB 1: STATE QUOTA ----------------
with tab1:
    if state_df is None:
        st.error("Error: Could not load the State Quota Eligibility Excel file.")
    else:
        available_states = sorted(state_df['State'].tolist())
        
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
                
                for _, row in state_df.iterrows():
                    target_state = row['State']
                    eligibility_type = row['Eligibility Type']
                    rule = row['Key Rule Summary']
                    
                    is_eligible = False
                    
                    if target_state == domicile_state:
                        state_info = get_state_info(target_state)
                        if state_info:
                            is_eligible = state_info["eval_logic"](domicile_answers)
                    
                    if not is_eligible and target_state == schooling_state:
                        state_info = get_state_info(target_state)
                        eval_answers = domicile_answers if domicile_state == schooling_state else schooling_answers
                        if state_info:
                            is_eligible = state_info["eval_logic"](eval_answers)
                                
                    if target_state != domicile_state and target_state != schooling_state:
                        has_domicile = (domicile_state == target_state)
                        has_schooling = (schooling_state == target_state)
                        
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
                
                if eligible_states:
                    st.success(f"🎉 **You form legal eligibility for {len(eligible_states)} state(s)!**")
                    for state_name, rule, eth_type in eligible_states:
                        with st.expander(f"✅ {state_name}"):
                            st.write(f"**Basis for eligibility:** {eth_type}")
                            st.info(f"**Official Rule Passed:** {rule}")
                else:
                    st.error("You do not meet the stringent criteria for any state quotas based on your exact answers.")

# ---------------- TAB 2: DEEMED PREDICTOR ----------------
with tab2:
    if deemed_df is None:
        st.error("Error: Could not load the Deemed Cutoff Excel file. Make sure it is named 'TAB_India_Deemed_MBBS_Cutoff_2025.xlsx' and exists in the project folder.")
    else:
        st.header("🏥 Deemed Medical College Predictor")
        st.markdown("Enter your rank to see your chances. The system intelligently runs a hidden **10% performance variance** on your rank during calculation to safely predict borderline college matches.")
        
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            student_rank = st.number_input("Enter your All India Rank (AIR):", min_value=1, value=500000, step=1000)
        with d_col2:
            round_choice = st.selectbox("Select Counselling Round:", ["R1", "R2", "R3"])
            
        if st.button("Predict Target Colleges", type="primary"):
            st.divider()
            
            rank_col = f"{round_choice} Rank"
            
            # The Hidden Variance Logic: Boost the student's rank by 10%
            # Rank 100,000 -> treated as 90,000. Effectively boosting chances.
            effective_rank = student_rank * 0.90
            
            # Copy dataframe and enforce numeric conversion (silencing 'XX' strings into NaN)
            temp_df = deemed_df.copy()
            temp_df[rank_col] = pd.to_numeric(temp_df[rank_col], errors='coerce')
            
            # Filter colleges where target cutoff rank is worse (i.e. numerically higher) than effective rank
            eligible_deemed = temp_df[temp_df[rank_col] >= effective_rank]
            
            # Sort by cutoff tightness (closest cutoff to their effective rank first)
            eligible_deemed = eligible_deemed.sort_values(by=rank_col, ascending=True)
            
            if not eligible_deemed.empty:
                st.success(f"🎉 Based on your rank and variance threshold, you have predictable chances at **{len(eligible_deemed)}** Deemed Colleges in {round_choice}!")
                
                # Format to remove NaN/decimals from display
                display_cols = ['Institute Name', 'State', rank_col]
                ui_dataframe = eligible_deemed[display_cols].rename(columns={rank_col: "Historical Target Rank"})
                
                st.dataframe(
                    ui_dataframe,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.error("No Deemed colleges matched your variance parameters in this round. Consider applying to state quotas or tweaking the predicted round!")

st.markdown("---")
st.caption("Developed securely. Note: AI evaluations are predictive guides based on 2024-2025 data architectures.")
