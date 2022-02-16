from django.urls import path

from . import views

app_name = 'index'
urlpatterns = [
    path('index', views.index_view, name='index_view'),
]