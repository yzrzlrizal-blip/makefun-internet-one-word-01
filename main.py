#!/usr/bin/env python3
"""The Internet in One Word — make.fun entry.

Writes a single word describing the whole internet to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The word: feral. The internet is not a garden, a library, or a town
square. Nobody tends it, nobody is in charge of it, and it answers to
no one. It is wild, untamed, and liable to bite — feral.
"""

import os
import sys

WORD = "feral"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    # Gate: UTF-8 text of 1 to 30 characters, not only whitespace,
    # and a single word — no spaces, no newlines, no punctuation.
    if not 1 <= len(WORD) <= 30:
        print(f"word must be 1-30 characters, got {len(WORD)}", file=sys.stderr)
        return 1
    if not WORD.strip() or any(ch.isspace() for ch in WORD):
        print("word must be a single non-blank word", file=sys.stderr)
        return 1
    if not WORD.isalpha():
        print("word must be letters only", file=sys.stderr)
        return 1

    data = WORD.encode("utf-8")

    # Atomic write: plain-named temp file in the same directory, then
    # replace. The name must NOT start with '.' — the grader watches
    # the output dir while the program runs and rejects dot-files.
    tmp = os.path.join(out_dir, "entry.txt.tmp")
    try:
        with open(tmp, "wb") as fh:
            fh.write(data)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

    # Re-read and verify the exact bytes landed.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        print("verification failed: bytes on disk differ", file=sys.stderr)
        return 1

    print(WORD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
