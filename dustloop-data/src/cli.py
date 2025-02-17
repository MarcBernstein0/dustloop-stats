from enum import Enum
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Dict
from sqlalchemy import text
from sqlmodel import Session
from typing_extensions import Annotated
import typer
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn, MofNCompleteColumn
from rich.console import Console
from rich import print
from .db import db

from .dustloop_api.dustloop_api import clean_data, get_fields, get_moves

app = typer.Typer(no_args_is_help=True)
console = Console()


class GAMES(str, Enum):
    ggst = "GGST"
    gbvsr = "GBVSR"
    bbcf = "BBCF"

# Database setup commands
    
@app.command("init-db")
def init_db() -> None:
    """Initialize postgres db"""
    print(f"[green]Initializing Alembic environment[/green]")
    subprocess.run(["alembic", "init", "migrations"], check=True)
    print(f"[green]Initialized Alembic environment[/green]")

@app.command("revise-db")
def db_revision(message: str):
    """Create a new database migration revision."""
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message], check=True)
    print(f"[green]Created new migration revision[/green]")

@app.command("upgrade-db")
def db_upgrade(revision: str = "head"):
    """Upgrade database to a specific revision."""
    subprocess.run(["alembic", "upgrade", revision], check=True)
    print(f"[green]Upgraded database to revision: {revision}[/green]")
    
@app.command("downgrade-db")
def db_downgrade(revision: str = "-1"):
    """Downgrade database to a specific revision."""
    subprocess.run(["alembic", "downgrade", revision], check=True)
    print(f"[green]Downgraded database to revision: {revision}[/green]")

# Getting dustloop data and filling database

@app.command("get-data")
def get_dustloop_data(
    game:  Annotated[GAMES, typer.Argument(help="Game to get data for", case_sensitive=False)] = GAMES.ggst,
    output_dir: Annotated[str, typer.Option(help="Directory to store downloaded API data")] = "output/api/",
    batch_size: Annotated[int, typer.Option(help="Number of records to fetch per request")] = 500
) -> None:
    """Download frame data from Dustloop's API."""
    table_name = f"MoveData_{game.value}"
    print(table_name)

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
    
    print(f"[green]Finished getting dustloop api data for game {game.value}[/green]")
    

@app.command("upload-data")
def upload_dustloop_data_to_database(
    game:  Annotated[GAMES, typer.Argument(help="Game to get data for", case_sensitive=False)] = GAMES.ggst,
    input_dir: Annotated[str, typer.Option(help="Directory to store downloaded API data")] = "output/api/",
    turncate: Annotated[bool, typer.Option(help="Whether to turncate existing data before importing")] = True
) -> None:
    """Upload frame data to Database"""
    json_path = Path(f"{input_dir}/MoveData_{game.value}_clean.json")
    if not json_path.exists():
        print(f"[red]Error: File {json_path} does not exist[/red]", file=sys.stderr)
        raise typer.Exit(1)
    
    f = open(json_path)
    dustloop_data: Dict[str, Any] = json.load(f)
    f.close()
    database: db = db()
    
    # Init db
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(description="Initializing database...", total=None)
        database.init_db()
        progress.update(task, description="Database initialized", total=None)

        if turncate:
            with Session(database.get_engine()) as session:
                try:
                    # Disable foreign key checks temporarily if using PostgreSQL
                    session.execute(text("SET CONSTRAINTS ALL DEFERRED"))
                            
                    # Truncate all tables in the correct order
                    session.execute(text("TRUNCATE TABLE normal_moves CASCADE"))
                    session.execute(text("TRUNCATE TABLE special_moves CASCADE"))
                    session.execute(text("TRUNCATE TABLE overdrive_moves CASCADE"))
                    session.execute(text("TRUNCATE TABLE system_core_data CASCADE"))
                    session.execute(text("TRUNCATE TABLE system_jump_data CASCADE"))
                    session.execute(text("TRUNCATE TABLE gatling_tables CASCADE"))
                    session.execute(text("TRUNCATE TABLE character_specific_tables CASCADE"))
                    session.execute(text("TRUNCATE TABLE characters CASCADE"))
                            
                    session.commit()
                    progress.update(task, description="Tables truncated")
                except Exception as e:
                    session.rollback()
                    print(f"[red]Error:[/] Failed to truncate tables: {str(e)}")
                    raise typer.Exit(1)
    
    
    # Truncate all tables if requested
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        # Import data
        task = progress.add_task(description="Importing move data...", total=len(dustloop_data))

if __name__ == "__main__":
    app()
