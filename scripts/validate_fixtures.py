#!/usr/bin/env python3
"""Sanity-check independent, fictional HIS reference-data fixtures.

This checks local example files only. It does NOT test a real HIS, external API,
health-data privacy, clinical validity, or production integration.
Run at repository root: python scripts/validate_fixtures.py
"""
from collections import defaultdict
from datetime import date
from pathlib import Path
import csv
import json
import sys

BASE = Path(__file__).resolve().parent.parent / "sample_data"


def gtin_ok(value):
    if not isinstance(value, str) or len(value) != 14 or not value.isdigit():
        return False
    digits = [int(c) for c in value]
    return sum(d * (3 if i % 2 == 0 else 1) for i, d in enumerate(digits[:13])) % 10 == (-digits[13]) % 10


def overlap(a, b):
    return max(a["start"], b["start"]) <= min(a["end"], b["end"])


def check():
    reg = json.loads((BASE / "registry_snapshot.json").read_text(encoding="utf-8"))
    with (BASE / "coverage_release.csv").open(encoding="utf-8", newline="") as fh:
        coverage = list(csv.DictReader(fh))
    expected = json.loads((BASE / "expected_reconciliation.json").read_text(encoding="utf-8"))
    today = date.fromisoformat(expected["evaluation_date"])

    assert reg["release_id"] and reg["exported_at"]
    packs = reg["records"]
    assert len({p["source_pack_id"] for p in packs}) == len(packs), "Duplicate package IDs"
    assert len({p["gtin"] for p in packs}) == len(packs), "Ambiguous registry GTIN"
    assert all(gtin_ok(p["gtin"]) for p in packs), "Invalid registry GTIN"
    assert all(p["status"] in {"ACTIVE", "WITHDRAWN"} for p in packs)
    pack_by_gtin = {p["gtin"]: p for p in packs}

    assert len({r["coverage_row_id"] for r in coverage}) == len(coverage), "Duplicate coverage ID"
    assert len({r["release_id"] for r in coverage}) == 1, "Mixed source release"
    parsed = []
    for row in coverage:
        assert gtin_ok(row["gtin"]), f"Invalid coverage GTIN: {row['coverage_row_id']}"
        assert row["coverage_status"] in {"ACTIVE", "SUSPENDED"}
        assert row["coverage_tier"] in {"FULL", "PARTIAL", "NONE"}
        start, end = date.fromisoformat(row["effective_from"]), date.fromisoformat(row["effective_to"])
        assert start <= end, f"Reversed coverage dates: {row['coverage_row_id']}"
        parsed.append({**row, "start": start, "end": end})

    matched_by_gtin = defaultdict(list)
    unmatched = []
    for row in parsed:
        if row["gtin"] not in pack_by_gtin:
            unmatched.append(row["coverage_row_id"])
        else:
            matched_by_gtin[row["gtin"]].append(row)

    overlaps = set()
    for rows in matched_by_gtin.values():
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                if overlap(rows[i], rows[j]):
                    overlaps.update((rows[i]["coverage_row_id"], rows[j]["coverage_row_id"]))

    accepted = [r for rows in matched_by_gtin.values() for r in rows if r["coverage_row_id"] not in overlaps]
    published, expired, withdrawn = [], [], []
    for row in accepted:
        pack = pack_by_gtin[row["gtin"]]
        if pack["status"] != "ACTIVE":
            withdrawn.append(row["coverage_row_id"])
        elif row["coverage_status"] != "ACTIVE" or not (row["start"] <= today <= row["end"]):
            expired.append(row["coverage_row_id"])
        else:
            published.append(row["coverage_row_id"])

    actual = {
        "evaluation_date": today.isoformat(),
        "registry": {
            "total": len(packs),
            "active": sum(p["status"] == "ACTIVE" for p in packs),
            "withdrawn": sum(p["status"] == "WITHDRAWN" for p in packs),
        },
        "coverage": {
            "total": len(coverage),
            "matched_nonconflicting": len(accepted),
            "quarantined_unmatched": len(unmatched),
            "quarantined_overlapping": len(overlaps),
            "suppressed_expired": len(expired),
            "suppressed_withdrawn": len(withdrawn),
            "publishable_current": len(published),
        },
        "publishable_row_ids": sorted(published),
        "quarantined_row_ids": sorted(set(unmatched) | overlaps),
    }
    assert actual == expected, "Fixture oracle mismatch:\nACTUAL " + json.dumps(actual, indent=2) + "\nEXPECTED " + json.dumps(expected, indent=2)
    assert sum([len(accepted),len(unmatched),len(overlaps)]) == len(coverage)
    print("PASS: fictional HIS fixture consistency check")
    print(json.dumps(actual, indent=2))


if __name__ == "__main__":
    try:
        check()
    except (AssertionError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
