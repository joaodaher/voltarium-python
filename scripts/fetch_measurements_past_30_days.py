#!/usr/bin/env python3
"""Fetch consumption measurements (Medições) for the past 30 days.

Usage:
    uv run python scripts/fetch_measurements_past_30_days.py <consumer_unit_code> <utility_agent_code>

Example:
    uv run python scripts/fetch_measurements_past_30_days.py UC-TESTE 100004

To capture real API samples for fixtures:
    uv run python scripts/fetch_measurements_past_30_days.py UC-TESTE 100004 --dump
"""

import argparse
import asyncio
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from voltarium.client import PRODUCTION_BASE_URL, VoltariumClient

BRAZIL_TZ = timezone(timedelta(hours=-3))


def month_ranges_for_past_30_days() -> list[tuple[str, str]]:
    """Split past 30 days into same-month datetime ranges (API requirement)."""
    now = datetime.now(BRAZIL_TZ)
    start = now - timedelta(days=30)

    ranges: list[tuple[str, str]] = []
    current_start = start

    while current_start <= now:
        year, month = current_start.year, current_start.month
        if month == 12:
            month_end = datetime(year, 12, 31, 23, 59, 59, tzinfo=BRAZIL_TZ)
        else:
            month_end = datetime(year, month + 1, 1, tzinfo=BRAZIL_TZ) - timedelta(seconds=1)

        range_end = min(month_end, now)
        start_str = current_start.strftime("%Y-%m-%dT%H:%M:%S%z")
        end_str = range_end.strftime("%Y-%m-%dT%H:%M:%S%z")
        # Format -0300 as -03:00 for ISO 8601
        start_str = start_str[:-2] + ":" + start_str[-2:]
        end_str = end_str[:-2] + ":" + end_str[-2:]
        ranges.append((start_str, end_str))

        current_start = month_end + timedelta(seconds=1)

    return ranges


async def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Medições for the past 30 days")
    parser.add_argument(
        "consumer_unit_code",
        help="Consumer unit code (e.g., UC-TESTE, UC123456)",
    )
    parser.add_argument(
        "utility_agent_code",
        help="Utility agent code (e.g., 100004)",
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use sandbox API instead of production",
    )
    parser.add_argument(
        "--client-id",
        default="05a08d93-c504-463a-b6d4-2a082c0a7137",
        help="OAuth2 client ID",
    )
    parser.add_argument(
        "--client-secret",
        default="26df06ff-5c39-409d-ae23-31ed0cc8ce6f",
        help="OAuth2 client secret",
    )
    parser.add_argument(
        "--agent-code",
        default="94716",
        help="Agent code",
    )
    parser.add_argument(
        "--profile-code",
        default="105108",
        help="Profile code",
    )
    parser.add_argument(
        "--dump",
        action="store_true",
        help="Save raw API response samples to tests/fixtures/measurements/captured_*.json",
    )
    args = parser.parse_args()

    base_url = "https://sandbox-api-abm.ccee.org.br" if args.sandbox else PRODUCTION_BASE_URL

    ranges = month_ranges_for_past_30_days()
    print(f"Fetching measurements for past 30 days ({len(ranges)} month(s))...")
    for start, end in ranges:
        print(f"  Range: {start} -> {end}")

    all_measurements: list = []
    async with VoltariumClient(
        base_url=base_url,
        client_id=args.client_id,
        client_secret=args.client_secret,
    ) as client:
        for start_dt, end_dt in ranges:
            print(f"\nFetching {start_dt[:10]} to {end_dt[:10]}...")
            async for m in client.list_measurements(
                consumer_unit_code=args.consumer_unit_code,
                utility_agent_code=args.utility_agent_code,
                start_datetime=start_dt,
                end_datetime=end_dt,
                agent_code=args.agent_code,
                profile_code=args.profile_code,
            ):
                all_measurements.append(m)

    print(f"\n--- Total: {len(all_measurements)} measurement(s) ---\n")
    for m in all_measurements:
        print(
            f"  {m.reference_day} | {m.consumption:,.2f} kWh | {m.consumption_type} | "
            f"{m.measurement_status} | id={m.measurement_consumption_id}"
        )

    if args.dump and all_measurements:
        fixture_dir = Path(__file__).parent.parent / "tests" / "fixtures" / "measurements"
        fixture_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(BRAZIL_TZ).strftime("%Y%m%d_%H%M%S")
        out_path = fixture_dir / f"captured_{timestamp}.json"
        raw_medicoes = [m.model_dump(by_alias=True) for m in all_measurements]
        payload = {"medicoes": raw_medicoes, "indexProximaPagina": None}
        out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"\n✓ Saved {len(raw_medicoes)} measurement(s) to {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
