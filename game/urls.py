from django.urls import path
from . import views

urlpatterns = [
    path('player/<str:game_code>/', views.player_dashboard, name='player_dashboard'),
    path('operator/<str:game_code>/', views.operator_dashboard, name='operator_dashboard'),
    path('api/<str:game_code>/call/', views.call_next_number, name='call_next_number'),
    path('api/<str:game_code>/status/', views.change_game_status, name='change_game_status'),
]
