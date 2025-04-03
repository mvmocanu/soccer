import pytest
import requests
from django.core.cache import cache

from soccer_project.tournament.api_client import APIClient


@pytest.fixture
def api_client():
    """Fixture to create an APIClient instance."""
    return APIClient(base_url="https://api.example.com")


def test_fetch_from_cache(mocker, api_client):
    """Test that APIClient returns data from cache if available."""
    mock_cache_get = mocker.patch.object(
        cache, "get", return_value={"data": "cached"}
    )

    response = api_client.get("/test")

    assert response == {"data": "cached"}
    mock_cache_get.assert_called_once_with("https://api.example.com/test")


def test_fetch_from_web(mocker, api_client):
    """Test that APIClient fetches from web if cache is empty and stores result in cache."""
    mock_cache_get = mocker.patch.object(cache, "get", return_value=None)
    mock_cache_set = mocker.patch.object(cache, "set")

    mock_response = mocker.Mock()
    mock_response.json.return_value = {"data": "fetched from web"}
    mock_response.raise_for_status = mocker.Mock()

    mock_get = mocker.patch.object(
        requests.Session, "get", return_value=mock_response
    )

    response = api_client.get("/test")

    assert response == {"data": "fetched from web"}
    mock_cache_get.assert_called_once_with("https://api.example.com/test")
    mock_get.assert_called_once_with(
        "https://api.example.com/test", params=None
    )
    mock_cache_set.assert_called_once_with(
        "https://api.example.com/test", {"data": "fetched from web"}
    )


def test_fetch_raises_error(mocker, api_client):
    """Test that APIClient raises an error when the request fails."""
    mocker.patch.object(cache, "get", return_value=None)

    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("Error")

    mock_get = mocker.patch.object(
        requests.Session, "get", return_value=mock_response
    )

    with pytest.raises(requests.HTTPError):
        api_client.get("/error")

    mock_get.assert_called_once_with(
        "https://api.example.com/error", params=None
    )


def test_session_closes(mocker, api_client):
    """Test that the session is closed when APIClient.close() is called."""
    mock_close = mocker.patch.object(api_client.session, "close")

    api_client.close()

    mock_close.assert_called_once()


def test_context_manager(mocker):
    """Test that APIClient properly closes the session when used with 'with'."""
    mock_close = mocker.patch(
        "soccer_project.tournament.api_client.APIClient.close"
    )

    with APIClient(base_url="https://api.example.com") as client:
        assert isinstance(client, APIClient)

    mock_close.assert_called_once()
