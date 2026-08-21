from __future__ import annotations

import hashlib
from pathlib import Path
from urllib.request import urlretrieve

URL = "https://zenodo.org/records/7395559/files/creditcard.csv?download=1"
TARGET = Path("data/raw/creditcard.csv")
MD5 = "e90efcb83d69faf99fcab8b0255024de"


def md5sum(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    if not TARGET.exists():
        urlretrieve(URL, TARGET)

    actual = md5sum(TARGET)
    if actual != MD5:
        raise SystemExit(f"MD5 mismatch: expected {MD5}, got {actual}")

    print(f"ok {TARGET} {actual}")


if __name__ == "__main__":
    main()
