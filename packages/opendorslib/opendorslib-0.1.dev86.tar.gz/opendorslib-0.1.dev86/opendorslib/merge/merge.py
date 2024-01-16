# SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT
from pydantic import ValidationError

from opendorslib.abc import WorkflowRule
from opendorslib.metadata import Corpus


########################################################################################################################
############################## Class
########################################################################################################################


class CorpusMerger(WorkflowRule):
    def __init__(
        self,
        input_jsons: list[str],
        output_json: str,
        log_file: str,
        log_level: str = "DEBUG",
        indent: int = 0,
    ):
        super().__init__(__name__, log_file, log_level, indent)
        self.input_jsons = input_jsons
        self.output_json = output_json

    ##################################################
    ########## Methods
    ##################################################

    ##########
    ### Main method
    ##########
    def run(self) -> None:
        c = Corpus()
        for input_json in self.input_jsons:
            with open(input_json, "r") as fi:
                try:
                    c_in = Corpus.model_validate_json(fi.read())
                except ValidationError as ve:
                    self.log.error(f"Cannot parse invalid OpenDORS JSON: {input_json}.")
                    raise ve
            for r_in in c_in.repositories:
                c.add_repository(r_in)

        with open(self.output_json, "w") as mj:
            self.log.info("Writing metadata to JSON.")
            if self.indent > 0:
                mj.write(c.model_dump_json(indent=self.indent))
            else:
                mj.write(c.model_dump_json())
