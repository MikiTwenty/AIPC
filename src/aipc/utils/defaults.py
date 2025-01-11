# aipc/core/defaults.py

import logging
from typing import Optional


class BaseClass:
    """
    A base class providing logging and configuration loading functionality.
    """
    def __init__(
            self,
            logger: Optional[logging.Logger] = None,
        ) -> None:
        """
        Initializes the base class.\n
        ---
        ### Args
        - `logger` (`Optional[logging.Logger]`): an optional logger instance.
        If not provided, a default logger is created.
        """
        if logger:
            self._logger = logger.getChild(self.__class__.__name__)
        else:
            self._logger = logging.getLogger(self.__class__.__name__)

        self._attributes = {}
        self.info = self._logger.info
        self.error = self._logger.error
        self.debug = self._logger.debug
        self.warning = self._logger.warning
        self.critical = self._logger.critical
        self.exception = self._logger.exception

    def __call__(self) -> None:
        """
        Handles the callable behavior of the class.
        Logs a message indicating that the class instance was called.
        """
        self.info(f"{self.__class__.__name__} is called.")

    def __str__(self) -> str:
        """
        Returns the string representation of the class instance.\n
        ---
        ### Returns:
        - `str`: the name of the class.
        """
        return f"{self.__class__.__name__}"