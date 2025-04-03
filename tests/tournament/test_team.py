import pytest

from tournament.players import Player
from tournament.team import Team


@pytest.fixture
def sample_players():
    """Provides a list of sample Player instances."""
    return [
        Player(name="p1", height=180, weight=75, soccer_power=50),
        Player(name="p2", height=175, weight=80, soccer_power=60),
        Player(name="p3", height=190, weight=85, soccer_power=70),
        Player(name="p4", height=170, weight=65, soccer_power=40),
        Player(name="p5", height=185, weight=90, soccer_power=55),
    ]


def test_build_team_correctly(sample_players):
    team = Team.build_team(sample_players, num_defenders=2, num_attackers=2)

    assert len(team.players) == 5
    assert len(team.defenders) == 2
    assert len(team.attackers) == 2
    assert isinstance(team.goalie, Player)  # Check goalie assignment
    assert team.goalie.name == "p3"
    assert team.goalie not in team.defenders
    assert team.goalie not in team.attackers
    assert {"p1", "p4"} == {p.name for p in team.attackers}
    assert {"p2", "p5"} == {p.name for p in team.defenders}
    assert not {p.name for p in team.attackers}.intersection(
        {p.name for p in team.defenders}
    )


def test_build_team_correctly_with_different_attackers_and_defenders(
    sample_players,
):
    team = Team.build_team(sample_players, num_defenders=3, num_attackers=1)

    assert len(team.players) == 5
    assert len(team.defenders) == 3
    assert len(team.attackers) == 1


def test_build_team_invalid_numbers(sample_players):
    """Test that invalid configurations raise ValueError."""
    with pytest.raises(
        ValueError,
        match="The number of attackers and defenders plus a goalie must be 5",
    ):
        Team.build_team(
            sample_players, num_defenders=3, num_attackers=3
        )  # Too many players

    with pytest.raises(
        ValueError,
        match="There must be at least one attacker and one defender",
    ):
        Team.build_team(
            sample_players, num_defenders=0, num_attackers=4
        )  # No defenders

    with pytest.raises(
        ValueError,
        match="There must be at least one attacker and one defender",
    ):
        Team.build_team(
            sample_players, num_defenders=4, num_attackers=0
        )  # No attackers


def test_team_power(sample_players):
    team = Team.build_team(sample_players, num_defenders=2, num_attackers=2)
    expected_power = sum(player.soccer_power for player in team.players)
    assert team.team_power == expected_power


def test_random_attacker_selection(sample_players, mocker):
    team = Team.build_team(sample_players, num_defenders=2, num_attackers=2)
    mock_choice = mocker.patch("random.choice", return_value=team.attackers[0])

    assert team.attacker == team.attackers[0]
    mock_choice.assert_called_once_with(team.attackers)


def test_random_defender_selection(sample_players, mocker):
    team = Team.build_team(sample_players, num_defenders=2, num_attackers=2)
    mock_choice = mocker.patch("random.choice", return_value=team.defenders[0])

    assert team.defender == team.defenders[0]
    mock_choice.assert_called_once_with(team.defenders)
