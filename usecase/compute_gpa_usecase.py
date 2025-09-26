# usecases/compute_gpa_usecase.py
from domain import DEFAULT_SCHEMES


class ComputeGpaUseCase:
    """Use case for computing GPA values.

    This use case takes a list of grade entries and computes GPA
    results for multiple predefined schemes (e.g., 5.0, 4.5, 4.3).
    """

    def __init__(self):
        """Initialize the ComputeGpaUseCase."""

    def execute(self, grades):
        """Compute GPA results for a given set of grades.

        Args:
            grades (list[GradeEntry]): A list of grade entries for which
                GPA should be calculated.

        Returns:
            list[GPAResult]: A list of GPA results, one for each scheme
            defined in DEFAULT_SCHEMES.

        Example:
            >>> uc = ComputeGpaUseCase()
            >>> gpa_results = uc.execute(grades)
            >>> for r in gpa_results:
            ...     print(r.scheme_name, r.value)
        """
        results = [s.compute(grades) for s in DEFAULT_SCHEMES]
        return results
