import json
import sys
from os import path

import click
import requests

from lara_cli import clinic
from lara_cli import config
from lara_cli import user
from lara_cli import reports
from lara_cli import forms
from lara_cli.api import APISession
from lara_cli.config import CONFIG_PATH

APIS = {
    "default": {
        "dev": "https://api.dev.larahealth.cloud",
        "preprod": "https://api-preprod.lara.health",
        "prod": "https://api.lara.health",
    },
    "forms": {
        "dev": "https://forms.dev.larahealth.cloud",
        "preprod": "https://api-preprod.lara.health",
        "prod": "https://api.lara.health",
    },
}


class APIContext:
    def __init__(self, default_host, username, password, dry_run, stage):
        self.default_host = default_host
        self.username = username
        self.password = password
        self.dry_run = dry_run
        self.stage = stage

        self.token = self.authenticate()
        self.session = APISession(base_url=default_host, token=self.token)

    def authenticate(self):
        response = requests.post(
            f"{self.default_host}/patientservice/api/auth/signinfor2fa",
            json=dict(Username=self.username, Password=self.password),
        )

        response.raise_for_status()

        auth_result = response.json().get("authenticationResult")

        return auth_result.get("idToken")

    def get_session(self, api):
        return APISession(APIS.get(api).get(self.stage), token=self.token)


@click.group()
@click.option(
    "--stage",
    type=click.Choice(["dev", "preprod", "prod"], case_sensitive=False),
    default="prod",
)
@click.option("--dry-run", is_flag=True, default=False)
@click.pass_context
def cli(ctx, stage, dry_run):
    click.secho(f"Using API: {stage}", fg="green")

    env_config_path = CONFIG_PATH + f".{stage}"

    if ctx.invoked_subcommand == "configure":
        return

    if not path.isfile(env_config_path):
        click.secho("Missing configuration file, before using the tool please run: lara configure")
        sys.exit(255)

    settings = {}
    with open(env_config_path, "r") as f:
        settings = json.load(f)

    try:
        ctx.obj = APIContext(
            default_host=APIS.get("default").get(stage),
            username=settings["username"],
            password=settings["password"],
            dry_run=dry_run,
            stage=stage,
        )
        click.secho("Connected to the API", fg="green")

        if ctx.obj.dry_run:
            click.secho("Running in dry-run mode", fg="yellow")

    except (requests.exceptions.HTTPError, json.decoder.JSONDecodeError) as e:
        click.secho("Failed to authenticate", fg="red")
        sys.exit(1)


cli.add_command(clinic.clinic)
cli.add_command(user.user)
cli.add_command(config.configure)
cli.add_command(config.test)
cli.add_command(reports.reports)
cli.add_command(forms.forms)
