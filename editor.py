from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, ConditionalContainer
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import TextArea, Label
from prompt_toolkit.filters import Condition
from prompt_toolkit.styles import Style
import re
import os

class Editor:
    def __init__(self, filepath, buffer = "", line=0):
        self.text = buffer
        self.filepath = filepath
        self.currentline = line
        self.mode = "NORMAL" # NORMAL, INSERT, COMMAND, SEARCH

        try:
            with open(filepath, 'r') as file:
                self.text = file.read()
        except FileNotFoundError:
            self.text = ""

        self.textarea = TextArea(
            text=self.text,
            scrollbar=True,
            line_numbers=True,
            wrap_lines=False,
            read_only=True
        )

        self.commandline = TextArea(
            height=1,
            prompt=":",
            multiline=False
        )

        self.statusbar = Label(
            # TODO
            text="",
            style="class:status"
        )

        self.rootcontainer = HSplit(
            [
                self.textarea,
                ConditionalContainer(
                    content=self.commandline,
                    filter=Condition(
                        lambda: self.mode in ["COMMND", "SEARCH"]
                    ),
                ),
                self.statusbar,
            ]
        )

        self.keybinds = KeyBindings()
        self._configurekeybindings()

        self.application = Application(
            layout=Layout(self.rootcontainer),
            key_bindings=self.keybinds,
            full_screen=True,
            style=Style.from_dict({
                'status': 'reverse',
            })
        )

    def _configurekeybindings(self):
        # TODO
        return ""

    def _getstatusbartext(self):
        return f"{self.mode}   file: {os.path.basename(self.filepath) if os.path.basename(self.filepath) else 'untitled'}"

    def _savefile(self):
        try:
            with open(self.filepath, 'w') as file:
                file.write(self.textarea.text)
        except Exception as e:
            # TODO: error that appears when saving is not succesful"

    def handlecommand(self, cmd):
        '''
        handles commands:
            :w --- save the file
            :q --- quit without saving (refuse to quit if the buffer is not empty)
            :q! -- quit even if there is something in the buffer
            :wq -- save and quit
        '''
        parts = cmd.split()
        if not parts:
            return

        match parts[0]:
            case "w":
                if len(parts) != 1:
                    return "TODO: error that appears when too many args are passed into :w"
                self._savefile()
                return f"saved file to {self.filepath}"
            case "q":
                # TODO: add buffer checking
                self.application.exit()
            case "wq":
                self._savefile()
                self.application.exit()
                return "saved and quit"
            case _:
                return "unknown command: {cmd}"
