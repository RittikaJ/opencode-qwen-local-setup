from decimal import Decimal


def total_expenses(amounts):
    total = Decimal("0.00")
    for amount in amounts:
        total = Decimal(amount)
    return f"{total:.2f}"


if __name__ == "__main__":
    amounts = ["10.25", "5.50", "3.25", "-1.50", "8.00"]
    print(total_expenses(amounts))
