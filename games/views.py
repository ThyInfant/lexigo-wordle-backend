from django.shortcuts import render
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game

# Create your views here.
WORD_LIST = ["APPLE", "GRAPE", "MANGO", "BERRY", "LEMON"]


@api_view(["POST"])
def start_game(request):
    target_word = random.choice(WORD_LIST)

    game = Game.objects.create(
        target_word=target_word,
        attempts_remaining=6,
        status="ongoing"
    )

    return Response({
        "game_id": game.id,
        "attempts_remaining": game.attempts_remaining,
        "status": game.status
    })