from rich.markdown import Markdown
from rich.console import Console
from rich.rule import Rule
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from bullet import Bullet, colors
from portainerlang.query.query import process_query

def entrypoint():
    """
    Initiates an interactive session for processing user queries related to the Portainer API. This function provides
    a console-based interface for users to enter queries, view the history of their queries, and receive generated
    responses. The user can choose to revise their query, start a new query, or exit the session.

    The function employs a while loop to continuously accept user input. It uses the `PromptSession` from the
    prompt_toolkit for user input, and the `Console` from rich for output display. Each query is added to a history
    list, and the `process_query` function is called to process the entire history of queries.

    Query prompts change style based on the number of queries entered. The first query is prompted with a green bold 
    style, and subsequent revisions are prompted with a yellow bold style. The function also displays the list of
    all queries entered in the session along with the results from the latest query.

    After displaying results, the user is presented with a bullet point selection menu to choose whether to revise
    the current query, start a new query, or exit the application. The session maintains the state of queries and
    query numbers across different interactions.

    The function gracefully handles KeyboardInterrupt exceptions to allow users to exit the session using keyboard
    interrupts.

    :return: None. The function is designed to run indefinitely until the user decides to exit.
    """
    console = Console()
    session = PromptSession()
    query_number = 1
    query_history = []

    try:
        while True:
            # Waiting for user input
            query_prompt_style = Style.from_dict({
                'prompt': 'ansiyellow bold' if query_number > 1 else 'ansigreen bold',
                'input': 'ansiwhite italic',
            })
            query_prompt = "Enter your revision: " if query_number > 1 else "Enter your query: "
            query = session.prompt(query_prompt, style=query_prompt_style)
            query_history.append(query)

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
                transient=False,
            ) as progress:
                task = progress.add_task("[cyan]Hold on, asking the model...", total=None)
                output = process_query(query_history)
                progress.update(task, total=1, completed=1)

            # Displaying the queries
            console.print()
            console.print(Rule("Query"))
            console.print("\n".join(f"{i+1}) {q}" for i, q in enumerate(query_history)))

            # Displaying the result
            console.print(Rule("Results"))
            console.print(Markdown(output))

            # Radiolist prompt for user options
            console.print()
            cli = Bullet(
                    choices = ["Revise this query", "New query", "Exit"], 
                    margin = 2,
                    bullet = " >",
                    bullet_color=colors.bright(colors.foreground["cyan"]),
                    word_color=colors.bright(colors.foreground["blue"]),
                    word_on_switch=colors.bright(colors.foreground["cyan"]),
                    background_color=colors.background["black"],
                    background_on_switch=colors.background["black"],
                    pad_right = 5
                )

            result = cli.launch()
            console.print()

            if result == "Revise this query":
                query_number += 1
                continue
            elif result == "New query":
                query_history = []
                query_number = 1
                continue
            elif result == "Exit":
                exit(0)
    except KeyboardInterrupt:
        exit(0)
