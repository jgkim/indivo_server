from lxml import etree
from copy import deepcopy
from django.core import serializers
from django.utils import simplejson

from indivo.data_models.options import DataModelOptions
from indivo.rdf.rdf import PatientGraph
from indivo.serializers import DataModelSerializers
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator
from indivo.serializers.json import IndivoJSONEncoder

SNOMED = 'http://purl.bioontology.org/ontology/SNOMEDCT/'
RXNORM = 'http://purl.bioontology.org/ontology/RXNORM/'
NUI = 'http://purl.bioontology.org/ontology/NDFRT/'
UNII = 'http://fda.gov/UNII/'

VALID_ALLERGEN_SYSTEMS = [
    RXNORM, # Drug allergy or intolerance
    NUI,    # Drug class allergy or intolerance
    UNII,   # Food or environmental allergy or intolerance
]

VALID_CATEGORY_IDS = [
    '414285001', # Food allergy
    '426232007', # Environmental allergy
    '416098002', # Drug allergy
    '59037007',  # Drug intolerance
    '235719002', # Food intolerance
    ]

VALID_SEVERITY_IDS = [
    '255604002', # Mild
    '442452003', # Life Threatening
    '6736007',   # Moderate
    '399166001', # Fatal
    '24484000',  # Severe
]

VALID_EXCLUSION_IDS = [
    '160244002', # No known allergies
    '428607008', # No known environmental allergy
    '429625007', # No known food allergy
    '409137002', # No known history of drug allergy
]

OLD_ALLERGEN_FIELD_PREFIXES = (
    'drug_allergen_',
    'drug_class_allergen_',
    'other_allergen_',
)

class AllergySerializers(DataModelSerializers):
    def to_rdf(query, record=None, carenet=None):
        if not record:
            record = carenet.record
        graph = PatientGraph(record)
        
        graph.addAllergyList(query.results.iterator())
        graph.addResponseSummary(query)
        return graph.toRDF()

    def to_xml(queryset, result_count, record=None, carenet=None):
        root = serializers.serialize("indivo_xml", queryset)
        for model_etree in root.findall('Model'):
            model_name = model_etree.get('name')
            if model_name == 'Allergy':
                system = None
                allergen_fields = []

                for field_etree in model_etree.findall('Field'):
                    field_name = field_etree.get('name')
                    if field_name and field_name.startswith('allergen_'):
                        allergen_fields.append(field_etree)
                        if field_name == 'allergen_code_system':
                            system = field_etree.text

                for field_etree in allergen_fields:
                    el = deepcopy(field_etree)
                    if system == RXNORM:
                        el.set('name', el.get('name').replace('allergen_', OLD_ALLERGEN_FIELD_PREFIXES[0]))
                    elif system == NUI:
                        el.set('name', el.get('name').replace('allergen_', OLD_ALLERGEN_FIELD_PREFIXES[1]))
                    elif system == UNII:
                        el.set('name', el.get('name').replace('allergen_', OLD_ALLERGEN_FIELD_PREFIXES[2]))
                    model_etree.append(el)

        return etree.tostring(root)

    def to_json(queryset, result_count, record=None, carenet=None):
        data = serializers.serialize("indivo_python", queryset)
        for obj in data:
            if obj["__modelname__"] == 'Allergy':
                system = None
                allergen_fields = []

                for field_name, field_value in obj.iteritems():
                    if field_name.startswith('allergen_'):
                        allergen_fields.append(field_name)
                        if field_name == 'allergen_code_system':
                            system = field_value

                for field_name in allergen_fields:
                    if system == RXNORM:
                        obj[field_name.replace('allergen_', OLD_ALLERGEN_FIELD_PREFIXES[0])] = obj[field_name]
                    elif system == NUI:
                        obj[field_name.replace('allergen_', OLD_ALLERGEN_FIELD_PREFIXES[1])] = obj[field_name]
                    elif system == UNII:
                        obj[field_name.replace('allergen_', OLD_ALLERGEN_FIELD_PREFIXES[2])] = obj[field_name]

        return simplejson.dumps(data, cls=IndivoJSONEncoder)

    def to_sdmx(model_etree):
        for field_etree in model_etree.findall('Field'):
            field_name = field_etree.get('name')
            if field_name and field_name.startswith(OLD_ALLERGEN_FIELD_PREFIXES):
                for old in OLD_ALLERGEN_FIELD_PREFIXES:
                    field_name = field_name.replace(old, 'allergen_', 1)
                    field_etree.set('name', field_name)

        return model_etree

class AllergyOptions(DataModelOptions):
    model_class_name = 'Allergy'
    serializers = AllergySerializers
    field_validators = {
        'allergic_reaction_title': [NonNullValidator()],
        'allergic_reaction_code_system': [ExactValueValidator(SNOMED)],
        'allergic_reaction_code_identifier': [NonNullValidator()],
        'allergic_reaction_code_title': [NonNullValidator()],
        'category_title': [NonNullValidator()],
        'category_code_system': [ExactValueValidator(SNOMED)],
        'category_code_identifier': [ValueInSetValidator(VALID_CATEGORY_IDS)],
        'category_code_title': [NonNullValidator()],
        'allergen_title': [NonNullValidator()],
        'allergen_code_system': [ValueInSetValidator(VALID_ALLERGEN_SYSTEMS)],
        'allergen_code_identifier': [NonNullValidator()],
        'allergen_code_title': [NonNullValidator()],
        'severity_title': [NonNullValidator()],
        'severity_code_system': [ExactValueValidator(SNOMED)],
        'severity_code_identifier': [ValueInSetValidator(VALID_SEVERITY_IDS)],
        'severity_code_title': [NonNullValidator()],
        }

class AllergyExclusionSerializers(DataModelSerializers):
    def to_rdf(query, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addAllergyExclusions(query.results.iterator())
        graph.addResponseSummary(query)
        return graph.toRDF()

class AllergyExclusionOptions(DataModelOptions):
    model_class_name = 'AllergyExclusion'
    serializers = AllergyExclusionSerializers
    field_validators = {
        'name_code_system': [ExactValueValidator(SNOMED)],
        'name_code_identifier': [ValueInSetValidator(VALID_EXCLUSION_IDS)],
        'name_code_title': [NonNullValidator()],
        'name_title': [NonNullValidator()],
        }
