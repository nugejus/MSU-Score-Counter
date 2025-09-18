from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class Mark(Enum):
    EXCELLENT = "отлично"
    GOOD = "хорошо"
    SATISFACTORY = "удов."
    FAILED = "не сдано"

@dataclass(frozen=True)
class GradeEntry:
    subject: str
    mark: Mark
    raw_html: str  # 추후 디버깅/정책 변경 대비

@dataclass(frozen=True)
class GPAResult:
    scheme_name: str     # "5.0", "4.5", "4.3" 등
    value: float
    count: int
