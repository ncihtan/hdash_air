"""Command Line Interface (CLI) to HDash Tools."""
import emoji
import click

from hdash.reader.atlas_reader import AtlasReader
from hdash.db.db_util import DbConnection
from hdash.util.slack import Slack

# These imports look like they are not used, but they are required to
# register the ORM classes with SQLAlchemy.
from hdash.db.atlas import Atlas
from hdash.db.atlas_file import AtlasFile
from hdash.db.atlas_stats import AtlasStats
from hdash.db.meta_cache import MetaCache
from hdash.db.path_stats import PathStats
from hdash.db.validation import Validation, ValidationError
from hdash.db.matrix import Matrix
from hdash.db.web_cache import WebCache
from hdash.db.longitudinal import Longitudinal

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
    """Reset the database (use with caution)."""
    db_connection = DbConnection()
    output_header("Resetting database.")
    db_connection.reset_database()
    output_header(emoji.emojize("Done :beer_mug:"))


@cli.command()
def slack():
    """Send a mock message to Slack."""
    slack = Slack()
    print(f"Sending slack message to web hook:  {slack.web_hook_url}.")
    r = slack.post_msg(True, "This is a mock message from the hdash command line tool.")
    print(r)

def output_header(msg):
    """Output header with emphasis."""
    click.echo(click.style(msg, fg="green"))


def output_message(msg):
    """Output message to console."""
    click.echo(msg)


if __name__ == "__main__":
    cli()
