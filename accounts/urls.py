from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.public_join_view, name='public_join'),
    path('dashboard/', views.home_view, name='home'),
    path('delete/<str:game_code>/', views.delete_game_view, name='delete_game'),
]
