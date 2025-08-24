"""Handler for the score"""

from dataclasses import dataclass


@dataclass
class Score:
    # Four kinds of scores.
    red: int = 0
    blue: int = 0
    green: int = 0
    yellow: int = 0

    def set_scores(self, red: int, blue: int, green: int, yellow: int) -> None:
        """Set the scores for each color."""
        self.red = red
        self.blue = blue
        self.green = green
        self.yellow = yellow


score = Score()
