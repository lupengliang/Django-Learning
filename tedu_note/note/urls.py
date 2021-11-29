from django.urls import path

from . import views


urlpatterns = [
    path('add', views.add_note),
    path('all', views.show_note),
    path('delete/<int: id>', views.delete_note),
]