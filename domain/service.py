# domain/services.py
from domain import GPAResult, GradeEntry, Mark
class GpaScheme:
    def __init__(self, name: str, mapping: dict[Mark, float], scale: float):
        self.name = name
        self.mapping = mapping
        self.scale = scale

    def compute(self, grades: list[GradeEntry]) -> GPAResult:
        pts = [self.mapping[g.mark] for g in grades]
        val = round(sum(pts) / max(len(pts), 1), 2)
        return GPAResult(self.name, val, len(pts))

DEFAULT_SCHEMES = [
    GpaScheme("5.0", {
        Mark.SATISFACTORY: 3.0, Mark.GOOD: 4.0, Mark.EXCELLENT: 5.0, Mark.FAILED: 2.0
    }, 5.0),
    GpaScheme("4.5", {
        Mark.SATISFACTORY: 2.7, Mark.GOOD: 3.6, Mark.EXCELLENT: 4.5, Mark.FAILED: 1.72
    }, 4.5),
    GpaScheme("4.3", {
        Mark.SATISFACTORY: 2.58, Mark.GOOD: 3.44, Mark.EXCELLENT: 4.3, Mark.FAILED: 1.8
    }, 4.3),
]

