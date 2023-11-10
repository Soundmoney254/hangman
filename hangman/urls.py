from django.urls import path
from .views import create, show, guess

urlpatterns = [
    path('new/', create, name='create_game'),
    path('<int:game_id>/', show, name='display_game'),
    path('<int:game_id>/guess/', guess, name='make_guess'),
]