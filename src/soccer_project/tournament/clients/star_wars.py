import random

from soccer_project.tournament.api_client import APIClient
from soccer_project.tournament.players import StarWarsPlayer

from .base import BaseClient


class StarWarsClient(BaseClient):
    def __init__(self, num_players=5):
        super().__init__(num_players)
        self._all_people = []

    def fetch_players(self):
        players = {}
        while True:
            random_id = random.randint(1, 83)  # SWAPI has 83 people in total
            if random_id in players.keys() or random_id == 17:
                # 17 is a 404, we can skip it
                continue
            with APIClient() as client:
                url = f"https://swapi.dev/api/people/{random_id}"
                person = client.get(url)
                if person["mass"] == "unknown":
                    continue
                weight = float(person["mass"].replace(",", ""))
                players[random_id] = StarWarsPlayer(
                    name=person["name"],
                    height=int(person["height"]),
                    weight=weight,
                )
                if len(players.keys()) == self.num_players:
                    break
        return players.values()

    def _fetch_all_people(self):
        if self._all_people:
            return self._all_people

        with APIClient() as client:
            url = "https://swapi.dev/api/people/"
            while url:
                response = client.get(url)
                self._all_people.extend(response["results"])
                url = response["next"]

        return self._all_people

    def expensive_fetch_players(self):
        all_people = self._fetch_all_people()
        random.shuffle(all_people)
        players = []
        _num_players = 0
        for person in all_people:
            if person["mass"] == "unknown":
                continue
            weight = float(person["mass"].replace(",", ""))
            players.append(
                StarWarsPlayer(
                    name=person["name"],
                    height=int(person["height"]),
                    weight=weight,
                )
            )
            if (_num_players := _num_players + 1) == self.num_players:
                break
        return players
