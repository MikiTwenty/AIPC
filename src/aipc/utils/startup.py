import logging
from .logger import config_logger


def init(verbose:bool=False) -> None:
    """
    Initialize the cyberdog package.\n
    ---
    ### Args
    - `verbose` (`bool`): if `False` (default) show messages at INFO level and above,
    if `True` show messages at DEBUG level and above. Defaults to `False`.\n
    """
    config_logger(verbose)
    logger = logging.getLogger(__name__)
    logger.debug(f"Verbose log enabled.")