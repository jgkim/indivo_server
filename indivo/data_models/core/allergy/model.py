from indivo.models import Fact
from django.db import models
from indivo.fields import CodedValueField

class Allergy(Fact):
    allergic_reaction = CodedValueField()
    category = CodedValueField()
    allergen = CodedValueField()
    severity = CodedValueField()
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    notes = models.CharField(max_length=600, null=True)

class AllergyExclusion(Fact):
    name = CodedValueField()
    date = models.DateTimeField(null=True)
