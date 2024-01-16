# SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT

import json

from ratelimit import limits, sleep_and_retry
import urllib3

from opendorslib.abc import WorkflowRule
from opendorslib.urls import canonical_url
from opendorslib.metadata import (
    Corpus,
    Repository,
    Mention,
    MentionMetadata,
    Author,
    DataSource,
    IdType,
    MentionContainer,
    ISSN,
)

URL_PAPER_BASE = "https://joss.theoj.org/papers/"
"""Base URL path for JOSS papers."""

URL_PUBLISHED_PAPERS = f"{URL_PAPER_BASE}published"
"""Base URL path for published JOSS papers."""

JOSS_LAST_NAME = "last_name"
"""The field name for authors' last names in JOSS JSON."""
JOSS_GIVEN_NAME = "given_name"
"""The field name for authors' first names in JOSS JSON."""

INVALID_NAME = "ANONYMOUS"
"""A string value to describe authors for which a valid name could not be retrieved."""


########################################################################################################################
############################## Class
########################################################################################################################


class JossRetriever(WorkflowRule):
    def __init__(
        self,
        output_json: str,
        log_file: str,
        log_level: str = "DEBUG",
        indent: int = 0,
    ):
        super().__init__(__name__, log_file, log_level, indent)
        self.output_json = output_json

    ##################################################
    ########## Methods
    ##################################################

    ##########
    ### Main method
    ##########
    def run(self) -> None:
        """
        Retrieves all published papers from the JOSS website at https://joss.theoj.org/papers/published,
        and saves them as OpenDORS metadata JSON.
        """

        all_repositories = []
        page = 1
        while True:
            response = self._get_page(page)
            if response.status == 200:
                data = self._get_json_from_response(response)
                if data:
                    for paper in data:
                        if paper_data := self._get_paper(paper["doi"]):
                            all_repositories.append(paper_data)
                else:
                    self.log.info("No more data found. Finishing retrieval.")
                    break
            else:
                self.log.error(
                    f"Unexpected response status: {response.status}. Aborting retrieval and writing metadata."
                )
                break
            page += 1

        with open(self.output_json, "w") as mj:
            self.log.info("Writing metadata to JSON.")
            if self.indent > 0:
                mj.write(
                    Corpus(repositories=all_repositories).model_dump_json(
                        indent=self.indent
                    )
                )
            else:
                mj.write(Corpus(repositories=all_repositories).model_dump_json())

    @sleep_and_retry
    @limits(calls=1, period=1)
    def _get_page(self, page: int) -> urllib3.response:
        """
        Retrieves the JSON response for a page of published paper from JOSS via HTTP.

        :param page: The page number to retrieve the data for
        :return: A urllib3 response containing the data for the page
        """
        return urllib3.request("GET", f"{URL_PUBLISHED_PAPERS}.json?page={page}")

    @sleep_and_retry
    @limits(calls=1, period=1)
    def _get_paper(self, doi: str) -> Repository | None:
        """
        Retrieves the HTTP response for a specific JOSS paper - identified by DOI - and
        transforms its data to an OpenDORS Repository datatype.

        :param doi: The DOI identifying the paper to retrieve
        :return: A Repository datatype containing the metadata for the retrieved paper
        """
        self.log.debug(f"Retrieving metadata for paper with DOI {doi}.")
        response = urllib3.request("GET", f"{URL_PAPER_BASE}{doi}.json")
        paper_data = self._get_json_from_response(response)
        orig_repo = paper_data["software_repository"]
        if canon_url := canonical_url(orig_repo):
            doi = paper_data["doi"]
            metadata = self._get_mention_metadata(paper_data)
            repository = Repository(
                url=canon_url,
                mentions=[
                    Mention(
                        DataSource.JOSS,
                        doi,
                        IdType.DOI,
                        orig_urls={orig_repo},
                        metadata=metadata,
                    )
                ],
            )
            return repository
        else:
            self.log.info(f"Could not get a canonical URL for {orig_repo}")

    def _get_authors(self, paper_data: dict) -> list[Author]:
        """
        Retrieve a list of Author metadata instances from a dictionary of JOSS paper data

        :param paper_data: The paper data to retrieve author metadata from
        :return: A list of Author instances encapsulating the metadata of the paper authors
        """
        authors = []
        for author in paper_data["authors"]:
            name = self._get_author_name(author)
            if not name or not isinstance(name, str):
                self.log.error(
                    f"Could not extract valid name from author of doi {paper_data['doi']}: {name}. "
                    f"Author data: {author}"
                )
                continue
            if "orcid" in author:
                authors.append(
                    Author(
                        name=name,
                        orcid=f"https://orcid.org/{author['orcid']}",
                    )
                )
            else:
                authors.append(Author(name=name))
        return authors

    def _get_mention_metadata(self, paper_data: dict) -> MentionMetadata:
        """
        Retrieves the metadata from a mentioning paper and returns an instance of MentionMetadata containing them.

        :param paper_data: The paper data to extract the metadata from
        """
        authors = self._get_authors(paper_data)
        return MentionMetadata(
            year=paper_data["year"],
            authors=authors,
            title=paper_data["title"],
            container=MentionContainer(
                name="Journal of Open Source Software",
                issn=ISSN.joss,
                abbreviation="JOSS",
            ),
        )

    ##################################################
    ########## Static methods
    ##################################################

    @staticmethod
    def _get_author_name(author: dict) -> str:
        """
        Extracts an author name from author data. Returns the last name if it exists, otherwise the given name
        if it exists, otherwise the string for an invalid name.

        :param author: The author data to extract the name from
        :return: The author name
        """
        if JOSS_LAST_NAME in author and author[JOSS_LAST_NAME]:
            return author[JOSS_LAST_NAME]
        elif JOSS_GIVEN_NAME in author and author[JOSS_GIVEN_NAME]:
            return author[JOSS_GIVEN_NAME]
        else:
            return INVALID_NAME

    @staticmethod
    def _get_json_from_response(response: urllib3.BaseHTTPResponse) -> dict:
        """
        Decodes the binary data of the input response as UTF-8 and returns a JSON data dictionary.

        :param response: The response whose data should be converted to JSON
        :return: A JSON dictionary containing the UTF-8-decoded binary response data
        """
        data_str = response.data.decode("utf8")
        return json.loads(data_str)
