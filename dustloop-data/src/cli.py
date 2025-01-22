from pathlib import Path
from typing_extensions import Annotated
import typer
from rich.console import Console
from rich import print

from .dustloop_api.dustloop_api import get_fields, get_moves

app = typer.Typer(no_args_is_help=True)

@app.command("get-data")
def get_dustloop_data(
    output_dir: Annotated[str, typer.Argument(help="Directory to store downloaded API data")] = "output/api/intermediate",
    batch_size: Annotated[int, typer.Argument(help="Number of records to fetch per request")] = 500
) -> None:
    """Download frame data from Dustloop's API."""
    table_name = "MoveData_GBVSR"

    fields = get_fields(table_name, output_dir)
    all_moves = get_moves(table_name, fields, batch_size)

    print(len(all_moves))
    
    
    

    # Get move info
    try:
        offset = 0
        all_moves = []
        # has_more = 
    except Exception as e:
        print(f"[red]Unexpected exception occurred when calling api:")

@app.command("upload-data")
def upload_dustloop_data_to_database():
    raise NotImplementedError

if __name__ == "__main__":
    app()
