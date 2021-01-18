from django.urls import path
from . import views
urlpatterns = [
path('songs', views.songs, name='songs'),
path('songs/<int:id>',views.songpost, name='songpost'),
path('login',views.login, name='login'),
path('logout_user',views.logout_user, name='logout_user'),
path('signup',views.signup, name='signup'),
path('watchlater',views.watchlater, name='watchlater'),
path('wl_delete/<int:id>',views.wl_delete, name='wl_delete'),
path('search',views.search, name='search'),

] 
