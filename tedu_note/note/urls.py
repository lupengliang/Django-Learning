from django.urls import path

from . import views

app_name = 'note'  # 添加应用命名空间
urlpatterns = [
    path('add/', views.add_note, name='add_note'),  # 重命名可以优化模板中的硬编码
    path('all/', views.show_note, name='show_note'),
    path('update/<int:note_id>/', views.update_note, name='update_note'),
    path('delete/', views.delete_note, name='delete_note'),
]