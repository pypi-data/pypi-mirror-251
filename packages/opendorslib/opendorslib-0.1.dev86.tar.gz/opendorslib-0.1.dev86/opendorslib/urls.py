# SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT
import re
from enum import Enum
from urllib.parse import urlparse
from pathlib import Path
from collections import namedtuple

_Parse = namedtuple("Parse", "scheme, subdomain, domain, tld, path1, path2")
_NetlocParse = namedtuple("NetlocParse", "subdomain, domain, tld")

_VALID_DOMAINS = [
    "github",
    "gitlab",
    "sourceforge",
    "bitbucket",
    "githubusercontent",
]

_INVALID_GH_SUBDOMAINS = [
    "gist",
    "cloud",
    "octoverse",
    "archiveprogram",
    "guides",
    "pages",
    "docs",
]

_INVALID_SF_SUBDOMAINS = [
    "lists",
    "users",
]

_ValidDomains = Enum(
    "_ValidDomains", dict(zip([k.upper() for k in _VALID_DOMAINS], _VALID_DOMAINS))
)

_TLDs = {
    _ValidDomains.GITHUB.value: "com",
    _ValidDomains.GITHUBUSERCONTENT.value: "com",
    _ValidDomains.GITLAB.value: "com",
    _ValidDomains.SOURCEFORGE.value: "net",
    _ValidDomains.BITBUCKET.value: "org",
}

_ALPHA_NUM_DASH = r"[a-zA-Z0-9_-]+"
_ALPHA_NUM_DASH_PERIOD = r"[a-zA-Z0-9\._-]+"

_VALID_URL_REGEX = {
    _ValidDomains.GITHUB.value: r"^https://github.com/"
    + _ALPHA_NUM_DASH
    + r"/"
    + _ALPHA_NUM_DASH_PERIOD
    + r"$",
    _ValidDomains.GITHUBUSERCONTENT.value: r"^https://github.com/"
    + _ALPHA_NUM_DASH
    + r"/"
    + _ALPHA_NUM_DASH_PERIOD
    + r"$",
    _ValidDomains.GITLAB.value: r"^https://gitlab.com/"
    + _ALPHA_NUM_DASH
    + r"/"
    + _ALPHA_NUM_DASH_PERIOD
    + r"$",
    _ValidDomains.SOURCEFORGE.value: r"https://sourceforge.net/projects/"
    + _ALPHA_NUM_DASH_PERIOD
    + r"$",
    _ValidDomains.BITBUCKET.value: r"^https://bitbucket.org/"
    + _ALPHA_NUM_DASH
    + r"/"
    + _ALPHA_NUM_DASH_PERIOD
    + r"$",
}


def _parse_netloc(netloc: str) -> _NetlocParse | None:
    """
    Parses the netloc part of a urlparse'd URL into a three-item named tuple
    with parts subdomain, domain and tld, where only subdomain can be empty,
    and only specific single-element TLDs are allowed.

    :param netloc: The netloc string to parse
    :return: A namedtuple with the parse result including subdomain, domain and top-level domain
    """
    parts = netloc.split(".")
    length = len(parts)
    if length in [2, 3] and parts[-1] in ["com", "org", "io", "net"]:
        return _NetlocParse(parts[-3] if length == 3 else "", parts[-2], parts[-1])


def _get_path_parts(path: str) -> tuple[str, ...] | None:
    """
    Gets the first two path elements for a given path string.
    Returns only the first path element if there is only one,
    and returns None if the path cannot be parsed.

    :param path: The path string to parse
    :return: A tuple containing the first path element and the second path element
    """
    two_paths = Path(path).parts[1:3]
    if two_paths:
        return (
            two_paths[0],
            two_paths[1] if len(two_paths) == 2 else "",
        )


def _handle_sourceforge_url(url: str) -> str:
    """
    Handles some specific cases for Sourceforge URLs.

    :param url: The Sourceforge URL to handle
    :return: The adapted Sourceforge URL
    """
    if "/p/" in url:
        return url.replace("/p/", "/projects/")
    elif "/apps/mediawiki/" in url:
        return url.replace("/apps/mediawiki/", "/projects/")
    else:
        return url


def parse_url(url: str) -> _Parse | None:
    """
    Parses a URL into parts and returns a namedtuple with the following parts.

    Note that this only works in the context of URLs with single-element effective TLDs!

    Parts:
    - 0: scheme (always returns "https")
    - 1: subdomain (subdomain or empty string)
    - 2: domain
    - 3: tld (only single element TLDs)
    - 4: first two path elements (e.g., '/path1/path2/'; returns empty string when path is "/",
    and only ever returns the first two path elements without any leading or trailing slashes)

    :param url: The URLs to parse
    :return: A namedtuple with the parse results, or None if the parse failed
    """

    if "sourceforge.net" in url:
        url = _handle_sourceforge_url(url)
    try:
        url_parts = urlparse(url, scheme="https")
    except ValueError:
        return None
    netloc_parts = _parse_netloc(url_parts.netloc)
    if netloc_parts:
        if url_parts.path and url_parts.path != "/":
            paths = _get_path_parts(url_parts.path)
            if not paths:
                paths = ("", "")
        else:
            paths = ("", "")
        return _Parse(
            "https",
            netloc_parts.subdomain,
            netloc_parts.domain,
            netloc_parts.tld,
            paths[0],
            paths[1],
        )


