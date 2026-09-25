from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
from pydantic import BaseModel, ValidationError


class SchemaValidityMetric(BaseMetric):  # type: ignore[no-untyped-call]  # deepeval hook is untyped
    """Deterministic metric: scores 1.0 when `actual_output` is valid JSON for `schema`."""

    def __init__(self, schema: type[BaseModel], threshold: float = 1.0) -> None:
        self.schema = schema
        self.threshold: float = threshold
        self.include_reason = True

    def measure(self, test_case: LLMTestCase, *args: object, **kwargs: object) -> float:
        score = 1.0
        try:
            self.schema.model_validate_json(test_case.actual_output or "")
        except ValidationError as exc:
            score = 0.0
            # Report locations and error types only; values may contain user data.
            problems = [
                f"{'.'.join(str(part) for part in error['loc']) or '<root>'}: {error['type']}"
                for error in exc.errors()
            ]
            self.reason = "; ".join(problems)
        else:
            self.reason = f"Output is a valid {self.schema.__name__}."
        self.score = score
        self.success = score >= self.threshold
        return score

    async def a_measure(self, test_case: LLMTestCase, *args: object, **kwargs: object) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return bool(self.success)

    @property
    def __name__(self) -> str:
        return f"Schema Validity ({self.schema.__name__})"
