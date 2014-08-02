"""
Utilities for creating vocabularies

"""

import csv
from vocabularies import models

def create_vocabulary(vocabulary_id, title, description=None, dependence=None):
    defaults = {'title' : title, 'description': description, 'dependence': dependence}

    vocabulary, created = models.Vocabulary.objects.get_or_create(_id = vocabulary_id, defaults = defaults)

    return vocabulary

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(data):
    for line in data:
        yield line.encode('utf-8')