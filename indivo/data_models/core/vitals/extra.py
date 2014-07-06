from lxml import etree
from copy import deepcopy
from django.core import serializers
from django.utils import simplejson

from indivo.data_models.options import DataModelOptions
from indivo.rdf.rdf import PatientGraph
from indivo.serializers import DataModelSerializers
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator
from indivo.serializers.json import IndivoJSONEncoder

LOINC_URI="http://purl.bioontology.org/ontology/LNC/"
SNOMED_URI="http://purl.bioontology.org/ontology/SNOMEDCT/"
BP_METHOD_URI="http://smartplatforms.org/terms/codes/BloodPressureMethod#"
BG_CONTEXT_URI="https://code.cophr.org/blood-glucose-context/"

BP_POSITION_IDS = [
    '40199007', # Supine
    '33586001', # Sitting
    '10904000', # Standing
]

BP_SITE_IDS = [
    '61396006',  # Left thigh
    '11207009',  # Right thigh
    '368208006', # Left arm
    '368209003', # Right arm
]

BP_METHODS = [
    'invasive',
    'palpation',
    'machine',
    'auscultation',
]

BG_CONTEXTS = [
    'AfterBreakfast',
    'AfterDinner',
    'AfterExercise',
    'AfterLunch',
    'AfterMeal',
    'BeforeBedtime',
    'BeforeBreakfast',
    'BeforeDinner',
    'BeforeExercise',
    'BeforeLunch',
    'BeforeMeal',
    'fasting',
    'Ignore',
    'non-fasting',
]

VITAL_SIGN_IDS = {
    'height': ['8306-3',                    # Body height (lying)
               '8302-2'],                   # Body height
    'weight': ['3141-9'],                   # Body weight
    'bmi': ['39156-5'],                     # Body mass index
    'head_circumference': ['8287-5'],       # Head circumference 
    'temperature': ['8310-5'],              # Body temperature
    'oxygen_saturation': ['2710-2'],        # Oxygen saturation
    'blood_pressure_diastolic': ['8462-4'], # Intravascular diastolic
    'blood_pressure_systolic': ['8480-6'],  # Intravascular systolic
    'heart_rate': ['8867-4'],               # Heart rate
    'respiratory_rate': ['9279-1'],         # Respiration rate
    'blood_glucose': ['2339-0',             # Blood glucose (whole blood)
                      '2345-7'],            # Blood glucose (serum or plasma)
    'cholesterol_ldl': ['2089-1'],          # LDL Cholesterol
    'cholesterol_hdl': ['2085-9'],          # LDL Cholesterol
    'cholesterol_triglyceride': ['2571-8'], # Triglyceride
    'cholesterol_total': ['2093-3'],        # Total Cholesterol
    }

UNITS = {
    'height': ['cm', 'm'],
    'weight': ['kg'],
    'bmi': ['kg/m2'],
    'head_circumference': ['cm'],
    'temperature': ['Cel'],
    'oxygen_saturation': ['%{HemoglobinSaturation}'],
    'blood_pressure': ['mm[Hg]'],
    'heart_rate': ['{beats}/min'],
    'respiratory_rate': ['{breaths}/min'],
    'blood_glucose': ['mg/dL'],
    'cholesterol': ['mg/dL'],
}


class VitalsSerializers(DataModelSerializers):
    def to_rdf(query, record=None, carenet=None):
        if not record:
            record = carenet.record

        graph = PatientGraph(record)
        resultOrder = graph.addVitalsList(query.results.iterator(), True if query.limit else False)
        graph.addResponseSummary(query, resultOrder)
        return graph.toRDF()

    def to_xml(queryset, result_count, record=None, carenet=None):
        root = serializers.serialize("indivo_xml", queryset)
        for model_etree in root.findall('Model'):
            model_name = model_etree.get('name')
            if model_name == 'VitalSigns':
                head_circ_fields = []
                bp_fields = []

                for field_etree in model_etree.findall('Field'):
                    field_name = field_etree.get('name')
                    if field_name and field_name.startswith('head_circumference_'):
                        head_circ_fields.append(field_etree)
                    elif field_name and field_name.startswith('blood_pressure_'):
                        bp_fields.append(field_etree)

                for field_etree in head_circ_fields:
                    el = deepcopy(field_etree)
                    el.set('name', el.get('name').replace('head_circumference_', 'head_circ_'))
                    model_etree.append(el)

                for field_etree in bp_fields:
                    el = deepcopy(field_etree)
                    el.set('name', el.get('name').replace('blood_pressure_', 'bp_'))
                    model_etree.append(el)

        return etree.tostring(root)

    def to_json(queryset, result_count, record=None, carenet=None):
        data = serializers.serialize("indivo_python", queryset)
        for obj in data:
            if obj["__modelname__"] == 'VitalSigns':
                head_circ_fields = []
                bp_fields = []

                for field_name, field_value in obj.iteritems():
                    if field_name and field_name.startswith('head_circumference_'):
                        head_circ_fields.append(field_name)
                    elif field_name and field_name.startswith('blood_pressure_'):
                        bp_fields.append(field_name)

                for field_name in head_circ_fields:
                    obj[field_name.replace('head_circumference_', 'head_circ_')] = obj[field_name]

                for field_name in bp_fields:
                    obj[field_name.replace('blood_pressure_', 'bp_')] = obj[field_name]

        return simplejson.dumps(data, cls=IndivoJSONEncoder)

    def to_sdmx(model_etree):
        height_unit = None
        height_value = None

        for field_etree in model_etree.findall('Field'):
            field_name = field_etree.get('name')
            if field_name and field_name.startswith('head_circ_'):
                field_name = field_name.replace('head_circ_', 'head_circumference_', 1)
                field_etree.set('name', field_name)
            elif field_name and field_name.startswith('bp_'):
                field_name = field_name.replace('bp_', 'blood_pressure_', 1)
                field_etree.set('name', field_name)
            elif field_name == 'height_unit':
                height_unit = field_etree
            elif field_name == 'height_value':
                height_value = field_etree

        if height_unit is not None and height_unit.text == 'm':
            height_unit.text = 'cm'
            height_value.text = str(float(height_value.text) * 100)

        return model_etree

