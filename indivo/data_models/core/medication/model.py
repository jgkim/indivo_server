from indivo.models import Fact
from django.db import models
from indivo.fields import CodedValueField, CodeField, ValueAndUnitField, PharmacyField, ProviderField

class Medication(Fact):
    name = CodedValueField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    frequency = ValueAndUnitField()
    quantity = ValueAndUnitField()
    instructions = models.CharField(max_length=255, null=True)
    notes = models.CharField(max_length=600, null=True)
    provenance = CodeField()

class Fill(Fact):
    date = models.DateTimeField(null=True)
    dispenseDaysSupply = models.FloatField(null=True)
    pbm = models.CharField(max_length=255, null=True)
    pharmacy = PharmacyField()
    provider = ProviderField()
    quantityDispensed = ValueAndUnitField()
    medication = models.ForeignKey(Medication, null=True, related_name='fulfillments')
  
