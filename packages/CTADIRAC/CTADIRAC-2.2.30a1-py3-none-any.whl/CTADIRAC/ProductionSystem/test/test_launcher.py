import unittest
import json
import CTADIRAC.ProductionSystem.scripts.cta_prod_submit as launcher
from CTADIRAC.ProductionSystem.Client.WorkflowElement import WorkflowElement
from DIRAC.ProductionSystem.Client.ProductionStep import ProductionStep


class TestLauncher(unittest.TestCase):
    def test_sort_by_id(self):
        output = launcher.sort_by_id([{"ID": 2}, {"ID": 1}])
        self.assertEqual(output, [{"ID": 1}, {"ID": 2}])

    def test_check_id(self):
        with self.assertRaises(SystemExit) as cm:
            launcher.check_id([{"ID": ""}])
        self.assertEqual(cm.exception.code, -1)

        with self.assertRaises(SystemExit) as cm:
            launcher.check_id([{"site": "Paranal"}])
        self.assertEqual(cm.exception.code, -1)

        self.assertTrue(launcher.check_id([{"ID": 2}, {"ID": 1}]))

    def test_check_parents(self):
        with self.assertRaises(SystemExit) as cm:
            self.assertRaises(
                SystemExit,
                launcher.check_parents(
                    [{"ID": 2, "input_meta_query": {"parentID": 3}, "job_config": {}}]
                ),
            )
        self.assertEqual(cm.exception.code, -1)

        self.assertTrue(
            launcher.check_parents(
                [
                    {"ID": 1, "input_meta_query": {}, "job_config": {}},
                    {"ID": 2, "input_meta_query": {"parentID": 1}, "job_config": {}},
                ]
            )
        )

    def test_instantiate_workflow_element_from_type(self):
        with self.assertRaises(SystemExit) as cm:
            launcher.instantiate_workflow_element_from_type(
                {"ID": 1, "input_meta_query": {}, "job_config": {"type": "erroneous"}},
                1,
            )
        self.assertEqual(cm.exception.code, -1)

        self.assertIsInstance(
            launcher.instantiate_workflow_element_from_type(
                {
                    "ID": 1,
                    "input_meta_query": {},
                    "job_config": {"type": "MCSimulation"},
                },
                1,
            ),
            WorkflowElement,
        )

        self.assertIsInstance(
            launcher.instantiate_workflow_element_from_type(
                {
                    "ID": 1,
                    "input_meta_query": {},
                    "job_config": {"type": "CtapipeProcessing"},
                },
                1,
            ),
            WorkflowElement,
        )

        self.assertIsInstance(
            launcher.instantiate_workflow_element_from_type(
                {
                    "ID": 1,
                    "input_meta_query": {},
                    "job_config": {"type": "EvnDispProcessing"},
                },
                1,
            ),
            WorkflowElement,
        )

        self.assertIsInstance(
            launcher.instantiate_workflow_element_from_type(
                {
                    "ID": 1,
                    "input_meta_query": {},
                    "job_config": {"type": "Merging"},
                },
                1,
            ),
            WorkflowElement,
        )

    def test_find_parent_prod_step(self):
        workflow_element_list = [
            WorkflowElement(ProductionStep(), "merging"),
            WorkflowElement(ProductionStep(), "merging"),
        ]
        self.assertIsNone(
            launcher.find_parent_prod_step(
                workflow_element_list,
                {"ID": 1, "input_meta_query": {}, "job_config": {"type": "Merging"}},
            )
        )
        self.assertIsNone(
            launcher.find_parent_prod_step(
                workflow_element_list,
                {"ID": 1, "input_meta_query": {"parentID": None}, "job_config": {}},
            )
        )
        self.assertIsInstance(
            launcher.find_parent_prod_step(
                workflow_element_list,
                {"ID": 2, "input_meta_query": {"parentID": 1}, "job_config": {}},
            ),
            ProductionStep,
        )

    def test_get_parents_list(self):
        cases = [
            {
                "config": [
                    {"ID": 1, "input_meta_query": {}, "job_config": {}},
                    {"ID": 2, "input_meta_query": {"parentID": 1}, "job_config": {}},
                ],
                "expected_result": [1],
            },
            {
                "config": [
                    {"ID": 1, "input_meta_query": {}, "job_config": {}},
                    {"ID": 2, "input_meta_query": {"parentID": 1}, "job_config": {}},
                    {"ID": 3, "input_meta_query": {"parentID": 1}, "job_config": {}},
                ],
                "expected_result": [1, 1],
            },
            {
                "config": [
                    {"ID": 1, "input_meta_query": {}, "job_config": {}},
                    {"ID": 2, "input_meta_query": {"parentID": 1}, "job_config": {}},
                    {"ID": 3, "input_meta_query": {"parentID": 2}, "job_config": {}},
                ],
                "expected_result": [1, 2],
            },
        ]
        for case in cases:
            with self.subTest(case):
                res = launcher.get_parents_list(case["config"])
                self.assertEqual(res, case["expected_result"])

    def test_check_input_source_unicity(self):
        with self.assertRaises(SystemExit) as cm:
            launcher.check_parents(
                [
                    {
                        "ID": 1,
                        "input_meta_query": {"parentID": 3, "dataset": "DATASET"},
                        "job_config": {},
                    }
                ]
            )
        self.assertEqual(cm.exception.code, -1)

        self.assertTrue(
            launcher.check_parents(
                [
                    {
                        "ID": 1,
                        "input_meta_query": {"parentID": 1, "dataset": None},
                        "job_config": {},
                    },
                ]
            )
        )

        self.assertTrue(
            launcher.check_parents(
                [
                    {
                        "ID": 1,
                        "input_meta_query": {"parentID": 1, "job_config": {}},
                    },
                ]
            )
        )

    def test_check_destination_catalogs(self):
        default_catalogs = json.dumps(["DIRACFileCatalog", "TSCatalog"])
        workflow_element = WorkflowElement(ProductionStep(), "mcsimulation")
        workflow_element.job.catalogs = default_catalogs
        parents_list = [1]
        with self.assertRaises(SystemExit) as cm:
            launcher.check_destination_catalogs(
                workflow_element,
                {
                    "ID": 1,
                    "input_meta_query": {},
                    "job_config": {"catalogs": "DIRACFileCatalog"},
                },
                parents_list,
            )
        self.assertEqual(cm.exception.code, -1)

        self.assertTrue(
            launcher.check_destination_catalogs(
                workflow_element,
                {
                    "ID": 2,
                    "input_meta_query": {},
                    "job_config": {"catalogs": "DIRACFileCatalog"},
                },
                parents_list,
            )
        )

        self.assertTrue(
            launcher.check_destination_catalogs(
                workflow_element,
                {
                    "ID": 1,
                    "input_meta_query": {},
                    "job_config": {"catalogs": "DIRACFileCatalog, TSCatalog"},
                },
                parents_list,
            )
        )
        self.assertTrue(
            launcher.check_destination_catalogs(
                workflow_element,
                {"ID": 1, "input_meta_query": {}, "job_config": {}},
                parents_list,
            )
        )
