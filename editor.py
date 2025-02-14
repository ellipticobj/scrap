from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, ConditionalContainer
from prompt_toolkit.widgets import TextArea, Label
from prompt_toolkit.filters import Condition
from prompt_toolkit.styles import Style
import os

class Editor:
    def __init__(self, filepath: str, text: str = "", line: int = 0) -> None:
        self.text = text
        self.buffer = text
        self.filepath = filepath
        self.usrhome = os.path.expanduser("~")
        self.currentline = line
        self.mode = "NORMAL" # NORMAL, INSERT, COMMAND

        try:
            with open(filepath, 'r') as file:
                self.text = file.read()
                self.buffer = file.read()
        except FileNotFoundError:
            self.text = ""
            self.text = ""

        self.keybinds = KeyBindings()
        self._configurekeybindings_FORNORMALMODE()
        self._configurekeybindings_FORCOMMANDMODE()
        self._configurekeybindings_FORINSERTMODE()

        self.textarea = TextArea(
            text=self.text,
            scrollbar=True,
            line_numbers=True,
            wrap_lines=True,
            read_only=True
        )
        # updates local buffer when text changes
        self.textarea.buffer.on_text_changed += self._updatebuffer

        self.commandline = TextArea(
            height=1,
            prompt=":",
            multiline=False
        )

        self.statusbar = Label(
            text="",
            style="class:status"
        )

        self.rootcontainer = HSplit([
            self.textarea,
            ConditionalContainer(
                content=self.commandline,
                filter=Condition(
                    lambda: self.mode == "COMMAND"
                ),
            ),
            self.statusbar,
        ])

        self.application = Application(
            layout=Layout(self.rootcontainer),
            key_bindings=self.keybinds,
            full_screen=True,
            style=Style.from_dict({
                'status': 'reverse',
            })
        )

    def _configurekeybindings_FORNORMALMODE(self) -> None:
        '''
        adds keybinds for normal mode
        '''
        condition = Condition(lambda: self.mode == "NORMAL")

        @self.keybinds.add(':', filter=condition)
        def entercommandmode(event):
            self.mode = "COMMAND"
            self.commandline.text = ''
            self.application.layout.focus(self.commandline)
            self._updatestatusbar()

        @self.keybinds.add('i', filter=condition)
        def enterinsertmode(event):
            self.mode = "INSERT"
            self.textarea.read_only = False
            self.application.layout.focus(self.textarea)
            self._updatestatusbar()

    def _configurekeybindings_FORCOMMANDMODE(self) -> None:
        '''
        adds keybinds for command mode
        '''
        condition = Condition(lambda: self.mode == "COMMAND")

        @self.keybinds.add('escape', filter=condition, eager=True)
        def cancelcommand(event):
            self.mode = "NORMAL"
            self.commandline.text = ''
            self.application.layout.focus(self.textarea)
            self._updatestatusbar()

        @self.keybinds.add('enter', filter=condition)
        def executecommand(event):
            command = self.commandline.text.strip()
            if command:
                self._handlecommand(command)
            self.mode = "NORMAL"
            self.commandline.text = ''
            self.application.layout.focus(self.textarea)
            self._updatestatusbar()

    def _configurekeybindings_FORINSERTMODE(self) -> None:
        '''
        adds keybinds for insert mode
        '''
        condition = Condition(lambda: self.mode == "INSERT")
        @self.keybinds.add('escape', filter=condition, eager=True)
        def cancelinsert(event):
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
        self.statusbar.text = text
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
        arg = parts[1] if len(parts) > 1 else None

        commands = {
            "w": self._savecmd,
            "q": self._quitcmd,
            "q!": self._quit,
            "wq": self._saveandquitcmd,
        }

        func = commands.get(command, self._unknowncmd)
        func(arg, parts)

    def _savecmd(self, arg: str, parts: list) -> None:
        '''
        helper command for _handlecommand
        '''
        if arg is not None:
            self._updatestatusbar("too many arguments for command `:w`")
            return
        self._savefile()
        self._updatestatusbar(f"saved file {os.path.basename(self.filepath)}")

    def _quitcmd(self, arg: str, parts: list) -> None:
        '''
        helper command for _handlecommand
        '''
        if arg == "!":
            self._quit()
            return

        try:
            with open(self.filepath, 'r') as file:
                curr = file.read()
        except FileNotFoundError:
            curr = ''

        if curr != self.buffer:
            self._updatestatusbar("unsaved changes. save with :w")
        else:
            self._quit()

    def _saveandquitcmd(self, arg: str, parts: list) -> None:
        '''
        helper command for _handlecommand
        '''
        self._savefile()
        self._updatestatusbar(f"saved file {os.path.basename(self.filepath)}")
        self._quit()

    def _unknowncmd(self, arg: str, parts: list) -> None:
        '''
        helper command for _handlecommand
        '''
        self._updatestatusbar(f"unknown command: {parts}")

    def run(self):
        self._updatestatusbar()
        self.application.run()
