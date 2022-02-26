from django.urls import path, re_path

from . import views

app_name = 'user'
urlpatterns = [
    # 登录相关
    path('reg', views.reg_view, name='reg_view'),
    path('login', views.login_view, name='login_view'),
    path('', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout_view'),

    # 用户CURD
    path('add/', views.add_user, name='add_user'),
    re_path('all/(?P<pIndex>[0-9]+)$', views.show_user, name='show_user'),
    re_path('update/(?P<user_id>[0-9]+)$', views.update_user, name='update_user'),
    path('delete/', views.delete_user, name='delete_user'),
    re_path('detail/(?P<user_id>[0-9]+$)', views.detail_user, name='detail_user'),

]