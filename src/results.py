class Results:
    def __init__(self, success: bool, error_message: list = None, data: any = None):
        self.success = success
        self.error_message = error_message if error_message else []  
        self.data = data
    
    def __str__(self):
        if self.success:
            return f"Success: {self.data}"
        else:
            return f"Errors: {', '.join(self.error_message)}"