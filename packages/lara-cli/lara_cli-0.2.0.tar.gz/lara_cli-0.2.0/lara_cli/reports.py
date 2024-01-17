import csv
import sys

import requests
import arrow
import click
from subprocess import Popen
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from pick import pick


def get_reports(api):
    return api.session.get("/internal/reports").json()


def display_report(names, data):
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    for name in names:
        table.add_column(name)

    for row in data:
        table.add_row(*map(str, row.values()))

    console.print(table)


def get_report(api, report):
    data = api.session.post(f"/internal/report/{report}").json()

    if "message" in data:
        click.secho(data["message"], fg="red")
        sys.exit(1)

    data = requests.get(data.get("file")).json()

    return data[0].keys(), data


def write_report(names, data, output):
    with open(output, "w+", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=names)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

    click.secho(f"File created: {output}")
    Popen(f"open {output}", shell=True)


@click.group(invoke_without_command=True)
@click.pass_obj
def reports(api):
    """Interact with reporting service"""

    options = get_reports(api)

    report, _ = pick(options, "Pick available report")
    output, _ = pick(["display", "csv"], "Output method")

    names, data = get_report(api, report)

    if output == "csv":
        output_file = f"{report}-{arrow.now().isoformat()}.csv"
        write_report(names, data, output_file)
    else:
        display_report(names, data)


@reports.command()
@click.pass_obj
def list(api):
    reports = get_reports(api)

    output = "**Available reports**\n"
    output += "\n".join(["- " + i for i in reports])

    console = Console()
    markdown = Markdown(output)
    console.print(markdown)


@reports.command()
@click.pass_obj
@click.argument("report")
@click.option("--output")
def get(api, output, report):
    names, data = get_report(api, report)

    if output:
        write_report(names, data, output)
    else:
        display_report(names, data)
