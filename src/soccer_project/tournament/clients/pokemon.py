import random

from soccer_project.tournament.api_client import APIClient
from soccer_project.tournament.players import PokePlayer

from .base import BaseClient


class PokemonClient(BaseClient):
    def __init__(self, num_players=5):
        super().__init__(num_players)
        self._all_pokemons = []

    def _fetch_all_pokemons(self):
        client = APIClient()
        if not self._all_pokemons:
            self._all_pokemons = client.get(
                "https://pokeapi.co/api/v2/pokemon/?limit=1302"
            )
        client.close()
        return self._all_pokemons

    def fetch_players(self):
        all_pokemons = self._fetch_all_pokemons()

        random_pokemons = random.choices(
            all_pokemons["results"], k=self.num_players
        )
        players = []
        with APIClient("https://pokeapi.co/api/v2/") as client:
            for poke in random_pokemons:
                pokemon = client.get(f"pokemon/{poke['name']}")
                players.append(
                    PokePlayer(
                        name=pokemon["name"],
                        height=pokemon["height"],
                        weight=pokemon["weight"],
                    )
                )
        return players
