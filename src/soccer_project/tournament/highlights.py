import random

from django.template import Context
from django.template import Template

from .team import Team

highlights = [
    "{{home_team.attacker.name}} scored a penalty againts {{away_team.goalie.name}}",
    "{{home_team.attacker.name}} scored a free kick againts {{away_team.goalie.name}}",
    "{{home_team.defender.name}} made a brilliant pass to {{away_team.attacker.name}}",
    "{{home_team.defender.name}} scored an own goal",
    "{{home_team.attacker.name}} made a crucial tackle",
    "{{home_team.goalie.name}} saved a penalty",
    "{{home_team.goalie.name}} saved a shot on goal",
    "{{home_team.defender.name}} blocked a shot from {{away_team.attacker.name}}",
    "{{home_team.attacker.name}} committed a foul on {{away_team.defender.name}}",
    "{{home_team.attacker.name}} received a yellow card",
    "{{home_team.defender.name}} made a long pass to {{home_team.attacker.name}}",
    "{{home_team.defender.name}} got injured",
]


def get_highlight(home_team: Team, away_team: Team):
    context = Context({"home_team": home_team, "away_team": away_team})
    template = Template(random.choice(highlights))
    rendered_string = template.render(context)
    return rendered_string
