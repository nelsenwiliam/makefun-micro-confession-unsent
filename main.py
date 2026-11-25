"""Unsent: The Micro-Confession Sprint.

Writes one two-part micro-confession to entry.txt:
a "To:" line naming who it was meant for, and the unsent message
itself, one line written exactly as it was typed.

The confession: a son who was taught to change a tyre so he would
never need anyone, and who still calls his dad from the hard shoulder
— not because he needs help, but because he likes hearing his dad
talk him through it. The reason it stayed in drafts is felt, never
stated: sending it would confess the calls are a pretence.

Pure standard library; deterministic: every run writes the same bytes.
"""

import os

TO_LINE = "To: Dad"

MESSAGE = (
    "You taught me to change a tyre so I'd never need anyone, and I "
    "still call you from the hard shoulder because I like hearing you "
    "talk me through it."
)

OUT_NAME = "entry.txt"
TOTAL_LIMIT = 260
MESSAGE_LIMIT = 200


def _text():
    return TO_LINE + "\n" + MESSAGE + "\n"


def _save(path):
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(_text())
    # Read back and confirm the file holds exactly what we meant to write.
    with open(path, "r", encoding="utf-8", newline="\n") as handle:
        assert handle.read() == _text(), "written entry differs from text"


def _targets():
    where = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if where:
        yield os.path.join(where, OUT_NAME)
    yield os.path.join("/output", OUT_NAME)
    yield os.path.join("out", OUT_NAME)


def main():
    text = _text()
    assert 1 <= len(text) <= TOTAL_LIMIT, "entry must be 1-260 characters"
    assert 1 <= len(MESSAGE) <= MESSAGE_LIMIT, "message must be 1-200 characters"
    assert "\n" not in MESSAGE, "message must be a single line"
    assert MESSAGE == MESSAGE.strip(), "message must not pad itself"
    lines = text.rstrip("\n").split("\n")
    assert len(lines) == 2, "entry must be exactly two lines"
    assert lines[0].startswith("To: "), "first line must be the To: line"
    failure = None
    for dest in _targets():
        try:
            folder = os.path.dirname(dest)
            if folder:
                os.makedirs(folder, exist_ok=True)
            _save(dest)
            return
        except OSError as exc:  # noqa: BLE001 - try the next target
            failure = exc
    raise RuntimeError(f"could not write {OUT_NAME}: {failure}")


if __name__ == "__main__":
    main()
