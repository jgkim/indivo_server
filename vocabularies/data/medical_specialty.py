"""
Medical Specialties loading

James G. Boram Kim
2014-08-02
"""

import codecs
import os.path

from vocabularies import models
from utils import *

def load(stream, vocabulary, delimiter='\t'):
    """
    load data from a file input stream.
    """

    csv_reader = unicode_csv_reader(stream, delimiter = delimiter)

    for row in csv_reader:
        try:
            identifier, preferred_label, preferred_label_ko = row
        except ValueError:
            continue

        models.Term.objects.create(vocabulary = vocabulary,
                                   identifier = identifier.strip(),
                                   system = 'http://vocab.cophr.org/medical-specialty/',
                                   code = identifier.strip(),
                                   preferred_label = preferred_label.strip(),
                                   preferred_label_ko = preferred_label_ko.strip())

def create_and_load_from(filepath):
    if not os.path.isfile(filepath):
        print "Can't load the medical specialties, the file does not exist at %s" % filepath
        return
    
    vocabulary = create_vocabulary('medical-specialty', 'Medical Specialty', "Specialty for the medical encounter, using a Microsoft HealthVault's wc:medical-specialties code")
    load(codecs.open(filepath, "r", encoding='utf-8'), vocabulary)