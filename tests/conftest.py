import pytest

from soccer_project.tournament.players import Player
from soccer_project.tournament.team import Team


@pytest.fixture
def sample_players():
    return [
        Player(name="p1", height=180, weight=75, soccer_power=50),
        Player(name="p2", height=175, weight=80, soccer_power=60),
        Player(name="p3", height=190, weight=85, soccer_power=70),
        Player(name="p4", height=170, weight=65, soccer_power=40),
        Player(name="p5", height=185, weight=90, soccer_power=55),
    ]


@pytest.fixture
def team(sample_players):
    return Team.build_team(sample_players, num_defenders=2, num_attackers=2)
