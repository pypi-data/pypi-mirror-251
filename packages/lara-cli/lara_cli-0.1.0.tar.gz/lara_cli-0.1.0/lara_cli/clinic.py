import sys

import click
import requests.exceptions

from lara_cli.utils import acronym


@click.group()
def clinic():
    """Manage clinics"""
    pass


@clinic.command()
@click.pass_obj
@click.pass_context
def create(ctx, obj):
    clinic_prompt = {
        "name": dict(desc="Clinic name", type=str),
        "addressLine1": dict(desc="Address linie 1", type=str),
        "addressLine2": dict(desc="Address linie 2", type=str, default=""),
        "city": dict(desc="City", type=str),
        "state": dict(desc="State", type=str),
        "zipCode": dict(desc="Zip Code", type=str),
        "phone": dict(desc="Phone", type=str),
    }

    clinic = {
        "eHRVendorId": 1,
    }
    for field, definition in clinic_prompt.items():
        clinic[field] = click.prompt(
            click.style(definition.pop("desc"), fg="blue"),
            show_default=False,
            **definition,
        )

    code = acronym(clinic.get("name"))

    clinic["code"] = click.prompt(click.style("Unique code", fg="blue"), type=str, default=code)
    response = obj.session.get(f"/clinicservice/api/clinic/{clinic['code']}")

    if not obj.dry_run:
        try:
            response = obj.session.post(f"/clinicservice/api/clinic", json=clinic)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            click.secho(f"Failed to create clinic: {e}", fg="red")
            click.secho(e.response.json(), fg="red")
            sys.exit(2)

    click.secho(f"Clinic created: {clinic.get('code')}\n", fg="green")

    if click.confirm(click.style("Would you like to setup SMS phone number?", fg="blue")):
        ctx.invoke(set_phone_number, clinic=clinic.get("code"))

    if not click.confirm(click.style("Would you like to create admin account?", fg="blue")):
        return

    from .user import create as create_user

    ctx.invoke(create_user, clinic=clinic.get("code"))


@clinic.command()
@click.pass_obj
@click.pass_context
@click.argument("clinic")
def set_phone_number(ctx, obj, clinic):
    sms_phone = click.prompt(click.style("SMS Phone number", fg="blue"))

    try:
        response = obj.session.put(f"/internal/clinic/{clinic}/set_phone_number", json=dict(number=sms_phone))
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        click.secho(f"Failed to update clinic: {e}", fg="red")
        click.secho(e.response.json(), fg="red")
        sys.exit(2)
