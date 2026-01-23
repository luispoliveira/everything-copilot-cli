import argparse


def calculate_mortgage(principal, annual_rate, years):
    """
    Calculates monthly mortgage payment using the amortization formula.
    M = P [ i(1 + i)^n ] / [ (1 + i)^n - 1 ]
    """
    if annual_rate == 0:
        return principal / (years * 12)

    monthly_rate = (annual_rate / 100) / 12
    num_payments = years * 12

    numerator = monthly_rate * ((1 + monthly_rate) ** num_payments)
    denominator = ((1 + monthly_rate) ** num_payments) - 1

    monthly_payment = principal * (numerator / denominator)
    total_payment = monthly_payment * num_payments
    total_interest = total_payment - principal

    return monthly_payment, total_payment, total_interest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate Mortgage Payments")
    parser.add_argument("--amount", type=float,
                        required=True, help="Loan Amount (€)")
    parser.add_argument("--rate", type=float, required=True,
                        help="Annual Interest Rate % (Euribor + Spread)")
    parser.add_argument("--years", type=int, required=True,
                        help="Loan Term in Years")

    args = parser.parse_args()

    monthly, total, interest = calculate_mortgage(
        args.amount, args.rate, args.years)

    print(f"--- Mortgage Simulation ---")
    print(f"Loan Amount: {args.amount:,.2f} €")
    print(f"Rate: {args.rate}% | Term: {args.years} years")
    print(f"\nMonthly Payment: {monthly:,.2f} €")
    print(f"Total Cost: {total:,.2f} €")
    print(f"Total Interest: {interest:,.2f} €")
