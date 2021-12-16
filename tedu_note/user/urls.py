from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('reg', views.reg_view, name='reg_view'),
    path('login', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout_view'),
]