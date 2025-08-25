import logging
import sys
import os
from enum import Enum, auto

# Logs folder relative to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
LOG_FOLDER_PATH = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_FOLDER_PATH, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_FOLDER_PATH, "Log.log")

class LoggerType(Enum):
    CORE = auto()
    CLIENT = auto()

TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")

class LogLevel(Enum):
    TRACE = TRACE_LEVEL
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARNING
    ERROR = logging.ERROR
    FATAL = logging.CRITICAL

COLOR_MAP = {
    LogLevel.TRACE: "\033[97m",    # White
    LogLevel.DEBUG: "\033[94m",    # Blue
    LogLevel.INFO: "\033[92m",     # Green
    LogLevel.WARN: "\033[93m",     # Yellow
    LogLevel.ERROR: "\033[91m",    # Bright Red
    LogLevel.FATAL: "\033[31m"     # Dark Red
}

RESET = "\033[0m"

def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, message, args, **kwargs)

logging.Logger.trace = trace

class ColorFormatter(logging.Formatter):
    pattern = "[{time}] [{logger_type}] [{level}] [{logger_name}]: {message}"

    @classmethod
    def set_pattern(cls, pattern: str):
        cls.pattern = pattern

    def format(self, record):
        logger_type = "CORE" if record.name == "SAW" else "CLIENT"
        level = next((lvl for lvl in LogLevel if lvl.value == record.levelno), None)
        level_name = level.name if level else record.levelname
        color = COLOR_MAP.get(level, RESET)
        formatted = self.pattern.format(
            time=self.formatTime(record, "%H:%M:%S"),
            logger_type=logger_type,
            level=level_name,
            logger_name=record.name,
            message=record.getMessage()
        )
        return f"{color}{formatted}{RESET}"

class Log:
    core_logger: logging.Logger = None
    client_logger: logging.Logger = None

    @staticmethod
    def init():
        ColorFormatter.set_pattern("[{time}] [{logger_type}] [{level}] [{logger_name}]: {message}")
        Log.core_logger = Log.create_logger("SAW")
        Log.client_logger = Log.create_logger("APP")

    @staticmethod
    def create_logger(name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(TRACE_LEVEL)  # Include TRACE

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColorFormatter())
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler(LOG_FILE_PATH)
        file_formatter = logging.Formatter(
            "[{asctime}] [{levelname}] [{name}]: {message}", 
            style='{', 
            datefmt="%H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        return logger

def SAW_DT_TRACE(msg): Log.core_logger.trace(msg)
def SAW_DT_DEBUG(msg): Log.core_logger.debug(msg)
def SAW_DT_INFO(msg): Log.core_logger.info(msg)
def SAW_DT_WARN(msg): Log.core_logger.warning(msg)
def SAW_DT_ERROR(msg): Log.core_logger.error(msg)
def SAW_DT_FATAL(msg): Log.core_logger.critical(msg)

def SAW_TRACE(msg): Log.client_logger.trace(msg)
def SAW_DEBUG(msg): Log.client_logger.debug(msg)
def SAW_INFO(msg): Log.client_logger.info(msg)
def SAW_WARN(msg): Log.client_logger.warning(msg)
def SAW_ERROR(msg): Log.client_logger.error(msg)
def SAW_FATAL(msg): Log.client_logger.critical(msg)