"""
    logging module
"""
import json
import logging

_static_loggers = []

def verify_log_level(level):
    return level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def set_log_level(level):
    #settings.LOG_LEVEL = level
    for logger in _static_loggers:
        logger.setLevel(level)

def get_logger(name, attrs_to_print=None, is_static=False):
    try:
        level = "DEBUG"
        attrs = ['levelname', 'asctime', 'message', 'name']
    except SyntaxError:
        print('Unable to read logger settings, defaulting to "DEBUG"')
        level = 'DEBUG'
        attrs = ['levelname', 'asctime', 'message', 'name']

    logger = logging.getLogger(name)

    if not logger.handlers:
        json_handler = logging.StreamHandler()
        json_handler.setFormatter(JSONFormatter(attrs))
        json_handler.set_name('JSON_Handler')
        logger.addHandler(json_handler)

    logger.setLevel(level)
    logger.propagate = False
    if is_static:
        _static_loggers.append(logger)

    return logger


class JSONFormatter(logging.Formatter):
    attrs_to_print = []

    def __init__(self, attrs_to_print=None):
        super().__init__()
        if attrs_to_print is None:
            self.attrs_to_print = ['levelname', 'asctime', 'message', 'name']
        elif attrs_to_print == 'ALL':
            self.attrs_to_print = ['levelno', 'levelname', 'asctime', 'filename',
                                   'lineno', 'name', 'message', 'pathname',
                                   'module', 'funcName', 'created', 'msecs',
                                   'relativeCreated', 'thread', 'threadName',
                                   'process', 'processName', 'args', 'msg',
                                   'exc_info', 'exc_text', 'stack_info']
        else:
            self.attrs_to_print = attrs_to_print

    def format(self, record):
        record_dict = record.__dict__
        record_dict['message'] = super().format(record)

        if 'asctime' not in record_dict:
            record_dict['asctime'] = self.formatTime(record)

        if record.exc_info:
            record_dict['exc_info'] = self.formatException(record.exc_info)

        out_dict = {}
        for attr_name in self.attrs_to_print:
            if attr_name in record_dict:
                out_dict[attr_name] = record_dict[attr_name]

        return json.dumps(out_dict)
