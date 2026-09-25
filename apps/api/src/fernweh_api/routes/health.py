from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class LivenessResponse(BaseModel):
    status: Literal["ok"] = "ok"


class ReadinessResponse(BaseModel):
    status: Literal["ready"] = "ready"


@router.get("/healthz")
async def healthz() -> LivenessResponse:
    return LivenessResponse()


@router.get("/readyz")
async def readyz() -> ReadinessResponse:
    return ReadinessResponse()
