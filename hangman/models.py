from django.db import models
import os
import json
import math
import random

class Game(models.Model):
    word = models.CharField(max_length=50)
    state = models.CharField(max_length=20, default="InProgress")
    incorrect_guesses = models.IntegerField(default=0)
    guessed_word = models.CharField(max_length=50, default="")
    guesses = models.TextField(default="[]")
    max_incorrect_guesses = models.IntegerField(default=0)
    
    #Loads the words from the json file
    with open(os.path.join(os.path.dirname(__file__), 'words.json')) as f:
        WORDS = json.load(f)

    #Returns the guesses as a list
    def get_guesses(self):
        return json.loads(self.guesses)

    #Sets the guesses json for saving to the database
    def set_guesses(self, guesses):
        self.guesses = json.dumps(guesses)

    #Returns the remaining guesses
    def remaining_guesses(self):
        """
        Calculates the remaining guesses based on half the length of the word rounded off.

        Returns:
            int: The remaining guesses.
        """
        return math.ceil(len(self.word) / 2) - self.incorrect_guesses

    #Returns true if the game is won
    def won(self):
        """
        Checks if the game is won.

        Returns:
            bool: True if the guessed word has no underscores(won), False otherwise. 
        """
        return "_" not in self.guessed_word

    #Returns true if the game is lost
    def lost(self):
        """
        Checks if the game is lost.

        Returns:
            bool: True if the remaining guesses are 0 or less, False otherwise.
        """
        return self.remaining_guesses() <= 0

    #Returns true if the game is over (won or lost)
    def guess(self, letter):
        """
        Processes a guess.

        Args:
            letter (str): The letter that was guessed.

        Returns:
            str: A message if the letter was already guessed, None otherwise.
        """
        if letter in self.get_guesses():
            return "You already guessed that letter."

        self.set_guesses(self.get_guesses() + [letter])

        if letter in self.word:
            self.guessed_word = "".join([c if c == letter or self.guessed_word[i] != "_" else "_" for i, c in enumerate(self.word)])
        else:
            self.incorrect_guesses += 1

    #Initializes the game
    def save(self, *args, **kwargs):
            """
            Overrides the save method to initialize the game when it's created.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.
            """
            if self.pk is None:  
                self.incorrect_guesses = 0
                self.word = random.choice(self.WORDS).upper()
                self.guessed_word = "_" * len(self.word)
                self.set_guesses([])
                self.state = 'InProgress'
            super().save(*args, **kwargs)