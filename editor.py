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
                        lambda: self.mode in ["COMMAND", "SEARCH"]
                    ),
                ),
                self.statusbar,
            ]
        )

        self.keybinds = KeyBindings()
        self._configurekeybindings_FORNORMALMODE()
        self._configurekeybindings_FORCOMMANDMODE()
        self._configurekeybindings_FORSEARCHMODE()
        self._configurekeybindings_FORINSERTMODE()

        self.application = Application(
            layout=Layout(self.rootcontainer),
            key_bindings=self.keybinds,
            full_screen=True,
            style=Style.from_dict({
                'status': 'reverse',
            })
        )

    def _configurekeybindings_FORNORMALMODE(self):
        condition = Condition(lambda: self.mode == "NORMAL")

        @self.keybinds.add(':', filter=condition)
        def entercommandmode(event):
            self.mode = "COMMAND"
            self.commandline.prompt = ':'
            self.commandline.text = ''
            self.application.layout.focus(self.commandline)
            self._updatestatusbar()

        @self.keybinds.add('i', filter=condition)
        def enterinsertmode(event):
            self.mode = "INSERT"
            self.application.layout.focus(self.textarea)
            self._updatestatusbar()

    def _configurekeybindings_FORCOMMANDMODE(self):
        condition = Condition(lambda: self.mode == "COMMAND")

        @self.keybinds.add('escape', filter=condition)
        def cancelcommand(event):
            self.mode = "NORMAL"
            self.commandline.prompt = ':'
            self.commandline.text = ''
            self.application.layout.focus(self.textarea)
            self._updatestatusbar()

        @self.keybinds.add('enter', filter=condition)
        def executecommand(event):
            command = self.commandline.text.strip()
            if command:
                self._handlecommand(command)
            self.mode = "NORMAL"
            self.commandline.prompt = ':'
            self.commandline.text = ''
            self.application.layout.focus(self.textarea)
            self._updatestatusbar()

    def _configurekeybindings_FORINSERTMODE(self):
        condition = Condition(lambda: self.mode == "INSERT")
        @self.keybinds.add('escape', filter=condition)
        def cancelinsert(event):
            self.mode = "NORMAL"
            self.commandline.prompt = ':'
            self.commandline.text = ''
            self.application.layout.focus(self.textarea)
            self._updatestatusbar()

    def _configurekeybindings_FORSEARCHMODE(self):
        condition = Condition(lambda: self.mode == "SEARCH")
        @self.keybinds.add('escape', filter=condition)
        def cancelsearch(event):
            self.mode = "NORMAL"
            self.commandline.prompt = '/'
            self.commandline.text = ''
            self.application.layout.focus(self.textarea)
            self._updatestatusbar()

        @self.keybinds.add('enter', filter=condition)
        def search(event):
            query = self.commandline.text.strip()
            if query:
                self._search(query)
            self.mode = "NORMAL"
            self.commandline.prompt = '/'
            self.commandline.text = ''
            self.application.layout.focus(self.textarea)
            self._updatestatusbar()

    def _getstatusbartext(self):
        return f"{self.mode}   file: {os.path.basename(self.filepath) if os.path.basename(self.filepath) else 'untitled'}"

    def _updatestatusbar(self, message=None):
        text = self._getstatusbartext()
        if message:
            text += " | " + message
        self.statusbar.text = text
        self.application.invalidate()

    def _savefile(self):
        try:
            with open(self.filepath, 'w') as file:
                file.write(self.textarea.text)
        except Exception as e:
            # TODO: error that appears when saving is not succesful"
            return f"error saving file {e}"

    def _quit(self):
        self.application.exit()

    def _search(self, query):
        # TODO: check this code
        lines = self.textarea.text.split('\n')
        matches = [i+1 for i, line in enumerate(lines) if query in line]
        return f"found {len(matches)} matches at lines {matches}"

    def _handlecommand(self, cmd):
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
                if len(parts) < 1:
                    if parts[1] and parts[1] == "!":
                        self._quit()
                # TODO: add buffer checking
                self._quit()
            case "wq":
                self._savefile()
                self._quit()
                return "saved and quit"
            case _:
                return "unknown command: {cmd}"

    def run(self):
        self._updatestatusbar()
        self.application.run()
