from pathlib import Path

OVERRIDES_PATH = Path("other/games-direct-overrides.txt")
TARGET_PATH = Path("other/games-direct.yaml")
SECTION_MARKER = "  # Local process overrides"
SECTION_PREFIX = "## "


def parse_overrides() -> list[tuple[str | None, list[str]]]:
    """Parse overrides file into list of (header, entries) tuples.

    Lines starting with SECTION_PREFIX become section headers.
    Other comments and empty lines are ignored.
    """
    sections: list[tuple[str | None, list[str]]] = []
    current_header: str | None = None
    current_entries: list[str] = []

    for raw_line in OVERRIDES_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(SECTION_PREFIX):
            if current_entries:
                sections.append((current_header, current_entries))
            current_header = line.removeprefix(SECTION_PREFIX).strip() or None
            current_entries = []
        elif line.startswith("#"):
            continue
        else:
            current_entries.append(line)

    if current_entries:
        sections.append((current_header, current_entries))

    return sections


def build_overrides_block(sections: list[tuple[str | None, list[str]]]) -> str:
    lines: list[str] = [f"\n{SECTION_MARKER}\n"]
    for header, entries in sections:
        if header:
            lines.append(f"\n  # {header}\n")
        for entry in entries:
            lines.append(f"  - {entry}\n")
    return "".join(lines)


def apply_overrides() -> None:
    content = TARGET_PATH.read_text(encoding="utf-8")
    sections = parse_overrides()

    if SECTION_MARKER in content:
        marker_idx = content.index(SECTION_MARKER)
        base_content = content[:marker_idx].rstrip("\n")
    else:
        base_content = content.rstrip("\n")

    filtered_sections: list[tuple[str | None, list[str]]] = []
    for header, entries in sections:
        missing_entries = [
            entry for entry in entries if f"  - {entry}" not in base_content
        ]
        if missing_entries:
            filtered_sections.append((header, missing_entries))

    if not filtered_sections:
        TARGET_PATH.write_text(f"{base_content}\n", encoding="utf-8")
        return

    new_block = build_overrides_block(filtered_sections)
    content = f"{base_content}\n{new_block}"

    TARGET_PATH.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    apply_overrides()
