from libzim.reader import File

class zimReader:
    def __init__(self,path:str):
        self.file_path=path
        self.file = File()