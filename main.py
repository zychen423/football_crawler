import json
import logging
import subprocess
import sys
from datetime import datetime

import click
import requests
from flask import Flask, render_template

from utils import get_api_key

log_format = """{"severity": "%(levelname)s", "timestamp": "%(asctime)s", "message": "%(message)s"}"""
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_format)


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--league_id",
    type=int,
    required=True,
    help="id of league, can be known by get-league-ids command",
)
@click.option(
    "--start_date", type=str, required=True, help="start date in format YYYY-MM-DD"
)
@click.option(
    "--end_date", type=str, required=True, help="start date in format YYYY-MM-DD"
)
@click.option(
    "--season", type=int, required=True, help="season of the league, e.g. 2021"
)
def get_fixture_infos(league_id, start_date, end_date, season):
    url = "https://v3.football.api-sports.io/fixtures"
    querystring = {
        "league": league_id,
        "season": season,
        "from": start_date,
        "to": end_date,
    }

    headers = {
        "x-rapidapi-host": "https://v3.football.api-sports.io/",
        "x-rapidapi-key": get_api_key(),
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(json.dumps(json.loads(response.text), indent=4))


@cli.command()
@click.option(
    "--fixture_id",
    type=int,
    required=True,
    help="fixture id, can be known by get-feature-infos command",
)
def display_fixture_widget(fixture_id):
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return render_template(
            "fixture_widget.jinja2", fixture_id=fixture_id, api_key=get_api_key()
        )

    subprocess.run(["open", "http://127.0.0.1:8080"])
    app.run(debug=True, port=8080, host="127.0.0.1")


if __name__ == "__main__":
    cli()
