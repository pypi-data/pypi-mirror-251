from typing import Annotated, Generator

from airfold_common.format import ChFormat, Format
from airfold_common.plan import print_plan
from airfold_common.project import ProjectFile
from cachetools import TTLCache, cached
from typer import Argument, Context

from airfold_cli import app
from airfold_cli.api import AirfoldApi
from airfold_cli.cli import AirfoldTyper
from airfold_cli.models import Config
from airfold_cli.options import DryRunOption, ForceOption, with_global_options
from airfold_cli.root import catch_airfold_error
from airfold_cli.utils import load_config

source_app = AirfoldTyper(
    name="source",
    help="Source commands.",
)

app.add_typer(source_app)


@cached(cache=TTLCache(maxsize=10000, ttl=5))
def get_source_names() -> list[str]:
    config: Config = load_config()
    api = AirfoldApi(config.key, config.endpoint)
    files = api.project_pull()
    formatter: Format = ChFormat()
    sources: list[ProjectFile] = list(filter(lambda f: formatter.is_source(f.data), files))
    return [source.name for source in sources]


def source_name_completion(cur: str) -> Generator[str, None, None]:
    """Pipe name completion."""
    try:
        source_names: list[str] = get_source_names()
        yield from filter(lambda name: name.startswith(cur), source_names) if cur else source_names
    except Exception as e:
        pass


@source_app.command("delete")
@catch_airfold_error()
@with_global_options
def delete(
    ctx: Context,
    name: Annotated[str, Argument(help="Source name", autocompletion=source_name_completion)],
    dry_run: Annotated[bool, DryRunOption] = False,
    force: Annotated[bool, ForceOption] = False,
) -> None:
    """Delete source.
    \f

    Args:
        ctx: Typer context
        name: source name
        dry_run: show plan without executing it
        force: force delete/overwrite even if data will be lost

    """
    source_app.apply_options(ctx)

    config: Config = load_config()
    api = AirfoldApi(config.key, config.endpoint)
    commands = api.project_source_delete(name=name, dry_run=dry_run, force=force)
    print_plan(commands, console=source_app.console)


@source_app.command("ls")
@catch_airfold_error()
@with_global_options
def ls(ctx: Context) -> None:
    """List sources.
    \f

    Args:
        ctx: Typer context

    """
    source_app.apply_options(ctx)

    config: Config = load_config()
    api = AirfoldApi(config.key, config.endpoint)

    files = api.project_pull()

    formatter: Format = ChFormat()

    sources: list[ProjectFile] = list(filter(lambda f: formatter.is_source(f.data), files))
    if not sources:
        source_app.console.print("\t[magenta]NO SOURCES[/magenta]")
        return

    for source in sources:
        source_app.console.print(source.name, style="general")


# @source_app.command("rename")
@catch_airfold_error()
@with_global_options
def rename(
    ctx: Context,
    name: Annotated[str, Argument(help="Source name", autocompletion=source_name_completion)],
    new_name: Annotated[str, Argument(help="New source name")],
    dry_run: Annotated[bool, DryRunOption] = False,
    force: Annotated[bool, ForceOption] = False,
) -> None:
    """Rename source.
    \f

    Args:
        ctx: Typer context
        name: source name
        new_name: new source name
        dry_run: show plan without executing it
        force: force delete/overwrite even if data will be lost

    """
    source_app.apply_options(ctx)

    config: Config = load_config()
    api = AirfoldApi(config.key, config.endpoint)
    commands = api.rename_source(name=name, new_name=new_name, dry_run=dry_run, force=force)
    print_plan(commands, console=source_app.console)
