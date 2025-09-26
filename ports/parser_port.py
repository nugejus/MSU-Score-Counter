# ports/parser_port.py
from typing import Protocol, List
from domain.models import GradeEntry


class ParserPort(Protocol):
    """Port interface for parsing grade information from HTML.

    Implementations of this protocol should take raw HTML from
    the MSU Cabinet (or other systems) and return structured
    grade entries for further processing.

    This abstraction allows the parsing logic to be swapped
    without affecting the use cases (e.g., BeautifulSoup vs.
    another HTML parser).
    """

    def extract_success_rows(self, html: str, diploma_only: bool) -> List[GradeEntry]:
        """Extract grade entries from an HTML page.

        Args:
            html (str): Full HTML source containing grade data.

        Returns:
            List[GradeEntry]: A list of parsed grade entries
            with subject, mark, and raw HTML.

        Example:
            >>> parser: ParserPort = BsParser()
            >>> entries = parser.extract_success_rows(html_source)
            >>> for e in entries:
            ...     print(e.subject, e.mark.value)
        """
