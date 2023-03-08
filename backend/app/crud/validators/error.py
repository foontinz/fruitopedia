class ValidationError(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
    
    def __str__(self):
        return self.message
