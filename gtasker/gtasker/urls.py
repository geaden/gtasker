import os
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Your project url
    url('^', include('apps.projects.urls',
                     namespace='projects',
                     app_name='projects'),
        ),
    url('^profiles/', include('apps.profiles.urls',
                              namespace='profiles',
                              app_name='profiles')),
    url('^tasks/', include('apps.tasks.urls',
                           namespace='tasks',
                           app_name='tasks')),

    url('^sms/', include('apps.sms.urls',
                         namespace='sms',
                         app_name='sms')),
)

