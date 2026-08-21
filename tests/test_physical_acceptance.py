from pathlib import Path

import pytest

from hoofcare.physical.acceptance import PhysicalPrototypeAcceptance


def test_physical_prototype_acceptance_passes_end_to_end(tmp_path: Path) -> None:
    result = PhysicalPrototypeAcceptance.synthetic(tmp_path).run()

    assert result.status == "PASS"
    assert result.checks["screen_layout"] == "PASS"
    assert result.checks["navigation"] == "PASS"
    assert result.checks["persistence_restart"] == "PASS"
    assert result.checks["local_report"] == "PASS"
    assert result.checks["synthetic_only"] == "PASS"
    assert result.checks["no_kvk_connection"] == "PASS"
    assert result.checks["no_machine_control_surface"] == "PASS"
    assert result.report_pdf.startswith(b"%PDF-1.4")


def test_physical_prototype_acceptance_rejects_machine_control_action(tmp_path: Path) -> None:
    acceptance = PhysicalPrototypeAcceptance.synthetic(tmp_path)

    with pytest.raises(ValueError, match="machine-control"):
        acceptance.assert_action_allowed("plc_write")


def test_physical_prototype_acceptance_is_not_field_acceptance(tmp_path: Path) -> None:
    result = PhysicalPrototypeAcceptance.synthetic(tmp_path).run()

    assert result.field_kvk_verified is False
    assert result.real_farm_data_used is False
    assert result.deployment_ready is False
