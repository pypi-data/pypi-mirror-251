from pathlib import Path
from typing import Annotated

import typer
from poppler import load_from_file
from rich.console import Console

app = typer.Typer()

console = Console()

err_console = Console(stderr=True)


@app.command(help="Prefixes PDF filenames with their creation date.")
def datetag_pdf(
        *,
        paths: Annotated[list[Path], typer.Argument(
            help="Path to a PDF file.",
        )],
        verbose: Annotated[bool, typer.Option(
            "-v", "--verbose",
            help="Enable verbose mode.",
        )] = False,
        dry_run: Annotated[bool, typer.Option(
            "-d", "--dry-run",
            help="Perform a dry run without actually renaming files.",
        )] = False,
):
    for path in paths:
        pdf_document = load_from_file(path)
        if pdf_document.creation_date is not None:
            prefix = pdf_document.creation_date.strftime('%Y-%m-%d ')

            if not path.name.startswith(prefix):
                new_path = path.with_name(prefix + path.name)

                if not new_path.exists():
                    if verbose:
                        console.print(f"Renamed [b magenta]{path}[/b magenta] to [b yellow]{new_path}[/b yellow].")

                    if not dry_run:
                        path.rename(new_path)
                else:
                    err_console.print(
                        f"Error: Cannot rename [b magenta]{path}[/b magenta] to [b yellow]{new_path}[/b yellow] "
                        f"as the target path already exists.",
                    )
            elif verbose:
                err_console.print(f"Error: [b yellow]{path.name}[/b yellow] already starts with the correct date.")
        else:
            err_console.print(f"Error: Unable to get creation date for [b magenta]{path}[/b magenta].")
