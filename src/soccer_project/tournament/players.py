import random
from dataclasses import dataclass
from dataclasses import field


@dataclass
class Player:
    name: str
    height: int
    weight: float
    soccer_power: int = field(default_factory=lambda: random.randint(1, 100))


@dataclass
class PokePlayer(Player):
    def __post_init__(self):
        self.height = self.height * 10  # decimeter to cm
        self.weight = self.weight / 10  # hectograms to kg


@dataclass
class StarWarsPlayer(Player):
    pass
