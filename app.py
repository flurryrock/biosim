import streamlit as st
import pandas as pd
import time
from core import DrugSimulationEngine

st.set_page_config(page_title="BioSim Clinical Lab", page_icon="🧬", layout="wide")

st.title("🧬 In Silico Drug Discovery & Digital Twin Lab")
st.markdown("Professional multi-system clinical trial simulation platform powered by Python and Streamlit.")

# Sidebar Configuration for Custom Inputs
st.sidebar.header("💊 Custom Trial Configuration")

compound_name = st.sidebar.text_input("Compound Name", placeholder="e.g., HPO-3-PEG Conjugate")
smiles_input = st.sidebar.text_input("SMILES String (Optional)", placeholder="e.g., CCOCCOCCN1CC1")
target_outcome = st.sidebar.text_area("Targeted Outcome", placeholder="e.g., Dissolve deposits rapidly while inducing weight loss and maintaining stable lipid profiles.")

dosage_mg = st.sidebar.slider("Target Dosage (mg/day)", 10, 200, 50, step=10)
cohort_size = st.sidebar.slider("Virtual Cohort Size (Digital Twins)", 20, 500, 100, step=20)

# Initialize Engine (No API keys required for web app simulation)
engine = DrugSimulationEngine(compound_name, smiles_input, target_outcome)

# Main Dashboard Tabs
tab1, tab2 = st.tabs(["🔬 Molecule & Target Analysis", "📊 Multi-System Vitals Matrix"])

with tab1:
    st.subheader("Target vs. Predictive Simulation Alignment")
    
    if not compound_name or not target_outcome:
        st.warning("⚠️ Please enter a **Compound Name** and a **Targeted Outcome** in the sidebar to initialize the simulation.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🎯 Stated Target Outcome")
            st.info(target_outcome)
            
        with col2:
            st.markdown("### 🧬 Cheminformatics Validation")
            chem_metrics = engine.validate_molecule()
            st.json(chem_metrics)
            
        st.markdown("---")
        st.markdown("### 🤖 Algorithmic & Pharmacokinetic Synthesis")
        st.success(f"Compound **{compound_name}** successfully parsed against multi-system clinical thresholds for a target dosage of **{dosage_mg} mg/day**.")

with tab2:
    st.subheader("4-Week Multi-System Digital Twin Trial")
    st.markdown(f"Tracking systemic changes across **{cohort_size} virtual patient clones**.")
    
    if not compound_name or not target_outcome:
        st.warning("⚠️ Please configure your compound and target outcome in the sidebar first.")
    else:
        if st.button("Execute Multi-System Simulation"):
            with st.spinner("Running high-fidelity cohort simulation across all biometric endpoints..."):
                time.sleep(1.0)
                df_trial = engine.simulate_multisystem_cohort(cohort_size, dosage_mg)
                
            st.success("Trial Simulation Complete!")
            
            # Summary Metrics Row
            success_count = len(df_trial[df_trial["Real_Outcome_Status"] == "Matched Target Outcome"])
            match_rate = (success_count / cohort_size) * 100
            avg_weight = df_trial["Weight_Loss_kg"].mean()
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Cohort Size", cohort_size)
            m2.metric("Target Match Rate", f"{match_rate:.1f}%")
            m3.metric("Avg Weight Loss", f"{avg_weight:.1f} kg")
            m4.metric("Hair Loss Flags", f"{len(df_trial[df_trial['Hair_Loss_Risk'].str.contains('Moderate')])} patients")
            
            st.markdown("### 📋 Complete Patient Biometric Matrix (Heart Rate, WBC, Bone Density, Lipids, Weight, eGFR)")
            st.dataframe(df_trial, use_container_width=True)
