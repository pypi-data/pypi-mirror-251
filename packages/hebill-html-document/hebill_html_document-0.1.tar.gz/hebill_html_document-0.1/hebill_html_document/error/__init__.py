class error(Exception):
    def __init__(self, message: str = "Unknown error occurred."):
        self.message = message
        super().__init__(self.message)
