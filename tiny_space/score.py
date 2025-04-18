"""Handler for the score"""

import logging


class Score:
    def __init__(self):
        self._score = 0

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score: int):
        if score < 0:
            raise ValueError("Can't set negative score!")
        logging.info(f"Set score to {score}.")
        self._score = score


score = Score()

# score.score = 5
# print(score.score)  # -> 5
