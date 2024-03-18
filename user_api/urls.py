from django.urls import re_path
from user_api import views

# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns=[
    re_path('register', views.UserRegister.as_view(), name='register'),
	re_path('login', views.UserLogin.as_view(), name='login'),
	re_path('logout', views.UserLogout.as_view(), name='logout'),
	re_path('user', views.UserView.as_view(), name='user'),
]