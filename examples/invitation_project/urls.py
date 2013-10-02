from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from registration.forms import RegistrationFormTermsOfService
from invitation.views import register

admin.autodiscover()

# Change URLs given the INVITE_MODE setting, useful for tests
if getattr(settings, 'INVITE_MODE', False):
    urlpatterns = patterns('',
        url(r'^accounts/register/$',    register,
                                            {
                                                'form_class': RegistrationFormTermsOfService,
                                                'backend': 'invitation.backends.InvitationBackend',
                                            },
                                            name='registration_register'),
    )
else:
    urlpatterns = patterns('',
        url(r'^accounts/register/$',    register,
                                            {
                                                'form_class': RegistrationFormTermsOfService,
                                                'backend': 'registration.backends.default.DefaultBackend',
                                            },
                                            name='registration_register'),
    )

urlpatterns += patterns('',
    url(r'^accounts/',              include('invitation.urls')),
    url(r'^accounts/',              include('registration.urls')),
    url(r'^admin/',                 include(admin.site.urls)),
    
)
