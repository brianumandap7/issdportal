from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

#def custom_page_not_found(request):
#    return django.views.defaults.page_not_found(request, None)

urlpatterns = [
    path('admin/', admin.site.urls),
    #JASB
    path('', include('account.urls')),
    path('', include('pnpki.urls')),    
    path('', include('spms.urls')),
    #JASB
    path('cs/', include('cs.urls')),
    path('issp/', include('issp.urls')),
]
