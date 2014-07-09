from indivo.models import Fact
from django.db import models
from indivo.fields import CodedValueField, OrganizationField, ProviderField

class Encounter(Fact):
    encounter_type = CodedValueField()
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    facility = OrganizationField()
    provider = ProviderField()
    specialty = CodedValueField()
    status = CodedValueField()
    notes = models.CharField(max_length=600, null=True)