def _ignore_url(parse: _Parse) -> bool:
    """
    Returns True for URLs that 1) are not validly patterned repository URLs,
    and 2) not URLs with a known pattern that can be converted to a valid repository URL,
    and 3) known subdomain URLs that are not user subdomains.

    # Known subdomain URLs to ignore

    - gist.github.com
    - cloud.github.com
    - octoverse.github.com
    - archiveprogram.github.com
    - guides.github.com
    - pages.github.com
    - docs.github.com
    - lists.sourceforge.net
    - users.sourceforge.net

    # Known paths to ignore
    - sourceforge.net/tracker

    :param parse: The parse object for the URL to check
    :return: Whether the URL should be ignored
    """
    # All interesting URLs apart from SourceForge need at least one path to not be ignored
    if parse.domain != _ValidDomains.SOURCEFORGE.value and not parse.path1:
        return True
    # Ignore user URLs
    if not parse.subdomain and not parse.path2:
        return True
    # Ignore platform-specific stuff
    if parse.domain == _ValidDomains.GITHUB.value:
        # Invalid subdomains
        if parse.subdomain in _INVALID_GH_SUBDOMAINS:
            return True
    elif parse.domain == _ValidDomains.GITLAB.value:
        return False
    elif parse.domain == _ValidDomains.SOURCEFORGE.value:
        # Invalid subdomains
        if parse.subdomain in _INVALID_SF_SUBDOMAINS:
            return True
        if not parse.subdomain and not parse.path1:
            return True
        if parse.path1 == "tracker":
            return True
    # GitHub raw pages need two path segments
    elif parse.domain == _ValidDomains.GITHUBUSERCONTENT.value:
        if not parse.path2:
            return True
    elif parse.domain == _ValidDomains.BITBUCKET.value:
        return False
    else:
        # When this is called, domain validity should already have been checked.
        raise ValueError("Parse domain is not valid.")


def _get_paths(parse: _Parse) -> tuple[str, str]:
    """
    Known URL patterns that can be transformed into valid repository URLs

    - https://(user).github.io/(repo) -> https://github.com/(user)/(repo)
    - https://(user).github.com/(repo) -> https://github.com/(user)/(repo)
    - https://raw.githubusercontent.com/(user)/(repo)
    - https://(user).gitlab.io/(repo) -> https://gitlab.com/(user)/(repo)
    - https://(group).gitlab.io/(subgroup/)+ -> https://gitlab.com/(group)/(subgroup)+
    - https://(repo).sourceforge.io/ -> https://sourceforge.net/projects/(repo)

    :param parse: The parse result for the URL for which to retrieve the paths
    :return: The transformed paths for the given URL
    """
    if parse.subdomain:
        if parse.domain == _ValidDomains.SOURCEFORGE.value:
            path1 = "projects"
            path2 = parse.subdomain
        elif parse.domain == _ValidDomains.GITHUBUSERCONTENT.value:
            path1 = parse.path1
            path2 = parse.path2
        else:
            path1 = parse.subdomain
            path2 = parse.path1
    else:
        path1 = parse.path1
        path2 = parse.path2

    return path1, path2


def _transform_url(parse: _Parse) -> str:
    """
    Transforms a given parse result into a valid canonical repository URL string
    with the pattern https://<domain>.<tld>/<path1>/<path2>.

    :param parse: The parse result for the URL to transform
    :return: The transformed URL
    """
    domain = (
        "github"
        if parse.domain
        in [_ValidDomains.GITHUB.value, _ValidDomains.GITHUBUSERCONTENT.value]
        else parse.domain
    )
    tld = _TLDs[parse.domain]
    path1, path2 = _get_paths(parse)

    return f"https://{domain}.{tld}/{path1}/{path2}"


def canonical_url(url: str) -> str | None:
    """
    Transforms a given URL into a valid canonical repository URL if possible,
    else returns None.

    Valid repository URL patterns for all platforms that are in the scope of this package are

    - https://github.com/(user)/(repo)
    - https://gitlab.com/(user)/(repo)
    - https://gitlab.com/(user)/(repo)
    - https://sourceforge.net/projects/(repo)
    - https://bitbucket.org/(user)/(repo)

    Note that currently, GitLab subgroup URLs cannot be canonicalized.

    Note also that this function may return URLs that don't resolve.

    :param url: The URL string to attempt to make canonical
    :return: The canonical URL string for the given URL string, or None
    """
    parse = parse_url(url)
    if parse:
        if parse.domain not in _VALID_DOMAINS:
            return None
        # Return early if URL is already canonical
        if re.match(_VALID_URL_REGEX[parse.domain], url):
            return url
        else:
            if _ignore_url(parse):
                return None
            return _transform_url(parse)
