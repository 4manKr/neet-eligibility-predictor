STATE_RULES = {
    # ------------------ CATEGORY 1: Domicile Only ------------------
    "Andaman & Nicobar Islands": {
        "questions": [
            ("q1", "Are you a Domicile holder of the Andaman & Nicobar Islands?")
        ],
        "eval_logic": lambda ans: ans["q1"]
    },
    "Bihar": {
        "questions": [
            ("q1", "Are your parents recognized residents of Bihar, OR are they refugees / Govt employees posted in Bihar?")
        ],
        "eval_logic": lambda ans: ans["q1"]
    },
    "Madhya Pradesh": {
        "questions": [
            ("q1", "Are you a Domicile holder of Madhya Pradesh?"),
            ("q2", "Are you a child of Defence / Central Govt employees currently posted in MP?")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"]
    },
    "Manipur": {
        "questions": [
            ("q1", "Are you a permanent resident or Domicile holder of Manipur?")
        ],
        "eval_logic": lambda ans: ans["q1"]
    },
    "Mizoram": {
        "questions": [
            ("q1", "Are you a permanent resident / Domicile holder of Mizoram?")
        ],
        "eval_logic": lambda ans: ans["q1"]
    },
    "Odisha": {
        "questions": [
            ("q1", "Are you a permanent native of Odisha?"),
            ("q2", "Are you a child of an All India Service (AIS) officer in the Odisha cadre?")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"]
    },
    "Punjab": {
        "questions": [
            ("q1", "Are you a bonafide resident of Punjab?"),
            ("q2", "Are you a child of Defence / Central Govt personnel exempted from typical residency?")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"]
    },
    "Tamil Nadu": {
        "questions": [
            ("q1", "Are you a bona fide resident or hold Nativity of Tamil Nadu?")
        ],
        "eval_logic": lambda ans: ans["q1"]
    },
    "West Bengal (Proforma A1/B)": {
        "questions": [
            ("q1", "Do you or your parents have 10-year continuous residence in West Bengal with a valid Domicile certificate?")
        ],
        "eval_logic": lambda ans: ans["q1"]
    },
    
    # ------------------ CATEGORY 2: Schooling Only ------------------
    "Delhi (DU/State Quota)": {
        "questions": [
            ("q1", "Did you pass Class 12 from a recognized school in Delhi-NCR (CBSE/ICSE/JMI affiliated)?")
        ],
        "eval_logic": lambda ans: ans["q1"]
    },
    
    # ------------------ CATEGORY 3: Either / Or ------------------
    "Andhra Pradesh": {
        "questions": [
            ("q1", "Did you study continuously for 4 years in a local AU/OU/SVU area?"),
            ("q2", "Have you resided permanently in an AU/OU/SVU area?"),
            ("q3", "Did you study for at least 7 years in the state of Andhra Pradesh?")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"] or ans["q3"]
    },
    "Telangana": {
        "questions": [
            ("q1", "Did you study continuously for 4 years in Telangana?"),
            ("q2", "Have you established residence in a local Telangana area?"),
            ("q3", "Did you study for at least 7 years in Telangana?")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"] or ans["q3"]
    },
    "Karnataka": {
        "questions": [
            ("q1", "Did you study for 7 years in Karnataka (between Class 1 to 12)?"),
            ("q2", "Did you pass Class 11 and 12 from Karnataka?"),
            ("q3", "Did your parent study for 7 years in Karnataka?"),
            ("q4", "Does your parent hold Karnataka Domicile AND pass the Kannada language test?")
        ],
        "eval_logic": lambda ans: ans["q1"] or (ans["q2"] and ans["q3"]) or ans["q4"]
    },
    "Kerala": {
        "questions": [
            ("q1", "Are you of Keralite origin or hold Kerala Domicile?"),
            ("q2", "Did you complete a qualifying course in Kerala AND do your parents meet employment/residency requirements?")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"]
    },
    "Uttar Pradesh": {
        "questions": [
            ("q1", "Are you a native of UP with resident parents (3+ yrs)?"),
            ("q2", "Did you pass BOTH Class 10 & 12 from recognized schools located in UP?")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"]
    },
    "Uttarakhand": {
        "questions": [
            ("q1", "Do you hold Permanent Residency within Uttarakhand?"),
            ("q2", "Did you pass BOTH Class 10 & 12 from Uttarakhand? (Without permanent residency)")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"]
    },
    "Rajasthan": {
        "questions": [
            ("q1", "Are you a certified resident (pure domicile) of Rajasthan?"),
            ("q2", "Have your parents stayed in Rajasthan for 10 years AND you completed Class 8-12 in Rajasthan?")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"]
    },
    "Puducherry": {
        "questions": [
            ("q1", "Do you have 5-year continuous residence in the UT?"),
            ("q2", "Did you complete 5 successive years of schooling in Puducherry with concurrent residence?")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"]
    },
    "Meghalaya": {
        "questions": [
            ("q1", "Are you a permanent resident of any NE state?"),
            ("q2", "Did you pass Class 11 & 12 from a recognized school in Meghalaya?")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"]
    },
    
    # ------------------ CATEGORY 4: Both Required ------------------
    "Assam": {
        "questions": [
            ("q1", "Have you or your parents lived continuously in Assam for 20+ years?"),
            ("q2", "Did you study Class 7 to 12 continuously in Assam?")
        ],
        "eval_logic": lambda ans: ans["q1"] and ans["q2"]
    },
    "Chhattisgarh": {
        "questions": [
            ("q1", "Were you born in Chhattisgarh AND hold domicile?"),
            ("q2", "Did you pass Class 12 from CG Board or a recognized board in the state?")
        ],
        "eval_logic": lambda ans: ans["q1"] and ans["q2"]
    },
    "Goa": {
        "questions": [
            ("q1", "Do you have 10 yrs residence in Goa (or 5 yrs if parents/grandparents were born there)?"),
            ("q2", "Did you pass Class 12 from a recognized Goa institution?")
        ],
        "eval_logic": lambda ans: ans["q1"] and ans["q2"]
    },
    "Gujarat": {
        "questions": [
            ("q1", "Were you born in OR domiciled in Gujarat?"),
            ("q2", "Did you pass BOTH Class 10 & 12 from Gujarat schools?")
        ],
        "eval_logic": lambda ans: ans["q1"] and ans["q2"]
    },
    "Haryana": {
        "questions": [
            ("q1", "Do you have 10 yrs residence in Haryana with bonafide resident parents?"),
            ("q2", "Did you pass Class 12 from a recognized Haryana school?")
        ],
        "eval_logic": lambda ans: ans["q1"] and ans["q2"]
    },
    "Himachal Pradesh": {
        "questions": [
            ("q1", "Do you hold Bonafide Himachali status?"),
            ("q2", "Did you pass at least 2 exams between Class 8 and 12 from HP schools?")
        ],
        "eval_logic": lambda ans: ans["q1"] and ans["q2"]
    },
    "Jammu & Kashmir / Ladakh": {
        "questions": [
            ("q1", "Do you hold Domicile of the UT?"),
            ("q2", "Did you pass Class 12 from a recognized board within the UT (with PCB + English)?")
        ],
        "eval_logic": lambda ans: ans["q1"] and ans["q2"]
    },
    "Jharkhand": {
        "questions": [
            ("q1", "Do you hold a valid Jharkhand Domicile certificate?"),
            ("q2", "Did you complete your 10+2 from recognized Jharkhand schools?")
        ],
        "eval_logic": lambda ans: ans["q1"] and ans["q2"]
    },
    "Maharashtra": {
        "questions": [
            ("q1", "Do you have a strict Domicile/Birth certificate or Parental Domicile in Maharashtra?"),
            ("q2", "Did you pass Class 10 AND 12 from an institution situated in Maharashtra?")
        ],
        "eval_logic": lambda ans: ans["q1"] and ans["q2"]
    },
    "Tripura": {
        "questions": [
            ("q1", "Do you hold Permanent residency (parents lived 10+ yrs in Tripura)?"),
            ("q2", "Did you pass Class 12 from a Tripura-recognized school?")
        ],
        "eval_logic": lambda ans: ans["q1"] and ans["q2"]
    },
    "West Bengal (Proforma A2)": {
        "questions": [
            ("q1", "Do you have 10-year continuous residence in West Bengal?"),
            ("q2", "Did you pass your 10+2 from a West Bengal institution?")
        ],
        "eval_logic": lambda ans: ans["q1"] and ans["q2"]
    },
    
    # ------------------ CATEGORY 5: Special / Mixed ------------------
    "Arunachal Pradesh": {
        "questions": [
            ("q1", "Are you an APST (Arunachal Pradesh Scheduled Tribe) candidate? [If Yes, you get 80% seats automatically]"),
            ("q2", "NON-APST: Do you have 3+ yrs residence in AP?"),
            ("q3", "NON-APST: Did you pass Class 12 from an AP school?")
        ],
        "eval_logic": lambda ans: ans["q1"] or (ans["q2"] and ans["q3"])
    },
    "Chandigarh": {
        "questions": [
            ("q1", "Did you complete schooling in Chandigarh schools as a regular student?"),
            ("q2", "Do your parents have long-term residence OR Govt service in Chandigarh?")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"]
    },
    "Dadra & NH / Daman & Diu": {
        "questions": [
            ("q1", "Do your parents have Domicile AND did you study Class 8-12 in local schools?"),
            ("q2", "Do your parents have Domicile even if you studied elsewhere?"),
            ("q3", "Are you a child of a Govt employee posted long-term in the UT?")
        ],
        "eval_logic": lambda ans: ans["q1"] or ans["q2"] or ans["q3"]
    }
}

def get_state_info(state_name):
    # Retrieve the state's specific questionnaire mapping
    return STATE_RULES.get(state_name, None)
