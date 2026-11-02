import unittest

from iaa import cohen_kappa, disagreements, fleiss_kappa, interpret, percent_agreement


class TestAgreement(unittest.TestCase):
    def test_perfect_agreement(self):
        self.assertAlmostEqual(cohen_kappa(["a", "b", "a"], ["a", "b", "a"]), 1.0)

    def test_cohen_known_value(self):
        # 20 items: both "yes" 10, both "no" 5, a-yes/b-no 2, a-no/b-yes 3 -> kappa = (0.75 - 0.53) / 0.47 ~= 0.468
        a = ["yes"] * 10 + ["no"] * 5 + ["yes"] * 2 + ["no"] * 3
        b = ["yes"] * 10 + ["no"] * 5 + ["no"] * 2 + ["yes"] * 3
        self.assertAlmostEqual(cohen_kappa(a, b), 0.4681, places=3)

    def test_fleiss_wikipedia_example(self):
        # Classic Fleiss (1971) style check: identical labels -> 1.0
        data = {str(i): {"x": "a", "y": "a", "z": "a"} for i in range(3)}
        data["3"] = {"x": "b", "y": "b", "z": "b"}
        self.assertAlmostEqual(fleiss_kappa(data), 1.0)

    def test_percent_and_disagreements(self):
        data = {"1": {"x": "a", "y": "a"}, "2": {"x": "a", "y": "b"}}
        self.assertEqual(percent_agreement(data), 0.5)
        self.assertEqual(list(disagreements(data)), ["2"])

    def test_interpret(self):
        self.assertEqual(interpret(0.7), "substantial")
        self.assertEqual(interpret(-0.1), "poor")


if __name__ == "__main__":
    unittest.main()
