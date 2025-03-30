import random
from dataclasses import dataclass

from .highlights import get_highlight
from .team import Team


@dataclass
class Match:
    home_team: Team
    away_team: Team

    @property
    def highlights(self):
        return [
            get_highlight(*random.sample([self.home_team, self.away_team], 2))
            for _ in range(20)
        ]
