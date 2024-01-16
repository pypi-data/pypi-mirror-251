# SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT

import json
import re

from jsonpath_ng import parse

from opendorslib.abc import WorkflowRule
from opendorslib.metadata import Repository, IdType, DataSource, Corpus, Mention
from opendorslib.urls import canonical_url


# ######################################################################################################################
# ############################ Class
# ######################################################################################################################


class ExtractURLsRetriever(WorkflowRule):
    def __init__(
        self,
        data_source: DataSource,
        input_json: str,
        output_json: str,
        log_file: str,
        log_level: str,
        indent: int = 0,
    ):
        """
        A retriever for publication metadata from the PMC and ArXiv subsets of the Extract URLs dataset.

        :param input_json: The input data JSON file
        :param output_json: The path string for the target OpenDORS JSON file
        :param log_file: The path string to the log file that logging output should be written to
        """
        super().__init__(f"{__name__}.{data_source.value}", log_file, log_level, indent)
        self.data_source = data_source
        self.input_json = input_json
        self.output_json = output_json

    def _extract_id(self, pdf_file: str) -> str:
        """
        Extracts the data source ID from a PDF file path in the Extract-URLs data.

        :param pdf_file: The pdf file path string to extract the ID from
        :return: the data source ID
        """
        pdf_file = pdf_file.strip("'").strip('"')
        pattern = id_candidate = None
        if self.data_source == DataSource.EXTRACT_URLS_ARXIV:
            id_candidate = pdf_file.replace(".pdf", "")
            pattern = r"^\d+\.\d+v\d+$"
        elif self.data_source == DataSource.EXTRACT_URLS_PMC:
            split_name = pdf_file.split(".")
            id_candidate = split_name[-2].replace("PMC", "")
            pattern = r"^\d+$"
        try:
            assert re.match(pattern, id_candidate)
        except AssertionError as ae:
            message = (
                f"Could not find data source id in {pdf_file}'s id candidate {id_candidate} "
                f"with pattern {pattern}."
            )
            ae.args += (message,)
            self.log.error(message)
            raise ae
        return id_candidate

    def run(self) -> None:
        """
        Extracts repository URLs from Extract-URLs parsed data JSON files,
        checks whether URLs can be transformed into canonical repository URLs,
        and if so, adds them to a corpus of repositories of canonical URLs
        and their mentions in the subset of the dataset.
        The corpus is then written into a JSON file.
        """
        c = Corpus()
        with open(self.input_json, "r") as json_in:
            data = json.load(json_in)
        expr = "$.*.files.*.url_count"
        jsonpath_expression = parse(expr)
        id_type = (
            IdType.ARXIV
            if self.data_source == DataSource.EXTRACT_URLS_ARXIV
            else IdType.PMC
        )

        for datum in jsonpath_expression.find(data):
            if int(datum.value) > 0:
                all_urls = datum.context.value["all_urls"]
                for url in all_urls:
                    if canon_url := canonical_url(url):
                        # Get data source ID for the paper and map it.
                        # The match can only have exactly one context, and that is the parent field,
                        # i.e., the PDF name, which contains the data source ID.
                        pdf_file = str(datum.context.path)
                        data_source_id = self._extract_id(pdf_file)
                        self.log.debug(
                            f"Mapping data source ID {data_source_id} to URL {canon_url}."
                        )
                        m = Mention(
                            data_source=self.data_source,
                            id=data_source_id,
                            id_type=id_type,
                            orig_urls={url},
                        )
                        c.add_repository(Repository(url=canon_url, mentions=[m]))
                    else:
                        self.log.info(f"Could not get a canonical URL for {url}")

        with open(self.output_json, "w") as mj:
            self.log.info(f"Writing corpus for extract_urls to {self.output_json}.")
            if self.indent > 0:
                mj.write(c.model_dump_json(indent=self.indent))
            else:
                mj.write(c.model_dump_json())
