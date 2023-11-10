from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Game
import json

# Create a new game at game/new
@require_http_methods(["GET"])
def create(request):
    """
    Creates a new game and returns the game id.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        JsonResponse: The HTTP response containing the game id.
    """

    game = Game()
    game.save()
    return JsonResponse({"id": game.id}, status=201)

# Get the game state at game/<game_id>
@require_http_methods(["GET"])
def show(request, game_id):
    """
    Returns the state of the game with the given id.

    Args:
        request (HttpRequest): The HTTP request.
        game_id (int): The id of the game.

    Returns:
        JsonResponse: The HTTP response containing the game state.
    """

    try:
        game = Game.objects.get(id=game_id)
        return JsonResponse({
            "state": game.state,
            "word": game.guessed_word,
            "incorrect_guesses": game.incorrect_guesses,
            "remaining_guesses": game.remaining_guesses()
        })
    except Game.DoesNotExist:
        return JsonResponse({"message": "Game not found"}, status=404)

# Make a guess in hangman at game/<game_id>/guess
@require_http_methods(["POST"])
def guess(request, game_id):
    """
    Processes a guess for the game with the given id.

    Args:
        request (HttpRequest): The HTTP request, containing the guessed letter in the body.
        game_id (int): The id of the game.

    Returns:
        JsonResponse: The HTTP response containing the game state after the guess.
    """
    try:
        game = Game.objects.get(id=game_id)
        data = json.loads(request.body)
        guessed_letter = str(data.get('guess'))

        #check if game is still in progress
        if game.state in ['Won', 'Lost']:
            return JsonResponse({"message": f"Game {game.state}. No more guesses are accepted."}, status=422)

        #check if guessed_letter is valid
        if not guessed_letter or len(guessed_letter) != 1 or not guessed_letter.isalpha():
            return JsonResponse({"message": "Invalid guess. Please enter a single letter."}, status=422)

        guessed_letter = guessed_letter.upper()
        result = game.guess(guessed_letter)

        #check if guessed letter has already been guessed
        if isinstance(result, str):
            return JsonResponse({"message": result}, status=422)

        #check if game is won or lost and update game state
        if game.won():
            game.state = 'Won'
        elif game.lost():
            game.state = 'Lost'

        game.save()

        return JsonResponse({
            "state": game.state,
            "word": game.guessed_word,
            "incorrect_guesses": game.incorrect_guesses,
            "remaining_guesses": game.remaining_guesses(),
            "correct_guess": guessed_letter in game.word
        }, status=200)

    except Game.DoesNotExist:
        return JsonResponse({"message": "Game not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)