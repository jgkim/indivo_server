"""
Allergy Exclusion Codes loading

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
            snomed_cid, preferred_label, alternate_label, preferred_label_ko = row
        except ValueError:
            continue

        models.Term.objects.create(vocabulary = vocabulary,
                                   identifier = snomed_cid.strip(),
                                   system = 'http://purl.bioontology.org/ontology/SNOMEDCT/',
                                   code = snomed_cid.strip(),
                                   preferred_label = preferred_label.strip(),
                                   preferred_label_ko = preferred_label_ko.strip(),
                                   alternate_label = [label.strip() for label in alternate_label.split('|')])

def create_and_load_from(filepath):
    if not os.path.isfile(filepath):
        print "Can't load the allergy severity codes, the file does not exist at %s" % filepath
        return

    vocabulary = create_vocabulary('allergy-exclusion',
      'Allergy Exclusion',
      "Nature of the allergy exclusion, using a SMART Platforms' sp: AllergyExclusion code",
      models.Vocabulary.objects.get(_id='snomed-ct'))
    load(codecs.open(filepath, "r", encoding='utf-8'), vocabulary)