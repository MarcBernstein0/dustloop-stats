import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def hello():
    print("Hello from dustloop-data!")

@app.command()
def goodbye():
    print("Goodbye")

if __name__ == "__main__":
    app()
