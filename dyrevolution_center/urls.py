from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('authapp.urls')),
    path('<str:subsidiary>/', include('subsidiaries.urls')),
    path('api/v1/',include('restapi.urls')),
]

admin.site.site_header  =  "Dy Revalution Center"  
admin.site.site_title  =  "Dy Revalution Center"
admin.site.index_title  =  "Dy Revalution Center"

from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
