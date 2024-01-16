import click
import os
import subprocess
    
from inter.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="inter")
def inter():
   pass


@inter.group()
def template():
    """Work with inter Template"""


@template.command("new")
# @click.argument("name")
def ship_new():
    """Creates a new template."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(script_dir, "template")

    comando_cookiecutter = f"cookiecutter {template_dir} --output-dir . --no-input"

    subprocess.run(comando_cookiecutter, shell=True, check=True)

    click.echo(f"Template created successfully")

