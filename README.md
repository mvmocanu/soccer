# Super Soccer Showdown

The Star Wars and Pokemon universes have collided and a big soccer tournament is being planned to
settle which universe is best.
You are tasked with creating a solution that can generate random teams for each universe!

## Team Generator

Using the publicly available APIs https://swapi.dev and https://pokeapi.co create a solution that can
generate random SuperSoccer Showdown teams for each universe, such that:

1. Each team consist of 5 players
1. Each player can play only one position
1. Each player has three stats:

- _Name_
- _Weight_ (Kg)
- _Height_ (cm)

4. Each team has three different player types:

- _Goalie_: The tallest player
- _Defence_: The heaviest players
- _Offence_: The shortest players

5. Each team can be configured with different lineups (the number of attackers and defenders)

## Developement

### Installing the project

Having docker on the local machine is a requirement.

1. In the root of the project, run the following command:

```
docker compose up --build
```

2. After the build is finished, run the following commands

```
docker compose exec django-web bash
cd src
python manage.py collectstatic
```

### Running the project

1. In the root of the porject, run the following command:

```
docker compose up
```

2. Go to http://localhost:8000/

### Running the tests

In the root of the project, the following command can be run:

```
docker compose run django-web pytest
```

## Architecture

The project is built on top of Django and leverages Django Rest Framework for exposing API endpoints.

For generating the teams, there is a `tournament` library within the project that can be used independently of the Django project

### Fetching players from Pokemon API

The following snippet of code can be used to fetch a specified number of players from Pokemon API

```
from tournament.clients.pokemon import PokemonClient
poke_client = PokemonClient(num_players=5)
players = poke_client.fetch_players()
```

### Fetching players from StarWars API

The following snippet of code can be used to fetch a specified number of players from StarWars API

```
from tournament.clients.star_wars import StarWarsClient
sw_client = StarWarsClient(num_players)
sw_players = sw_client.fetch_players()

```

### Building a team

Once we have players, we can build a team.

```
from tournament.team import Team
team = Team.build_team(players, num_attackers=2, num_defenders=2)

```

On the `team` object multiple properties about that team are available:

- `attacker` - a random attacker
- `defender` - a random defender
- `goalie` - the goalie of the team
- `attackers` - all attackers whitin the team
- `defenders` - all defenders within the team
- `team_power` - the sum of a new statistic 'player soccer power'

### Play a match

If we have more teams, a match can be played between two teams.

```
from tournament.match import Match
match = Match.play(home_team=poke_team, away_team=sw_team)
```

On the `match` object, the `highlights` of the match can be found.

## Things to improve

The primary performance bottleneck of the application is the reliance on external requests to the Star Wars and Pokémon APIs. To speed up team generation, one effective approach is to fetch the necessary data asynchronously. This can be achieved in various ways, such as implementing a management command that runs as a scheduled cron job. The command can periodically retrieve data, check for updates in the APIs, and update the local dataset accordingly.

If we store this data in a local database, adopting a master/slave architecture can significantly improve efficiency. By directing all read queries to a slave instance, we can reduce the load on the primary database while maintaining performance. Additionally, as the application scales and gains more users, implementing a caching layer on top of the database can further optimize response times and ensure a seamless user experience.
