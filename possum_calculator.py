# pages/possum_calculator.py
import streamlit as st
import math

# POSSUM physiological variables with proper scoring options
physiological_variables = {
    "Age": {
        "options": ["≤ 60", "61-70", "≥ 71"],
        "scores": [1, 2, 4]
    },
    "Cardiac signs | Chest X-ray": {
        "options": [
            "Normal",
            "Cardiac drugs or steroids", 
            "Oedema; warfarin | Borderline cardiomegaly",
            "Jugular venous pressure | Cardiomegaly"
        ],
        "scores": [1, 2, 4, 8]
    },
    "Respiratory signs | Chest X-ray": {
        "options": [
            "Normal",
            "Shortness of breath on exertion | Mild chronic obstructive airway disease",
            "Shortness of breath on stairs | Moderate chronic obstructive airway disease", 
            "Shortness of breath at rest | Any other change"
        ],
        "scores": [1, 2, 4, 8]
    },
    "Systolic blood pressure (mmHg)": {
        "options": ["110-130", "131-170 or 100-109", "≥ 171 or 90-99", "≤ 89"],
        "scores": [1, 2, 4, 8]
    },
    "Pulse rate (bpm)": {
        "options": ["50-80", "81-100 or 40-49", "101-120 or ≤ 39", "≥ 121"],
        "scores": [1, 2, 4, 8]
    },
    "Glasgow Coma Scale": {
        "options": ["15", "12-14", "9-11", "≤ 8"],
        "scores": [1, 2, 4, 8]
    },
    "Hemoglobin (g/dL)": {
        "options": [
            "13-16 (male), 11.5-14.5 (female)",
            "10-12.9 or 16.1-17",
            "8-9.9 or 17.1-18",
            "≤ 7.9 or ≥ 18.1"
        ],
        "scores": [1, 2, 4, 8]
    },
    "White cell count (×10⁹/L)": {
        "options": ["4-10", "10.1-20 or 3.1-3.9", "≥ 20.1 or ≤ 3", "N/A"],
        "scores": [1, 2, 4, 8]
    },
    "Urea (mmol/L)": {
        "options": ["≤ 7.5", "7.6-10", "10.1-15", "≥ 15.1"],
        "scores": [1, 2, 4, 8]
    },
    "Sodium (mmol/L)": {
        "options": ["≥ 136", "131-135", "126-130", "≤ 125"],
        "scores": [1, 2, 4, 8]
    },
    "Potassium (mmol/L)": {
        "options": ["3.5-5", "3.2-3.4 or 5.1-5.3", "2.9-3.1 or 5.4-5.9", "≤ 2.8 or ≥ 6"],
        "scores": [1, 2, 4, 8]
    },
    "ECG": {
        "options": [
            "Normal",
            "Atrial fibrillation (rate 60-90)",
            "Other arrhythmia or minor abnormality", 
            "Ventricular arrhythmia or multiple abnormalities"
        ],
        "scores": [1, 2, 4, 8]
    }
}

# Operative variables
operative_variables = {
    "Operative severity": {
        "options": ["Minor", "Intermediate", "Major", "Major+"],
        "scores": [1, 2, 4, 8]
    },
    "Multiple procedures": {
        "options": ["No", "Yes, 2 procedures", "Yes, major procedure", "Yes, >1 major procedure"],
        "scores": [1, 2, 4, 8]
    },
    "Total blood loss (ml)": {
        "options": ["< 100", "100-500", "501-999", "≥ 1000"],
        "scores": [1, 2, 4, 8]
    },
    "Peritoneal soiling": {
        "options": ["None", "Minor (serous fluid)", "Local pus", "Free pus or blood or feces"],
        "scores": [1, 2, 4, 8]
    },
    "Presence of malignancy": {
        "options": ["None", "Primary only", "Nodal mets", "Distant mets"],
        "scores": [1, 2, 4, 8]
    },
    "Timing of surgery": {
        "options": ["Elective", "Emergency (within 24h)", "Emergency (within 6h)", "Emergency (immediate)"],
        "scores": [1, 2, 4, 8]
    }
}

def get_score(variable_name, variable_type):
    """Get the score for a selected option"""
    key_prefix = "physio_" if variable_type == "physiological" else "opera_"
    selected_option = st.session_state.get(f"{key_prefix}{variable_name}", None)
    variable_data = physiological_variables[variable_name] if variable_type == "physiological" else operative_variables[variable_name]
    if selected_option and selected_option in variable_data["options"]:
        option_index = variable_data["options"].index(selected_option)
        return variable_data["scores"][option_index]
    return 0

def main():
    st.title("POSSUM Calculator")
    st.subheader("Physiological and Operative Severity Score for the enUmeration of Mortality and Morbidity")
    
    # Physiological Score Section
    st.header("Physiological Score")
    physiological_score = 0
    
    for i, (var_name, var_data) in enumerate(physiological_variables.items(), 1):
        st.markdown(f"**{i}. {var_name}**")
        selected = st.radio(
            f"Select option for {var_name}:",
            options=var_data["options"],
            key=f'physio_{var_name}',
            format_func=lambda x, scores=var_data["scores"], options=var_data["options"]: 
                f"{x} ({scores[options.index(x)]})" if x in options else x
        )
        if selected:
            physiological_score += get_score(var_name, "physiological")
        st.write("")  # Add spacing
    
    st.write(f"**Total Physiological Score: {physiological_score}**")
    st.write("")
    
    # Operative Score Section
    st.header("Operative Score")
    operative_score = 0
    
    for i, (var_name, var_data) in enumerate(operative_variables.items(), 1):
        st.markdown(f"**{i}. {var_name}**")
        selected = st.radio(
            f"Select option for {var_name}:",
            options=var_data["options"],
            key=f'opera_{var_name}',
            format_func=lambda x, scores=var_data["scores"], options=var_data["options"]: 
                f"{x} ({scores[options.index(x)]})" if x in options else x
        )
        if selected:
            operative_score += get_score(var_name, "operative")
        st.write("")  # Add spacing
    
    st.write(f"**Total Operative Score: {operative_score}**")
    st.write("")
    
    # Calculate Risk
    if st.button("Calculate Risk", type="primary"):
        if physiological_score > 0 and operative_score > 0:
            # POSSUM equations
            # Mortality: ln(R1/(1-R1)) = -9.065 + 0.1692 * physiological + 0.1550 * operative
            # Morbidity: ln(R2/(1-R2)) = -5.91 + 0.16 * physiological + 0.19 * operative
            
            logit_mortality = -9.065 + 0.1692 * physiological_score + 0.1550 * operative_score
            logit_morbidity = -5.91 + 0.16 * physiological_score + 0.19 * operative_score
            
            mortality_risk = 1 / (1 + math.exp(-logit_mortality))
            morbidity_risk = 1 / (1 + math.exp(-logit_morbidity))
            
            st.session_state['possum_results'] = {
                'mortality': mortality_risk,
                'morbidity': morbidity_risk
            }
            
            st.subheader("Predicted Risk")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Mortality Risk", f"{mortality_risk:.2%}")
            with col2:
                st.metric("Morbidity Risk", f"{morbidity_risk:.2%}")
        else:
            st.error("Please complete all physiological and operative assessments before calculating risk.")
    
    # Return to Basic Info
    if st.button("← Return to Basic Info"):
        st.session_state.show_possum = False
        st.rerun()


if __name__ == "__main__":
    main()
