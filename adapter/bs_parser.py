    # adapters/bs_parser.py
from bs4 import BeautifulSoup as bs
from typing import List
from domain import GradeEntry, Mark
from ports import ParserPort
import re

class BsParser(ParserPort):
    def __init__(self):
        pass

    def __extract_subject_name(self, text: str) -> str:
        soup = bs(text, "html.parser")
        subjects = []

        # 1) <span class="text-success">...</span>
        for span in soup.find_all("span", class_="text-success"):
            text = span.get_text(strip=True)
            subjects.append(text.strip('"'))  # 따옴표 제거

        # 2) <td>...</td>
        for td in soup.find_all("td"):
            text = td.get_text(" ", strip=True)
            if text:  # 빈칸 제외
                subjects.append(text.strip('"'))
        
        subject = next(filter(lambda x: "Зачетных единиц" in x,subjects))
        pattern = re.compile(r'^(.*?)(?=\s+Зачетных\s+единиц:)', re.IGNORECASE)
        return pattern.search(subject).group(1)
    
    def extract_success_rows(self, html: str, diploma_only: bool) -> List[GradeEntry]:
        soup = bs(html, "html.parser")
        rows = soup.find_all("tr")
        out = []
        for tr in rows:
            if diploma_only and "text-success" not in str(tr):
                continue
            text = tr.get_text(" ", strip=True).lower()
            mark = None
            if "удов." in text:       mark = Mark.SATISFACTORY
            elif "хорошо" in text:    mark = Mark.GOOD
            elif "отлично" in text:   mark = Mark.EXCELLENT
            elif "не сдано" in text:  mark = Mark.FAILED
            if mark:
                subject = self.__extract_subject_name(str(tr))
                out.append(GradeEntry(subject=subject, mark=mark, raw_html=str(tr)))
        return out