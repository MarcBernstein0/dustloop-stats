import json
from pathlib import Path
from typing import Any, Dict, Final, List
import requests
import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console

from .action import Action
from ..exceptions import CliException

DUSTLOOP_URL: Final[str] = "https://www.dustloop.com/wiki/api.php"
console = Console()


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


def get_fields(table_name: str, path: Path) -> str:
    """Get the fields/Schema of a Dustloop table"""
    try:
        fields_url = build_url(Action.FIELDS, table_name)
        print(f"[green]Downloading API field definitions from {fields_url} ...[/green]")

        fields_response = requests.get(fields_url)
        fields_response.raise_for_status()
        fields_data = fields_response.json()
        if "error" in fields_data:
            raise CliException(
                "Successful response back, but got an error", 
                fields_url, 
                fields_data["error"]["info"]
            )

        # Might get rid of this file, who knows
        fields_file = path / f"{table_name}_fields.json"
        with open(fields_file, 'w', encoding='utf-8') as f:
            json.dump(fields_data, f, indent=2)
        
        print(f"[blue]Saved field definitions to {fields_file}[/blue]")

        fields = ",".join(fields_data['cargofields'].keys())
        return fields
    except requests.exceptions.HTTPError as e:
        print(f"[red]Exception occurred when calling API with status code {e.response.status_code}:\n{str(e)}[/red]")
        raise typer.Exit(1)
    except CliException as e:
        print(f"[red]Exception, could not parse fields data:\n{str(e)}[/red]")
        raise typer.Exit(1)
    except json.JSONDecodeError as e:
        print(f"[red]Failed to parse JSON response: {str(e)}[/red]")
        # Save raw responses for inspection
        raw_fields_file = path / "move_data_raw.txt"
        with open(raw_fields_file, 'w', encoding='utf-8') as f:
            f.write(fields_data.text)
        print(f"[yellow]Saved raw responses to {raw_fields_file} for inspection[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        print(f"[red]Exception that was not expected occurred when getting fields:\n{str(e)}[/red]")
        raise typer.Exit(1)

def get_moves(table_name: str, fields: str, batch_size: int, path: Path) -> List[Dict[Any, Any]]:
    """Get the move data from Dustloop API."""
    offset = 0
    all_moves: List[Dict[Any, Any]] = []
    is_done = False

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(description="Downloading move data...", total=None)

            while not is_done:
                move_data_url = build_url(Action.QUERY, table_name, fields, batch_size, offset)
                data_response = requests.get(move_data_url)
                data_response.raise_for_status()

                # parse return data
                move_data = data_response.json()
                if "error" in move_data:
                    raise CliException(
                        "Successful response back, but got an error", 
                        move_data_url, 
                        move_data["error"]["info"]
                    )
                current_batch = move_data['cargoquery']
                all_moves.extend(current_batch)

                # Update progress
                progress.update(task, description=f"Downloaded ({len(all_moves)}) moves so far...")

                # Check if there is more moves to get
                is_done = len(current_batch) < batch_size
                offset += batch_size
        
        final_data = {'cargoquery': all_moves}
        move_data_file = path / f"{table_name}_moves.json"
        with open(move_data_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2)
    
        print(f"[blue]Save {len(all_moves)} moves to {move_data_file}[/blue]")
    except requests.exceptions.HTTPError as e:
        print(f"[red]Exception occurred when calling API with status code {e.response.status_code}:\n{str(e)}[/red]")
        raise typer.Exit(1)
    except CliException as e:
        print(f"[red]Exception, could not parse move data:\n{str(e)}[/red]")
        raise typer.Exit(1)
    except json.JSONDecodeError as e:
        print(f"[red]Failed to parse JSON response: {str(e)}[/red]")
        # Save raw responses for inspection
        raw_data_file = path / "move_data_raw.txt"
        with open(raw_data_file, 'w', encoding='utf-8') as f:
            f.write(data_response.text)
        print(f"[yellow]Saved raw responses to {raw_data_file} for inspection[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        print(f"[red]Unexpected exception occurred when trying to get move data:\n{str(e)}")
        raise typer.Exit(1)


    return all_moves

def clean_data(all_moves: List[Dict[Any, Any]], path: Path) -> Dict[Any, Any]:
    """Take response data from dustloop and clean it up into a more structured data"""
    ret_dict = {}
    exclude_keys = set(["chara"])
    for move in all_moves:
        move_block = move["title"]
        chara_name = move_block["chara"]

        if chara_name not in ret_dict:
            ret_dict[chara_name] = {
                "name": chara_name, 
                "normal": [],
                "special": [],
                "super": [],
            }
        if move_block["type"] == "normal":
            ret_dict[chara_name]["normal"].append({k: move_block[k] for k in move_block if k not in exclude_keys})
        elif move_block["type"] == "special":
            ret_dict[chara_name]["special"].append({k: move_block[k] for k in move_block if k not in exclude_keys})
        elif move_block["type"] == "super":
            ret_dict[chara_name]["super"].append({k: move_block[k] for k in move_block if k not in exclude_keys})

    return ret_dict