from __future__ import annotations

from .audit import AuditLog
from .backend import DToolsBackend
from .model import ActionKind, ActionRequest, ActionResult
from .policy import ActionPolicy
from .session import SessionGuard


class BridgeController:
    def __init__(
        self,
        *,
        backend: DToolsBackend,
        policy: ActionPolicy,
        session: SessionGuard,
        audit: AuditLog,
    ) -> None:
        self.backend = backend
        self.policy = policy
        self.session = session
        self.audit = audit

    def execute(self, token: str, request: ActionRequest) -> ActionResult:
        self.session.authorize(token)
        try:
            before = self.backend.snapshot()
            before_image = self.backend.capture()
        except Exception as error:
            self.session.stop("precondition_error")
            self.audit.append(
                tool=request.kind.value,
                arguments={"target": request.target, "value": request.value},
                decision="NOT_EVALUATED",
                result="PRECONDITION_ERROR",
                error_type=type(error).__name__,
                config_sha256=self.policy.config_sha256,
                mechanism=getattr(self.backend, "mechanism", "TEST_BACKEND"),
                confirmation_required=False,
            )
            return ActionResult(
                "PRECONDITION_ERROR",
                "DTools precondition could not be read; the session was stopped.",
            )
        decision = self.policy.evaluate(request, before)
        if not decision.allowed:
            if decision.code in {
                "EXECUTABLE_MISMATCH",
                "PROJECT_MISMATCH",
                "UNEXPECTED_DIALOG",
                "PRECONDITION_MISMATCH",
            }:
                self.session.stop(decision.code.casefold())
            operation = self.audit.append(
                tool=request.kind.value,
                arguments={"target": request.target, "value": request.value},
                decision=decision.code,
                result=decision.code,
                precondition=before.context,
                config_sha256=self.policy.config_sha256,
                process_id=before.pid,
                window_class=before.window_class,
                project_title=before.title,
                mechanism=getattr(self.backend, "mechanism", "TEST_BACKEND"),
                confirmation_required=False,
                evidence_before_image=before_image,
            )
            evidence_before = self.audit.evidence_filename(operation, "before")
            return ActionResult(
                decision.code,
                decision.reason,
                evidence_before=evidence_before,
            )

        try:
            self._perform(request, token)
            after = self.backend.snapshot()
            after_image = self.backend.capture()
        except Exception as error:
            self.session.stop("backend_error")
            operation = self.audit.append(
                tool=request.kind.value,
                arguments={"target": request.target, "value": request.value},
                decision=decision.code,
                result="BACKEND_ERROR",
                precondition=before.context,
                error_type=type(error).__name__,
                config_sha256=self.policy.config_sha256,
                process_id=before.pid,
                window_class=before.window_class,
                project_title=before.title,
                mechanism=getattr(self.backend, "mechanism", "TEST_BACKEND"),
                confirmation_required=False,
                evidence_before_image=before_image,
            )
            evidence_before = self.audit.evidence_filename(operation, "before")
            return ActionResult(
                "BACKEND_ERROR",
                "Backend action failed; the session was stopped without retry.",
                evidence_before=evidence_before,
            )

        expected = self.policy.expected_postcondition(request.target)
        if expected is not None and after.context != expected:
            self.session.stop("postcondition_mismatch")
            code = "POSTCONDITION_MISMATCH"
            message = "Observed state does not match the literal postcondition."
        else:
            code = "OK"
            message = "Bounded action completed and was verified."

        operation = self.audit.append(
            tool=request.kind.value,
            arguments={"target": request.target, "value": request.value},
            decision=decision.code,
            result=code,
            precondition=before.context,
            observed_postcondition=after.context,
            expected_postcondition=expected,
            config_sha256=self.policy.config_sha256,
            process_id=before.pid,
            window_class=before.window_class,
            project_title=before.title,
            mechanism=getattr(self.backend, "mechanism", "TEST_BACKEND"),
            confirmation_required=request.kind is ActionKind.REQUEST_SAVE,
            evidence_before_image=before_image,
            evidence_after_image=after_image,
        )
        evidence_before = self.audit.evidence_filename(operation, "before")
        evidence_after = self.audit.evidence_filename(operation, "after")
        return ActionResult(
            code,
            message,
            postcondition=after.context,
            evidence_before=evidence_before,
            evidence_after=evidence_after,
        )

    def _perform(self, request: ActionRequest, token: str) -> None:
        if request.kind in {ActionKind.INSPECT, ActionKind.CAPTURE}:
            return
        if request.kind in {ActionKind.RUN_STEP, ActionKind.OPEN_MENU}:
            self.backend.perform_named_step(request.target)
            return
        if request.kind is ActionKind.ACTIVATE:
            self.backend.activate(request.target)
            return
        if request.kind is ActionKind.SET_TEXT:
            if request.value is None:
                raise ValueError("A text value is required.")
            self.backend.set_text(request.target, request.value)
            return
        if request.kind is ActionKind.SEND_SHORTCUT:
            self.backend.send_shortcut(request.target)
            return
        if request.kind is ActionKind.REQUEST_SAVE:
            self.session.request_save(token)
            return
        if request.kind is ActionKind.EMERGENCY_STOP:
            self.session.stop("mcp_emergency_stop", emergency=True)
            return
        raise ValueError(f"Unsupported action kind: {request.kind.value}")
