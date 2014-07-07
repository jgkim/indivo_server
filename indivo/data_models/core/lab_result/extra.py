from indivo.serializers import DataModelSerializers
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator
from indivo.data_models.options import DataModelOptions
from indivo.rdf.rdf import PatientGraph

LAB_INTERP_URI="http://smartplatforms.org/terms/codes/LabResultInterpretation#"
LAB_STATUS_URI="http://smartplatforms.org/terms/codes/LabStatus#"
LOINC_URI="http://purl.bioontology.org/ontology/LNC/"

VALID_INTERPS = [
    'normal',
    'critical',
    'abnormal',
]

VALID_STATUSES = [
    'correction',
    'preliminary',
    'final',
]

class LabResultSerializers(DataModelSerializers):
    def to_rdf(query, record=None, carenet=None):
        if not record:
            record = carenet.record
        graph = PatientGraph(record)
        resultOrder = graph.addLabResultList(query.results.iterator(), True if query.limit else False)
        graph.addResponseSummary(query, resultOrder)
        return graph.toRDF()

class LabResultOptions(DataModelOptions):
    model_class_name = 'LabResult'
    serializers = LabResultSerializers
    field_validators = {
        'date': [NonNullValidator()],
        'name_title': [NonNullValidator()],
        'name_code_system': [ExactValueValidator(LOINC_URI)],
        'name_code_identifier': [NonNullValidator()],
        'name_code_title': [NonNullValidator()],
        'status_code_system': [ExactValueValidator(LAB_STATUS_URI, nullable=True)],
        'status_code_identifier': [ValueInSetValidator(VALID_STATUSES, nullable=True)],
        'abnormal_interpretation_code_system': [ExactValueValidator(LAB_INTERP_URI, nullable=True)],
        'abnormal_interpretation_code_identifier': [ValueInSetValidator(VALID_INTERPS, nullable=True)],
        }
