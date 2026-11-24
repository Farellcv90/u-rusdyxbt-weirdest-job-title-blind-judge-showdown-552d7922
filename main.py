#!/usr/bin/env python3
"""Weirdest Job Title: Blind Judge Showdown.

Writes exactly one job title -- the weirdest one we could think of --
to /output/entry.txt. Nothing else, no trailing newline.

Pipeline: validate -> encode -> write -> read-back verify.
"""

import os

ENTRY_TITLE = "Head of Lost Umbrella Reunions"
OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 60


def check_not_empty(title):
    """The gate refuses an empty file."""
    if not title:
        raise ValueError("title is empty")
    return title


def check_no_surrounding_whitespace(title):
    """No leading/trailing whitespace, and no trailing newline."""
    if title != title.strip():
        raise ValueError("title has leading or trailing whitespace")
    return title


def check_not_only_whitespace(title):
    """The gate refuses a file of only whitespace."""
    if not title.strip():
        raise ValueError("title is only whitespace")
    return title


def check_within_limit(title):
    """The gate allows 1 to 60 characters."""
    if len(title) > MAX_CHARS:
        raise ValueError("title is %d chars, over the %d limit" % (len(title), MAX_CHARS))
    return title


def validate_title(title):
    """Check the title against the competition gate, step by step."""
    for check in (
        check_not_empty,
        check_no_surrounding_whitespace,
        check_not_only_whitespace,
        check_within_limit,
    ):
        title = check(title)
    return title


def encode_title(title):
    """Encode the validated title as UTF-8 bytes, nothing else."""
    return title.encode("utf-8")


def write_entry(data):
    """Write the bytes to /output/entry.txt, exactly as given."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)


def verify_entry(expected_data):
    """Read the file back and confirm it is byte-identical to what we wrote."""
    with open(OUTPUT_PATH, "rb") as f:
        actual = f.read()
    if actual != expected_data:
        raise ValueError("read-back mismatch: wrote %r, read %r" % (expected_data, actual))
    return actual


def main():
    title = validate_title(ENTRY_TITLE)
    data = encode_title(title)
    write_entry(data)
    verify_entry(data)
    print("wrote %d chars (%d bytes) to %s" % (len(title), len(data), OUTPUT_PATH))


if __name__ == "__main__":
    main()
