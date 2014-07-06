from indivo.models import Encounter, VitalSigns
from indivo.lib.iso8601 import parse_iso8601_datetime as date

encounter_fact = Encounter(
    encounter_type_title="Ambulatory encounter",
    encounter_type_code_title="Ambulatory encounter",
    encounter_type_code_system="http://smartplatforms.org/terms/codes/EncounterType#",
    encounter_type_code_identifier="ambulatory",
    start_date=date("2009-05-16T12:00:00Z"),
    end_date=date("2009-05-16T16:00:00Z"),
    facility_name="Wonder Hospital",
    facility_adr_country="Australia",
    facility_adr_city="WonderCity",
    facility_adr_postalcode="5555",
    facility_adr_street="111 Lake Drive", 
    provider_name_given="Josuha",
    provider_name_family="Mandel",
    provider_email="joshua.mandel@fake.emailserver.com",
    provider_tel_1_type="w",
    provider_tel_1_number="1-235-947-3452",
    provider_tel_1_preferred_p=True,
    provider_dea_number="325555555",
    provider_npi_number="5235235",
    )
encounter_fact.save()

# NOTE: all vitals readings are OPTIONAL. You don't need
# to add all fields here to create a VitalSigns object.
vitals_fact = VitalSigns(
    date=date("2009-05-16T12:00:00Z"),
    encounter=encounter_fact,

    # Height
    height_unit="cm",
    height_value=180,
    height_name_title="Body height",
    height_name_code_title="Body height",
    height_name_code_system="http://purl.bioontology.org/ontology/LNC/",
    height_name_code_identifier="8302-2",

    # Weight
    weight_unit="kg",
    weight_value=70.8,
    weight_name_title="Body weight",
    weight_name_code_title="Body weight",
    weight_name_code_system="http://purl.bioontology.org/ontology/LNC/",
    weight_name_code_identifier="3141-9",

    # Body Mass Index
    bmi_unit="kg/m2",
    bmi_value=21.8,
    bmi_name_title="Body mass index",
    bmi_name_code_title="Body mass index",
    bmi_name_code_system="http://purl.bioontology.org/ontology/LNC/",
    bmi_name_code_identifier="39156-5",

    # Head circumference
    head_circumference_unit="cm",
    head_circumference_value=70,
    head_circumference_name_title="Head circumference",
    head_circumference_name_code_title="Head circumference",
    head_circumference_name_code_system="http://purl.bioontology.org/ontology/LNC/",
    head_circumference_name_code_identifier="8287-5",

    # Temperature
    temperature_unit="Cel",
    temperature_value=37,
    temperature_name_title="Body temperature",
    temperature_name_code_title="Body temperature",
    temperature_name_code_system="http://purl.bioontology.org/ontology/LNC/",
    temperature_name_code_identifier="8310-5",

    # Oxygen Saturation
    oxygen_saturation_unit="%{HemoglobinSaturation}",
    oxygen_saturation_value=99,
    oxygen_saturation_name_title="Oxygen saturation",
    oxygen_saturation_name_code_title="Oxygen saturation",
    oxygen_saturation_name_code_system="http://purl.bioontology.org/ontology/LNC/",
    oxygen_saturation_name_code_identifier="2710-2",

    # Blood Pressure
    blood_pressure_diastolic_unit="mm[Hg]",
    blood_pressure_diastolic_value=82,
    blood_pressure_diastolic_name_title="Intravascular diastolic",
    blood_pressure_diastolic_name_code_title="Intravascular diastolic",
    blood_pressure_diastolic_name_code_identifier="8462-4",
    blood_pressure_diastolic_name_code_system="http://purl.bioontology.org/ontology/LNC/",
    blood_pressure_systolic_unit="mm[Hg]",
    blood_pressure_systolic_value=132,
    blood_pressure_systolic_name_title="Intravascular systolic",
    blood_pressure_systolic_name_code_title="Intravascular systolic",
    blood_pressure_systolic_name_code_identifier="8480-6",
    blood_pressure_systolic_name_code_system="http://purl.bioontology.org/ontology/LNC/",
    blood_pressure_position_code_title="Sitting",
    blood_pressure_position_code_title="Sitting",
    blood_pressure_position_code_identifier="33586001",
    blood_pressure_position_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    blood_pressure_site_title="Right arm",
    blood_pressure_site_code_title="Right arm",
    blood_pressure_site_code_identifier="368209003",
    blood_pressure_site_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    blood_pressure_method_title="Auscultation",
    blood_pressure_method_code_title="Auscultation",
    blood_pressure_method_code_identifier="auscultation",
    blood_pressure_method_code_system="http://smartplatforms.org/terms/codes/BloodPressureMethod#",

    # Heart Rate
    heart_rate_unit="{beats}/min",
    heart_rate_value=70,
    heart_rate_name_title="Heart rate",
    heart_rate_name_code_title="Heart rate",
    heart_rate_name_code_system="http://purl.bioontology.org/ontology/LNC/",
    heart_rate_name_code_identifier="8867-4",

    # Respiratory Rate
    respiratory_rate_unit="{breaths}/min",
    respiratory_rate_value=16,
    respiratory_rate_name_title="Respiration rate",
    respiratory_rate_name_code_title="Respiration rate",
    respiratory_rate_name_code_system="http://purl.bioontology.org/ontology/LNC/",
    respiratory_rate_name_code_identifier="9279-1",

    # Blood Glucose
    blood_glucose_level_unit="mg/dL"
    blood_glucose_level_value=124
    blood_glucose_level_name_title="Whole blood"
    blood_glucose_level_name_code_title="Whole blood"
    blood_glucose_level_name_code_system="http://purl.bioontology.org/ontology/LNC/"
    blood_glucose_level_name_code_identifier="2339-0"
    blood_glucose_context_title="After meal"
    blood_glucose_context_code_title="After meal"
    blood_glucose_context_code_system="https://code.cophr.org/blood-glucose-context/"
    blood_glucose_context_code_identifier="AfterMeal"

    # Cholesterol
    cholesterol_ldl_unit="mg/dL"
    cholesterol_ldl_value=112
    cholesterol_ldl_name_title="Cholesterol in LDL"
    cholesterol_ldl_name_code_title="Cholesterol in LDL"
    cholesterol_ldl_name_code_system="http://purl.bioontology.org/ontology/LNC/"
    cholesterol_ldl_name_code_identifier="2089-1"
    cholesterol_hdl_unit="mg/dL"
    cholesterol_hdl_value=58
    cholesterol_hdl_name_title="Cholesterol in HDL"
    cholesterol_hdl_name_code_title="Cholesterol in HDL"
    cholesterol_hdl_name_code_system="http://purl.bioontology.org/ontology/LNC/"
    cholesterol_hdl_name_code_identifier="2085‐9"
    cholesterol_triglyceride_unit="mg/dL"
    cholesterol_triglyceride_value=148
    cholesterol_triglyceride_name_title="Triglyceride"
    cholesterol_triglyceride_name_code_title="Triglyceride"
    cholesterol_triglyceride_name_code_system="http://purl.bioontology.org/ontology/LNC/"
    cholesterol_triglyceride_name_code_identifier="2571‐8"
    cholesterol_total_unit="mg/dL"
    cholesterol_total_value=194
    cholesterol_total_name_title="Cholesterol"
    cholesterol_total_name_code_title="Cholesterol"
    cholesterol_total_name_code_system="http://purl.bioontology.org/ontology/LNC/"
    cholesterol_total_name_code_identifier="2093‐3"
)
