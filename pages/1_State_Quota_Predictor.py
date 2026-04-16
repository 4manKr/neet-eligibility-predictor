import streamlit as st
import sys
import os

# Ensure project root is on sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.data_loader import load_state_data
from rules_engine import get_state_info

st.set_page_config(page_title="State Quota Predictor | NEET UG", page_icon="🏛️", layout="wide")

st.title("🏛️ 85% State Quota Predictor")
st.markdown("Discover which states you are eligible for under the **85% regional quota** based on your domicile and schooling background.")
st.markdown("---")

state_df = load_state_data()

if state_df is None:
    st.error("Error: Could not load the State Quota Eligibility Excel file. Please ensure `neet ug state quota eligibility.xlsx` exists in the project root.")
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
