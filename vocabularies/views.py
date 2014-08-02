"""
.. module:: vocabularies.views
   :synopsis: Views for vocabularies

.. moduleauthor:: James G. Boram Kim <jgkim@jayg.org>

"""

import json

from django.http import *
from django.db.models import Q
from models import *
from serializers import JSONSerializer
from data.utils import utf_8_encoder

def vocabulary_list(request):
    """ List available vocabularies. """

    serializer = JSONSerializer()
    serializer.serialize(Vocabulary.objects.all(), ensure_ascii=False)

    return HttpResponse(utf_8_encoder(serializer.getvalue()), mimetype='application/json')

def vocabulary_meta(request, vocabulary_id):
    """ Return a description of a single vocabulary. """

    try:
        vocabulary = Vocabulary.objects.get(_id=vocabulary_id)
    except Vocabulary.DoesNotExist:
        raise Http404

    serializer = JSONSerializer()
    serializer.serialize([vocabulary,], ensure_ascii=False)

    return HttpResponse(utf_8_encoder(json.dumps(json.loads(serializer.getvalue())[0], ensure_ascii=False)), mimetype='application/json')

def vocabulary_query(request, vocabulary_id):
    """ Query a vocabulary for a value.

    **ARGUMENTS**:
    
    * *request*: The incoming Django request object. ``request.GET`` may contain
      *q*, the keyword to search for, *lang*, the language to search in, and
      *limit*, the maximum number of terms to return.

    * *vocabulary_id*: The slug identifier of the vocabulary, i.e. ``snomed-ct``.

    **RETURNS**:
    
    * :http:statuscode:`200`, with JSON describing vocabulary terms that 
      matched *q*, on success.

    **RAISES**:

    * :py:exc:`~django.http.Http404` if *vocabulary_id* doesn't identify a 
      valid loaded vocabulary.

    """
    try:
        vocabulary = Vocabulary.objects.get(_id=vocabulary_id)
    except Vocabulary.DoesNotExist:
        raise Http404

    keyword = request.GET.get('q', None)
    language = request.GET.get('lang', None)
    limit = request.GET.get('limit', 100)

    query = Q(**{'vocabulary': vocabulary})
    if keyword is not None and len(keyword) > 0:
        if language is not None and len(language) > 0:
            label = 'preferred_label_{}__icontains'.format(language)
        else:
            label = 'preferred_label__icontains'

        query = query & Q(**{label: keyword})

    serializer = JSONSerializer()
    serializer.serialize(Term.objects.filter(query)[:limit], ensure_ascii=False)

    return HttpResponse(utf_8_encoder(serializer.getvalue()), mimetype='application/json')

def vocabulary_term_meta(request, vocabulary_id, term_id):
    """ Return a description of a single vocabulary. """

    try:
        vocabulary = Vocabulary.objects.get(_id=vocabulary_id)
    except Vocabulary.DoesNotExist:
        raise Http404

    try:
        term = Term.objects.get(vocabulary = vocabulary, identifier = term_id)
    except Term.DoesNotExist:
        raise Http404

    serializer = JSONSerializer()
    serializer.serialize([term,], ensure_ascii=False)

    return HttpResponse(utf_8_encoder(json.dumps(json.loads(serializer.getvalue())[0], ensure_ascii=False)), mimetype='application/json')

def coding_systems_list(request):
    return vocabulary_list(request)

def coding_system_query(request, system_short_name):
    """ Query a vocabulary for a value in the deprecated style.

    **ARGUMENTS**:
    
    * *request*: The incoming Django request object. ``request.GET`` must contain
      *q*, the query to search for.

    * *system_short_name*: The slug identifier of the vocabulary, i.e. ``snomed-ct``.

    **RETURNS**:
    
    * :http:statuscode:`200`, with JSON describing vocabulary entries that 
      matched *q*, on success.

    **RAISES**:

    * :py:exc:`~django.http.Http404` if *vocabulary_id* doesn't identify a 
      valid loaded vocabulary.

    """
    try:
        vocabulary = Vocabulary.objects.get(_id=system_short_name)
    except Vocabulary.DoesNotExist:
        raise Http404

    results = []
    for term in Term.objects.filter(vocabulary = vocabulary,
                                   preferred_label__icontains = request.GET.get('q', None))[:100]:
        result = {}
        result['abbreviation'] = None
        result['code'] = term.identifier
        result['consumer_value'] = None
        result['umls_code'] = term.umls_cui
        result['full_value'] = term.preferred_label
        results.append(result)
    
    return HttpResponse(utf_8_encoder(json.dumps(results, ensure_ascii=False)), mimetype='application/json')