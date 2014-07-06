from lxml import etree
from copy import deepcopy
from django.core import serializers
from django.utils import simplejson

from indivo.data_models.options import DataModelOptions
from indivo.rdf.rdf import PatientGraph
from indivo.serializers import DataModelSerializers
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator
from indivo.serializers.json import IndivoJSONEncoder

ENC_TYPE_URI="http://smartplatforms.org/terms/codes/EncounterType#"
ENC_TYPES = [
    'home',
    'emergency',
    'ambulatory',
    'inpatient',
    'field',
    'virtual',
]

class EncounterSerializers(DataModelSerializers):
    def to_rdf(query, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        resultOrder = graph.addEncounterList(query.results.iterator(), True if query.limit else False)
        graph.addResponseSummary(query, resultOrder)
        return graph.toRDF()

    def to_xml(queryset, result_count, record=None, carenet=None):
        root = serializers.serialize("indivo_xml", queryset)
        for model_etree in root.findall('Model'):
            model_name = model_etree.get('name')
            if model_name == 'Encounter':
                field_etrees = []
                type_fields = []

                for field_etree in model_etree.findall('Field'):
                    field_name = field_etree.get('name')
                    if field_name and field_name.startswith('encounter_type_'):
                        type_fields.append(field_etree)
                    elif field_name == 'start_date':
                        el = deepcopy(field_etree)
                        el.set('name', 'startDate')
                        field_etrees.append(el)
                    elif field_name == 'end_date':
                        el = deepcopy(field_etree)
                        el.set('name', 'endDate')
                        field_etrees.append(el)

                for field_etree in field_etrees:
                    model_etree.append(field_etree)

                for field_etree in type_fields:
                    el = deepcopy(field_etree)
                    el.set('name', el.get('name').replace('encounter_type_', 'type_'))
                    model_etree.append(el)

        return etree.tostring(root)

    def to_json(queryset, result_count, record=None, carenet=None):
        data = serializers.serialize("indivo_python", queryset)
        for obj in data:
            if obj["__modelname__"] == 'Encounter':
                field_etrees = {}
                type_fields = []

                for field_name, field_value in obj.iteritems():
                    if field_name.startswith('encounter_type_'):
                        type_fields.append(field_name)
                    elif field_name == 'start_date':
                        field_etrees['startDate'] = field_value
                    elif field_name == 'end_date':
                        field_etrees['endDate'] = field_value

                for field_name, field_value in field_etrees.iteritems():
                    obj[field_name] = field_value

                for field_name in type_fields:
                    obj[field_name.replace('encounter_type_', 'type_')] = obj[field_name]

        return simplejson.dumps(data, cls=IndivoJSONEncoder)

    def to_sdmx(model_etree):
        for field_etree in model_etree.findall('Field'):
            field_name = field_etree.get('name')
            if field_name and field_name.startswith('type_'):
                field_name = field_name.replace('type_', 'encounter_type_', 1)
                field_etree.set('name', field_name)
            elif field_name == 'startDate':
                field_etree.set('name', 'start_date')
            elif field_name == 'endDate':
                field_etree.set('name', 'end_date')

        return model_etree

class EncounterOptions(DataModelOptions):
    model_class_name = 'Encounter'
    serializers = EncounterSerializers
    field_validators = {
        'encounter_type_title': [NonNullValidator()],
        'encounter_type_code_system': [ExactValueValidator(ENC_TYPE_URI)],
        'encounter_type_code_identifier': [ValueInSetValidator(ENC_TYPES)],
        'encounter_type_code_title': [NonNullValidator()],
        'start_date': [NonNullValidator()],
        }

