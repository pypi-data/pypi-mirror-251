import logging
from pathlib import Path
import typer

# tbd: redirect smtp debug to log file: https://stackoverflow.com/a/7303587/3127170

FILE_NAME_LOG = 'odk-mailer.log'
APP_NAME = 'odk-mailer'
app_dir=typer.get_app_dir(APP_NAME, force_posix=True)
log_path: Path = Path(app_dir) / FILE_NAME_LOG


logging.basicConfig(
    filename=log_path, 
    encoding='utf-8', 
    level=logging.DEBUG, 
    format='%(asctime)s: %(levelname)s: %(message)s'
)

def write(msg, type="info"):

    if type == "info":
        logging.info(msg)

    if type=="error":
        logging.error(msg)
