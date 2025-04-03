import random

import pytest

from tournament.clients.star_wars import StarWarsClient
from tournament.players import StarWarsPlayer


@pytest.fixture
def mock_api_client(mocker):
    mock_client = mocker.patch("tournament.clients.star_wars.APIClient")
    instance = mock_client.return_value
    # Mock response for a valid person
    instance.get.side_effect = (
        lambda url: {
            "name": f"Person{url.split('/')[-2]}",
            "height": str(random.randint(150, 250)),
            "mass": str(random.randint(50, 100)),
        }
        if "/people/" in url and "17" not in url
        else None
    )
    return instance


def test_fetch_players(mock_api_client):
    client = StarWarsClient(num_players=5)
    players = client.fetch_players()

    assert len(players) == 5
    assert all(isinstance(player, StarWarsPlayer) for player in players)
