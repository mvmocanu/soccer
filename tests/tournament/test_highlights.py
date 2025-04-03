from tournament.highlights import get_highlight


def test_get_highlight_returns_non_empty_string(team):
    """Ensure the function returns a valid string."""
    highlight = get_highlight(team, team)
    assert isinstance(highlight, str)
    assert highlight  # Ensure it's not empty
