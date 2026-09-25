from fernweh_api.guards.base import GuardResult


class NoOpGuard[T]:
    """Passes every payload through unchanged. Placeholder until real guards land."""

    name = "noop"

    async def check(self, payload: T) -> GuardResult[T]:
        return GuardResult.allow(payload)
