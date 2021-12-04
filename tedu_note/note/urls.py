from django.urls import path

from . import views


urlpatterns = [
    path('add', views.add_note),
    path('all', views.show_note),
    path('update/<int:note_id>', views.update_note),
    path('delete', views.delete_note),
]