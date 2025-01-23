import json
from pathlib import Path
import time
from typing_extensions import Annotated
import typer
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn, MofNCompleteColumn
from rich.console import Console
from rich import print

from .dustloop_api.dustloop_api import clean_data, get_fields, get_moves

app = typer.Typer(no_args_is_help=True)
console = Console()

@app.command("get-data")
def get_dustloop_data(
    output_dir: Annotated[str, typer.Argument(help="Directory to store downloaded API data")] = "output/api/",
    batch_size: Annotated[int, typer.Argument(help="Number of records to fetch per request")] = 500
) -> None:
    """Download frame data from Dustloop's API."""
    table_name = "MoveData_GBVSR"

    # Create output directories if none exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    intermediate_output = output_path / "intermediate"
    intermediate_output.mkdir(parents=True, exist_ok=True)

    character_info_output = output_path / "character_info"
    character_info_output.mkdir(parents=True, exist_ok=True)


    fields = get_fields(table_name, intermediate_output)
    all_moves = get_moves(table_name, fields, batch_size, output_path/"intermediate")

    # clean data
    len(all_moves)
    cleaned_data = clean_data(all_moves, output_path)
    
    # save data to files
    try:
        cleaned_moves_data_file = output_path / f"{table_name}_clean.json"
        with open(cleaned_moves_data_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, indent=2)
        print(f"[blue]Saved cleaned move info to {cleaned_moves_data_file}[/blue]")


        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("•"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(description="Creating character files...", total=len(cleaned_data))

            for k, v in cleaned_data.items():
                character_file = character_info_output / f"{k}.json"
                with open(character_file, 'w', encoding='utf-8') as f:
                    json.dump(v, f, indent=2)
                
                progress.update(task, advance=1)
                time.sleep(0.2)




    except Exception as e:
        print(e)
        raise typer.Exit(1)
    
    

    

@app.command("upload-data")
def upload_dustloop_data_to_database():
    """Upload frame data to Database"""
    raise NotImplementedError

if __name__ == "__main__":
    app()
