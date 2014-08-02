"""
SNOMED CT loading

James G. Boram Kim
2014-07-22
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
            snomed_cid, alternate_label, preferred_label, preferred_label_ko = row
        except ValueError:
            continue

        alternate_label = alternate_label.strip()
        if alternate_label == 'N/A':
            alternate_label = ''

        preferred_label_ko = preferred_label_ko.strip()
        if preferred_label_ko == 'N/A':
            preferred_label_ko = ''

        models.Term.objects.create(vocabulary = vocabulary,
                                   identifier = snomed_cid.strip(),
                                   system = 'http://purl.bioontology.org/ontology/SNOMEDCT/',
                                   code = snomed_cid.strip(),
                                   preferred_label = preferred_label.strip(),
                                   preferred_label_ko = preferred_label_ko,
                                   alternate_label = [label.strip() for label in alternate_label.split('|')])

def create_and_load_from(filepath):
    if not os.path.isfile(filepath):
        print "Can't load SNOMED CT, the file does not exist at %s" % filepath
        return
    
    vocabulary = create_vocabulary('snomed-ct', 'SNOMED CT', 'SNOMED Clinical Terms')
    load(codecs.open(filepath, "r", encoding='utf-8'), vocabulary)