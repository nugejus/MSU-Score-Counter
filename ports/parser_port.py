# ports/parser_port.py
from typing import Protocol, List
from domain.models import GradeEntry

class ParserPort(Protocol):
    def extract_success_rows(self, html: str) -> List[GradeEntry]: ...
