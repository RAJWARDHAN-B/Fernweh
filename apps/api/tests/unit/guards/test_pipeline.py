from dataclasses import dataclass

import pytest
from structlog.testing import capture_logs

from fernweh_api.guards import Boundary, GuardPipeline, GuardResult, GuardViolation, NoOpGuard


@dataclass
class _UppercaseGuard:
    name: str = "uppercase"

    async def check(self, payload: str) -> GuardResult[str]:
        return GuardResult.allow(payload.upper())


@dataclass
class _RejectingGuard:
    name: str = "reject"
    reason: str | None = "blocked for test"

    async def check(self, payload: str) -> GuardResult[str]:
        if self.reason is None:
            return GuardResult(passed=False, payload=payload)
        return GuardResult.reject(payload, self.reason)


@dataclass
class _RecordingGuard:
    calls: list[str]
    name: str = "recording"

    async def check(self, payload: str) -> GuardResult[str]:
        self.calls.append(payload)
        return GuardResult.allow(payload)


async def test_noop_guard_passes_payload_through_unchanged() -> None:
    result = await NoOpGuard[str]().check("hello")

    assert result == GuardResult(passed=True, payload="hello")


async def test_empty_pipeline_returns_payload() -> None:
    pipeline = GuardPipeline[str](Boundary.INPUT, [])

    assert await pipeline.run("hello") == "hello"


async def test_pipeline_feeds_each_guard_the_previous_output() -> None:
    recorder = _RecordingGuard(calls=[])
    pipeline = GuardPipeline[str](Boundary.INPUT, [NoOpGuard(), _UppercaseGuard(), recorder])

    assert await pipeline.run("hello") == "HELLO"
    assert recorder.calls == ["HELLO"]
    assert pipeline.guard_names == ("noop", "uppercase", "recording")


async def test_pipeline_stops_at_first_rejection() -> None:
    recorder = _RecordingGuard(calls=[])
    pipeline = GuardPipeline[str](Boundary.ACTION, [_RejectingGuard(), recorder])

    with pytest.raises(GuardViolation) as excinfo:
        await pipeline.run("book it")

    assert excinfo.value.guard == "reject"
    assert excinfo.value.boundary is Boundary.ACTION
    assert excinfo.value.reason == "blocked for test"
    assert recorder.calls == []


async def test_rejection_without_reason_uses_default() -> None:
    pipeline = GuardPipeline[str](Boundary.OUTPUT, [_RejectingGuard(reason=None)])

    with pytest.raises(GuardViolation, match="rejected payload: rejected"):
        await pipeline.run("x")


async def test_rejection_is_logged_without_payload() -> None:
    pipeline = GuardPipeline[str](Boundary.INPUT, [_RejectingGuard()])

    with capture_logs() as logs, pytest.raises(GuardViolation):
        await pipeline.run("my passport is X1234567")

    assert logs == [
        {
            "event": "guard_rejected",
            "log_level": "warning",
            "guard": "reject",
            "boundary": "input",
            "reason": "blocked for test",
        }
    ]
