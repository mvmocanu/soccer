from soccer_project.tournament.players import Player
from soccer_project.tournament.players import PokePlayer


def test_player_initialization():
    player = Player(name="John Doe", height=180, weight=75.5, soccer_power=50)

    assert player.name == "John Doe"
    assert player.height == 180
    assert player.weight == 75.5
    assert player.soccer_power == 50


def test_pokeplayer_conversion_of_height_and_weight():
    poke_player = PokePlayer(name="Pikachu", height=4, weight=60)

    assert poke_player.name == "Pikachu"
    assert poke_player.height == 40  # 4 dm → 40 cm
    assert poke_player.weight == 6.0  # 60 hg → 6.0 kg
