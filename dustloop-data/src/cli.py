from pathlib import Path
from typing_extensions import Annotated
import typer
from rich.console import Console
from rich import print
from typing import Final
import requests

from src.exceptions import CliException
from src.action import Action

app = typer.Typer(no_args_is_help=True)
console = Console()

DUSTLOOP_URL: Final[str] = "https://www.dustloop.com/wiki/api.php"

def build_url(
        action: Action, 
        tables:str, 
        fields:str = "", 
        limit:int = 100, 
        offset:int = 0
) -> str:
    """Build the dustloop API url based on the action and param data."""
    ret_url: str
    if action == Action.FIELDS:
        ret_url = (
            f"{DUSTLOOP_URL}"
            f"?action={action.value}"
            f"&table={tables}"
            f"&format=json"
        )
    else:
        ret_url = (
            f"{DUSTLOOP_URL}"
            f"?action={action.value}"
            f"&tables={tables}&fields={fields}&limit={limit}&offset={offset}"
            f"&format=json"
        )
    
    return ret_url


@app.command("get-data")
def get_dustloop_data(
    output_dir: Annotated[str, typer.Argument(help="Directory to store downloaded API data")] = "output/api/intermediate",
    batch_size: Annotated[int, typer.Argument(help="Number of records to fetch per request")] = 500
) -> None:
    """Download frame data from Dustloop's API."""
    
    fields: str

    # Get list of fields
    try:
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)

        fields_url = build_url(Action.FIELDS, "MoveData_GBVSR")
        print(f"[green]Downloading API field definitions from {fields_url} ...[/green]")

        fields_response = requests.get(fields_url)
        fields_response.raise_for_status()
        fields_data = fields_response.json()
        if "error" in fields_data:
            raise CliException("Successful response back, but got an error", fields_url, fields_response.json()["error"]["info"])

        print(fields_response.json())
        fields = ",".join(fields_data['cargofields'].keys())
    except requests.exceptions.RequestException as e:
        print(f"[red]Exception occurred when calling API:\n{str(e)}[/red]")
    except CliException as e:
        print(f"[red]Exception when calling the api: {str(e)}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        print(f"[red]Exception downloading API data: {str(e)}[/red]")
        raise typer.Exit(1)
    
    print(fields)

    # Get move info

@app.command("upload-data")
def upload_dustloop_data_to_database():
    raise NotImplementedError

if __name__ == "__main__":
    app()
