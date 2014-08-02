"""
LOINC loading

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
            loinc_id, alternate_label, preferred_label, preferred_label_ko, umls_cui = row
        except ValueError:
            continue

        alternate_label = alternate_label.strip()
        if alternate_label == 'N/A':
            alternate_label = ''

        preferred_label_ko = preferred_label_ko.strip()
        if preferred_label_ko == 'N/A':
            preferred_label_ko = ''

        umls_cui = umls_cui.strip()
        if umls_cui == 'N/A':
            umls_cui = ''

        models.Term.objects.create(vocabulary = vocabulary,
                                   identifier = loinc_id.strip(),
                                   system = 'http://purl.bioontology.org/ontology/LNC/',
                                   code = loinc_id.strip(),
                                   preferred_label = preferred_label.strip(),
                                   preferred_label_ko = preferred_label_ko,
                                   alternate_label = [label.strip() for label in alternate_label.split('|')],
                                   umls_cui = umls_cui)

def create_and_load_from(filepath):
    if not os.path.isfile(filepath):
        print "Can't load LOINC, the file does not exist at %s" % filepath
        return
    
    vocabulary = create_vocabulary('loinc', 'LOINC', 'Logical Observation Identifiers Names and Codes')
    load(codecs.open(filepath, "r", encoding='utf-8'), vocabulary)