"""
Encounter Types loading

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
            identifier, preferred_label, preferred_label_ko = row
        except ValueError:
            continue

        if identifier == 'daySurgery':
          system = 'http://vocab.cophr.org/encounter-type/'
        else:
          system = 'http://smartplatforms.org/terms/codes/EncounterType#'

        models.Term.objects.create(vocabulary = vocabulary,
                                   identifier = identifier.strip(),
                                   system = system,
                                   code = identifier.strip(),
                                   preferred_label = preferred_label.strip(),
                                   preferred_label_ko = preferred_label_ko.strip())

def create_and_load_from(filepath):
    if not os.path.isfile(filepath):
        print "Can't load the encounter types, the file does not exist at %s" % filepath
        return
    
    vocabulary = create_vocabulary('encounter-type', 'Encounter Type', "Type of encounter, using a SMART Platforms' sp:EncounterType code")
    load(codecs.open(filepath, "r", encoding='utf-8'), vocabulary)