import logging


def config_logger(verbose: bool) -> None:
    """
    Configure the logger.\n
    ---
    ### Args
    - `verbose` (`bool`): if `True` logger level set to `DEBUG`, else `INFO`.
    """
    logging.basicConfig(
        level = logging.DEBUG if verbose else logging.INFO,
        format = '[%(levelname)s][%(name)s] %(message)s',
        handlers = [logging.StreamHandler()])