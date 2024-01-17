import click
from rich.markdown import Markdown
from rich.console import Console
from portainerlang.query.query import process_query

@click.command()
@click.argument('query', nargs=-1)  # nargs set to -1 to accept an unlimited number of arguments
def entrypoint(query):
    """
    Entry point for the CLI command. This function parses the user's query from the command line,
    passes it to the process_query function, and displays the formatted output.

    :param query: A tuple of command line arguments which are combined to form the full query string.
    """
    full_query = ' '.join(query)
    output = process_query(full_query)
    console = Console()
    console.print(Markdown(output))
