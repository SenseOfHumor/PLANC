import typer
from rich import print
from rich.console import Console
from pathlib import Path
import os
import json
import shutil

CONFIG_PATH = Path.home() / ".planc" / "config.json"

def run_setup():
    """
    Run the setup process to create a config file.
    Returns:
        str: A message indicating the result of the setup process.
    """
    print("[bold red] Running setup...[/]")

    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text("{}")  ## placeholder json content
        print(f"[bold green]Config file created at {CONFIG_PATH}.[/]")
    else:
        print(f"[bold red]Config file already exists at {CONFIG_PATH}.[/], want to re-initialize? (y/n)")
        if input().lower() == 'y':
            shutil.rmtree(CONFIG_PATH.parent)
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            CONFIG_PATH.write_text("{}")
            print(f"[bold green]Config file re-initialized at {CONFIG_PATH}.[/]")
        else: 
            print( "[bold red]Exiting setup...[/]")
            return 
    print("[bold green]Setup complete![/]")
    print("[bold green]------------------------------[/]")
    print("[bold green]To proceed, enter yout Google Gemini API key: [/]")
    api_key = input()
    if not api_key:
        print("[bold red]No API key provided. Exiting setup...[/]")
        return
    config_data = {
        "gemini_api_key": api_key,
    }
    CONFIG_PATH.write_text(json.dumps(config_data, indent=2))
    



app = typer.Typer()

@app.command()
def planc(
    setup: bool = typer.Option(False, "--setup", help="Run initial setup"),
):
    if setup:
        run_setup()
        return
    
    print("[bold yellow]No option provided. Use --help to know more.[/bold yellow]")


if __name__ == "__main__":
    app()