import re

class Editor:
    def __init__(self, filepath, buffer = [], line=0):
        self.buffer = buffer
        self.filepath = filepath
        self.currentline = line

        try:
            with open(filepath, 'r') as file:
                self.buffer = file.read().splitlines()
        except FileNotFoundError:
            self.buffer = []


    def printbuffer(self):
        print("\n--- File Buffer ---")
        for i, line in enumerate(self.buffer):
            prefix = "-> " if i == self.currentline else "   "
            print(f"{prefix}{i+1}: {line}")
        print("-------------------\n")

    def run(self):
        print("Welcome to VimLikeEditor (a minimal vim-like editor).")
        while True:
            self.printbuffer()
            cmd = input(":")
            if cmd.startswith(":"):
                self.handlecolon(cmd)
            elif cmd.startswith("/"):
                self.handlesearch(cmd)
            elif cmd == "i":
                self.handleinsert()
            elif re.match(r'^d(\d*)d$', cmd):
                self.handledelete(cmd)
            elif cmd == "j":
                self.movedown()
            elif cmd == "k":
                self.moveup()
            else:
                print("unknown command. supported commands: :w, :q, :wq, /pattern, i, dd, dNd, j, k.")

    def handlecolon(self, cmd):
        pass

    def handlesearch(self, cmd):
        pass

    def handleinsert(self):
        pass

    def handledelete(self, cmd):
        pass

    def movedown(self):
        pass

    def moveup(self):
        pass
