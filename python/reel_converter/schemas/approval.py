from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ApprovalAction(str, Enum):
    APPROVE = "approve"
    RETRY = "retry"
    CHANGE_LAYOUT = "change_layout"
    EDIT_CONTENT = "edit_content"
    SKIP = "skip"


class ApprovalDecision(BaseModel):
    action: ApprovalAction
    slide_number: int
    new_layout: str | None = None
    edited_content: dict[str, str] | None = None