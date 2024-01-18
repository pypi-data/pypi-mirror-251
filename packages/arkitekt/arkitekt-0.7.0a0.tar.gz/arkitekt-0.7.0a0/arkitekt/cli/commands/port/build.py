import rich_click as click
from arkitekt.cli.vars import get_console, get_manifest
import os
from rich.panel import Panel
import subprocess
import uuid
from arkitekt.cli.io import generate_build
from click import Context
from arkitekt.cli.types import Flavour, Manifest
import yaml
from typing import List, Dict, Optional

from arkitekt.utils import create_arkitekt_folder


def build_flavour(flavour_name: str, flavour: Flavour) -> str:
    """Builds the flavour to docker

    Parameters
    ----------
    flavour : Flavour
        The flavour to build
    manifest : Manifest
        The manifest of the app

    Returns
    -------

    tag: str
        The tag of the built docker container

    """

    build_id = str(uuid.uuid4())

    relative_dir = ".arkitekt/flavours/{}/".format(flavour_name)

    command = flavour.generate_build_command(build_id, relative_dir)

    docker_run = subprocess.run(" ".join(command), shell=True)

    if docker_run.returncode != 0:
        raise click.ClickException("Could not build docker container")

    return build_id


def get_flavours(ctx: Context, select: Optional[str] = None) -> Dict[str, Flavour]:
    """Gets the flavours for this app"""

    arkitekt_folder = create_arkitekt_folder()

    flavours_folder = os.path.join(arkitekt_folder, "flavours")

    if not os.path.exists(flavours_folder):
        raise click.ClickException(
            f"We could not find the flavours folder. Please run `arkitekt port init` first to create a buildable flavour"
        )

    flavours = {}

    for dir_name in os.listdir(flavours_folder):
        dir = os.path.join(flavours_folder, dir_name)
        if os.path.isdir(dir):
            if select is not None and select != dir_name:
                continue

            if os.path.exists(os.path.join(dir, "config.yaml")):
                with open(os.path.join(dir, "config.yaml")) as f:
                    valued = yaml.load(f, Loader=yaml.SafeLoader)
                try:
                    flavour = Flavour(**valued)
                    flavour.check_relative_paths(dir)
                    flavours[dir_name] = flavour

                except Exception as e:
                    get_console(ctx).print_exception()
                    raise click.ClickException(
                        f"Could not load flavour {dir_name} from {dir} ` config.yaml ` is invalid"
                    ) from e

    return flavours


@click.command()
@click.option(
    "--flavour",
    "-f",
    help="The flavour to build. By default all flavours are being built",
    default=None,
    required=False,
)
@click.pass_context
def build(ctx: Context, flavour: str) -> None:
    """Builds the arkitekt app to docker"""

    manifest = get_manifest(ctx)
    console = get_console(ctx)

    flavours = get_flavours(ctx, select=flavour)

    md = Panel(
        "Starting to Build Containers for App [bold]{}[/bold]".format(
            manifest.identifier
        ),
        subtitle="Selected Flavours: {}".format(", ".join(flavours.keys())),
    )
    console.print(md)

    build_run = str(uuid.uuid4())

    for key, flavour in flavours.items():
        md = Panel(
            "Building Flavour [bold]{}[/bold]".format(key),
            subtitle="This may take a while...",
            subtitle_align="right",
        )
        console.print(md)

        build_tag = build_flavour(key, flavour)

        generate_build(build_run, build_tag, key, flavour, manifest)

        md = Panel(
            "Built Flavour [bold]{}[/bold]".format(key),
            subtitle="Build ID: {}".format(build_run),
            subtitle_align="right",
        )

        console.print(md)
