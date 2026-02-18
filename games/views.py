from django.shortcuts import render
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game, Guess

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
    
def generate_feedback(guess, target):
    feedback = []
    target_letters = list(target)

    # First pass: correct positions
    for i in range(len(guess)):
        if guess[i] == target[i]:
            feedback.append("correct")
            target_letters[i] = None
        else:
            feedback.append(None)

    # Second pass: wrong position or incorrect
    for i in range(len(guess)):
        if feedback[i] is None:
            if guess[i] in target_letters:
                feedback[i] = "wrong_position"
                target_letters[target_letters.index(guess[i])] = None
            else:
                feedback[i] = "incorrect"

    return feedback


@api_view(["POST"])
def submit_guess(request):
    game_id = request.data.get("game_id")
    guess_word = request.data.get("guess")

    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response({"error": "Game not found"}, status=404)

    if game.status != "ongoing":
        return Response({"error": "Game already finished"}, status=400)

    guess_word = guess_word.upper()

    feedback = generate_feedback(guess_word, game.target_word)

    Guess.objects.create(
        game=game,
        guess_word=guess_word,
        feedback=feedback
    )

    game.attempts_remaining -= 1

    if guess_word == game.target_word:
        game.status = "won"
    elif game.attempts_remaining == 0:
        game.status = "lost"

    game.save()

    return Response({
        "feedback": feedback,
        "attempts_remaining": game.attempts_remaining,
        "status": game.status
    })
    
@api_view(["GET"])
def game_status(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response({"error": "Game not found"}, status=404)

    guesses = Guess.objects.filter(game=game)

    guess_data = []
    for guess in guesses:
        guess_data.append({
            "guess_word": guess.guess_word,
            "feedback": guess.feedback,
            "created_at": guess.created_at
        })

    return Response({
        "game_id": game.id,
        "attempts_remaining": game.attempts_remaining,
        "status": game.status,
        "guesses": guess_data
    })