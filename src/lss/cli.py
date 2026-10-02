"""Command-line interface for serial port discovery."""

import argparse
import sys
from collections.abc import Sequence

from serial import SerialException
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo


def filter_ports(ports: list[ListPortInfo], keyword: str) -> list[ListPortInfo]:
    """Match literal text in the device, name, or description."""
    needle = keyword.casefold()
    return sorted(
        port
        for port in ports
        if any(
            needle in (value or "").casefold()
            for value in (port.device, port.name, port.description)
        )
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="lss",
        description="List serial ports; filter device, name, and description by keyword."
    )
    parser.add_argument("keyword", nargs="?", help="Case-insensitive literal substring")
    parser.add_argument("-f", "--filter", dest="filter_keyword", help="Filter by keyword")
    args = parser.parse_args(argv)
    if args.keyword is not None and args.filter_keyword is not None:
        parser.error("use either a positional keyword or --filter")
    keyword = args.filter_keyword if args.filter_keyword is not None else args.keyword

    try:
        ports = filter_ports(list_ports.comports(), keyword or "")
    except (OSError, SerialException) as exc:
        print(f"Unable to list serial ports: {exc}", file=sys.stderr)
        return 1

    if not ports:
        print("No matching serial ports." if keyword else "No serial ports found.")
        return 0

    rows = [("PORT", "NAME", "DESCRIPTION")]
    rows.extend(
        (port.device, port.name or "-", port.description or "-") for port in ports
    )
    port_width = max(len(row[0]) for row in rows)
    name_width = max(len(row[1]) for row in rows)
    for device, name, description in rows:
        print(f"{device:<{port_width}}  {name:<{name_width}}  {description}")
    return 0
