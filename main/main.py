from sys import argv
from typing import Any, List
from os import makedirs
from os.path import expanduser, isdir

from editor import Editor

def main() -> None:
    usrhome: str = expanduser("~")
    args: List[Any] = argv[1:]
    if not isdir(f"{usrhome}/.config/scrappad/"):
        makedirs(f"{usrhome}/.config/scrappad/")
    editor: Editor = Editor(f"{usrhome}/.config/scrappad/notes.txt")
    if args:
        editor = Editor(filepath=args[0])

    editor.run()

if __name__ == "__main__":
    main()
