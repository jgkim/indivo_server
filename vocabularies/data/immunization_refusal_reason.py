"""
Immunization Refusal Reasons loading

James G. Boram Kim
2014-08-03
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
                                   system = 'http://smartplatforms.org/terms/codes/ImmunizationRefusalReason#',
                                   code = identifier.strip(),
                                   preferred_label = preferred_label.strip(),
                                   preferred_label_ko = preferred_label_ko.strip())

def create_and_load_from(filepath):
    if not os.path.isfile(filepath):
        print "Can't load the immunization refusal reasons, the file does not exist at %s" % filepath
        return
    
    vocabulary = create_vocabulary('immunization-refusal-reason', 'Immunization Refusal Reason', "Controlled vocabulary of immunization refusal reasons, using a SMART Platforms' sp:ImmunizationRefusal-Reason code")
    load(codecs.open(filepath, "r", encoding='utf-8'), vocabulary)