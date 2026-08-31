# SPDX-License-Identifier: BSD-3-Clause

'''Check the mathematical behavior of the first reusable course module.'''

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from urllib.request import urlretrieve

import numpy as np

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / 'src/phugoid.py'
)
# Load the maintained source for these author-side tests without installing it.
spec = importlib.util.spec_from_file_location('phugoid', MODULE_PATH)
phugoid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phugoid)
discrete_l1_difference = phugoid.discrete_l1_difference
euler_step = phugoid.euler_step
rhs_full_phugoid = phugoid.rhs_full_phugoid


class PhugoidTests(unittest.TestCase):
    def test_downloaded_file_imports_without_installation(self):
        # A local file URL keeps this check offline until the source is published.
        with TemporaryDirectory() as notebook_dir:
            filename = Path(notebook_dir) / 'phugoid.py'
            urlretrieve(MODULE_PATH.as_uri(), filename)
            self.assertEqual(filename.read_bytes(), MODULE_PATH.read_bytes())
            subprocess.run(
                [
                    sys.executable,
                    '-c',
                    'from pathlib import Path; '
                    'import phugoid; '
                    'assert Path(phugoid.__file__).resolve() '
                    '== Path("phugoid.py").resolve(); '
                    'assert callable(phugoid.euler_step); '
                    'assert callable(phugoid.rhs_full_phugoid); '
                    'assert callable(phugoid.discrete_l1_difference)',
                ],
                cwd=notebook_dir,
                check=True,
            )

    def test_rhs_at_horizontal_trim_speed(self):
        u = np.array([5.0, 0.0, 3.0, 20.0])
        original = u.copy()
        actual = rhs_full_phugoid(u, 1.0, 0.2, 10.0, 5.0)
        np.testing.assert_allclose(actual, [-2.0, 0.0, 5.0, 0.0])
        np.testing.assert_array_equal(u, original)

    def test_drag_free_trim(self):
        actual = rhs_full_phugoid(
            np.array([5.0, 0.0, 3.0, 20.0]), 1.0, 0.0, 10.0, 5.0
        )
        np.testing.assert_allclose(actual, [0.0, 0.0, 5.0, 0.0])

    def test_euler_forwards_parameters_and_preserves_input(self):
        def rhs(u, a, b):
            return np.array([u[1] + a, b * u[0]])

        u = np.array([2.0, -1.0])
        original = u.copy()
        actual = euler_step(u, rhs, 0.1, 3.0, 4.0)
        np.testing.assert_allclose(actual, [2.2, -0.2])
        np.testing.assert_array_equal(u, original)
        self.assertFalse(np.shares_memory(actual, u))

    def test_difference_aligns_nested_grids(self):
        coarse = np.array([0.0, 2.0, 4.0])
        fine = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
        self.assertAlmostEqual(
            discrete_l1_difference(coarse, fine, 0.5, 0.25), 1.5
        )

    def test_difference_on_identical_grids(self):
        q = np.array([0.0, 2.0, 4.0])
        self.assertEqual(discrete_l1_difference(q, q, 0.5, 0.5), 0.0)

    def test_difference_rejects_nonnested_spacing(self):
        with self.assertRaisesRegex(ValueError, 'nested grids'):
            discrete_l1_difference(
                np.zeros(3), np.zeros(4), 0.3, 0.2
            )

    def test_difference_rejects_mismatched_endpoints(self):
        with self.assertRaisesRegex(ValueError, 'endpoints or sample counts'):
            discrete_l1_difference(
                np.zeros(3), np.zeros(7), 0.5, 0.25
            )

    def test_module_matches_lesson_three_definitions(self):
        # The originating notebook remains a readable reference.
        lesson_path = (
            Path(__file__).resolve().parents[1]
            / 'book/modules/01-phugoid/03-full-model.ipynb'
        )
        with lesson_path.open(encoding='utf-8') as lesson_file:
            notebook = json.load(lesson_file)

        reference = {'np': np}
        names = (
            'rhs_full_phugoid',
            'euler_step',
            'discrete_l1_difference',
        )
        for cell in notebook['cells']:
            source = ''.join(cell['source'])
            if cell['cell_type'] == 'code' and any(
                source.startswith(f'def {name}(') for name in names
            ):
                exec(compile(source, str(lesson_path), 'exec'), reference)

        state = np.array([6.5, -0.1, 0.0, 2.0])
        reference_state = state.copy()
        parameters = (1.0, 0.2, 9.81, 4.9)
        for _ in range(100):
            state = euler_step(
                state, rhs_full_phugoid, 0.01, *parameters
            )
            reference_state = reference['euler_step'](
                reference_state,
                reference['rhs_full_phugoid'],
                0.01,
                *parameters,
            )
        np.testing.assert_array_equal(state, reference_state)

        coarse = np.array([0.0, 2.0, 4.0])
        fine = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
        self.assertEqual(
            discrete_l1_difference(coarse, fine, 0.5, 0.25),
            reference['discrete_l1_difference'](
                coarse, fine, 0.5, 0.25
            ),
        )


if __name__ == '__main__':
    unittest.main()
