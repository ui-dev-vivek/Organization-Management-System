from django.urls import path
from authentication.views import *

urlpatterns = [
   path('' , user_login, name="auth.login" ),
   path('logout',user_logout,name="aurh.logout"),
   path('forgot-password',forgot_password,name='auth.forgot'),
   path('reset-password/<uidb64>/<token>/',reset_password,name='auth.reset-pass'),
   
   # path('subsidiaries/', subsidiaries,name='subsidiaries')
]