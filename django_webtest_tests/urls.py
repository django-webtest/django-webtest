from django.conf.urls.defaults import *
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

def simple_method_test(request):
    return HttpResponse(unicode(request.method))

urlpatterns = patterns('',
    url(r'^$', simple_method_test, name='simple-method-test'),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
