from dataclasses import dataclass
from enum import Enum


class Mark(Enum):
    """Enumeration of possible marks/grades.

    Attributes:
        EXCELLENT (str): "отлично"
        GOOD (str): "хорошо"
        SATISFACTORY (str): "удов."
        FAILED (str): "не сдано"
    """

    EXCELLENT = "отлично"
    GOOD = "хорошо"
    SATISFACTORY = "удов."
    FAILED = "не сдано"


@dataclass(frozen=True)
class GradeEntry:
    """Represents a single grade entry parsed from the MSU Cabinet.

    Attributes:
        subject (str): Name of the subject/course.
        mark (Mark): Grade achieved in this subject.
        raw_html (str): Original HTML snippet for debugging or policy changes.
    """

    subject: str
    mark: Mark
    raw_html: str


@dataclass(frozen=True)
class GPAResult:
    """Represents the computed GPA value for a specific scheme.

    Attributes:
        scheme_name (str): Name of the grading scheme (e.g., "5.0", "4.5", "4.3").
        value (float): Computed GPA value.
        count (int): Number of subjects included in the calculation.
    """

    scheme_name: str
    value: float
    count: int
