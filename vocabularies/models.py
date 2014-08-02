from django.db import models
from djangotoolbox.fields import ListField, DictField
from django_mongodb_engine.fields import ObjectId

class Vocabulary(models.Model):
    """ A set of terms """
    _id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    dependence = models.ForeignKey('self', null=True)

class Term(models.Model):
    """ A term in a vocabulary """
    vocabulary = models.ForeignKey(Vocabulary)
    identifier = models.CharField(max_length=255)
    system = models.URLField(null=True)
    code = models.CharField(max_length=255, null=True)
    umls_cui = models.CharField(max_length=31, null=True)
    preferred_label = models.CharField(max_length=255)
    preferred_label_ko = models.CharField(max_length=255, null=True)
    alternate_label = ListField(null=True)
    alternate_label_ko = ListField(null=True)
    meta = DictField(null=True)

    class Meta:
        unique_together = (('vocabulary', 'identifier'), ('vocabulary', 'system', 'code'))