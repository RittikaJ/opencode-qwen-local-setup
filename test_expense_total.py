import unittest

from expense_total import total_expenses


class ExpenseTotalTests(unittest.TestCase):
    def test_sample_expenses(self):
        self.assertEqual(
            total_expenses(["10.25", "5.50", "3.25", "-1.50", "8.00"]),
            "25.50",
        )

    def test_refund(self):
        self.assertEqual(total_expenses(["10.00", "-2.50"]), "7.50")

    def test_decimal_arithmetic(self):
        self.assertEqual(total_expenses(["0.10", "0.20"]), "0.30")

    def test_empty_input(self):
        self.assertEqual(total_expenses([]), "0.00")

    def test_single_expense(self):
        self.assertEqual(total_expenses(["8.00"]), "8.00")


if __name__ == "__main__":
    unittest.main()
