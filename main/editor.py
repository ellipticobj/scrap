from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, ConditionalContainer
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.filters import Condition
from prompt_toolkit.styles import Style
from typing import Optional, Dict, Any
import os

from prompt_toolkit.widgets import TextArea

class Editor:
    def __init__(self, filepath: str, text: str = "") -> None:
        self.text: str = text
        self.buffer: str = text
        self.filepath: str = filepath
        self.mode: str = "NORMAL" # NORMAL, INSERT, COMMAND

        try:
            with open(filepath, 'r') as file:
                self.text = file.read()
            self.buffer = self.text
        except FileNotFoundError:
            pass

        self.keybinds = KeyBindings()
        self._configurekeybindings_FORNORMALMODE()
        self._configurekeybindings_FORCOMMANDMODE()
        self._configurekeybindings_FORINSERTMODE()

        blackstatusbar = Style.from_dict({
            'statusbar': 'bg:black fg:white',
        })

        self.textarea = TextArea(
            text = self.text,
            scrollbar = True,
            line_numbers = True,
            wrap_lines = True,
            read_only = True
        )
        # updates local buffer when text changes
        self.textarea.buffer.on_text_changed += self._updatebuffer

        self.commandline = TextArea(
            height = 1,
            prompt = ":",
            multiline = False
        )

        self.statusbartext: FormattedTextControl = FormattedTextControl(text="")
        self.statusbar: ConditionalContainer = ConditionalContainer(
            content = Window(
                content = self.statusbartext,
                height = 1,
                style = 'class:statusbar'
            ),
            filter = Condition(lambda: True)
        )

        self.rootcontainer: HSplit = HSplit([
            self.textarea,
            ConditionalContainer(
                content = self.commandline,
                filter = Condition(
                    lambda: self.mode == "COMMAND"
                ),
            ),
            self.statusbar,
        ])

        self.application: Application = Application(
            layout = Layout(self.rootcontainer),
            key_bindings = self.keybinds,
            full_screen = True,
            style = blackstatusbar
        )

        self._updatestatusbar()

    def _configurekeybindings_FORNORMALMODE(self) -> None:
        '''
        adds keybinds for normal mode
        '''
        condition = Condition(lambda: self.mode == "NORMAL")

        @self.keybinds.add(':', filter=condition)
        def entercommandmode(event) -> None:
            self.mode = "COMMAND"
            self.commandline.text = ''
            self.application.layout.focus(self.commandline)
            self._updatestatusbar()

        @self.keybinds.add('i', filter=condition)
        def enterinsertmode(event) -> None:
            self.mode = "INSERT"
            self.textarea.read_only = False
            self.application.layout.focus(self.textarea)
            self._updatestatusbar()

    def _configurekeybindings_FORCOMMANDMODE(self) -> None:
        '''
        adds keybinds for command mode
        '''
        condition = Condition(lambda: self.mode == "COMMAND")

        @self.keybinds.add('escape', filter = condition, eager = True)
        def cancelcommand(event) -> None:
            self.mode = "NORMAL"
            self.commandline.text = ''
            self.application.layout.focus(self.textarea)
            self._updatestatusbar()

        @self.keybinds.add('enter', filter=condition)
        def executecommand(event) -> None:
            command = self.commandline.text.strip()
            if command:
                self._handlecommand(command)
            else:
                self._updatestatusbar()
            self.mode = "NORMAL"
            self.commandline.text = ''
            self.application.layout.focus(self.textarea)

    def _configurekeybindings_FORINSERTMODE(self) -> None:
        '''
        adds keybinds for insert mode
        '''
        condition = Condition(lambda: self.mode == "INSERT")
        @self.keybinds.add('escape', filter=condition, eager=True)
        def cancelinsert(event) -> None:
            self.mode = "NORMAL"
            self.textarea.read_only = True
            self.application.layout.focus(self.textarea)
            self._updatestatusbar()

    def _getstatusbartext(self) -> str:
        '''
        returns current status bar text
        '''
        return f"{self.mode} | in: {os.path.basename(self.filepath) if os.path.basename(self.filepath) else 'untitled'}"

    def _updatestatusbar(self, message: str = "") -> None:
        '''
        changes status bar text
        '''
        text = self._getstatusbartext()
        if message:
            text += " | " + message
        self.statusbartext.text = text
        self.application.invalidate()

    def _savefile(self) -> None:
        '''
        saves the file
        '''
        try:
            with open(self.filepath, 'w') as file:
                file.write(self.textarea.text)
        except Exception as e:
            self._updatestatusbar(f"error saving file {e}")

    def _updatebuffer(self, _) -> None:
        '''
        helper function to update the buffer
        '''
        self.buffer = self.textarea.text

    def _quit(self) -> None:
        '''
        quits the app
        '''
        self.application.exit()

    def _handlecommand(self, cmd: str) -> None:
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

        command = parts[0]
        arg: Optional[str] = parts[1] if len(parts) > 1 else None

        commands: Dict[str, Any] = {
            "w": self._savecmd_wrapper,
            "q": self._quitcmd_wrapper,
            "q!": self._forcequitcmd_wrapper,
            "wq": self._saveandquit_wrapper,
        }

        func = commands.get(command, self._unknowncmd_wrapper)
        func(arg, parts)

    def _savecmd_wrapper(self, arg: str | None, parts: list) -> None:
        '''
        helper command for _handlecommand
        '''
        if arg is not None:
            self._updatestatusbar("too many arguments for command `:w`")
            return
        self._savefile()
        self._updatestatusbar(f"saved file {os.path.basename(self.filepath)}")

    def _quitcmd_wrapper(self, arg: str, parts: list) -> None:
        '''
        helper command for _handlecommand
        '''
        try:
            with open(self.filepath, 'r') as file:
                curr = file.read()
        except FileNotFoundError:
            curr = ''

        if curr != self.buffer:
            self._updatestatusbar("unsaved changes. save with :w")
        else:
            self._quit()

    def _forcequitcmd_wrapper(self, arg: str, parts: list) -> None:
        '''
        helper command for _handlecommand
        '''
        self._quit()

    def _saveandquit_wrapper(self, arg: str, parts: list) -> None:
        '''
        helper command for _handlecommand
        '''
        self._savefile()
        self._updatestatusbar(f"saved file {os.path.basename(self.filepath)}")
        self._quit()

    def _unknowncmd_wrapper(self, arg: str, parts: list) -> None:
        '''
        helper command for _handlecommand
        '''
        self._updatestatusbar(f"unknown command: {parts}")

    def run(self):
        self._updatestatusbar()
        self.application.run()
