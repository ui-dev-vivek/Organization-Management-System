from django.urls import path
from authentication.views import *

urlpatterns = [
   path('' , user_login, name="auth.login" ),
   path('logout',user_logout,name="aurh.logout"),
]