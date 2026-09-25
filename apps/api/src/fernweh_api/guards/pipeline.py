from collections.abc import Sequence

from fernweh_api.guards.base import Boundary, Guard, GuardViolation
from fernweh_api.logging import get_logger

logger = get_logger(__name__)


class GuardPipeline[T]:
    """Runs guards for one boundary in order; each guard sees the previous guard's output."""

    def __init__(self, boundary: Boundary, guards: Sequence[Guard[T]]) -> None:
        self.boundary = boundary
        self._guards = tuple(guards)

    @property
    def guard_names(self) -> tuple[str, ...]:
        return tuple(guard.name for guard in self._guards)

    async def run(self, payload: T) -> T:
        for guard in self._guards:
            result = await guard.check(payload)
            if not result.passed:
                reason = result.reason or "rejected"
                logger.warning(
                    "guard_rejected", guard=guard.name, boundary=str(self.boundary), reason=reason
                )
                raise GuardViolation(guard=guard.name, boundary=self.boundary, reason=reason)
            payload = result.payload
        return payload
