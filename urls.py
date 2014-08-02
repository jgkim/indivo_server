from django.conf.urls import patterns, include

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Coding Systems (Deprecated)
    (r'^codes/', include('vocabularies.urls_deprecated')),

    # Vocabularies
    (r'^vocabularies/', include('vocabularies.urls')),

    # Everything to indivo
    (r'^', include('indivo.urls.urls')),
)
