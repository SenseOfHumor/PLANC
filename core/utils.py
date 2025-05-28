from pathlib import Path
import json
import shutil

CONFIG_PATH = Path.home() / ".planc" / "config.json"    # User directory, then .planc, then config.json


def config_exists() -> bool:
    return CONFIG_PATH.exists() ## Checks for the config file

def reset_config_folder():
    if CONFIG_PATH.parent.exists(): ## Checks for the config folder
        shutil.rmtree(CONFIG_PATH.parent)
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)   ## Creates the config folder
    CONFIG_PATH.write_text("{}")  # Create empty config file

def load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}

def save_config(data: dict):
    CONFIG_PATH.write_text(json.dumps(data, indent=2))  ## Destructive write, overwrites the entire file, helper function

def get_resume_text_path() -> Path:
    return CONFIG_PATH.parent / "resume_raw.txt"    ## Config folder -> path to resume plain text file

def get_resume_json_path() -> Path:
    return CONFIG_PATH.parent / "resume.json"   ## Config folder -> path to resume json file

def update_config_field(key: str, value: str):
    """
    Loads, adds and then re-writes the config file with a new field.
    Args:
        key (str): The key to add or update in the config.
        value (str): The value to set for the key.
    Returns:
        None
    """
    config = load_config()
    config[key] = value
    save_config(config)

def get_gemini_api_key() -> str:
    config = load_config()
    if "gemini_api_key" in config:
        return config["gemini_api_key"]
    else:
        raise ValueError("Gemini API key not found in config file. Please run setup.")
    
def get_resume_json() -> json:
    if get_resume_json_path().exists():
        return json.loads(get_resume_json_path().read_text())
    else:
        raise ValueError("Resume JSON file not found. Please run setup.")
    
def get_structured_job_description_path() -> Path:
    return CONFIG_PATH.parent / "structured_job_description.json"  # Config folder -> path to structured job description file (volatile data with most recent job description)

def load_structured_job_description() -> dict:
    return json.loads(get_structured_job_description_path().read_text()) if get_structured_job_description_path().exists() else {}
    
def load_resume_text() -> str:
    return get_resume_text_path().read_text() if get_resume_text_path().exists() else {}

