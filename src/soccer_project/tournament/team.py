import logging
import random
from dataclasses import dataclass

from .players import Player

logger = logging.getLogger(__name__)


@dataclass
class Team:
    players: list[Player]
    goalie: Player
    defenders: list[Player]
    attackers: list[Player]

    @property
    def attacker(self) -> Player:
        return random.choice(self.attackers)

    @property
    def defender(self) -> Player:
        return random.choice(self.defenders)

    @property
    def team_power(self) -> int:
        return sum({p.soccer_power for p in self.players})

    @classmethod
    def build_team(
        cls, players: list[Player], num_defenders: int, num_attackers: int
    ):
        if (num_defenders + num_attackers + 1) != len(players):
            raise ValueError(
                f"The number of attackers and defenders plus a goalie must be {len(players)}"
            )

        if num_attackers == 0 or num_defenders == 0:
            raise ValueError(
                "There must be at least one attacker and one defender"
            )

        all_players = players
        players = sorted(
            players, key=lambda player: (player.height, -player.weight)
        )
        goalie = players.pop()

        # We want to fetch first the smallest number of players in order to delete them from
        # the list of players
        if num_attackers < num_defenders:
            # first fetch the attackers and after that defenders
            players = sorted(
                players, key=lambda player: (player.height, player.weight)
            )
            attackers = players[:num_attackers]
            del players[:num_attackers]
            defenders = sorted(
                players, key=lambda player: (-player.weight, -player.height)
            )[:num_defenders]
        else:
            players = sorted(
                players, key=lambda player: (-player.weight, -player.height)
            )
            defenders = players[:num_defenders]
            del players[:num_defenders]
            attackers = sorted(
                players, key=lambda player: (player.height, player.weight)
            )[:num_attackers]
        return cls(
            players=all_players,
            goalie=goalie,
            defenders=defenders,
            attackers=attackers,
        )
