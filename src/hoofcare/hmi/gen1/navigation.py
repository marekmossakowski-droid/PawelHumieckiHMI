from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Gen1Route(str, Enum):
    START_RECOVERY = "G1-00"
    OPERATOR_DASHBOARD = "G1-10"
    JOB_SELECTION = "G1-20"
    JOB_PRICING = "G1-21"
    PRICE_CORRECTION = "G1-22"
    ANIMAL_IDENTITY = "G1-30"
    LIMB_CLAW = "G1-31"
    ZONE_LESION = "G1-32"
    TREATMENT = "G1-33"
    MATERIALS = "G1-34"
    FOLLOW_UP = "G1-35"
    COW_SUMMARY = "G1-36"
    WORK_STATISTICS = "G1-40"
    JOB_HISTORY = "G1-41"
    JOB_CLOSURE = "G1-42"
    CLOSED_SETTLEMENT = "G1-43"
    OWNER_PIN = "G1-50"
    OWNER_DASHBOARD = "G1-51"
    LOCAL_ADMIN = "G1-52"
    DIAGNOSTICS = "G1-53"
    RECONCILIATION = "G1-60"


class RouteDecisionKind(str, Enum):
    ALLOW = "ALLOW"
    DENY_WITH_REASON = "DENY_WITH_REASON"
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"


@dataclass(frozen=True)
class RouteDecision:
    kind: RouteDecisionKind
    destination: Gen1Route | None
    reason: str | None = None


@dataclass(frozen=True)
class NavigationContext:
    current_route: Gen1Route
    owner_session_active: bool = False
    dirty_form: bool = False

    @classmethod
    def synthetic_operator(cls) -> "NavigationContext":
        return cls(current_route=Gen1Route.OPERATOR_DASHBOARD)


_TRANSITIONS: dict[Gen1Route, dict[str, Gen1Route]] = {
    Gen1Route.START_RECOVERY: {
        "open_dashboard": Gen1Route.OPERATOR_DASHBOARD,
        "open_reconciliation": Gen1Route.RECONCILIATION,
        "open_diagnostics": Gen1Route.DIAGNOSTICS,
    },
    Gen1Route.OPERATOR_DASHBOARD: {
        "new_job": Gen1Route.JOB_SELECTION,
        "resume_job": Gen1Route.ANIMAL_IDENTITY,
        "open_statistics": Gen1Route.WORK_STATISTICS,
        "open_owner_pin": Gen1Route.OWNER_PIN,
        "open_owner_admin": Gen1Route.LOCAL_ADMIN,
    },
    Gen1Route.JOB_SELECTION: {
        "open_job_pricing": Gen1Route.JOB_PRICING,
        "back": Gen1Route.OPERATOR_DASHBOARD,
    },
    Gen1Route.JOB_PRICING: {
        "confirm_job": Gen1Route.ANIMAL_IDENTITY,
        "back": Gen1Route.JOB_SELECTION,
    },
    Gen1Route.PRICE_CORRECTION: {
        "save_correction": Gen1Route.JOB_CLOSURE,
        "back": Gen1Route.JOB_CLOSURE,
    },
    Gen1Route.ANIMAL_IDENTITY: {
        "next": Gen1Route.LIMB_CLAW,
        "cancel": Gen1Route.OPERATOR_DASHBOARD,
    },
    Gen1Route.LIMB_CLAW: {"next": Gen1Route.ZONE_LESION, "back": Gen1Route.ANIMAL_IDENTITY},
    Gen1Route.ZONE_LESION: {"next": Gen1Route.TREATMENT, "back": Gen1Route.LIMB_CLAW},
    Gen1Route.TREATMENT: {"next": Gen1Route.MATERIALS, "back": Gen1Route.ZONE_LESION},
    Gen1Route.MATERIALS: {"next": Gen1Route.FOLLOW_UP, "back": Gen1Route.TREATMENT},
    Gen1Route.FOLLOW_UP: {"next": Gen1Route.COW_SUMMARY, "back": Gen1Route.MATERIALS},
    Gen1Route.COW_SUMMARY: {
        "complete_cow": Gen1Route.ANIMAL_IDENTITY,
        "back": Gen1Route.FOLLOW_UP,
    },
    Gen1Route.WORK_STATISTICS: {
        "open_history": Gen1Route.JOB_HISTORY,
        "back": Gen1Route.OPERATOR_DASHBOARD,
    },
    Gen1Route.JOB_HISTORY: {
        "open_settlement": Gen1Route.CLOSED_SETTLEMENT,
        "back": Gen1Route.WORK_STATISTICS,
    },
    Gen1Route.JOB_CLOSURE: {
        "correct_price": Gen1Route.PRICE_CORRECTION,
        "confirm_close": Gen1Route.CLOSED_SETTLEMENT,
        "back": Gen1Route.OPERATOR_DASHBOARD,
    },
    Gen1Route.CLOSED_SETTLEMENT: {
        "open_history": Gen1Route.JOB_HISTORY,
        "back": Gen1Route.OPERATOR_DASHBOARD,
    },
    Gen1Route.OWNER_PIN: {
        "unlock": Gen1Route.OWNER_DASHBOARD,
        "cancel": Gen1Route.OPERATOR_DASHBOARD,
    },
    Gen1Route.OWNER_DASHBOARD: {
        "open_owner_admin": Gen1Route.LOCAL_ADMIN,
        "open_history": Gen1Route.JOB_HISTORY,
        "open_diagnostics": Gen1Route.DIAGNOSTICS,
        "back": Gen1Route.OPERATOR_DASHBOARD,
    },
    Gen1Route.LOCAL_ADMIN: {"back": Gen1Route.OWNER_DASHBOARD},
    Gen1Route.DIAGNOSTICS: {"back": Gen1Route.OPERATOR_DASHBOARD},
    Gen1Route.RECONCILIATION: {
        "retry": Gen1Route.START_RECOVERY,
        "open_diagnostics": Gen1Route.DIAGNOSTICS,
        "back": Gen1Route.OPERATOR_DASHBOARD,
    },
}

_OWNER_ROUTES = frozenset({Gen1Route.OWNER_DASHBOARD, Gen1Route.LOCAL_ADMIN})


def next_route(context: NavigationContext, action: str) -> RouteDecision:
    if context.dirty_form and action == "back":
        return RouteDecision(RouteDecisionKind.DENY_WITH_REASON, None, "UNSAVED_CHANGES")

    destination = _TRANSITIONS.get(context.current_route, {}).get(action)
    if destination is None:
        return RouteDecision(
            RouteDecisionKind.RECOVERY_REQUIRED,
            Gen1Route.RECONCILIATION,
            "INVALID_TRANSITION",
        )

    if destination in _OWNER_ROUTES and not context.owner_session_active:
        return RouteDecision(RouteDecisionKind.DENY_WITH_REASON, None, "OWNER_UNLOCK_REQUIRED")

    return RouteDecision(RouteDecisionKind.ALLOW, destination)
