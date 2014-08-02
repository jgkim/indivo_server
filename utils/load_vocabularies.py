"""
Driver for vocabulary loading
"""

from vocabularies.data import language_code, country_code
from vocabularies.data import snomed_ct
from vocabularies.data import allergy_category, allergic_reaction, allergy_severity, allergy_exclusion, drug_allergen, ndf_rt, unii
from vocabularies.data import problem_status
from vocabularies.data import encounter_type, encounter_status, medical_specialty
from vocabularies.data import blood_pressure_body_position, blood_pressure_body_site, blood_pressure_method
from vocabularies.data import loinc, blood_glucose_type, blood_glucose_context
from vocabularies.data import lab_result_status, lab_result_interpretation
from vocabularies.data import procedure_status
from vocabularies.data import drug_name
from vocabularies.data import immunization_product_name, immunization_product_class, immunization_administration_status, immunization_refusal_reason

def load_vocabularies():
    language_code.create_and_load_from('vocabularies/data/complete/ISO-639-1.txt')
    country_code.create_and_load_from('vocabularies/data/complete/ISO-3166-1.txt')
    snomed_ct.create_and_load_from('vocabularies/data/complete/SNOMEDCT_KOSTOM_20140131.txt')
    allergy_category.create_and_load_from('vocabularies/data/complete/Allergy_Category.txt')
    allergic_reaction.create_and_load_from('vocabularies/data/complete/Allergic_Reaction.txt')
    allergy_severity.create_and_load_from('vocabularies/data/complete/Allergy_Severity.txt')
    allergy_exclusion.create_and_load_from('vocabularies/data/complete/Allergy_Exclusion.txt')
    drug_allergen.create_and_load_from('vocabularies/data/complete/Drug_Allergen.txt')
    ndf_rt.create_and_load_from('vocabularies/data/complete/NDF-RT.txt')
    unii.create_and_load_from('vocabularies/data/complete/UNII.txt')
    problem_status.create_and_load_from('vocabularies/data/complete/Problem_Status.txt')
    encounter_type.create_and_load_from('vocabularies/data/complete/Encounter_Type.txt')
    encounter_status.create_and_load_from('vocabularies/data/complete/Encounter_Status.txt')
    medical_specialty.create_and_load_from('vocabularies/data/complete/Medical_Specialty.txt')
    blood_pressure_body_position.create_and_load_from('vocabularies/data/complete/Blood_Pressure_Body_Position.txt')
    blood_pressure_body_site.create_and_load_from('vocabularies/data/complete/Blood_Pressure_Body_Site.txt')
    blood_pressure_method.create_and_load_from('vocabularies/data/complete/Blood_Pressure_Method.txt')
    loinc.create_and_load_from('vocabularies/data/complete/LOINC_KOSTOM_20140627.txt')
    blood_glucose_type.create_and_load_from('vocabularies/data/complete/Blood_Glucose_Type.txt')
    blood_glucose_context.create_and_load_from('vocabularies/data/complete/Blood_Glucose_Context.txt')
    lab_result_status.create_and_load_from('vocabularies/data/complete/Lab_Result_Status.txt')
    lab_result_interpretation.create_and_load_from('vocabularies/data/complete/Lab_Result_Interpretation.txt')
    procedure_status.create_and_load_from('vocabularies/data/complete/Procedure_Status.txt')
    drug_name.create_and_load_from('vocabularies/data/complete/Drug_Name.txt')
    immunization_product_name.create_and_load_from('vocabularies/data/complete/Immunization_Product_Name.txt')
    immunization_product_class.create_and_load_from('vocabularies/data/complete/Immunization_Product_Class.txt')
    immunization_administration_status.create_and_load_from('vocabularies/data/complete/Immunization_Administration_Status.txt')
    immunization_refusal_reason.create_and_load_from('vocabularies/data/complete/Immunization_Refusal_Reason.txt')
    
if __name__ == '__main__':
    load_vocabularies()