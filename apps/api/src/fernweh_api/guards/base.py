from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class Boundary(StrEnum):
    INPUT = "input"
    TOOL_OUTPUT = "tool_output"
    OUTPUT = "output"
    ACTION = "action"


@dataclass(frozen=True, slots=True)
class GuardResult[T]:
    passed: bool
    payload: T
    reason: str | None = None

    @classmethod
    def allow(cls, payload: T) -> "GuardResult[T]":
        return cls(passed=True, payload=payload)

    @classmethod
    def reject(cls, payload: T, reason: str) -> "GuardResult[T]":
        return cls(passed=False, payload=payload, reason=reason)


class Guard[T](Protocol):
    """A single check at one boundary. May transform the payload (e.g. redaction)."""

    @property
    def name(self) -> str: ...

    async def check(self, payload: T) -> GuardResult[T]: ...


class GuardViolation(Exception):  # noqa: N818 - domain term, not a generic error
    def __init__(self, *, guard: str, boundary: Boundary, reason: str) -> None:
        super().__init__(f"{boundary} guard '{guard}' rejected payload: {reason}")
        self.guard = guard
        self.boundary = boundary
        self.reason = reason
