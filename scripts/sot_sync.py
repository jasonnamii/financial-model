#!/usr/bin/env python3
"""
SoT (Source of Truth) Synchronization Verifier

Verifies that Source of Truth values in a registry are consistent with
all references in downstream markdown files. Supports Korean number units
(만, 억, 조) and provides detailed mismatch reporting.
"""

import re
import sys
import csv
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


@dataclass
class SoTEntry:
    """Represents a Source of Truth entry from the registry."""
    key: str
    value: float
    unit: str
    source: str


@dataclass
class FoundReference:
    """Represents a found reference to a SoT key."""
    file: Path
    line_number: int
    line_content: str
    found_value: float
    match: bool


def parse_korean_number(value_str: str) -> float:
    """
    Parse Korean number notation and convert to base value.

    Supports: 만 (10,000), 억 (100,000,000), 조 (1,000,000,000,000)

    Args:
        value_str: String representation of number with optional Korean unit

    Returns:
        Float representation of the number
    """
    value_str = value_str.strip()

    # Korean unit multipliers
    units = {
        '조': 1_000_000_000_000,
        '억': 100_000_000,
        '만': 10_000,
    }

    # Check for Korean units
    for korean_unit, multiplier in units.items():
        if korean_unit in value_str:
            # Remove the unit and parse the number
            num_part = value_str.replace(korean_unit, '').strip()
            try:
                return float(num_part) * multiplier
            except ValueError:
                return None

    # No Korean unit, try direct conversion
    try:
        return float(value_str)
    except ValueError:
        return None


def parse_sot_registry(registry_path: Path) -> Dict[str, SoTEntry]:
    """
    Parse SoT registry from markdown table format.

    Expected format:
    | SoT Key | Value | Unit | Source |
    |---------|-------|------|--------|
    | TAM | 500 | 억원 | 정부통계 |

    Args:
        registry_path: Path to the registry markdown file

    Returns:
        Dictionary mapping SoT key to SoTEntry
    """
    sot_entries = {}

    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading registry file: {e}", file=sys.stderr)
        sys.exit(1)

    # Find the header row
    header_idx = None
    for idx, line in enumerate(lines):
        if 'SoT Key' in line and 'Value' in line:
            header_idx = idx
            break

    if header_idx is None:
        print("Error: Could not find table header in registry file", file=sys.stderr)
        sys.exit(1)

    # Parse data rows (skip header and separator)
    for line in lines[header_idx + 2:]:
        line = line.strip()
        if not line or not line.startswith('|'):
            break

        # Parse the table row
        parts = [p.strip() for p in line.split('|')]
        # Remove empty parts from split (first and last are empty due to leading/trailing |)
        parts = [p for p in parts if p]

        if len(parts) >= 4:
            key = parts[0]
            value_str = parts[1]
            unit = parts[2]
            source = parts[3]

            parsed_value = parse_korean_number(value_str)
            if parsed_value is not None:
                sot_entries[key] = SoTEntry(
                    key=key,
                    value=parsed_value,
                    unit=unit,
                    source=source
                )

    return sot_entries


def search_sot_references(
    target_folder: Path,
    sot_key: str,
    registry_value: float
) -> List[FoundReference]:
    """
    Search for references to a SoT key in all markdown files.

    Looks for patterns like "TAM 500" or "TAM: 500" and extracts
    the numeric value for comparison.

    Args:
        target_folder: Folder to search in
        sot_key: The SoT key to search for
        registry_value: The expected value from registry

    Returns:
        List of FoundReference objects
    """
    references = []

    # Pattern: SoT Key followed by optional colon, whitespace, and a number
    # with optional Korean unit
    pattern = rf'\b{re.escape(sot_key)}\s*:?\s*([0-9]+\.?[0-9]*\s*[만억조]?)'

    # Find all markdown files
    md_files = list(target_folder.glob('**/*.md'))

    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            continue

        for line_number, line_content in enumerate(lines, 1):
            match = re.search(pattern, line_content)
            if match:
                value_str = match.group(1).strip()
                found_value = parse_korean_number(value_str)

                if found_value is not None:
                    # Allow small floating point differences
                    match_bool = abs(found_value - registry_value) < 0.01

                    references.append(FoundReference(
                        file=md_file.relative_to(target_folder),
                        line_number=line_number,
                        line_content=line_content.strip(),
                        found_value=found_value,
                        match=match_bool
                    ))

    return references


def format_number(value: float) -> str:
    """Format a number for display, removing unnecessary decimals."""
    if value == int(value):
        return str(int(value))
    return str(value)


def main():
    """Main entry point for the SoT synchronization verifier."""
    if len(sys.argv) < 3:
        print("Usage: python sot_sync.py <sot_registry.md> <target_folder>", file=sys.stderr)
        sys.exit(1)

    registry_path = Path(sys.argv[1])
    target_folder = Path(sys.argv[2])

    # Validate inputs
    if not registry_path.exists():
        print(f"Error: Registry file not found: {registry_path}", file=sys.stderr)
        sys.exit(1)

    if not target_folder.exists():
        print(f"Error: Target folder not found: {target_folder}", file=sys.stderr)
        sys.exit(1)

    # Parse the registry
    sot_entries = parse_sot_registry(registry_path)

    if not sot_entries:
        print("Error: No SoT entries found in registry", file=sys.stderr)
        sys.exit(1)

    # Collect all results
    all_results = []
    has_mismatches = False

    # Search for each SoT key
    for sot_key, entry in sorted(sot_entries.items()):
        references = search_sot_references(target_folder, sot_key, entry.value)

        if references:
            for ref in references:
                all_results.append({
                    'Key': sot_key,
                    'Registry Value': format_number(entry.value),
                    'Found Value': format_number(ref.found_value),
                    'File': str(ref.file),
                    'Line': ref.line_number,
                    'Match': 'Yes' if ref.match else 'No'
                })
                if not ref.match:
                    has_mismatches = True
        else:
            # No references found for this key
            all_results.append({
                'Key': sot_key,
                'Registry Value': format_number(entry.value),
                'Found Value': '-',
                'File': '-',
                'Line': '-',
                'Match': 'No Reference'
            })

    # Output results as a table
    if all_results:
        # Print header
        print(f"{'Key':<15} {'Registry Value':<20} {'Found Value':<20} {'File':<40} {'Line':<6} {'Match':<15}")
        print("-" * 116)

        # Print rows
        for result in all_results:
            print(f"{result['Key']:<15} {result['Registry Value']:<20} {result['Found Value']:<20} {result['File']:<40} {str(result['Line']):<6} {result['Match']:<15}")
    else:
        print("No SoT entries found in registry")

    # Exit with appropriate code
    sys.exit(1 if has_mismatches else 0)


if __name__ == '__main__':
    main()
