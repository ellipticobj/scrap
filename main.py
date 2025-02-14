import sys
from editor import Editor

def main():
    args = sys.argv[1:]
    editor = Editor(filepath=args[0])

    editor.run()
    # match len(args):
    #     case 0:
    #         # TODO: handle default config
    #         pass
    #     case 1:
    #         if args[0] == "config":
    #             # handle config
    #             pass
    #         else:
    #             pass
    #             # TODO
    #     case _:
    #         # TODO: handle others
    #         pass

if __name__ == "__main__":
    main()
