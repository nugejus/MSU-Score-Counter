# adapters/bs_parser.py
from typing import List
import re

from bs4 import BeautifulSoup as bs
from domain import GradeEntry, Mark
from ports import ParserPort


class BsParser(ParserPort):
    """HTML parser implementation using BeautifulSoup.

    This parser extracts subject names and grade information
    from MSU Cabinet grade pages. It implements the ParserPort
    interface so it can be swapped with other parser backends
    if needed.
    """

    def __init__(self):
        """Initialize the parser."""

    def __extract_subject_name(self, text: str) -> str:
        """Extract the subject name from a given HTML snippet.

        Args:
            text (str): The HTML content of a `<tr>` row.

        Returns:
            str: The extracted subject name (without quotes).

        Raises:
            AttributeError: If the regex does not find a matching group.
        """
        soup = bs(text, "html.parser")
        subjects = []

        # 1) <span class="text-success">...</span>
        for span in soup.find_all("span", class_="text-success"):
            text = span.get_text(strip=True)
            subjects.append(text.strip('"'))

        # 2) <td>...</td>
        for td in soup.find_all("td"):
            text = td.get_text(" ", strip=True)
            if text:
                subjects.append(text.strip('"'))

        subject = next(filter(lambda x: "Зачетных единиц" in x, subjects))
        pattern = re.compile(r"^(.*?)(?=\s+Зачетных\s+единиц:)", re.IGNORECASE)
        return pattern.search(subject).group(1)

    def extract_success_rows(self, html: str, diploma_only: bool) -> List[GradeEntry]:
        """Extract grade entries from an HTML page.

        Iterates through all table rows (`<tr>`), determines whether
        they represent successful exam results, and returns them as
        structured GradeEntry objects.

        Args:
            html (str): Full HTML source of the grades page.
            diploma_only (bool): If True, include only rows with
                `"text-success"` class (i.e. diploma-related results).

        Returns:
            List[GradeEntry]: List of parsed grade entries, each with
            subject name, mark, and raw HTML.

        Example:
            >>> parser = BsParser()
            >>> entries = parser.extract_success_rows(html, diploma_only=True)
            >>> for e in entries:
            ...     print(e.subject, e.mark)
        """
        soup = bs(html, "html.parser")
        rows = soup.find_all("tr")
        out = []
        for tr in rows:
            if diploma_only and "text-success" not in str(tr):
                continue
            text = tr.get_text(" ", strip=True).lower()
            mark = None
            if "удов." in text:
                mark = Mark.SATISFACTORY
            elif "хорошо" in text:
                mark = Mark.GOOD
            elif "отлично" in text:
                mark = Mark.EXCELLENT
            elif "не сдано" in text:
                mark = Mark.FAILED
            if mark:
                subject = self.__extract_subject_name(str(tr))
                out.append(GradeEntry(subject=subject, mark=mark, raw_html=str(tr)))
        return out
