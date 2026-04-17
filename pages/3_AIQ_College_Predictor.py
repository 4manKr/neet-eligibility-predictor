import streamlit as st
import pandas as pd
import os

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

st.set_page_config(page_title="All India Quota Predictor | NEET UG", page_icon="🇮🇳", layout="wide")

st.title("🇮🇳 All India Quota (MCC) College Predictor")
st.markdown(
    "Enter your **NEET rank** and **category** to predict your realistic chances at "
    "government medical colleges under the **15% All India Quota** counselled by MCC. "
    "The system applies a hidden **10% rank safety buffer** for more accurate predictions."
)
st.markdown("---")

aiq_df = load_aiq_data()

if aiq_df is None:
    st.error(
        "Error: Could not load the MCC AIQ Cutoff Excel file. "
        "Make sure `Aman_TAB_India_MCC_AIQ_MBBS_Cutoff_2025.xlsx` exists in the project folder."
    )
else:
    # ----- PRE-PROCESS: ensure numeric columns -----
    for col in ['cutoff', 'score', 'Fee1']:
        if col in aiq_df.columns:
            aiq_df[col] = pd.to_numeric(aiq_df[col], errors='coerce')

    # ----- INPUT SECTION -----
    input_col1, input_col2, input_col3 = st.columns(3)

    with input_col1:
        student_rank = st.number_input(
            "Enter your All India Rank (AIR):",
            min_value=1,
            value=50000,
            step=1000,
            key="aiq_rank"
        )

    with input_col2:
        all_categories = sorted(aiq_df['Category_Name'].dropna().unique().tolist())
        category_choice = st.selectbox("Select your Category:", all_categories, key="aiq_category")

    with input_col3:
        all_rounds = sorted(aiq_df['round'].dropna().unique().tolist())
        round_choice = st.selectbox("Select Counselling Round:", all_rounds, key="aiq_round")

    # ----- OPTIONAL FEE FILTER -----
    fee_col = aiq_df['Fee1'].dropna()
    if not fee_col.empty:
        min_fee = int(fee_col.min())
        max_fee = int(fee_col.max())
        if min_fee < max_fee:
            fee_range = st.slider(
                "Filter by Fee Range (₹):",
                min_value=min_fee,
                max_value=max_fee,
                value=(min_fee, max_fee),
                step=5000,
                format="₹%d",
                key="aiq_fee"
            )
        else:
            fee_range = None
    else:
        fee_range = None

    if st.button("🔍 Predict Target Colleges", type="primary", key="aiq_predict"):
        st.divider()

        # Step 1: Apply 10% safety buffer
        adjusted_rank = student_rank + (0.10 * student_rank)

        # Step 2: Filter by category (exact match) and round
        filtered = aiq_df[
            (aiq_df['Category_Name'] == category_choice) &
            (aiq_df['round'] == round_choice) &
            (aiq_df['cutoff'].notna())
        ].copy()

        # Step 3: Cutoff Rank >= adjusted_rank (colleges where last admitted rank is higher
        # numerically, meaning the candidate's rank is better/lower than cutoff)
        eligible = filtered[filtered['cutoff'] >= adjusted_rank].copy()

        # Step 4: Apply fee filter
        if fee_range is not None:
            eligible = eligible[
                (eligible['Fee1'] >= fee_range[0]) & (eligible['Fee1'] <= fee_range[1])
            ]

        # Step 5: Sort by cutoff ascending (best chances first)
        eligible = eligible.sort_values(by='cutoff', ascending=True)

        if not eligible.empty:
            st.success(
                f"🎉 Based on your rank **{student_rank:,}** (adjusted to **{int(adjusted_rank):,}**), "
                f"category **{category_choice}**, round **{round_choice}**, "
                f"you have realistic chances at **{len(eligible)}** All India Quota colleges!"
            )

            # Prepare display dataframe
            display_df = eligible[['Institute_Name', 'Category_Name', 'Fee1', 'cutoff', 'round']].copy()
            display_df = display_df.rename(columns={
                'Institute_Name': 'Institute Name',
                'Category_Name': 'Category',
                'Fee1': 'Fee',
                'cutoff': 'Cutoff Rank',
                'round': 'Round'
            })
            display_df['Fee'] = display_df['Fee'].apply(
                lambda x: f"₹{int(x):,}" if pd.notna(x) else "N/A"
            )
            display_df['Cutoff Rank'] = display_df['Cutoff Rank'].apply(
                lambda x: f"{int(x):,}" if pd.notna(x) else "N/A"
            )

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.error(
                "No colleges found for your rank and category. "
                "Try a higher rank range or different category."
            )
