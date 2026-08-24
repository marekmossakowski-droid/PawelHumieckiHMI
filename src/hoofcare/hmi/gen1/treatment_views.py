from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from hoofcare.domain.clinical import CanonicalClinicalRecord
from hoofcare.domain.session import IdentityStatus, Session, SessionState
from hoofcare.hmi.workflow import (
    HMIWorkflow,
    TreatmentStep,
    complete_synthetic_wizard,
)


_DEVICE_UNAVAILABLE = "NIEDOSTĘPNE W GENERACJI 1 / AUTHORITY REQUIRED"

_STEP_PRESENTATION = {
    TreatmentStep.IDENTITY: ("G1-30", "Identyfikacja zwierzęcia"),
    TreatmentStep.LIMB_CLAW: ("G1-31", "Kończyna i racica"),
    TreatmentStep.ZONE_LESION: ("G1-32", "Strefa i zmiana"),
    TreatmentStep.TREATMENT: ("G1-33", "Zabieg"),
    TreatmentStep.MATERIALS: ("G1-34", "Materiały dodatkowe"),
    TreatmentStep.FOLLOW_UP: ("G1-35", "Termin kontroli"),
    TreatmentStep.SUMMARY: ("G1-36", "Podsumowanie krowy"),
}

_STEP_REQUIREMENTS = {
    TreatmentStep.IDENTITY: ("animal_identity",),
    TreatmentStep.LIMB_CLAW: ("limb", "claw"),
    TreatmentStep.ZONE_LESION: ("zone", "lesion"),
    TreatmentStep.TREATMENT: ("treatment",),
    TreatmentStep.MATERIALS: ("materials",),
    TreatmentStep.FOLLOW_UP: ("follow_up_decision",),
}

_ACTION_LABELS_PL = {
    "manual_identity": "WPROWADŹ RĘCZNIE",
    "cancel": "ANULUJ",
    "next": "DALEJ",
    "back": "WSTECZ",
    "save_draft": "ZAPISZ SZKIC",
    "complete_cow": "ZAKOŃCZ",
    "open_reconciliation": "UZGODNIJ",
}


@dataclass(frozen=True)
class TreatmentMaterialView:
    code: str
    label: str
    quantity: float
    unit: str


@dataclass(frozen=True)
class TreatmentActionView:
    action_id: str
    label_pl: str


@dataclass(frozen=True)
class TreatmentWizardView:
    step: TreatmentStep
    route_id: str
    title_pl: str
    required_fields: tuple[str, ...]
    missing_fields: tuple[str, ...]
    materials: tuple[TreatmentMaterialView, ...]
    prices_visible: bool
    primary_actions: tuple[str, ...]
    action_labels_pl: tuple[TreatmentActionView, ...]
    camera_status: str
    rfid_status: str
    follow_up_due_date: date | None
    recovery_required: bool
    completion_ready: bool


def _validate_inputs(
    session: Session,
    step: TreatmentStep,
    workflow: HMIWorkflow | None,
    clinical_record: CanonicalClinicalRecord | None,
    follow_up_decided: bool,
    follow_up_due_date: date | None,
    durable_write_ready: bool,
) -> None:
    if not isinstance(session, Session):
        raise ValueError("session must be a Session")
    if not isinstance(step, TreatmentStep):
        raise ValueError("step must be a TreatmentStep")
    if workflow is not None and not isinstance(workflow, HMIWorkflow):
        raise ValueError("workflow must be an HMIWorkflow")
    if clinical_record is not None and not isinstance(
        clinical_record, CanonicalClinicalRecord
    ):
        raise ValueError("clinical_record must be a CanonicalClinicalRecord")
    if type(follow_up_decided) is not bool:
        raise ValueError("follow_up_decided must be boolean")
    if follow_up_due_date is not None and (
        not isinstance(follow_up_due_date, date)
        or isinstance(follow_up_due_date, datetime)
    ):
        raise ValueError("follow_up_due_date must be a date")
    if type(durable_write_ready) is not bool:
        raise ValueError("durable_write_ready must be boolean")


def _record_matches(
    session: Session,
    clinical_record: CanonicalClinicalRecord | None,
) -> bool:
    return (
        clinical_record is not None
        and clinical_record.session_id == session.session_id
        and clinical_record.animal_id == session.animal_id
        and clinical_record.synthetic_test_only
    )


