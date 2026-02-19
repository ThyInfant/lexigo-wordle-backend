from django.urls import path
from .views import start_game, submit_guess, game_status, register_user, login_user

urlpatterns = [
    # Game endpoints
    path("start-game/", start_game, name="start_game"),
    path("submit-guess/", submit_guess, name="submit_guess"),
    path("game-status/<int:game_id>/", game_status, name="game_status"),

    # User authentication
    path("register/", register_user, name="register_user"),
    path("login/", login_user, name="login_user"),
]