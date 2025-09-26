# domain/services.py
from domain import GPAResult, GradeEntry, Mark


class GpaScheme:
    """Represents a GPA calculation scheme.

    Each scheme defines a name, a mapping of `Mark` values to numerical
    grade points, and a maximum GPA scale (e.g., 5.0, 4.5, 4.3).

    Attributes:
        name (str): The name of the scheme (e.g., "5.0").
        mapping (dict[Mark, float]): A dictionary mapping marks to numeric values.
        scale (float): The maximum GPA value for the scheme.
    """

    def __init__(self, name: str, mapping: dict[Mark, float], scale: float):
        """Initialize a GPA scheme.

        Args:
            name (str): The name of the scheme (e.g., "5.0").
            mapping (dict[Mark, float]): A mapping from marks to GPA points.
            scale (float): The maximum GPA scale value.
        """
        self.name = name
        self.mapping = mapping
        self.scale = scale

    def compute(self, grades: list[GradeEntry]) -> GPAResult:
        """Compute the GPA for a list of grades.

        Args:
            grades (list[GradeEntry]): A list of grade entries to include.

        Returns:
            GPAResult: The result containing scheme name, GPA value, and
            number of subjects considered.

        Example:
            >>> scheme = GpaScheme("5.0", {Mark.EXCELLENT: 5.0, Mark.GOOD: 4.0,
            ...                            Mark.SATISFACTORY: 3.0, Mark.FAILED: 2.0}, 5.0)
            >>> grades = [GradeEntry("Math", Mark.EXCELLENT, "<tr>...</tr>"),
            ...           GradeEntry("History", Mark.GOOD, "<tr>...</tr>")]
            >>> result = scheme.compute(grades)
            >>> result.value
            4.5
        """
        pts = [self.mapping[g.mark] for g in grades]
        val = round(sum(pts) / max(len(pts), 1), 2)
        return GPAResult(self.name, val, len(pts))


DEFAULT_SCHEMES = [
    GpaScheme(
        "5.0",
        {Mark.SATISFACTORY: 3.0, Mark.GOOD: 4.0, Mark.EXCELLENT: 5.0, Mark.FAILED: 2.0},
        5.0,
    ),
    GpaScheme(
        "4.5",
        {
            Mark.SATISFACTORY: 2.7,
            Mark.GOOD: 3.6,
            Mark.EXCELLENT: 4.5,
            Mark.FAILED: 1.72,
        },
        4.5,
    ),
    GpaScheme(
        "4.3",
        {
            Mark.SATISFACTORY: 2.58,
            Mark.GOOD: 3.44,
            Mark.EXCELLENT: 4.3,
            Mark.FAILED: 1.8,
        },
        4.3,
    ),
]
"""list[GpaScheme]: Default GPA schemes commonly used (5.0, 4.5, 4.3)."""
