import typer
from rich import print
from rich.console import Console
from pathlib import Path
import os
import json
import shutil
from datetime import datetime
import core.parse as parse
import core.utils as utils

CONFIG_PATH = Path.home() / ".planc" / "config.json"

def run_setup():
    """
    Run the setup process to create a config file.
    Returns:
        str: A message indicating the result of the setup process.
    """
    print("[bold red] Running setup...[/]")

    if not utils.config_exists():
        utils.reset_config_folder()
        print(f"[bold green]Config file created at {utils.CONFIG_PATH}.[/]")
    else:
        print(f"[bold red]Config file already exists at {utils.CONFIG_PATH}.[/], want to re-initialize? (y/n)")
        if input().lower() == 'y':
            utils.reset_config_folder()
            print(f"[bold green]Config file re-initialized at {utils.CONFIG_PATH}.[/]")
        else: 
            print("[bold red]Exiting setup...[/]")
            return
        
    print("[bold green]Setup complete!\n------------------------------\nTo proceed, enter your Google Gemini API key: [/]")

    ## API key storage
    api_key = input()
    if not api_key:
        print("[bold red]No API key provided. Exiting setup...[/]")
        return
    utils.update_config_field("gemini_api_key", api_key)
    print("[bold yellow]Note: This key will be stored in the config file.[/]")

    ## Resume file parsing and storage
    resume_path = input("Please provide the absolute path to your resume file ( .pdf or .docx): ").strip()
    data = ""
    try:
        if not os.path.exists(resume_path):
            raise FileNotFoundError(f"[bold red]File not found at {resume_path}, perhaps you provided a relative path?[/]")
        if not resume_path.endswith(('.pdf', '.docx')):
            raise ValueError("[bold red]Invalid file type. Please provide a .pdf or .docx file.[/]")
        
        if resume_path.endswith('.pdf'):
            data = parse.read_pdf_file(resume_path)
            if not data:
                raise ValueError("[bold red]No text found in the PDF file.[/]")
            ## implement llm call to save structured data to file
        elif resume_path.endswith('.docx'):
            data = parse.read_docx_file(resume_path)
            if not data:
                raise ValueError("[bold red]No text found in the DOCX file.[/]")
            ## implement llm call to save structured data to file

        ## Save structured data, add to config
        utils.update_config_field("resume_file", resume_path)
        utils.update_config_field("timestamp", datetime.now().isoformat())
        utils.get_resume_text_path().write_text(data)
        print(f"[bold green]Resume data saved at {CONFIG_PATH.parent / 'resume_raw.txt'}.[/]")

    except Exception as e:
        print(f"[bold red] Error during setup: {e}\nPlease try again.[/]")

    



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