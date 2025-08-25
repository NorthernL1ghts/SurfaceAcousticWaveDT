VERSION = "0.1.0"

class Application:
    def __init__(self):
        self.version = VERSION
    
    def get_version_info(self):
        return f"Version: { self.version }"
    
    def run(self):
        while True:
            print("Application is running...")