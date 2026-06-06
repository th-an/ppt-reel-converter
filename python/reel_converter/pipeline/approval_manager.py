"""Manage user approval decisions and retry routing."""

from __future__ import annotations

from ..schemas.approval import ApprovalDecision, ApprovalAction
from ..schemas.generation_result import SlideResult


class ApprovalManager:
    def __init__(self):
        self.approved_slides: set[int] = set()
        self.skipped_slides: set[int] = set()
        self.retry_history: dict[int, list[str]] = {}

    def process_decision(self, decision: ApprovalDecision) -> str:
        if decision.action == ApprovalAction.APPROVE:
            self.approved_slides.add(decision.slide_number)
            return f"Slide {decision.slide_number} approved and locked."

        elif decision.action == ApprovalAction.SKIP:
            self.skipped_slides.add(decision.slide_number)
            return f"Slide {decision.slide_number} skipped."

        elif decision.action == ApprovalAction.RETRY:
            self.retry_history.setdefault(decision.slide_number, []).append("retry")
            return f"Re-processing slide {decision.slide_number}."

        elif decision.action == ApprovalAction.CHANGE_LAYOUT:
            self.retry_history.setdefault(decision.slide_number, []).append(
                f"change_layout:{decision.new_layout}"
            )
            return f"Re-processing slide {decision.slide_number} with layout: {decision.new_layout}"

        elif decision.action == ApprovalAction.EDIT_CONTENT:
            self.retry_history.setdefault(decision.slide_number, []).append("edit_content")
            return f"Re-processing slide {decision.slide_number} with edited content."

        return "Unknown action."

    def is_slide_approved(self, slide_number: int) -> bool:
        return slide_number in self.approved_slides

    def is_slide_skipped(self, slide_number: int) -> bool:
        return slide_number in self.skipped_slides

    def is_slide_resolved(self, slide_number: int) -> bool:
        return slide_number in self.approved_slides or slide_number in self.skipped_slides

    def can_proceed(self, current_slide: int) -> bool:
        return current_slide == 1 or self.is_slide_resolved(current_slide - 1)