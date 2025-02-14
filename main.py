from sys import argv
from os import makedirs
from os.path import expanduser, isdir

from editor import Editor

def main():
    usrhome = expanduser("~")
    args = argv[1:]
    if not isdir(f"{usrhome}/.config/scrappad/"):
        makedirs(f"{usrhome}/.config/scrappad/")
    if args:
        editor = Editor(filepath=args[0])
    else:
        editor = Editor(f"{usrhome}/.config/scrappad/notes.txt")

    editor.run()

if __name__ == "__main__":
    main()
