"""Command Line Interface (CLI) for HTAN Dashboard."""
from hdash.graph.graph_flattener import GraphFlattener
import logging
import emoji
import click
from hdash.reader.atlas_reader import AtlasReader
from hdash.db.db_util import DbConnection
from hdash.db.atlas_file import AtlasFile
from hdash.db.atlas_stats import AtlasStats
from hdash.db.meta_cache import MetaCache
from hdash.db.validation import Validation, ValidationError
from hdash.db.web_cache import WebCache

@click.group()
def cli():
    pass

@cli.command()
def init():
    """Initialize the database with atlases."""
    db_connection = DbConnection()
    session = db_connection.session
    reader = AtlasReader("config/htan_projects.csv")
    atlas_list = reader.atlas_list
    output_header(f"Saving {len(atlas_list)} atlases to the database.")
    for atlas in atlas_list:
        session.add(atlas)
    session.commit()
    output_header(emoji.emojize("Done :beer_mug:"))


@cli.command()
def reset():
    """Reset the database."""
    db_connection = DbConnection()
    output_header("Resetting database.")
    db_connection.reset_database()
    output_header(emoji.emojize("Done :beer_mug:"))

@cli.command()
def web():
    """Create Website from Database."""
    db_connection = DbConnection()
    session = db_connection.session
    output_header("Creating web site.")
    web_list = session.query(WebCache).all()
    if len(web_list) > 0:
        for web_cache in web_list:
            path = f"deploy/{web_cache.file_name}"
            output_message(f"Writing:  {path}.")
            with open(path, "w") as fd:
                fd.write(web_cache.content)
        output_header(emoji.emojize("Done :beer_mug:"))
    else:
        output_header(emoji.emojize(":warning:  No web cache files found."))

def output_header(msg):
    """Output header with emphasis."""
    click.echo(click.style(msg, fg="green"))


def output_message(msg):
    """Output message to console."""
    click.echo(msg)


if __name__ == '__main__':
    cli()