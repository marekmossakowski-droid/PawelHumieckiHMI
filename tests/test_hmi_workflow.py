import unittest

from hoofcare.hmi.workflow import (
    AnatomicalZone,
    Claw,
    HMIWorkflow,
    Limb,
    LesionCode,
    WorkflowStep,
)


class HMIWorkflowTests(unittest.TestCase):
    def test_dashboard_exposes_required_banner_and_committed_counters(self):
        workflow = HMIWorkflow.synthetic()
        dashboard = workflow.dashboard(completed_animals=7, consumed_dressings=12)
        self.assertEqual(dashboard.banner, "Paweł Humięcki the best zootechnik")
        self.assertEqual(dashboard.completed_animals, 7)
        self.assertEqual(dashboard.consumed_dressings, 12)
        self.assertFalse(hasattr(dashboard, "kvk_commands"))

    def test_workflow_requires_limb_then_claw_then_zone_then_lesion(self):
        workflow = HMIWorkflow.synthetic()
        self.assertEqual(workflow.step, WorkflowStep.LIMB)
        workflow = workflow.select_limb(Limb.REAR_LEFT)
        self.assertEqual(workflow.step, WorkflowStep.CLAW)
        workflow = workflow.select_claw(Claw.LATERAL)
        self.assertEqual(workflow.step, WorkflowStep.ZONE)
        workflow = workflow.select_zone(AnatomicalZone.INTERDIGITAL_SPACE)
        self.assertEqual(workflow.step, WorkflowStep.LESION)
        workflow = workflow.select_lesion(LesionCode.INTERDIGITAL_DERMATITIS)
        self.assertEqual(workflow.step, WorkflowStep.TREATMENT)

    def test_anatomical_zone_set_contains_verified_required_areas(self):
        self.assertEqual(
            {zone.value for zone in AnatomicalZone},
            {
                "TOE",
                "SOLE",
                "WHITE_LINE",
                "AXIAL_WALL",
                "ABAXIAL_WALL",
                "HEEL_BULB",
                "SOFT_HEEL_TISSUE",
                "INTERDIGITAL_SPACE",
            },
        )

    def test_interdigital_and_soft_heel_lesions_are_selectable(self):
        self.assertIn(LesionCode.INTERDIGITAL_DERMATITIS, tuple(LesionCode))
        self.assertIn(LesionCode.DIGITAL_DERMATITIS, tuple(LesionCode))
        self.assertIn(LesionCode.HEEL_HORN_EROSION, tuple(LesionCode))

    def test_no_machine_control_affordance_is_exposed(self):
        public_names = {name for name in dir(HMIWorkflow) if not name.startswith("_")}
        forbidden_fragments = {"gate", "strap", "winch", "lift", "valve", "hydraulic", "kvk_command", "actuate"}
        lowered = {name.lower() for name in public_names}
        self.assertTrue(all(not any(fragment in name for fragment in forbidden_fragments) for name in lowered))

    def test_out_of_order_selection_fails_closed(self):
        workflow = HMIWorkflow.synthetic()
        with self.assertRaises(ValueError):
            workflow.select_zone(AnatomicalZone.SOLE)


if __name__ == "__main__":
    unittest.main()
