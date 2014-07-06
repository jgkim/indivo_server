from indivo.models import Fact
from indivo.fields import CodedValueField
from django.db import models

class Problem(Fact):
  name = CodedValueField()
  status = CodedValueField()
  start_date = models.DateTimeField(null=True)
  end_date = models.DateTimeField(null=True)
  stop_reason = models.TextField(null=True)
  notes = models.CharField(max_length=600, null=True)
  encounters = models.ManyToManyField('Encounter', null=True)
