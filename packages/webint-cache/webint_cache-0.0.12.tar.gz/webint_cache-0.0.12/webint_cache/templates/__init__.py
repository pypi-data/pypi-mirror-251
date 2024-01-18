import math
import re
from collections import defaultdict
from hashlib import sha256
from pprint import pformat

import pendulum
import pendulum.parser
import phonenumbers
import webagt
from web import now, tx
from webagt import uri

from ..silos import silos

__all__ = [
    "re",
    "get_dt",
    "tx",
    "uri",
    "silos",
    "pformat",
    "get_silo",
    "get_human_size",
    "now",
    "sha256",
    "format_phonenumber",
    "defaultdict",
    "pendulum",
    "math",
]


def format_phonenumber(tel):
    return phonenumbers.format_number(
        phonenumbers.parse(tel, "US"), phonenumbers.PhoneNumberFormat.INTERNATIONAL
    )


def get_dt(dt):
    try:
        return pendulum.instance(dt)
    except ValueError:
        return pendulum.parser.parse(dt)


def get_silo(url):
    for silo, details in silos.items():
        try:
            domain, profile_patterns, _ = details
        except ValueError:
            domain, profile_patterns = details
        for profile_pattern in profile_patterns:
            if match := re.match(
                f"{domain}/{profile_pattern}", url.removeprefix("www.")
            ):
                return silo, webagt.uri(url).host, profile_pattern, match.groups()[0]
    return None


suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]


def get_human_size(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])
