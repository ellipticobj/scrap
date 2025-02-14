class Editor:
    def __init__(self, filename, buffer = [], line=0):
        self.buffer = buffer
        self.filename = filename
        self.currentline = line
