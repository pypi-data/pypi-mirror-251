# SPDX-FileCopyrightText: 2022-2023 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import asyncio
from argparse import ArgumentParser, Namespace
from typing import Callable

import httpx

from pontos.nvd.cve.api import CVEApi

__all__ = ("CVEApi",)


async def query_cves(args: Namespace) -> None:
    async with CVEApi(token=args.token) as api:
        async for cve in api.cves(
            keywords=args.keywords,
            cpe_name=args.cpe_name,
            cvss_v2_vector=args.cvss_v2_vector,
            cvss_v3_vector=args.cvss_v3_vector,
            source_identifier=args.source_identifier,
            request_results=args.number,
            start_index=args.start,
        ):
            print(cve)


async def query_cve(args: Namespace) -> None:
    async with CVEApi(token=args.token) as api:
        cve = await api.cve(args.cve_id)
        print(cve)


def cves_main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--token", help="API key to use for querying.")
    parser.add_argument(
        "--keywords",
        nargs="*",
        help="Search for CVEs containing the keyword in their description.",
    )
    parser.add_argument(
        "--cpe-name", help="Get all CVE information associated with the CPE"
    )
    parser.add_argument(
        "--cvss-v2-vector",
        help="Get all CVE information with the CVSSv2 vector",
    )
    parser.add_argument(
        "--cvss-v3-vector",
        help="Get all CVE information with the CVSSv3 vector",
    )
    parser.add_argument(
        "--source-identifier",
        help="Get all CVE information with the source identifier. For example: "
        "cve@mitre.org",
    )
    parser.add_argument(
        "--number", "-n", metavar="N", help="Request only N CVEs", type=int
    )
    parser.add_argument(
        "--start",
        "-s",
        help="Index of the first CVE to request.",
        type=int,
    )

    main(parser, query_cves)


def cve_main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--token", help="API key to use for querying.")
    parser.add_argument("cve_id", metavar="CVE-ID", help="ID of the CVE")

    main(parser, query_cve)


def main(parser: ArgumentParser, func: Callable) -> None:
    try:
        args = parser.parse_args()
        asyncio.run(func(args))
    except KeyboardInterrupt:
        pass
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error {e.response.status_code}: {e.response.text}")
