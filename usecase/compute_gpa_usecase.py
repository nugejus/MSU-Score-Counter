# usecases/compute_gpa_usecase.py
from domain import DEFAULT_SCHEMES

class ComputeGpaUseCase:
    def __init__(self):
        pass
    
    def execute(self, grades):
        results = [s.compute(grades) for s in DEFAULT_SCHEMES]
        return results
