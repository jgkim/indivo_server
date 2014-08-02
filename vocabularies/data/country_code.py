"""
ISO-3166-1 Alpha-3 Country Codes loading

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
            identifier, country_name = row
        except ValueError:
            continue

        models.Term.objects.create(vocabulary = vocabulary,
                                   identifier = identifier.strip(),
                                   system = 'http://vocab.cophr.org/country-code/',
                                   code = identifier.strip(),
                                   preferred_label = country_name.strip())

def create_and_load_from(filepath):
    if not os.path.isfile(filepath):
        print "Can't load the country codes, the file does not exist at %s" % filepath
        return
    
    vocabulary = create_vocabulary('country-code', 'Country Code', 'ISO 3166-1 alpha-3 country code')
    load(codecs.open(filepath, "r", encoding='utf-8'), vocabulary)