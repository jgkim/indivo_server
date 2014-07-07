from indivo.data_models.options import DataModelOptions
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator

SPECIALTY_URI="http://code.cophr.org/medical-specialty/"
ENC_TYPE_URI="http://smartplatforms.org/terms/codes/EncounterType#"
APNTMT_STATUS_URI="http://code.cophr.org/appointment-status/"

ENC_TYPES = [
    'home',
    'emergency',
    'ambulatory',
    'inpatient',
    'field',
    'virtual',
]

APNTMT_STATUSES = [
    'Abs', # Missed
    'Can', # Cancelled
    'Cmp', # Completed
    'Sch', # Scheduled
    'Tbs', # To be scheduled
]

class AppointmentOptions(DataModelOptions):
    model_class_name = 'Appointment'
    field_validators = {
        'start_date': [NonNullValidator()],
        'specialty_code_system': [ExactValueValidator(SPECIALTY_URI, nullable=True)],
        'appointment_type_code_identifier': [ValueInSetValidator(ENC_TYPES, nullable=True)],
        'status_code_system': [ExactValueValidator(APNTMT_STATUS_URI, nullable=True)],
        'status_code_identifier': [ValueInSetValidator(APNTMT_STATUSES, nullable=True)],
    }