from django.shortcuts import render
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Game, Guess, Word
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Create your views here.
WORD_LIST = ["APPLE", "GRAPE", "MANGO", "BERRY", "LEMON"]


@api_view(["POST"])
def start_game(request):
    words_qs = Word.objects.filter(is_active=True)
    count = words_qs.count()

    if count == 0:
        return Response(
            {"error": "No words available in the database"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Fast random selection
    import random
    random_index = random.randint(0, count - 1)
    target_word = words_qs[random_index].text.upper()

    game = Game.objects.create(
        target_word=target_word,
        attempts_remaining=6,
        status="ongoing"
    )

    return Response({
        "game_id": game.id,
        "attempts_remaining": game.attempts_remaining,
        "status": game.status
    }, status=status.HTTP_201_CREATED)
    
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

    # convert both to lowercase for accurate comparison
    guess_word_lower = guess_word.lower()
    target_word_lower = game.target_word.lower()

    feedback = generate_feedback(guess_word_lower, target_word_lower)

    Guess.objects.create(
        game=game,
        guess_word=guess_word_lower,
        feedback=feedback
    )

    game.attempts_remaining -= 1

    if guess_word_lower == target_word_lower:
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
    
# Register new user
@api_view(["POST"])
def register_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)

    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

# Login existing user
@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }, status=status.HTTP_200_OK)