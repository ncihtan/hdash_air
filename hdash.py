"""Command Line Interface (CLI) for HTAN Dashboard."""
from hdash.graph.graph_flattener import GraphFlattener
import logging
import emoji
import click
import boto3
from hdash.reader.atlas_reader import AtlasReader
from hdash.db.db_util import DbConnection
from hdash.util.s3_credentials import S3Credentials
from hdash.util.slack import Slack

# These imports look like they are not used, but they are required to
# register the ORM classes with SQLAlchemy.
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
def web():
    """Download website from the database to deploy directory."""
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


@cli.command()
def deploy():
    """Deploy website from database to S3 bucket."""
    db_connection = DbConnection()
    session = db_connection.session
    s3_credentials = S3Credentials()
    s3_config = s3_credentials.get_s3_config()
    client = boto3.client("s3", **s3_config)
    output_header(
        f"Deploying to:  {s3_credentials.endpoint_url}/{s3_credentials.bucket_name}."
    )
    web_list = session.query(WebCache).all()
    if len(web_list) > 0:
        for web_cache in web_list:
            output_message(f"Writing:  {web_cache.file_name}.")
            client.put_object(
                Bucket=s3_credentials.bucket_name,
                Key=web_cache.file_name,
                Body=web_cache.content,
                ACL='public-read',
                ContentType='text/html'
            )
        output_header(emoji.emojize("Done :beer_mug:"))
    else:
        output_header(emoji.emojize(":warning:  No web cache files found."))

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
