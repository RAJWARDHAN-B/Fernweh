import pytest
from deepeval.evaluate.evaluate import assert_test
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

from fernweh_domain import ErrorEnvelope
from fernweh_evals.datasets import EvalCase, load_cases
from fernweh_evals.metrics import SchemaValidityMetric

CASES = load_cases("smoke/error_envelopes.jsonl")


@pytest.mark.parametrize("case", CASES, ids=[case.id for case in CASES])
def test_error_envelope_outputs_are_schema_valid(case: EvalCase) -> None:
    test_case = LLMTestCase(input=case.input, actual_output=case.actual_output)
    metrics: list[BaseMetric] = [SchemaValidityMetric(ErrorEnvelope)]

    assert_test(test_case, metrics, run_async=False)
