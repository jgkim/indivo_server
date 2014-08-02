"""
ISO 639-1 Two-letter Language Codes loading

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
            identifier, language_name, native_name = row
        except ValueError:
            continue

        models.Term.objects.create(vocabulary = vocabulary,
                                   identifier = identifier.strip(),
                                   system = 'http://vocab.cophr.org/language-code/',
                                   code = identifier.strip(),
                                   preferred_label = language_name.strip(),
                                   meta = {'native_name': native_name.strip()})

def create_and_load_from(filepath):
    if not os.path.isfile(filepath):
        print "Can't load the language codes, the file does not exist at %s" % filepath
        return
    
    vocabulary = create_vocabulary('language-code', 'Language Code', 'ISO 639-1 two-letter language code')
    load(codecs.open(filepath, "r", encoding='utf-8'), vocabulary)