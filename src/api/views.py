from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from tournament.clients.pokemon import PokemonClient
from tournament.clients.star_wars import StarWarsClient
from tournament.match import Match
from tournament.team import Team

from .serializers import MatchSerializer


@api_view(["GET"])
def api_root(request, format=None):
    """
    The Star Wars and Pokemon universes have collided and a big soccer tournament is being planned to settle which universe is best.
    If you navigate to the play endpoint, you will see the greatest match of all time.
    """
    return Response({"play": reverse("play_match", request=request)})


class MatchView(APIView):
    """
    Each team consist of 5 players (by default, but the number can be changed).
    There are three roles in a team:
     * 'Goalie': The tallest player
     * 'Defence': The heaviest players
     * 'Offence': The shortest players

    The number of players can be changed by passing `num_players` as a query param (default: 5).
    The number of attackers can be changed by passing `num_attackers` as a query param (default: 2).
    The number of defenders can be changed by passing `num_defenders` as a query param (default: 2).

    In the payload the teams that are playing can be seen and also the highlights of the match.
    """

    def get(self, request, format=None):
        try:
            num_players = int(request.query_params.get("num_players", 5))
            num_attackers = int(request.query_params.get("num_attackers", 2))
            num_defenders = int(request.query_params.get("num_defenders", 2))
        except ValueError as e:
            raise ValidationError(str(e)) from e

        try:
            poke_client = PokemonClient(num_players)
            poke_players = poke_client.fetch_players()
            sw_client = StarWarsClient(num_players)
            sw_players = sw_client.fetch_players()
        except Exception as e:
            raise ValidationError(str(e)) from e

        try:
            poke_team = Team.build_team(
                poke_players,
                num_attackers=num_attackers,
                num_defenders=num_defenders,
            )
            sw_team = Team.build_team(
                sw_players,
                num_attackers=num_attackers,
                num_defenders=num_defenders,
            )
        except ValueError as e:
            raise ValidationError(str(e)) from e

        # Return the data as a JsonResponse
        return Response(
            MatchSerializer(
                Match.play(home_team=poke_team, away_team=sw_team)
            ).data
        )
