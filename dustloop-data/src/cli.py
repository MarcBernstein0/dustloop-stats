from enum import Enum
from pathlib import Path
from typing_extensions import Annotated
import typer
from rich.console import Console
from rich import print
from typing import Final, Optional

app = typer.Typer(no_args_is_help=True)
console = Console()

class Action(Enum):
    FIELDS = "cargofields"
    QUERY = "cargoquery"

DUSTLOOP_URL: Final[str] = "https://www.dustloop.com/wiki/api.php"

def build_url(
        action: Action, 
        tables:str, 
        fields: Optional[str] = None, 
        limit: Optional[int] = None, 
        offset: Optional[int] = None
) -> str:
    
    if action == Action.QUERY:
    tables_param = f"&tables={tables}&fields={fields}" if fields is not None else f"&table={tables}"
    limit_param = f"&limit={limit}" if limit is not None else ""
    offset_param = f"&offset={offset}" if offset is not None else ""

    res_url = (
        f"{DUSTLOOP_URL}"
        f"?action={action}"
        f"{tables_param}"
        f"{limit_param}"
        f"{offset_param}"
        f"&format=json"
    )
    return res_url


@app.command("get-data")
def get_dustloop_data(
    output_dir: Annotated[str, typer.Argument(help="Directory to store downloaded API data")] = "output/api/intermediate",
    batch_size: Annotated[int, typer.Argument(help="Number of records to fetch per request")] = 500
) -> None:
    """Download frame data from Dustloop's API."""
    
    try:
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)

        fields_url = build_url(Action.FIELDS, "MoveData_GBVSR")
        print(f"[green]fields_url: {fields_url}[/green]")
    except Exception as e:
        print(f"[red]Error downloading API data: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command("upload-data")
def upload_dustloop_data_to_database():
    raise NotImplementedError

if __name__ == "__main__":
    app()
