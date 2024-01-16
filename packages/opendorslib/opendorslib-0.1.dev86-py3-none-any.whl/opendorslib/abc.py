# SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from opendorslib.logging import get_logger


class WorkflowRule(ABC):
    """
    An abstract workflow rule.
    Provides a file logger for the provided log_file with log level log_level.
    """

    def __init__(
        self, name: str, log_file: str, log_level: str = "DEBUG", indent: int = 0
    ) -> None:
        """
        Initializes a workflow rule object.

        :param name: The name to pass to the logger
        :param log_file: The log file to log to
        :param log_level: The log level to log at, must be one of "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"
        :param indent: The indent of any JSON output the retriever creates
        """
        self.name = name
        self.log_file = log_file
        self.log_level = log_level
        self.indent = indent
        self.log = get_logger(self.name, self.log_file, self.log_level)

    @abstractmethod
    def run(self) -> None:
        """
        Runs the workflow rule.

        :return: None
        """
        pass