class VitalsOptions(DataModelOptions):
    model_class_name = 'VitalSigns'
    serializers = VitalsSerializers
    field_validators = {
        'date': [NonNullValidator()],

        'height_unit': [ValueInSetValidator(UNITS['height'], nullable=True)],
        'height_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'height_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['height'], nullable=True)],

        'weight_unit': [ValueInSetValidator(UNITS['weight'], nullable=True)],
        'weight_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'weight_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['weight'], nullable=True)],

        'bmi_unit': [ValueInSetValidator(UNITS['bmi'], nullable=True)],
        'bmi_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'bmi_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['bmi'], nullable=True)],

        'head_circumference_unit': [ValueInSetValidator(UNITS['head_circumference'], nullable=True)],
        'head_circumference_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'head_circumference_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['head_circumference'], nullable=True)],

        'temperature_unit': [ValueInSetValidator(UNITS['temperature'], nullable=True)],
        'temperature_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'temperature_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['temperature'], nullable=True)],

        'oxygen_saturation_unit': [ValueInSetValidator(UNITS['oxygen_saturation'], nullable=True)],
        'oxygen_saturation_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'oxygen_saturation_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['oxygen_saturation'], nullable=True)],

        'blood_pressure_diastolic_unit': [ValueInSetValidator(UNITS['blood_pressure'], nullable=True)],
        'blood_pressure_diastolic_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'blood_pressure_diastolic_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['blood_pressure_diastolic'], nullable=True)],
        'blood_pressure_systolic_unit': [ValueInSetValidator(UNITS['blood_pressure'], nullable=True)],
        'blood_pressure_systolic_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'blood_pressure_systolic_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['blood_pressure_systolic'], nullable=True)],
        'blood_pressure_position_code_system': [ExactValueValidator(SNOMED_URI, nullable=True)],
        'blood_pressure_position_code_identifier': [ValueInSetValidator(BP_POSITION_IDS, nullable=True)],
        'blood_pressure_site_code_system': [ExactValueValidator(SNOMED_URI, nullable=True)],
        'blood_pressure_site_code_identifier': [ValueInSetValidator(BP_SITE_IDS, nullable=True)],
        'blood_pressure_method_code_system': [ExactValueValidator(BP_METHOD_URI, nullable=True)],
        'blood_pressure_method_code_identifier': [ValueInSetValidator(BP_METHODS, nullable=True)],
       
        'heart_rate_unit': [ValueInSetValidator(UNITS['heart_rate'], nullable=True)],
        'heart_rate_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'heart_rate_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['heart_rate'], nullable=True)],

        'respiratory_rate_unit': [ValueInSetValidator(UNITS['respiratory_rate'], nullable=True)],
        'respiratory_rate_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'respiratory_rate_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['respiratory_rate'], nullable=True)],

        'blood_glucose_level_unit': [ValueInSetValidator(UNITS['blood_glucose'], nullable=True)],
        'blood_glucose_level_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'blood_glucose_level_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['blood_glucose'], nullable=True)],
        'blood_glucose_context_code_system': [ExactValueValidator(BG_CONTEXT_URI, nullable=True)],
        'blood_glucose_context_code_identifier': [ValueInSetValidator(BG_CONTEXTS, nullable=True)],

        'cholesterol_ldl_unit': [ValueInSetValidator(UNITS['cholesterol'], nullable=True)],
        'cholesterol_ldl_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'cholesterol_ldl_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['cholesterol_ldl'], nullable=True)],
        'cholesterol_hdl_unit': [ValueInSetValidator(UNITS['cholesterol'], nullable=True)],
        'cholesterol_hdl_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'cholesterol_hdl_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['cholesterol_hdl'], nullable=True)],
        'cholesterol_triglyceride_unit': [ValueInSetValidator(UNITS['cholesterol'], nullable=True)],
        'cholesterol_triglyceride_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'cholesterol_triglyceride_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['cholesterol_triglyceride'], nullable=True)],
        'cholesterol_total_unit': [ValueInSetValidator(UNITS['cholesterol'], nullable=True)],
        'cholesterol_total_name_code_system': [ExactValueValidator(LOINC_URI, nullable=True)],
        'cholesterol_total_name_code_identifier': [ValueInSetValidator(VITAL_SIGN_IDS['cholesterol_total'], nullable=True)],
    }

