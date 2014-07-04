from lxml import etree
from copy import deepcopy
from django.core import serializers
from django.utils import simplejson

from indivo.data_models.options import DataModelOptions
from indivo.rdf.rdf import PatientGraph
from indivo.serializers import DataModelSerializers
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator
from indivo.serializers.json import IndivoJSONEncoder

SNOMED_URI = 'http://purl.bioontology.org/ontology/SNOMEDCT/'

VALID_STATUS_IDS = [
    '55561003',  # Active
    '73425007',  # Inactive
    '7087005',   # Intermittent
    '413322009', # Resolved
]

class ProblemSerializers(DataModelSerializers):

    def to_rdf(query, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        resultOrder = graph.addProblemList(query.results.iterator(), True if query.limit else False)
        graph.addResponseSummary(query, resultOrder)
        return graph.toRDF()

    def to_xml(queryset, result_count, record=None, carenet=None):
        root = serializers.serialize("indivo_xml", queryset)
        for model_etree in root.findall('Model'):
            model_name = model_etree.get('name')
            field_etrees = []

            if model_name == 'Problem':
                for field_etree in model_etree.findall('Field'):
                    field_name = field_etree.get('name')
                    if field_name == 'start_date':
                        el = deepcopy(field_etree)
                        el.set('name', 'startDate')
                        field_etrees.append(el)
                    elif field_name == 'end_date':
                        el = deepcopy(field_etree)
                        el.set('name', 'endDate')
                        field_etrees.append(el)

                for field_etree in field_etrees:
                    model_etree.append(field_etree)

        return etree.tostring(root)

    def to_json(queryset, result_count, record=None, carenet=None):
        data = serializers.serialize("indivo_python", queryset)
        for obj in data:
            if obj["__modelname__"] == 'Problem':
                field_etrees = {}

                for field_name, field_value in obj.iteritems():
                    if field_name == 'start_date':
                        field_etrees['startDate'] = field_value
                    elif field_name == 'end_date':
                        field_etrees['endDate'] = field_value

                for field_name, field_value in field_etrees.iteritems():
                    obj[field_name] = field_value

        return simplejson.dumps(data, cls=IndivoJSONEncoder)

    def to_sdmx(model_etree):
        for field_etree in model_etree.findall('Field'):
            field_name = field_etree.get('name')
            if field_name == 'startDate':
                field_name = field_name.replace('startDate', 'start_date')
                field_etree.set('name', field_name)
            elif field_name == 'endDate':
                field_name = field_name.replace('endDate', 'end_date')
                field_etree.set('name', field_name)

        return model_etree

class ProblemOptions(DataModelOptions):
    model_class_name = 'Problem'
    serializers = ProblemSerializers
    field_validators = {
        'name_title': [NonNullValidator()],
        'name_code_system': [ExactValueValidator(SNOMED_URI)],
        'name_code_identifier': [NonNullValidator()],
        'name_code_title': [NonNullValidator()],
        'status_code_system': [ExactValueValidator(SNOMED_URI, nullable=True)],
        'status_code_identifier': [ValueInSetValidator(VALID_STATUS_IDS, nullable=True)],
        'start_date': [NonNullValidator()],
        }
