from django.urls import path
from authapp.views import *

urlpatterns = [
   path('' , user_login, name="auth.login" ),
   path('accounts/login/' , redirect_login, name="" ),
   path('api-auth-token',api_auth_token,name='api-auth-token'),
   path('logout',user_logout,name="auth.logout"),
   path('forgot-password',forgot_password,name='auth.forgot'),
   path('reset-password/<uidb64>/<token>/',reset_password,name='auth.reset-pass'),
   path('404-error',error_404,name='error_404'),
   
  
   # path('subsidiaries/', subsidiaries,name='subsidiaries')
]