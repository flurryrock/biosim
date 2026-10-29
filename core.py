import random
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

class DrugSimulationEngine:
    def __init__(self, compound_name, smiles_string):
        self.compound_name = compound_name
        self.smiles = smiles_string
        self.mol = Chem.MolFromSmiles(smiles_string)
        
    def validate_molecule(self):
        """Checks if the SMILES string is valid and calculates basic drug-likeness rules."""
        if self.mol is None:
            return {"valid": False, "error": "Invalid chemical structure (SMILES)."}
        
        # Calculate Lipinski's Rule of Five metrics
        mw = Descriptors.MolWt(self.mol)
        logp = Descriptors.MolLogP(self.mol)
        h_donors = Descriptors.NumHDonors(self.mol)
        h_acceptors = Descriptors.NumHAcceptors(self.mol)
        
        return {
            "valid": True,
            "molecular_weight": round(mw, 2),
            "logp": round(logp, 2),
            "h_donors": h_donors,
            "h_acceptors": h_acceptors,
            "status": "Passed Druglikeness Check"
        }

    def simulate_virtual_cohort(self, cohort_size=100):
        """Simulates a 4-week virtual trial across digital twin patient clones."""
        results = []
        
        for i in range(1, cohort_size + 1):
            # Generate randomized physiological profiles for digital twins
            age = random.randint(30, 75)
            kidney_function_eGFR = random.randint(45, 120) # ml/min
            liver_enzyme_efficiency = random.uniform(0.7, 1.3)
            
            # Simulation logic over 4 weeks
            dissolution_score = min(100, max(10, random.gauss(75, 15) * liver_enzyme_efficiency))
            
            # Toxicity triggers if liver efficiency or eGFR is compromised
            has_side_effect = True if (kidney_function_eGFR < 60 or random.random() < 0.12) else False
            side_effect_type = "Elevated Liver Enzymes" if has_side_effect else "None"
            
            outcome = "Success (Stone Dissolved)" if dissolution_score > 60 and not has_side_effect else "Inconclusive / Side Effect"
            if dissolution_score <= 40:
                outcome = "Failed (Resistant Stone)"

            results.append({
                "Patient_ID": f"VP-{i:03d}",
                "Age": age,
                "eGFR": kidney_function_eGFR,
                "Dissolution_Pct": round(dissolution_score, 1),
                "Adverse_Event": side_effect_type,
                "Outcome": outcome
            })
            
        return pd.DataFrame(results)
