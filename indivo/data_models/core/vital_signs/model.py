from indivo.models import Fact
from django.db import models
from indivo.fields import VitalSignField, BloodPressureField, BloodGlucoseField, CholesterolField

class VitalSigns(Fact):
    date = models.DateTimeField(null=True)
    encounter = models.ForeignKey('Encounter', null=True)
    height = VitalSignField()
    weight = VitalSignField()
    bmi = VitalSignField()
    head_circumference = VitalSignField(db_column='head_circ')
    temperature = VitalSignField()
    oxygen_saturation = VitalSignField()
    blood_pressure = BloodPressureField(db_column='bp')
    heart_rate = VitalSignField()
    respiratory_rate = VitalSignField()
    blood_glucose = BloodGlucoseField()
    cholesterol = CholesterolField()
    notes = models.CharField(max_length=600, null=True)