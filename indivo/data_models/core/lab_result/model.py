from indivo.models import Fact
from django.db import models
from indivo.fields import CodedValueField, QuantitativeResultField

class LabResult(Fact):
    date = models.DateTimeField(null=True)
    name = CodedValueField()
    status = CodedValueField()
    quantitative_result = QuantitativeResultField()
    narrative_result = models.CharField(max_length=255, null=True)
    abnormal_interpretation = CodedValueField()
    accession_number = models.CharField(max_length=255, null=True)
    notes = models.CharField(max_length=600, null=True)
    lab_panel = models.ForeignKey('LabPanel', null=True, related_name='lab_results')