from unittest.mock import patch

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


def test_match_view_success(api_client, mocker):
    """Test successful retrieval of match data"""
    with (
        patch(
            "soccer_project.tournament.clients.pokemon.PokemonClient"
        ) as mock_poke_client,
        patch(
            "soccer_project.tournament.clients.star_wars.StarWarsClient"
        ) as mock_sw_client,
        patch(
            "soccer_project.tournament.team.Team.build_team"
        ) as mock_build_team,
        patch("soccer_project.api.views.MatchSerializer") as mock_serializer,
    ):
        # Setup mock clients and team building logic
        mock_poke_client.return_value.fetch_players.return_value = ["poke"]
        mock_sw_client.return_value.fetch_players.return_value = ["star wars"]
        mock_build_team.return_value = "Mock Team"
        mock_serializer.return_value.data = {"match": "won"}

        response = api_client.get(
            "/play/",
            {"num_players": 5, "num_attackers": 2, "num_defenders": 2},
        )

        # Ensure the response is successful
        assert response.status_code == status.HTTP_200_OK


def test_match_view_missing_parameters(api_client):
    """Test that default values are used when parameters are missing"""
    with (
        patch(
            "soccer_project.tournament.clients.pokemon.PokemonClient"
        ) as mock_poke_client,
        patch(
            "soccer_project.tournament.clients.star_wars.StarWarsClient"
        ) as mock_sw_client,
        patch(
            "soccer_project.tournament.team.Team.build_team"
        ) as mock_build_team,
        patch("soccer_project.api.views.MatchSerializer") as mock_serializer,
    ):
        mock_poke_client.return_value.fetch_players.return_value = ["poke"]
        mock_sw_client.return_value.fetch_players.return_value = ["star wars"]
        mock_build_team.return_value = "Mock Team"
        mock_serializer.return_value.data = {"match": "won"}

        response = api_client.get("/play/")

        # Ensure default values are used and the response is successful
        assert response.status_code == status.HTTP_200_OK


def test_match_view_invalid_parameters(api_client):
    """Test handling of invalid parameters"""
    url = "/play/"

    # Test invalid num_players parameter
    response = api_client.get(url, {"num_players": "invalid"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Test invalid num_attackers parameter
    response = api_client.get(url, {"num_attackers": "invalid"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Test invalid num_defenders parameter
    response = api_client.get(url, {"num_defenders": "invalid"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_match_view_client_fetch_error(api_client):
    """Test that errors in client fetching (e.g., API failure) return a 400 status"""
    with (
        patch(
            "soccer_project.tournament.clients.pokemon.PokemonClient"
        ) as mock_poke_client,
        patch(
            "soccer_project.tournament.clients.star_wars.StarWarsClient"
        ) as mock_sw_client,
    ):
        # Simulate client fetching error (e.g., timeout, invalid response)
        mock_poke_client.return_value.fetch_players.side_effect = Exception(
            "API failure"
        )
        mock_sw_client.return_value.fetch_players.side_effect = Exception(
            "API failure"
        )

        response = api_client.get("/play/")

        # Ensure 400 Bad Request is returned due to fetching errors
        assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_match_view_team_build_error(api_client):
    """Test that errors in building teams return a 400 status"""
    with (
        patch(
            "soccer_project.tournament.clients.pokemon.PokemonClient"
        ) as mock_poke_client,
        patch(
            "soccer_project.tournament.clients.star_wars.StarWarsClient"
        ) as mock_sw_client,
        patch(
            "soccer_project.tournament.team.Team.build_team"
        ) as mock_build_team,
    ):
        mock_poke_client.return_value.fetch_players.return_value = ["poke"]
        mock_sw_client.return_value.fetch_players.return_value = ["star wars"]

        # Simulate team build failure (e.g., wrong number of players)
        mock_build_team.side_effect = ValueError("Invalid team configuration")

        response = api_client.get("/play/")

        # Ensure 400 Bad Request is returned due to team build errors
        assert response.status_code == status.HTTP_400_BAD_REQUEST
