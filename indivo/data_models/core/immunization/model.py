from indivo.models import Fact
from django.db import models
from indivo.fields import CodedValueField

class Immunization(Fact):
    date = models.DateTimeField(null=True)
    product_name = CodedValueField()
    product_class = CodedValueField()
    product_class_2 = CodedValueField()
    administration_status = CodedValueField()
    refusal_reason = CodedValueField()
    notes = models.CharField(max_length=600, null=True)