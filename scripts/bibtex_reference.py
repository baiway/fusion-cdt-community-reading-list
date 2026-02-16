"""
BibTeX Reference — A Python Markdown preprocessor extension.

Transforms fenced BibTeX code blocks (and an optional doi: line) into
formatted reference headers at build time, without modifying source files.
"""

import re
from markdown import Extension
from markdown.preprocessors import Preprocessor


def _parse_bibtex_field(entry, field):
    """Extract a single field value from a BibTeX entry string."""
    pattern = rf"{field}\s*=\s*\{{(.*?)\}}"
    match = re.search(pattern, entry, re.DOTALL)
    if match:
        # Collapse internal whitespace (multi-line values)
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return None


def _format_pages(pages):
    """Replace double-hyphen with en-dash in page ranges."""
    if pages:
        return pages.replace("--", "\u2013")
    return None


def _format_authors(raw):
    """Turn 'Last, First and Last, First' into a middot-separated list."""
    if not raw:
        return None
    authors = [a.strip() for a in raw.split(" and ")]
    return " \u00b7 ".join(authors)


def _build_journal_line(journal, volume, number, pages, year):
    """Build the italicised journal / volume / pages / year line."""
    if not journal:
        return None

    parts = [f"<em>{journal}</em>"]

    vol_part = ""
    if volume:
        vol_part = f"<strong>{volume}</strong>"
        if number:
            vol_part += f"({number})"
    if vol_part:
        parts.append(vol_part)

    if pages:
        parts.append(_format_pages(pages))

    line = ", ".join(parts)
    if year:
        line += f" ({year})"
    return line


class BibtexReferencePreprocessor(Preprocessor):
    """Replace bibtex fenced blocks + doi lines with formatted headers."""

    FENCE_OPEN = re.compile(r"^```bibtex\s*$")
    FENCE_CLOSE = re.compile(r"^```\s*$")
    DOI_LINE = re.compile(r"^doi:\s*(.+)$", re.IGNORECASE)

    def run(self, lines):
        new_lines = []
        i = 0

        while i < len(lines):
            # Look for opening ```bibtex fence
            if self.FENCE_OPEN.match(lines[i].strip()):
                # Collect the BibTeX block
                bibtex_lines = []
                i += 1
                while i < len(lines) and not self.FENCE_CLOSE.match(lines[i].strip()):
                    bibtex_lines.append(lines[i])
                    i += 1
                i += 1  # skip closing ```

                entry = "\n".join(bibtex_lines)

                # Skip blank lines, then look for a doi: line
                doi = None
                doi_end = i
                while doi_end < len(lines) and lines[doi_end].strip() == "":
                    doi_end += 1
                if doi_end < len(lines):
                    m = self.DOI_LINE.match(lines[doi_end].strip())
                    if m:
                        doi = m.group(1).strip()
                        doi_end += 1  # consume the doi line
                        i = doi_end

                # Parse BibTeX fields
                title = _parse_bibtex_field(entry, "title")
                author = _parse_bibtex_field(entry, "author")
                journal = _parse_bibtex_field(entry, "journal")
                volume = _parse_bibtex_field(entry, "volume")
                number = _parse_bibtex_field(entry, "number")
                pages = _parse_bibtex_field(entry, "pages")
                year = _parse_bibtex_field(entry, "year")

                # Build formatted output
                if title:
                    new_lines.append(f"# {title}")
                    new_lines.append("")

                authors = _format_authors(author)
                if authors:
                    new_lines.append(f'<p class="ref-authors">{authors}</p>')
                    new_lines.append("")

                journal_line = _build_journal_line(journal, volume, number, pages, year)
                if journal_line:
                    new_lines.append(f'<p class="ref-journal">{journal_line}</p>')
                    new_lines.append("")

                if doi:
                    new_lines.append(
                        f'<p class="ref-doi"><a href="https://doi.org/{doi}">doi:{doi}</a></p>'
                    )
                    new_lines.append("")

                new_lines.append("---")
                new_lines.append("")
            else:
                new_lines.append(lines[i])
                i += 1

        return new_lines


class BibtexReferenceExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(
            BibtexReferencePreprocessor(md), "bibtex_reference", 30
        )


def makeExtension(**kwargs):
    return BibtexReferenceExtension(**kwargs)
