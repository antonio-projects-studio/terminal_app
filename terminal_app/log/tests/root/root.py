from log import BaseLogging


class Root(BaseLogging):
    LOGGING = True
    
    def __init__(self) -> None:
        self.logger.info("Root init...")
        self.root_logger.info("Root init...")

        
Root()