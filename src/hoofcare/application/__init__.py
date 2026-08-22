"""Local bench application contract for the HMI/edge boundary."""

ALLOWED_ACTIONS = frozenset(
    {
        "create_session",
        "get_session",
        "resolve_identity",
        "open_reports",
        "back",
    }
)


def require_allowed_action(action: str) -> str:
    """Return an approved local bench action or fail closed for anything else."""
    if action not in ALLOWED_ACTIONS:
        raise ValueError(f"action is not allowlisted: {action}")
    return action
