import pandas as pd
import sys
import os

def predict_eligibility():
    excel_path = r'c:\Users\Aman Kumar\OneDrive\Desktop\TABINDIA\neet ug state quota eligibility.xlsx'
    
    if not os.path.exists(excel_path):
        print(f"Error: Could not find Excel file at {excel_path}")
        return

    try:
        # The main header starts at row 3 (index 2)
        df = pd.read_excel(excel_path, header=2)
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    # Normalize column names by replacing newlines with spaces
    df.columns = df.columns.str.replace('\n', ' ')

    # Drop rows where 'Eligibility Type' is missing
    df = df.dropna(subset=['Eligibility Type'])
    
    # Strip whitespace from string columns to avoid mismatches
    df['State'] = df['State / UT'].str.strip()
    df['Eligibility Type'] = df['Eligibility Type'].str.strip()
    df['Key Rule Summary'] = df['Key Rule Summary'].str.strip()

    available_states = df['State'].tolist()
    
    print("\n" + "="*50)
    print(" NEET UG State Quota Eligibility Predictor ")
    print("="*50)
    
    state_input = input("\nEnter the name of the state you want to check: ").strip()
    
    # Find state (case insensitive partial/exact match)
    matches = df[df['State'].str.lower() == state_input.lower()]
    if matches.empty:
        # Try a substring match if exact match fails
        matches = df[df['State'].str.lower().str.contains(state_input.lower(), na=False)]
        if matches.empty:
            print(f"\nState '{state_input}' not found in the Excel rules!")
            return
        elif len(matches) > 1:
            print(f"\nMultiple states matched '{state_input}'. Please be more specific.")
            print("Matches:", ", ".join(matches['State'].tolist()))
            return
            
    state_row = matches.iloc[0]
        
    state_name = state_row['State']
    eligibility_type = state_row['Eligibility Type']
    rule_summary = state_row['Key Rule Summary']
    
    print(f"\n--- Checking eligibility for: {state_name} ---")
    
    domicile_input = input(f"Do you have domicile in {state_name}? (yes/no): ").strip().lower()
    schooling_input = input(f"Did you complete your schooling in {state_name}? (yes/no): ").strip().lower()
    
    has_domicile = domicile_input in ['yes', 'y', 'true', '1']
    has_schooling = schooling_input in ['yes', 'y', 'true', '1']
    
    is_eligible = False
    details = ""
    
    if eligibility_type == 'Domicile Only':
        if has_domicile:
            is_eligible = True
            details = "You are eligible because this state requires Domicile only, and you have it."
        else:
            is_eligible = False
            details = "You are NOT eligible because this state requires Domicile, which you don't have."
            
    elif eligibility_type == 'Schooling Only':
        if has_schooling:
            is_eligible = True
            details = "You are eligible because this state requires Schooling only, and you have it."
        else:
            is_eligible = False
            details = "You are NOT eligible because this state requires Schooling, which you don't have."
            
    elif eligibility_type == 'Either / Or':
        if has_domicile or has_schooling:
            is_eligible = True
            details = "You are eligible because this state requires either Domicile OR Schooling, and you meet at least one criteria."
        else:
            is_eligible = False
            details = "You are NOT eligible because this state requires either Domicile OR Schooling, and you have neither."
            
    elif eligibility_type == 'Both Required':
        if has_domicile and has_schooling:
            is_eligible = True
            details = "You are eligible because you have both Domicile AND Schooling in this state."
        else:
            is_eligible = False
            details = "You are NOT eligible. This state requires BOTH Domicile AND Schooling, which you do not fully meet."
            
    elif eligibility_type == 'Special':
        print("\n" + "="*50)
        print(" Result: DEPENDS ON SPECIAL CONDITIONS ")
        print("="*50)
        print("This state has special/mixed frameworks. It cannot be determined with simple yes/no.")
        print(f"The rule is: {rule_summary}")
        return
    else:
        print("\nUnknown applicability.")
        return
        
    print("\n" + "="*50)
    state_result = "ELIGIBLE" if is_eligible else "NOT ELIGIBLE"
    print(f" Result: {state_result} ")
    print("="*50)
    print("Reason:", details)
    print("\nKey Rule for this state:")
    print(rule_summary)

if __name__ == "__main__":
    try:
        predict_eligibility()
    except KeyboardInterrupt:
        print("\nExiting...")
