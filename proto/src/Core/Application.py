from Core.Log import *

VERSION = "0.1.0"
application_running = True

class Application:
    def __init__(self):
        Log.init()
        self.version = VERSION
        SAW_DT_INFO(f"Application initialized. Version: {self.version}")

    def get_version_info(self):
        SAW_DT_INFO(f"Version: {self.version}")
        return f"Version: {self.version}"

    def run(self):
        global application_running
        while application_running:
            SAW_INFO("Application is running...")
            import time
            time.sleep(1)
