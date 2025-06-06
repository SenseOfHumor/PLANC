import typer
import sys
from rich import print
from rich.console import Console
from pathlib import Path
from typing import Optional
import os
import json
import shutil
from datetime import datetime
import core.parse as parse
import core.utils as utils
import core.planc_engine as planc_engine
from contextlib import contextmanager
import time
import asyncio

CONFIG_PATH = Path.home() / ".planc" / "config.json"

@contextmanager
def spinner(message: str = "Thinking...", style: str = "toggle2"):
    """ spinner functions, returns a context manager"""
    console = Console()
    with console.status(f"[bold green]{message}", spinner=style):
        yield


def test_gemini() -> None:
    """ Test the API key """
    with spinner("Testing API key..."):
        test_response = planc_engine.test_gemini()
    if not test_response:
        print("[bold red]Test failed. Please check your API key.[/]")
        return
    print(f"[green]Planc Engine {test_response}[/]")


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
            test_gemini()
            print("[bold red]Exiting setup...[/]")
            return
        
    print("[bold green]Setup complete!\n--------------------------------------------\nTo proceed, enter your Google Gemini API key: [/]")

    ## API key storage
    api_key = input()
    if not api_key:
        print("[bold red]No API key provided. Exiting setup...[/]")
        return
    utils.update_config_field("gemini_api_key", api_key)
    print("[bold yellow]Note: This key will be stored in the config file.[/]")

    ## Resume file parsing and storage
    resume_path = input("Please provide the absolute path to your resume file (.pdf or .docx): ").strip()
    data = ""
    try:
        if not os.path.exists(resume_path):
            raise FileNotFoundError(f"[bold red]File not found at {resume_path}, perhaps you provided a relative path?[/]")
        if not resume_path.endswith(('.pdf', '.docx')):
            raise ValueError("[bold red]Invalid file type. Please provide a .pdf or .docx file.[/]")
        
        if resume_path.endswith('.pdf'):
            with spinner("Reading PDF file..."):
                data = parse.read_pdf_file(resume_path)
            if not data:
                raise ValueError("[bold red]No text found in the PDF file.[/]")

        elif resume_path.endswith('.docx'):
            with spinner("Reading PDF file..."):
                data = parse.read_pdf_file(resume_path)
            if not data:
                raise ValueError("[bold red]No text found in the DOCX file.[/]")

        ## Save structured data, add to config
        utils.update_config_field("resume_file", resume_path)
        utils.update_config_field("timestamp", datetime.now().isoformat())
        utils.get_resume_text_path().write_text(data)
        print(f"[bold green]Resume data saved at {CONFIG_PATH.parent / 'resume_raw.txt'}.[/]")

    except Exception as e:
        print(f"[bold red] Error during setup: {e}\nPlease try again.[/]")

    ## Test the API key
    with spinner("Testing API key..."):
        test_gemini()

    ## TODO: Add option to parse resume before completing setup, they can choose to skip and do it later using --parser command
    print("[bold yellow]Do you want to convert your resume to computer-readable format? You can do it later by using \"--parser\" flag(y/n)[/]")
    if input().lower() == 'y':
        with spinner("Converting resume..."):
            try:
                pass
                ## TODO: Implement the LLM parsing logic
                structured_data = planc_engine.parse_resume(utils.load_resume_text())
                ## TODO: Save the parsed data to a JSON file
                utils.get_resume_json_path().write_text(json.dumps(structured_data, indent=2))
                ## TODO: Add the parsed file path to the config file
                utils.update_config_field("resume_parsed_file", str(utils.get_resume_json_path()))
                ## TODO: Show the user the path to the parsed file
                print(f"[bold green]Resume parsed successfully! Data saved at {utils.get_resume_json_path()}[/]")
            except Exception as e:
                print(f"[bold red]Error during conversion: {e}[/]")
                return
    else:
        print("[bold yellow]Skipping resume conversion.[/]")

    print("[bold green]Setup completed successfully![/]")
    print("[yellow]Use --help to know more about the commands.[/]")


################################################################################################################################
#                                                                                                                              #
#                                                  Helper Functions End                                                        #
#                                                  CLI Application Starts                                                      #
#                                                                                                                              #
################################################################################################################################


app = typer.Typer()

