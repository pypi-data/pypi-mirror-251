import click
from transformers import AutoTokenizer, AutoModelForCausalLM
from pathlib import Path
from colorama import init, Fore, Back, Style
import shutil
import os

init(autoreset=True)
green = Fore.LIGHTGREEN_EX
red = Fore.LIGHTRED_EX
blue = Fore.LIGHTBLUE_EX
yellow = Fore.YELLOW
background_color = Back.BLACK  # You can choose different background colors
reset = Style.RESET_ALL


def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def check_model_existence(repo_id, model_name):
    """
    Check if both the model and the tokenizer for the given model_name exist in the local cache.
    """
    model_path = Path.home() / ".cache" / "huggingface" / "hub" / f"models--{repo_id.replace('/', '--')}--{model_name}"
    return model_path.exists()

def download_model(repo_id, model_name):
    """
    Download the model and the tokenizer for the given model_name.
    """
    click.echo(f"\n    Downloading {blue}{repo_id}/{model_name}{reset} from {blue}HuggingFace{reset}...\n")
    AutoModelForCausalLM.from_pretrained(f"{repo_id}/{model_name}")
    AutoTokenizer.from_pretrained(f"{repo_id}/{model_name}")
    click.echo(f"\n    {blue}{repo_id}/{model_name}{reset} downloaded successfully!\n")

def list_models():
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"

    click.echo("\n    Available Models: ")

    for model_dir in cache_dir.iterdir():
        if model_dir.is_dir() and model_dir.name.startswith("models--"):
            parts = model_dir.name.split("--")
            if len(parts) == 3:
                repo_id = parts[1]
                model_id = parts[2]

                # Check the size of the folder
                folder_size = get_folder_size(model_dir)
                if folder_size < 50 * 1024 * 1024:  # 500 MB in bytes
                    # Delete the folder if its size is less than 10MB
                    shutil.rmtree(model_dir)

                else:
                    click.echo(f"       * {blue}{repo_id}/{model_id}{reset}")

    click.echo(f"\n    Download new models ${yellow}lc add --model <model_name>{reset}\n")

def add_model(model_identifier):
    # Splitting the identifier into repo_id and model_name
    try:
        repo_id, model_name = model_identifier.split('/')
        if check_model_existence(repo_id, model_name):
            click.echo(f"\n    Model {blue}{repo_id}/{model_name}{reset} is already available!")
            list_models()
        else:
            try:
                download_model(repo_id, model_name)
                list_models()
            except OSError:
                click.echo(f"    {blue}{model_identifier}{reset} is not a valid model identifier listed on 'https://huggingface.co/models'\n")
                shutil.rmtree(Path.home() / ".cache" / "huggingface" / "hub" / f"models--{repo_id.replace('/', '--')}--{model_name}")

    except ValueError:
        click.echo(f"\n    {red}[Invalid]{reset} Model format\n    Use format: {blue}repo_id/model_name{reset}\n")