"""
Immunization Product Names loading

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
            identifier, preferred_label = row
        except ValueError:
            continue

        models.Term.objects.create(vocabulary = vocabulary,
                                   identifier = identifier.strip(),
                                   system = 'http://www2a.cdc.gov/vaccines/IIS/IISStandards/vaccines.asp?rpt=cvx#',
                                   code = identifier.strip(),
                                   preferred_label = preferred_label.strip())

def create_and_load_from(filepath):
    if not os.path.isfile(filepath):
        print "Can't load the immunization product names, the file does not exist at %s" % filepath
        return
    
    vocabulary = create_vocabulary('immunization-product-name', 'Immunization Product Name', 'Coded name describing the product according to the set of codes in the CVX for immunizations controlled vocabulary')
    load(codecs.open(filepath, "r", encoding='utf-8'), vocabulary)