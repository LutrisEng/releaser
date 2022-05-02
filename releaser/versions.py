from datetime import date
from typing import Optional, Tuple

Version = Tuple[int, int, int]


def current_year() -> int:
    return date.today().year


def current_month() -> int:
    return date.today().month


def base_version() -> Version:
    return (current_year(), current_month(), 0)


def increment_version(version: Optional[Version]) -> Version:
    if version is None:
        return base_version()
    (year, month, number) = version
    if year != current_year() or month != current_month():
        return base_version()
    else:
        return (year, month, number + 1)


def format_version(version: Version) -> str:
    (year, month, number) = version
    return f"{year}.{month}.{number}"


def parse_version(version: str) -> Version:
    split = version.split(".")
    if len(split) != 3:
        raise Exception(
            "Versions should have three numbers delimited by dots (.)")
    (yearStr, monthStr, numberStr) = split
    return (int(yearStr), int(monthStr), int(numberStr))