def _missing_fields(
    session: Session,
    workflow: HMIWorkflow | None,
    clinical_record: CanonicalClinicalRecord | None,
    follow_up_decided: bool,
    follow_up_due_date: date | None,
    durable_write_ready: bool,
) -> dict[str, bool]:
    record_matches = _record_matches(session, clinical_record)
    clinical_selection_matches = (
        record_matches
        and workflow is not None
        and workflow.zone is not None
        and workflow.lesion is not None
        and clinical_record.lesion.anatomical_zone == workflow.zone.value
        and clinical_record.lesion.code == workflow.lesion.value
    )
    treatment_refs_match = (
        record_matches
        and tuple(item.code for item in clinical_record.treatments)
        == session.treatment_refs
    )
    material_refs_match = (
        record_matches
        and tuple(item.code for item in clinical_record.materials)
        == session.material_refs
    )
    follow_up_consistent = follow_up_decided and (
        (
            session.state is SessionState.FOLLOW_UP_REQUIRED
            and follow_up_due_date is not None
        )
        or (
            session.state is SessionState.IN_PROGRESS
            and follow_up_due_date is None
        )
    )
    return {
        "animal_identity": not (
            session.identity.status is IdentityStatus.CONFIRMED
            and bool(session.animal_id)
        ),
        "limb": workflow is None or workflow.limb is None,
        "claw": workflow is None or workflow.claw is None,
        "zone": workflow is None or workflow.zone is None,
        "lesion": workflow is None or workflow.lesion is None,
        "treatment": not (
            record_matches
            and bool(clinical_record.treatments)
            and treatment_refs_match
        ),
        "materials": not (
            record_matches
            and bool(clinical_record.materials)
            and material_refs_match
        ),
        "follow_up_decision": not follow_up_consistent,
        "clinical_selection_match": not clinical_selection_matches,
        "canonical_record_match": not record_matches,
        "canonical_record_committed": not (
            record_matches and clinical_record.committed
        ),
        "durable_write_ready": not durable_write_ready,
        "session_completable": session.state
        not in {SessionState.IN_PROGRESS, SessionState.FOLLOW_UP_REQUIRED},
    }


def _requirements_for(step: TreatmentStep) -> tuple[str, ...]:
    if step is not TreatmentStep.SUMMARY:
        return _STEP_REQUIREMENTS[step]
    return (
        "animal_identity",
        "limb",
        "claw",
        "zone",
        "lesion",
        "treatment",
        "materials",
        "follow_up_decision",
        "clinical_selection_match",
        "canonical_record_match",
        "canonical_record_committed",
        "durable_write_ready",
        "session_completable",
    )


def _actions_for(
    step: TreatmentStep,
    missing_fields: tuple[str, ...],
) -> tuple[str, ...]:
    if step is TreatmentStep.IDENTITY:
        if missing_fields:
            return ("manual_identity", "cancel")
        return ("next", "cancel")
    if step is TreatmentStep.SUMMARY:
        if not missing_fields:
            return ("back", "save_draft", "complete_cow")
        return ("back", "save_draft", "open_reconciliation")
    actions = ["back", "save_draft"]
    if not missing_fields:
        actions.append("next")
    return tuple(actions)


def project_treatment_step(
    session: Session,
    step: TreatmentStep,
    *,
    workflow: HMIWorkflow | None = None,
    clinical_record: CanonicalClinicalRecord | None = None,
    follow_up_decided: bool = False,
    follow_up_due_date: date | None = None,
    durable_write_ready: bool = False,
) -> TreatmentWizardView:
    _validate_inputs(
        session,
        step,
        workflow,
        clinical_record,
        follow_up_decided,
        follow_up_due_date,
        durable_write_ready,
    )
    requirements = _requirements_for(step)
    missing_map = _missing_fields(
        session,
        workflow,
        clinical_record,
        follow_up_decided,
        follow_up_due_date,
        durable_write_ready,
    )
    missing = tuple(field for field in requirements if missing_map[field])
    completion_ready = step is TreatmentStep.SUMMARY and not missing
    materials = ()
    if _record_matches(session, clinical_record):
        materials = tuple(
            TreatmentMaterialView(item.code, item.label, item.quantity, item.unit)
            for item in clinical_record.materials
        )
    route_id, title_pl = _STEP_PRESENTATION[step]
    primary_actions = _actions_for(step, missing)
    return TreatmentWizardView(
        step=step,
        route_id=route_id,
        title_pl=title_pl,
        required_fields=requirements,
        missing_fields=missing,
        materials=materials,
        prices_visible=False,
        primary_actions=primary_actions,
        action_labels_pl=tuple(
            TreatmentActionView(action, _ACTION_LABELS_PL[action])
            for action in primary_actions
        ),
        camera_status=_DEVICE_UNAVAILABLE,
        rfid_status=_DEVICE_UNAVAILABLE,
        follow_up_due_date=follow_up_due_date,
        recovery_required=step is TreatmentStep.SUMMARY and not completion_ready,
        completion_ready=completion_ready,
    )


def allowed_treatment_actions(
    session: Session,
    step: TreatmentStep,
    *,
    workflow: HMIWorkflow | None = None,
    clinical_record: CanonicalClinicalRecord | None = None,
    follow_up_decided: bool = False,
    follow_up_due_date: date | None = None,
    durable_write_ready: bool = False,
) -> tuple[str, ...]:
    return project_treatment_step(
        session,
        step,
        workflow=workflow,
        clinical_record=clinical_record,
        follow_up_decided=follow_up_decided,
        follow_up_due_date=follow_up_due_date,
        durable_write_ready=durable_write_ready,
    ).primary_actions