@app.command()
def planc(
    setup: bool = typer.Option(False, "--setup", help="Run initial setup"),
    test: bool = typer.Option(False, "--test", help="Test the API Key"),
    parser: bool = typer.Option(False, "--parser", help="Parse the resume file to structured data"),
    interactive_jd: bool = typer.Option(False, "--jd", help="Paste job description interactively"),
    cover_letter: bool = typer.Option(False, "--c", help="Generate cover letter from resume and job description"),
    tailored_resume: bool = typer.Option(False, "--r", help="Generate tailored resume from resume and job description"),
):
    if setup:
        run_setup()
        return
    
    if test:
        test_gemini()
        return
    
    if parser:
        with spinner("Parsing resume..."):
            try:
                structured_data = planc_engine.parse_resume(utils.load_resume_text())
                utils.get_resume_json_path().write_text(json.dumps(structured_data, indent=2))
                utils.update_config_field("resume_parsed_file", str(utils.get_resume_json_path()))
                print(f"[bold green]Resume parsed successfully! Data saved at {utils.get_resume_json_path()}[/]")
            except Exception as e:
                print(f"[bold red]Error during parsing: {e}[/]")
        return
    
    if interactive_jd:

        typer.echo("📩 Paste the job description below. Press ENTER then CTRL+D (or CTRL+Z on Windows) when done:\n")
        jd = sys.stdin.read()
        with spinner("Parsing job description..."):
            data = planc_engine.parse_job(jd)
        if not data:
            print("[bold red]No data found in the job description.[/]")
            return
        print("[bold green]Job description parsed successfully![/]")
        print(f"[green]Summary of your job: {json.dumps(data.get('summary'), indent=2)}[/]")
        # TODO: Create a file to save the structured job description in case of future use, its a one-time use file, gets overwritten every time with the latest job description
        # use utils.get_structured_job_description_path() to get the path and save the data
        utils.get_structured_job_description_path().write_text(json.dumps(data, indent=2))
        print(f"[bold green]Structured job description saved at {utils.get_structured_job_description_path()}[/]")
        print(json.dumps(data, indent=2))
        # use utils.update_config_field("structured_job_description", str(utils.get_structured_job_description_path())) to update the config file with the path to the structured job description file
        # for reading, use utils.load_structured_job_description to get the structured job description data
        utils.update_config_field("temp_structured_job_description", str(utils.get_structured_job_description_path()))

    if cover_letter:
        job_data = utils.load_structured_job_description()
        resume_data = utils.load_resume_json()
        if not job_data or not resume_data:
            print("[bold red]Job description or resume data is missing. Please run  --parser first.[/]")
            return
        with spinner("Generating cover letter..."):
            try:
                coverletter_data = planc_engine.create_coverletter(job_data, resume_data)
                cover_letter_path = utils.CONFIG_PATH.parent / "cover_letter.json"
                cover_letter_path.write_text(json.dumps(coverletter_data, indent=2))
                print(f"[bold green]Cover letter generated successfully! Data saved at {cover_letter_path}[/]")
                utils.update_config_field("temp_cover_letter_file", str(cover_letter_path))
            except Exception as e:
                print(f"[bold red]Error during cover letter generation: {e}[/]")
                return
            
    if tailored_resume:
        job_data = utils.load_structured_job_description()
        resume_data = utils.load_resume_json()
        if not job_data or not resume_data:
            print("[bold red]Job description or resume data is missing. Please run --parser first.[/]")
            return
        with spinner("Generating tailored resume..."):
            try:
                tailored_resume_data = planc_engine.create_tailored_resume(job_data, resume_data)
                tailored_resume_path = utils.CONFIG_PATH.parent / "tailored_resume.json"
                tailored_resume_path.write_text(json.dumps(tailored_resume_data, indent=2))
                print(f"[bold green]Tailored resume generated successfully! Data saved at {tailored_resume_path}[/]")
                utils.update_config_field("temp_tailored_resume_file", str(tailored_resume_path))
            except Exception as e:
                print(f"[bold red]Error during tailored resume generation: {e}[/]")
                return

    # TODO: Print help message if no option is provided
    if not (setup or test or parser or interactive_jd or cover_letter or tailored_resume):
        print("[bold yellow]No option provided. Use --help to know more.[/bold yellow]")


if __name__ == "__main__":
    app()