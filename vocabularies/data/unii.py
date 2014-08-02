"""
UNII loading

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
            unii_id, preferred_label = row
        except ValueError:
            continue

        models.Term.objects.create(vocabulary = vocabulary,
                                   identifier = unii_id.strip(),
                                   system = 'http://fda.gov/UNII/',
                                   code = unii_id.strip(),
                                   preferred_label = preferred_label.strip())

def create_and_load_from(filepath):
    if not os.path.isfile(filepath):
        print "Can't load UNII, the file does not exist at %s" % filepath
        return
    
    vocabulary = create_vocabulary('unii', 'UNII', 'UNique Ingredient Identifier')
    load(codecs.open(filepath, "r", encoding='utf-8'), vocabulary)