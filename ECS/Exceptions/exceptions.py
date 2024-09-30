class FileNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class SceneNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)