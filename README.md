# Hangman Game

This is a simple implementation of the classic Hangman game using Django for the backend.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.11 or higher
- Django 3.2 or higher

### Installation

1. Clone the repository

```
git clone git@github.com:Soundmoney254/hangman.git
```

2. Navigate into the cloned repository

```
cd hangman
```

3. Install Django

```
pip install Django
```

4. Run the server

```
python manage.py runserver
```

You can now access the server on the endpoint

```
http://127.0.0.1:8000/
```

## Usage

- To create a new game, make a GET request to `/game/new`. The response will include the game id.
- To get the current state of a game, make a GET request to `/game/<game_id>`.
- To make a guess, make a POST request to `/game/<game_id>/guess` with the guessed letter in the body.

## Contributing

I welcome all contributions. If you have any suggestions, bug reports, or feature requests, please open an issue on the GitHub repository or submit a pull request.

## License and copyright

- The code in this project is licensed under the terms of the General Public License (GPL-3.0).

- You are granted permission to use, modify, and contribute to the project under the conditions outlined in the GPL-3.0 license.

- It is important to preserve and include the copyright and license notices in all copies and distributions of the project.

## Author

This project was created by Samuel Mbugua.
