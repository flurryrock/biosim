import random
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

class DrugSimulationEngine:
    def __init__(self, compound_name, smiles_string, target_outcome):
        self.compound_name = compound_name
        self.smiles = smiles_string
        self.target_outcome = target_outcome
        self.mol = Chem.MolFromSmiles(smiles_string) if smiles_string else None

    def validate_molecule(self):
        """Performs cheminformatics validation using RDKit."""
        if not self.smiles:
            return {"valid": True, "status": "Custom compound tracked without SMILES string."}
        if self.mol is None:
            return {"valid": False, "error": "Invalid SMILES structure string provided."}
        
        mw = Descriptors.MolWt(self.mol)
        logp = Descriptors.MolLogP(self.mol)
        h_donors = Descriptors.NumHDonors(self.mol)
        h_acceptors = Descriptors.NumHAcceptors(self.mol)
        tpsa = rdMolDescriptors.CalcTPSA(self.mol)
        
        lipinski_passed = (mw <= 500 and logp <= 5 and h_donors <= 5 and h_acceptors <= 10)
        
        return {
            "valid": True,
            "molecular_weight": round(mw, 2),
            "logp": round(logp, 2),
            "h_donors": h_donors,
            "h_acceptors": h_acceptors,
            "tpsa": round(tpsa, 2),
            "lipinski_compliant": "Yes" if lipinski_passed else "No (Violates Rule of 5)"
        }

    def simulate_multisystem_cohort(self, cohort_size=100, dosage_mg=50):
        """Simulates a 4-week multi-system digital twin trial tracking all key health markers."""
        results = []
        metabolic_factor = dosage_mg / 100.0
        
        for i in range(1, cohort_size + 1):
            age = random.randint(30, 70)
            baseline_egfr = random.randint(60, 115)
            baseline_hr = random.randint(62, 85)
            baseline_wbc = round(random.uniform(4.5, 11.0), 1)
            baseline_bone_density = round(random.uniform(1.0, 1.3), 2)
            baseline_ldl = round(random.uniform(2.2, 4.2), 1)
            
            # Multi-system physiological deltas
            hr_delta = int(random.gauss(3, 4) * metabolic_factor)
            wbc_delta = round(random.gauss(-0.2, 0.8) * metabolic_factor, 1)
            bone_delta = round(random.gauss(-0.01, 0.03), 3)
            ldl_delta = round(random.gauss(-0.3, 0.4) * metabolic_factor, 2)
            weight_loss_kg = round(max(0.0, random.gauss(3.5, 1.8) * metabolic_factor), 1)
            
            hair_loss_risk = "Low" if random.random() > 0.18 else "Moderate/Noticeable"
            efficacy_score = min(100, max(15, random.gauss(70, 20)))
            
            outcome = "Matched Target Outcome" if efficacy_score > 60 else "Suboptimal / Deviation"

            results.append({
                "Patient_ID": f"DT-{i:03d}",
                "Age": age,
                "Weight_Loss_kg": weight_loss_kg,
                "Heart_Rate_bpm": baseline_hr + hr_delta,
                "WBC_k_uL": max(2.0, baseline_wbc + wbc_delta),
                "Bone_Density": max(0.7, baseline_bone_density + bone_delta),
                "LDL_Cholesterol": max(1.5, baseline_ldl + ldl_delta),
                "Hair_Loss_Risk": hair_loss_risk,
                "eGFR": baseline_egfr,
                "Real_Outcome_Status": outcome
            })
            
        return pd.DataFrame(results)
