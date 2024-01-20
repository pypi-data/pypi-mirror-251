import logging
import os
from configparser import RawConfigParser
from pathlib import Path


def main_logger():
    loglevel = os.getenv('LOGLEVEL', 'INFO')
    logger = logging.getLogger(name="amlensing")
    formatter = logging.Formatter(
        fmt="%(asctime)s@%(module)s:%(lineno)03d[%(levelname)s]: %(message)s",
        datefmt="%H:%M:%S")
    ch_main = logging.StreamHandler()
    ch_main.setFormatter(formatter)
    ch_main.setLevel(loglevel)
    logger.addHandler(ch_main)
    logger.setLevel(loglevel)
    return logger


def logger_pbar():
    # progressbar logger, which uses '\r' as line ending
    loglevel = os.getenv('LOGLEVEL', 'INFO')
    pbar = logging.getLogger(name="pbar")
    formatter_pbar = logging.Formatter()
    ch_pbar = logging.StreamHandler()
    ch_pbar.setLevel(loglevel)
    ch_pbar.setFormatter(formatter_pbar)
    ch_pbar.terminator = '\r'
    pbar.addHandler(ch_pbar)
    pbar.setLevel(loglevel)
    return pbar


def amlensing_config():
    config = RawConfigParser()
    curdir = Path().resolve()
    package_config = Path(__file__).with_name("amlensing.cfg")

    # load default configuration file
    logger.debug("Loading default configuration")
    config.read(package_config)

    # recursively read configuration files
    # let subfolder configs override parent folders
    for dir in list(curdir.parents)[::-1] + [curdir]:
        config_file = dir.joinpath("amlensing.cfg")
        if config_file.exists():
            logger.debug("Loading %s", config_file)
            config.read(config_file)

    return config


def set_loglevel(level):
    logger.setLevel(level)
    logger_pbar.setLevel(level)


logger = main_logger()
logger_pbar = logger_pbar()
config = amlensing_config()
__all__ = ['config', 'logger', 'logger_pbar', 'set_loglevel']
