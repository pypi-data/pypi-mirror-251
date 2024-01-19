import unittest
from unittest.mock import patch

from luminaria.animations import Flame


class TestFlame(unittest.TestCase):
    @patch('random.uniform', side_effect=[0.1, 0.9])
    def test_update(self, _):
        # Create an instance of Flame
        flame = Flame("TestFlame")

        # Verify that we start with a fully extended flame (0.0 - 1.0)
        self.assertEqual(flame.model.from_min, 0.0)
        self.assertEqual(flame.model.from_max, 1.0)

        # Update to 100ms after start. Verify that the flame hasn't moved yet.
        flame.update(100)
        self.assertEqual(flame.model.from_min, 0.0)
        self.assertEqual(flame.model.from_max, 1.0)

        # Update to 120ms after start. Verify that the flame map has updated as expected.
        flame.update(120)
        self.assertEqual(flame.model.from_min, 0.1)
        self.assertEqual(flame.model.from_max, 0.9)


if __name__ == '__main__':
    unittest.main()
