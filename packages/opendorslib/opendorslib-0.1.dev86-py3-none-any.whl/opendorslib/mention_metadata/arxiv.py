# SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT
import logging

import urllib3
import xmltodict

from opendorslib.abc import WorkflowRule
from opendorslib.metadata import (
    Corpus,
    IdType,
    MentionMetadata,
    Author,
    MentionContainer,
    MentionId,
    Mention,
)

# ######################################################################################################################
# ############################ Class
# ######################################################################################################################


class ArXivMetadataRetriever(WorkflowRule):
    def __init__(
        self,
        input_json: str,
        output_json: str,
        log_file: str,
        log_level: str = "DEBUG",
        indent: int = 0,
    ):
        super().__init__(__name__, log_file, log_level, indent)
        self.input_json = input_json
        self.output_json = output_json
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    # ################################################
    # ######## Main method
    # ################################################

    def run(self) -> None:
        with open(self.input_json, "r") as ijf:
            c = Corpus.model_validate_json(ijf.read())
        mention_lut = {}

        for r in c.repositories:
            for m in r.mentions:
                if m.id_type == IdType.ARXIV:
                    if m.id in mention_lut:
                        mention_lut[m.id].append(m)
                    else:
                        mention_lut[m.id] = [m]
        self._attach_mention_metadata(mention_lut)

        with open(self.output_json, "w") as ofj:
            ofj.write(c.model_dump_json())

    # ################################################
    # ######## Methods
    # ################################################
    def _attach_mention_metadata(self, mention_lut: dict[str, list[Mention]]) -> None:
        """
        Attaches mention metadata retrieved from the ArXiv OAI-PMH interface to mentions in the dataset.

        :param mention_lut: A lookup table from ArXiv ID to Mention instance
        :param batch_size: the size of the batches of PMD IDs to retrieve from the PMC ESummary service. Default: 499
        (This is known to work from manual experimentation.)
        """
        for arxiv_id, mentions in mention_lut.items():
            unversioned_id = arxiv_id.split("v")[0]
            metadata_dict = self._query_metadata(unversioned_id)
            if metadata_dict:
                metadata = metadata_dict["OAI-PMH"]["GetRecord"]["record"]["metadata"][
                    "arXiv"
                ]

                for mention in mentions:
                    mention.metadata = self._convert_mention_metadata(
                        metadata, arxiv_id
                    )
                    mention_lut[arxiv_id].remove(mention)

            else:
                self.log.error(f"Could not retrieve metadata for ArXiv id {arxiv_id}.")

    def _convert_mention_metadata(
        self, mention_metadata: dict, arxiv_id: str
    ) -> MentionMetadata:
        year = authors = title = ids = categories = None
        if "created" in mention_metadata:
            year = mention_metadata["created"].split("-")[0]
        else:
            self.log.debug(
                f"Missing publication date for ArXiv article {arxiv_id}. Retrieved metadata: {mention_metadata}."
            )

        if "authors" in mention_metadata:
            authors = []
            m_authors = mention_metadata["authors"]
            if m_authors and "author" in m_authors:
                for author in m_authors["author"]:
                    if isinstance(author, dict) and "keyname" in author:
                        authors.append(Author(name=author["keyname"]))
                    else:
                        self.log.debug(
                            f"Missing name for author of ArXiv article {arxiv_id}. "
                            f"Retrieved metadata: {mention_metadata}."
                        )
            else:
                self.log.debug(
                    f"Could not retrieve author for ArXiv article {arxiv_id}. Retrieved metadata: {mention_metadata}."
                )
        else:
            self.log.debug(
                f"Could not retrieve authors for ArXiv article {arxiv_id}. Retrieved metadata: {mention_metadata}."
            )

        if "id" in mention_metadata:
            ids = []
            _aid = mention_metadata["id"]
            ids.append(MentionId(id=_aid, id_type=IdType.ARXIV))
            ids.append(
                MentionId(
                    id=f"https://doi.org/10.48550/arXiv.{_aid}", id_type=IdType.DOI
                )
            )
        else:
            self.log.debug(
                f"Could not retrieve identifier for ArXiv article {arxiv_id}. Retrieved metadata: {mention_metadata}."
            )

        if "title" in mention_metadata:
            title = mention_metadata["title"].replace("\n", " ")
        else:
            self.log.debug(
                f"Could not retrieve title for ArXiv article {arxiv_id}. Retrieved metadata: {mention_metadata}."
            )

        if "categories" in mention_metadata:
            categories = self._get_unique_major_categories(
                mention_metadata["categories"]
            )

        return MentionMetadata(
            year=year,
            authors=authors if authors else None,
            title=title,
            container=MentionContainer(
                name="ArXiv", issn="2331-8422", abbreviation=None
            ),
            ids=ids,
            domain=categories,
        )

    def _query_metadata(self, arxiv_id: str) -> dict | None:
        url = f"https://export.arxiv.org/oai2?verb=GetRecord&identifier=oai:arXiv.org:{arxiv_id}&metadataPrefix=arXiv"

        retries = urllib3.Retry(
            total=10,
            backoff_factor=0.1,
            respect_retry_after_header=True,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        http = urllib3.PoolManager(retries=retries)

        response = http.request(
            "GET",
            url,
            timeout=30,
        )

        if response.status == 200:
            return xmltodict.parse(response.data.decode("utf-8"))
        else:
            self.log.error(
                f"Error requesting {url} from PMC ESummaries: {response.status}. {response.data}."
            )
            return None

    @staticmethod
    def _get_unique_major_categories(categories_str: str) -> str:
        return ",".join(set([cat.split(".")[0] for cat in categories_str.split(" ")]))
