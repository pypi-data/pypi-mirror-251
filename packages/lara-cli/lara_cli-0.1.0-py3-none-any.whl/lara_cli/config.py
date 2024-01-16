import json
from os import path

import click

CONFIG_PATH = path.join(path.expanduser("~"), ".lara")


@click.command()
@click.pass_context
def configure(ctx):
    """Configure credentials"""
    prompts = {
        "username": dict(desc="User name (email)", type=str),
        "password": dict(
            desc="Password",
            type=str,
            hide_input=True,
        ),
    }

    settings = {}
    for field, prompt in prompts.items():
        settings[field] = click.prompt(
            click.style(prompt.pop("desc"), fg="blue"),
            show_default=False,
            **prompt,
        ).strip()

    env_config_file = CONFIG_PATH + "." + ctx.parent.params.get("stage")
    with open(env_config_file, "w+") as config_file:
        json.dump(settings, config_file)

    click.secho("Settings saved", fg="green")


@click.command()
def test():
    """Test credentials"""
    pass
