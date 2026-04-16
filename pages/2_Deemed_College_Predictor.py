import streamlit as st
import pandas as pd
import sys
import os

# Ensure project root is on sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.data_loader import load_deemed_data

st.set_page_config(page_title="Deemed College Predictor | NEET UG", page_icon="🏥", layout="wide")

st.title("🏥 Deemed Medical College Predictor")
st.markdown(
    "Enter your rank to see your chances. The system intelligently runs a hidden **10% rank variance** "
    "on your rank during calculation to safely predict borderline college matches."
)
st.markdown("---")

deemed_df = load_deemed_data()

if deemed_df is None:
    st.error(
        "Error: Could not load the Deemed Cutoff Excel file. "
        "Make sure `Aman_TAB_India_Deemed_MBBS_Cutoff_2025.xlsx` exists in the project folder."
    )
else:
    # ----- PRE-PROCESS: convert XX → NaN for rank/score/fee columns -----
    rank_score_cols = ['R1 Rank', 'R1 Score', 'R2 Rank', 'R2 Score', 'R3 Rank', 'R3 Score', 'Fee']
    for col in rank_score_cols:
        if col in deemed_df.columns:
            deemed_df[col] = deemed_df[col].replace('XX', pd.NA)
            deemed_df[col] = pd.to_numeric(deemed_df[col], errors='coerce')

    # ----- INPUT SECTION -----
    d_col1, d_col2, d_col3 = st.columns(3)
    with d_col1:
        student_rank = st.number_input("Enter your All India Rank (AIR):", min_value=1, value=500000, step=1000)
    with d_col2:
        round_choice = st.selectbox("Select Counselling Round:", ["R1", "R2", "R3"])
    with d_col3:
        all_categories = sorted(deemed_df['Category'].dropna().unique().tolist())
        category_choice = st.selectbox("Filter by Category:", ["All"] + all_categories)

    # ----- OPTIONAL FEE FILTER -----
    fee_col = deemed_df['Fee'].dropna()
    if not fee_col.empty:
        min_fee = int(fee_col.min())
        max_fee = int(fee_col.max())
        fee_range = st.slider(
            "Filter by Fee Range (₹):",
            min_value=min_fee,
            max_value=max_fee,
            value=(min_fee, max_fee),
            step=50000,
            format="₹%d"
        )
    else:
        fee_range = None

    if st.button("Predict Target Colleges", type="primary"):
        st.divider()

        rank_col = f"{round_choice} Rank"
        adjusted_student_rank = student_rank * 1.10

        temp_df = deemed_df.copy()

        base_eligible = temp_df[
            (temp_df[rank_col] >= adjusted_student_rank) &
            (temp_df[rank_col].notna())
        ].copy()

        if category_choice == "All":
            eligible_deemed = base_eligible.copy()
        else:
            specific = base_eligible[base_eligible['Category'] == category_choice]
            open_cat = base_eligible[base_eligible['Category'] == 'OPEN']
            eligible_deemed = pd.concat([specific, open_cat]).drop_duplicates().copy()

        if fee_range is not None:
            eligible_deemed = eligible_deemed[
                (eligible_deemed['Fee'] >= fee_range[0]) & (eligible_deemed['Fee'] <= fee_range[1])
            ]

        if not eligible_deemed.empty:
            eligible_deemed = eligible_deemed.sort_values(by=rank_col, ascending=True)

            st.success(
                f"🎉 Based on your rank **{student_rank:,}** (adjusted to {adjusted_student_rank:,.0f}), "
                f"you have predictable chances at **{len(eligible_deemed)}** "
                f"Deemed Colleges in **{round_choice}**!"
            )

            display_df = eligible_deemed[['Institute Name', 'State', 'Category', 'Fee', rank_col]].copy()
            display_df = display_df.rename(columns={rank_col: "Cutoff Rank"})
            display_df['Fee'] = display_df['Fee'].apply(lambda x: f"₹{int(x):,}" if pd.notna(x) else "N/A")

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.error(
                "No Deemed colleges matched your variance parameters in this round. "
                "Consider applying to state quotas or tweaking the predicted round!"
            )