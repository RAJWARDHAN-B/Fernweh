from deepeval.test_case import LLMTestCase
from pydantic import BaseModel

from fernweh_evals.datasets import load_cases
from fernweh_evals.metrics import SchemaValidityMetric


class _Trip(BaseModel):
    destination: str
    nights: int


def _case(output: str) -> LLMTestCase:
    return LLMTestCase(input="plan a trip", actual_output=output)


def test_valid_output_scores_one_and_succeeds() -> None:
    metric = SchemaValidityMetric(_Trip)

    assert metric.measure(_case('{"destination": "Lisbon", "nights": 4}')) == 1.0
    assert metric.is_successful()
    assert metric.__name__ == "Schema Validity (_Trip)"


def test_invalid_output_scores_zero_and_reports_locations_without_values() -> None:
    metric = SchemaValidityMetric(_Trip)

    score = metric.measure(_case('{"destination": "Passport X1234567", "nights": "many"}'))

    assert score == 0.0
    assert not metric.is_successful()
    assert metric.reason == "nights: int_parsing"
    assert "X1234567" not in (metric.reason or "")


def test_non_json_output_fails_at_root() -> None:
    metric = SchemaValidityMetric(_Trip)

    assert metric.measure(_case("Sure! Here is your trip.")) == 0.0
    assert metric.reason == "<root>: json_invalid"


def test_missing_output_fails() -> None:
    metric = SchemaValidityMetric(_Trip)

    assert metric.measure(LLMTestCase(input="plan a trip")) == 0.0


async def test_async_measure_matches_sync() -> None:
    metric = SchemaValidityMetric(_Trip)

    assert await metric.a_measure(_case('{"destination": "Oslo", "nights": 2}')) == 1.0


def test_smoke_dataset_loads() -> None:
    cases = load_cases("smoke/error_envelopes.jsonl")

    assert [case.id for case in cases] == ["timeout", "guard"]
