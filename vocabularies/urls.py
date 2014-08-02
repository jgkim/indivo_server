from django.conf.urls import *
from indivo.lib.utils import MethodDispatcher
from views import *

urlpatterns = patterns('',
    (r'^(?P<vocabulary_id>[^/]+)/(?P<term_id>[^/]+)$', MethodDispatcher({'GET': vocabulary_term_meta})),
	(r'^(?P<vocabulary_id>[^/]+)/$', MethodDispatcher({'GET': vocabulary_query})),
	(r'^(?P<vocabulary_id>[^/]+)$', MethodDispatcher({'GET': vocabulary_meta})),
    (r'^$', MethodDispatcher({'GET': vocabulary_list})),
)
