from soccer_project.tournament.match import Match


def test_match_highlights_length(team):
    """Ensure the match generates exactly 20 highlights."""
    match = Match(team, team)
    assert len(match.highlights) == 20
    assert all(isinstance(h, str) and h for h in match.highlights)
