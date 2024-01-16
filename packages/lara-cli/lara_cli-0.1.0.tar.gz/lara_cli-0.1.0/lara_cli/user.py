import sys

import click
import requests.exceptions


@click.group()
def user():
    """Manage users"""
    pass


@user.command()
@click.argument("clinic")
@click.pass_obj
def create(obj, clinic):
    user_prompt = {
        "firstName": dict(desc="First name", type=str),
        "lastName": dict(desc="Last name", type=str),
        "email": dict(desc="Email", type=str),
        "phoneNo": dict(desc="Phone number", type=str),
    }

    user = {"jobtitleId": 5, "roleId": 3}
    for field, definition in user_prompt.items():
        user[field] = click.prompt(click.style(definition.get("desc"), fg="blue"), type=definition.get("type"))

    if not obj.dry_run:
        try:
            response = obj.session.post(f"/clinicservice/api/clinic/{clinic}/user", json=user)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            click.secho(f"Failed to create user: {e}", fg="red")
            if response.status_code == 500:
                click.secho(e.response.json().get("Message"), fg="red")

            # print(e.response.text)
            sys.exit(3)

    click.secho("Administrator created", fg="green")
