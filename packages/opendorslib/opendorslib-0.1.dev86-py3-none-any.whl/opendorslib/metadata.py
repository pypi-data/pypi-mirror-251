# SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT

from enum import Enum
from typing import Optional, Union
import re

from pydantic.dataclasses import dataclass
from pydantic import AnyHttpUrl, BaseModel, field_validator, model_serializer


class ISSN(str, Enum):
    """Enum defining the ISSNs for different data sources."""

    arxiv = "2331-8422"
    joss = "2475-9066"


class IdType(str, Enum):
    """Enum defining the type of identifier for a mentioning resource."""

    ARXIV = "arxiv"
    PMC = "pmc"
    DOI = "doi"
    PUBMED = "pubmed"


class DataSource(str, Enum):
    """Enum defining the data source for the data."""

    EXTRACT_URLS_PMC = "extract-urls-pmc"
    EXTRACT_URLS_ARXIV = "extract-urls-arxiv"
    JOSS = "joss"


@dataclass
class Author:
    """Represents an author of a mentioning publication."""

    name: Optional[str] = None
    orcid: Optional[Union[AnyHttpUrl, str]] = None

    @field_validator("orcid", mode="before")
    def convert_to_url(cls, v):
        """
        Converts a string, assuming that the string represents an ORCiD identifier value,
        into an instance of :class:AnyUrl.

        :param v: A value
        :return: An instance of :class:AnyUrl wrapping the value if it is a string
        """
        if isinstance(v, str):
            if re.match(r"https?://orcid\.org/", str(v)):
                return AnyHttpUrl(v)
            return AnyHttpUrl(f"https://orcid.org/{v}")


@dataclass
class MentionContainer:
    """Represents the container of a mention, e.g., a journal or preprint server."""

    name: Optional[str] = None
    issn: Optional[str] = None
    abbreviation: Optional[str] = None


@dataclass
class MentionId:
    id: str
    id_type: IdType


@dataclass
class MentionMetadata:
    """Represents the metadata for a mentioning publication."""

    year: Optional[int] = None
    authors: Optional[list[Author]] = None
    title: Optional[str] = None
    container: Optional[MentionContainer] = None
    domain: Optional[str] = None
    ids: Optional[list[MentionId]] = None


@dataclass
class Mention:
    """Represents a mention of a research software within a resource."""

    data_source: DataSource
    id: str
    id_type: IdType
    orig_urls: set[str]
    metadata: Optional[MentionMetadata] = None


@dataclass
class Repository:
    """Represents a source code repository."""

    url: AnyHttpUrl
    mentions: list[Mention]

    @field_validator("url", mode="before")
    def wrap_url(cls, v):
        """
        Wraps a string value into an instance of :class:AnyUrl.

        :param v: A value
        :return: An instance of :class:AnyUrl wrapping the value if it is a string
        """
        if isinstance(v, str):
            return AnyHttpUrl(v)

    @model_serializer
    def ser_model(self) -> dict:
        """
        Prepares a model serialization of an instance of repository as a dict of url string to mentions list.

        :return: The serializable dict
        """
        return {"url": str(self.url), "mentions": self.mentions}


class Corpus(BaseModel):
    """Represents a corpus of research software repositories."""

    repositories: list[Repository] = []

    def add_repository(self, new_repo: Repository):
        """
        Adds a repository to a corpus safely, in that it checks

        - that if a repository with the URL already exists,
        the existing repository is used, and
        - that all mention IDs in the new repository are
        added to the existing repository only if they don't exist yet.


        :param new_repo: The repository to add
        """
        for existing_repo in self.repositories:
            if existing_repo.url == new_repo.url:
                ex_mention_lut = {
                    ex_mention.id: ex_mention for ex_mention in existing_repo.mentions
                }
                for mention in new_repo.mentions:
                    if mention.id not in ex_mention_lut:
                        existing_repo.mentions.append(mention)
                    else:
                        ex_mention_lut[mention.id].orig_urls.update(mention.orig_urls)

                return
        self.repositories.append(new_repo)
