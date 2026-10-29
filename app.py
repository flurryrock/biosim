import streamlit as st
import pandas as pd
import time
from core import DrugSimulationEngine

# Page Config for Mobile
st.set_page_config(page_title="BioSim Lab", page_icon="🧬", layout="centered")

st.title("🧬 AI Drug Simulation & Clinical Trials")
st.markdown("*In Silico* platform for evaluating targeted compounds and digital twin cohorts.")

# Sidebar Configuration
st.sidebar.header("🧪 Compound Parameters")
compound_name = st.sidebar.text_input("Compound Name", "HPO-3-PEG Conjugate")
smiles_input = st.sidebar.text_input("SMILES String", "CCOCCOCCN1CC1")

cohort_size = st.sidebar.slider("Virtual Cohort Size (Digital Twins)", 10, 500, 100, step=10)

# Initialize Engine
engine = DrugSimulationEngine(compound_name, smiles_input)

# Main Tab Layout
tab1, tab2 = st.tabs(["🔬 Molecule Validator", "📊 Virtual Clinical Trial"])

with tab1:
    st.subheader("Chemical Structure & Druglikeness")
    if st.button("Validate Compound"):
        validation_results = engine.validate_molecule()
        if validation_results["valid"]:
            st.success("Compound structure validated successfully!")
            st.json(validation_results)
        else:
            st.error(validation_results["error"])

with tab2:
    st.subheader("4-Week Digital Twin Cohort Simulation")
    st.markdown(f"Simulating treatment efficacy and adverse events across **{cohort_size} virtual patient clones**.")
    
    if st.button("Run 4-Week Trial Simulation"):
        # Visual Simulation Progress Bar for Mobile
        progress_text = st.empty()
        my_bar = st.progress(0)
        
        stages = [
            ("Day 1: Initial Dosing & Acute Toxicity Screening...", 20),
            ("Week 1: Pharmacokinetic Distribution & Clearance...", 50),
            ("Week 2-3: Target Binding & Efficacy Tracking...", 80),
            ("Week 4: Final Cohort Evaluation & Synthesis...", 100)
        ]
        
        for text, percent in stages:
            progress_text.text(text)
            my_bar.progress(percent)
            time.sleep(0.8)
            
        progress_text.text("Trial Simulation Complete!")
        
        # Run actual trial data generation
        df_results = engine.simulate_virtual_cohort(cohort_size)
        
        # Display Metrics Summary
        success_count = len(df_results[df_results["Outcome"].str.contains("Success")])
        success_rate = round((success_count / cohort_size) * 100, 1)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Cohort Size", cohort_size)
        col2.metric("Efficacy Rate", f"{success_rate}%")
        col3.metric("Adverse Events", f"{len(df_results[df_results['Adverse_Event'] != 'None']) } patients")
        
        # Show Dataframe Table
        st.markdown("### 📋 Patient Cohort Breakdown")
        st.dataframe(df_results, use_container_width=True)
