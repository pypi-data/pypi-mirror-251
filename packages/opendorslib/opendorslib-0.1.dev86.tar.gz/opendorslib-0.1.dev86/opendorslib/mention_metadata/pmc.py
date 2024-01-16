# SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT

from itertools import islice

import urllib3
from ratelimit import limits, sleep_and_retry

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


_ID_TYPES = {"doi": IdType.DOI, "pmid": IdType.PUBMED, "pmcid": IdType.PMC}


class PMCMetadataRetriever(WorkflowRule):
    def __init__(
        self,
        input_json: str,
        output_json: str,
        pmc_api_key: str,
        log_file: str,
        log_level: str = "DEBUG",
        indent: int = 0,
    ):
        super().__init__(__name__, log_file, log_level, indent)
        self.input_json = input_json
        self.output_json = output_json
        self.pmc_api_key = pmc_api_key

    # ################################################
    # ######## Main method
    # ################################################

    def run(self) -> None:
        with open(self.input_json, "r") as ijf:
            c = Corpus.model_validate_json(ijf.read())
        mention_lut = {}

        for r in c.repositories:
            for m in r.mentions:
                if m.id_type == IdType.PMC:
                    if m.id in mention_lut:
                        mention_lut[m.id].append(m)
                    else:
                        mention_lut[m.id] = [m]
        self._attach_mention_metadata(mention_lut)

        with open(self.output_json, "w") as ofj:
            ofj.write(c.model_dump_json())

    def _attach_mention_metadata(
        self, mention_lut: dict[str, list[Mention]], batch_size: int = 499
    ) -> None:
        """
        Attaches mention metadata retrieved from the PMC ESummary service to mentions in the dataset.

        :param mention_lut: A lookup table from PMC ID to Mention instance
        :param batch_size: the size of the batches of PMD IDs to retrieve from the PMC ESummary service. Default: 499
        (This is known to work from manual experimentation.)
        """
        for batch in self._chunk_ids(mention_lut, batch_size):
            self.log.debug(
                f"Processing new batch of {batch_size} PMC IDs from {self.input_json}."
            )
            metadata = self._query_metadata([k for k in batch.keys()])
            if metadata:
                result = metadata["result"]
                for uid in result["uids"]:
                    for mention in mention_lut[uid]:
                        mention.metadata = self._convert_mention_metadata(result, uid)
                        mention_lut[uid].remove(mention)
            else:
                self.log.error(
                    f"Could not retrieve metadata for PMC ids in batch of {batch_size}."
                )
                # Retry with a smaller batch size
                self._attach_mention_metadata(mention_lut, batch_size - 50)

    # ################################################
    # ######## Methods
    # ################################################

    def _convert_mention_metadata(self, result: dict, uid: str) -> MentionMetadata:
        mention_metadata = result[uid]
        year = authors = title = name = abbreviation = ids = None
        if "pubdate" in mention_metadata:
            year = mention_metadata["pubdate"].split(" ")[0].split("-")[0]
        elif "printpubdate" in mention_metadata:
            year = mention_metadata["printpubdate"].split(" ")[0].split("-")[0]
        elif "epubdate" in mention_metadata:
            year = mention_metadata["epubdate"].split(" ")[0].split("-")[0]
        else:
            self.log.debug(f"Missing publication date for PMC article {uid}.")

        if "authors" in mention_metadata:
            authors = []
            for author in mention_metadata["authors"]:
                if "name" in author:
                    authors.append(
                        Author(name=" ".join(author["name"].split(" ")[0:-1]))
                    )
                else:
                    self.log.debug(f"Missing name for author of PMC article {uid}.")
        else:
            self.log.debug(f"Could not retrieve authors for PMC article {uid}.")

        if "articleids" in mention_metadata:
            ids = []
            for _id in mention_metadata["articleids"]:
                if _id["idtype"] in _ID_TYPES:
                    ids.append(
                        MentionId(id=_id["value"], id_type=_ID_TYPES[_id["idtype"]])
                    )
        else:
            self.log.debug(f"Could not retrieve identifiers for PMC article {uid}.")

        if "title" in mention_metadata:
            title = mention_metadata["title"]
        else:
            self.log.debug(f"Could not retrieve title for PMC article {uid}.")

        if "fulljournalname" in mention_metadata:
            name = mention_metadata["fulljournalname"]
        else:
            self.log.debug(f"Missing container name for PMC article {uid}.")

        if "source" in mention_metadata:
            abbreviation = mention_metadata["source"]

        return MentionMetadata(
            year=year,
            authors=authors,
            title=title,
            container=MentionContainer(name=name, abbreviation=abbreviation),
            ids=ids,
        )

    @sleep_and_retry
    @limits(calls=10, period=1)
    def _query_metadata(self, prepared_ids: list[str]) -> dict | None:
        url = (
            f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&api_key={self.pmc_api_key}"
            f"&id={','.join(prepared_ids)}&retmode=json"
        )

        retry = urllib3.Retry(
            total=10,
            backoff_factor=0.1,
            respect_retry_after_header=True,
            raise_on_status=True,
        )
        timeout = urllib3.Timeout(10.0)
        http = urllib3.PoolManager(
            retries=retry,
            timeout=timeout,
        )

        try:
            response = http.request(
                "GET" if len(prepared_ids) <= 200 else "POST",
                url,
            )
        except Exception as e:
            self.log.error(f"Request raised an exception for URL {url}: {e}")
            raise e

        if response.status == 200:
            return response.json()
        else:
            self.log.error(
                f"Error requesting {url} from PMC ESummaries: {response.status}. "
                f"{response.data}"
            )
            return None

    # ################################################
    # ######## "Static methods"
    # ################################################

    @staticmethod
    def _chunk_ids(id_lut: dict, size: int) -> dict:
        """Yield successive n-sized chunks from lookup table."""
        it = iter(id_lut)
        for i in range(0, len(id_lut), size):
            yield {k: id_lut[k] for k in islice(it, size)}
