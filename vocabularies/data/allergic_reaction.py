"""
Allergic Reactions loading

James G. Boram Kim
2014-07-24
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
            snomed_cid, preferred_label = row
        except ValueError:
            continue

        snomed_ct = models.Vocabulary.objects.get(_id='snomed-ct')
        snomed_ct_term = models.Term.objects.get(vocabulary=snomed_ct, identifier=snomed_cid.strip())

        alternate_label = []
        if preferred_label.lower() != snomed_ct_term.preferred_label.lower():
          alternate_label.append(snomed_ct_term.preferred_label)
        alternate_label += snomed_ct_term.alternate_label

        models.Term.objects.create(vocabulary = vocabulary,
                                   identifier = snomed_cid.strip(),
                                   system = 'http://purl.bioontology.org/ontology/SNOMEDCT/',
                                   code = snomed_cid.strip(),
                                   preferred_label = preferred_label.strip(),
                                   preferred_label_ko = snomed_ct_term.preferred_label_ko,
                                   alternate_label = alternate_label)

def create_and_load_from(filepath):
    if not os.path.isfile(filepath):
        print "Can't load the allergic reactions, the file does not exist at %s" % filepath
        return

    vocabulary = create_vocabulary('allergic-reaction',
      'Allergic Reaction',
      "Reaction associated with an allergy, using a code drawn from SNOMED CT",
      models.Vocabulary.objects.get(_id='snomed-ct'))
    load(codecs.open(filepath, "r", encoding='utf-8'), vocabulary)