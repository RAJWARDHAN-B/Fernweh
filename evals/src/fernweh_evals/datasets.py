from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

DATASETS_DIR = Path(__file__).resolve().parents[2] / "datasets"


class EvalCase(BaseModel):
    """One golden row. `actual_output` is set for static cases; agent suites generate it."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(min_length=1)
    input: str
    actual_output: str | None = None
    expected_output: str | None = None


def load_cases(relative_path: str) -> list[EvalCase]:
    path = DATASETS_DIR / relative_path
    return [
        EvalCase.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
