import click

from rich.console import Console
from rich.table import Table


@click.group
def forms():
    """Interact with forms"""
    pass


@forms.command()
@click.option("--user", required=True, help="User id (externalId)")
@click.option("--form", required=True, help="Name of the form")
@click.option("--phone", required=True, help="Name of the form")
@click.pass_obj
@click.pass_context
def send(ctx, obj, user, form, phone):
    """Send text message about form to given user"""
    session = obj.get_session("forms")
    response = session.post("/internal/send", json={"user": user, "form": form, "phone_number": phone})

    click.secho("Message sent")


@forms.command()
@click.option("--user", required=True, help="User id (externalId)")
@click.pass_obj
@click.pass_context
def data(ctx, obj, user):
    session = obj.get_session("forms")
    data = session.get(f"/internal/data/{user}").json()

    if "message" in data:
        click.secho(data["message"], fg="red")
        return

    if len(data) == 0:
        click.secho("No data", fg="yellow")
        return

    names = data[0].keys()

    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    for name in names:
        table.add_column(name)

    for row in data:
        table.add_row(*map(str, row.values()))

    console.print(table)
