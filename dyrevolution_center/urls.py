from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('authapp.urls')),
    path('<str:subsidiary>/', include('subsidiaries.urls')),
]

admin.site.site_header  =  "Dy Revalution Center"  
admin.site.site_title  =  "Dy Revalution Center"
admin.site.index_title  =  "Dy Revalution Center"