
from jsoncomparison import Compare, NO_DIFF

class FunctionCallEvaluator:
    
    def __init__(self):
        pass
    
    def __call__(self, intent, expected_calls, actual_calls):
        
        diff = Compare().check(expected_calls, actual_calls)

        # todo: walk the diff to generate a discrete score between 0.0 and 1.0

        return 1.0 if diff == NO_DIFF else 0.0
