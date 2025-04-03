import random

import pytest

from soccer_project.tournament.clients.pokemon import PokemonClient
from soccer_project.tournament.players import PokePlayer


@pytest.fixture
def mock_api_client(mocker):
    mock_client = mocker.patch(
        "soccer_project.tournament.clients.pokemon.APIClient"
    )
    instance = mock_client.return_value
    instance.get.side_effect = lambda url: (
        {"results": [{"name": f"pokemon{i}"} for i in range(1, 1303)]}
        if "pokemon/?limit=1302" in url
        else {
            "name": url.split("/")[-1],
            "height": random.randint(5, 20),
            "weight": random.randint(10, 100),
        }
    )
    return instance


def test_fetch_all_pokemons(mock_api_client):
    client = PokemonClient()
    pokemons = client._fetch_all_pokemons()

    assert isinstance(pokemons, dict)
    assert "results" in pokemons
    assert len(pokemons["results"]) == 1302
    assert all("name" in p for p in pokemons["results"])


def test_fetch_players(mock_api_client):
    client = PokemonClient(num_players=5)
    players = client.fetch_players()
    assert len(players) == 5
    assert all(isinstance(player, PokePlayer) for player in players)
