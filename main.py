import sys

from editor import Editor

def main():
    args = sys.argv[1:]
    if args:
        editor = Editor(filepath=args[0])
    else:
        # TODO: add default file path
        editor = Editor("default.txt")

    editor.run()

if __name__ == "__main__":
    main()
