from odk_mailer.lib import utils
from types import SimpleNamespace

class Message:
    sender: str
    subject: str
    source: str
    content: str
    format: str

    def __init__(self, data) -> None:

        if type(data) is dict:
            self.sender = data["sender"]
            self.subject = data["subject"]
            self.source = data["source"]
            self.format = data["type"]
            
            if self.source == "stdin":
                self.content = data["location"]

            if self.source == "path":            
                with open(data["location"]) as f:
                    data_string = f.read()
                    # base64_string = utils.base64_encode_str(data_string)
                    # self.content = base64_string
                    self.content = data_string

            if self.source == "url":
                #tbd: read from url and store as base64
                self.content = data["location"]

        if type(data) is SimpleNamespace:
            self.sender = data.sender
            self.subject = data.subject
            self.source = data.source
            self.format = data.format
            self.content = data.content