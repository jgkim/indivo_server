from django.conf.urls import *
from indivo.lib.utils import MethodDispatcher
from views import *

urlpatterns = patterns('',
    (r'^systems/(?P<system_short_name>[^/]+)/query$', MethodDispatcher({'GET': coding_system_query})),
    (r'^systems/$', MethodDispatcher({'GET': coding_systems_list})),
)