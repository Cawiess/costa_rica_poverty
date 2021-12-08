import logging

from config.config import config

class ProcessLogger:
    def __init__(self, module):
        self.module = module
        self.processLogger = logging.getLogger(self.module)
        self.processLogger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
        file_handler = logging.FileHandler(f"logs/{config.package_config.process_log_file}")
        file_handler.setFormatter(formatter)
        self.processLogger.addHandler(file_handler)
