import typer
from typing import Optional
from typing_extensions import Annotated
from odk_mailer import commands, before
import importlib.metadata

app = typer.Typer(
    add_completion=False, 
    pretty_exceptions_enable=True
)

@app.callback()
def callback():
    """
    ODK Mailer

    Setup mail jobs by fetching recipients from CSV files or ODK API.

    Run mail jobs immediately or schedule them to be run over time.

    Evaluate available Mailjobs.

    """

    before.init()

@app.command()
def create(
    source: Annotated[Optional[str], typer.Option("--source", "-s", help="Define source as [type:path|url|api]::[location:str]")]= "",
    fields: Annotated[Optional[str], typer.Option("--fields", "-f", help="Define fields as [email:str]::[data: 'field_1,field_2']")]= "",
    message: Annotated[Optional[str], typer.Option("--message", "-m", help="Define message as [sender:str]::[subject:str]::[source:'stdin'|'path'|'url']::[location:str]::[type:'plain'|'html']")]= "",
    schedule: Annotated[Optional[str], typer.Option("--schedule", help="Define schedule as 'now' or [time:str] in 'YYYY-MM-DD HH:mm' format")]= "",
):
    """
    Create mail job
    """
    commands.create(source, fields, message, schedule)

@app.command()
def run(
    hash: Annotated[str, typer.Argument(help="Hash or id of mailjob to be run")],
    dry: Annotated[bool, typer.Option("--dry", help="Dry run - without sending mails.")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", help="Print out smtp debugging information")] = False,
):
    """
    Run mail job
    """
    commands.run(hash, dry, verbose)

@app.command()
def delete(
    id: Annotated[str, typer.Argument(help="Hexadecimal hash")]
):
    """
    Delete mail job
    """
    commands.delete(id)

@app.command()
def list():
    """
    List mail jobs
    """    
    commands.list_jobs()

@app.command()
def evaluate(
    dry: Annotated[bool, typer.Option("--dry", help="Dry run without sending mails.")] = False
):
    """
    Evaluate mail jobs
    """
    commands.evaluate(dry)

@app.command()
def test(
    sender: Annotated[str, typer.Option("--sender")] = "ODK-Mailer <odk-mailer@freesmtpservers.com>",
    recipient: Annotated[str, typer.Option("--recipient")] = "foo@bar.com",
    host: Annotated[str, typer.Option("--host")] = "smtp.freesmtpservers.com",
    port: Annotated[str, typer.Option("--port")] = "25",
    username: Annotated[str, typer.Option("--user")] = "",
    password: Annotated[str, typer.Option("--pass")] = ""
):
    """
    Send test mail
    """
    commands.test(sender, recipient, host, port, username, password)

@app.command()
def version():
    version = importlib.metadata.version('odk_mailer')
    print(version)

# @app.command()
# def config():
#     """
#     Configure ODK-Mailer
#     """
#     commands.config()
