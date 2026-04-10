from pathlib import Path


OVERRIDES_PATH = Path("other/games-direct-overrides.txt")
TARGET_PATH = Path("other/games-direct.yaml")
MARKER = "  # Local process overrides"


def load_overrides() -> list[str]:
    entries: list[str] = []
    for raw_line in OVERRIDES_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        entries.append(line)
    return entries


def ensure_overrides() -> None:
    content = TARGET_PATH.read_text(encoding="utf-8")
    entries = load_overrides()

    missing = [entry for entry in entries if f"  - {entry}" not in content]
    if not missing:
        return

    if not content.endswith("\n"):
        content += "\n"

    if MARKER not in content:
        content += f"\n{MARKER}\n"

    for entry in missing:
        content += f"  - {entry}\n"

    TARGET_PATH.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    ensure_overrides()
