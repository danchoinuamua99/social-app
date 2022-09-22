from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('settings/', views.setting, name='settings'),
]

htmx_urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('upload/', views.upload, name='upload'),
]

urlpatterns += htmx_urlpatterns
