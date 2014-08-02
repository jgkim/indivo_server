"""
Blood Glucose Types loading

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
            loinc_id, preferred_label, preferred_label_ko = row
        except ValueError:
            continue

        loinc = models.Vocabulary.objects.get(_id='loinc')
        loinc_term = models.Term.objects.get(vocabulary=loinc, identifier=loinc_id.strip())

        alternate_label = []
        if preferred_label.lower() != loinc_term.preferred_label.lower():
          alternate_label.append(loinc_term.preferred_label)
        alternate_label += loinc_term.alternate_label

        models.Term.objects.create(vocabulary = vocabulary,
                                   identifier = loinc_id.strip(),
                                   system = 'http://purl.bioontology.org/ontology/LNC/',
                                   code = loinc_id.strip(),
                                   preferred_label = preferred_label.strip(),
                                   preferred_label_ko = preferred_label_ko,
                                   alternate_label = alternate_label,
                                   alternate_label_ko = [ loinc_term.preferred_label_ko ])

def create_and_load_from(filepath):
    if not os.path.isfile(filepath):
        print "Can't load the blood glucose types, the file does not exist at %s" % filepath
        return

    vocabulary = create_vocabulary('blood-glucose-type',
      'Blood Glucose Type',
      'Type of the blood glucose measurement, using a LOINC code',
      models.Vocabulary.objects.get(_id='loinc'))
    load(codecs.open(filepath, "r", encoding='utf-8'), vocabulary)