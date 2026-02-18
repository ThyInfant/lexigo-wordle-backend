project:
name: Lexigo Wordle Backend API
type: Django REST API
description: >
Backend API for the Wordle game mode inside the Lexigo platform.
Handles game sessions, guesses, validation logic, and optional
authentication and leaderboard features.

tech_stack:

- Python
- Django
- Django REST Framework
- SQLite
- GitHub

database:
entities:
User:
description: Built-in Django authentication model
fields: - id - username - email - password

    Game:
      description: Stores each Wordle session
      fields:
        - id
        - user (ForeignKey, optional)
        - target_word
        - attempts_remaining
        - status (ongoing, won, lost)
        - created_at

    Guess:
      description: Stores each guess submitted in a game
      fields:
        - id
        - game (ForeignKey)
        - guess_word
        - feedback (JSON)
        - created_at

relationships: - One User has many Games - One Game has many Guesses - Each Guess belongs to one Game

api_endpoints:
game: - method: POST
endpoint: /api/start-game/
description: Start a new Wordle game

    - method: POST
      endpoint: /api/submit-guess/
      description: Submit a guess and receive feedback

    - method: GET
      endpoint: /api/game-status/<game_id>/
      description: Retrieve game progress and previous guesses

optional: - method: GET
endpoint: /api/leaderboard/
description: Retrieve top players

    - method: POST
      endpoint: /api/token/
      description: Obtain authentication token

roadmap:

- Project setup
- Database models
- Game start endpoint
- Guess submission endpoint
- Game status endpoint
- Authentication
- Leaderboard
- Daily challenge
- Integration with Lexigo frontend
