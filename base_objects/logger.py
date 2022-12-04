import logging

class Logger:

    def __init__(self, control_name: str) -> None:
        
        super().__init__()
        self.logger = logging.getLogger(control_name)
        self.logger.setLevel(logging.DEBUG)
        self.control_name = control_name

    def log_info(self, msg: str) -> None:

        self.logger.info('[INFO:{control_name}] {msg}'.format(control_name = self.control_name, msg = msg))

    def log_err(self, msg: str) -> None:

        self.logger.info('[ERR:{control_name}] {msg}'.format(control_name = self.control_name, msg = msg))

    def log_warn(self, msg: str) -> None:

        self.logger.info('[WARN:{control_name}] {msg}'.format(control_name = self.control_name, msg = msg))