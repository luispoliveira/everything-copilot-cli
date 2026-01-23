import argparse


def project_compound_interest(initial, monthly, annual_rate, years):
    months = years * 12
    monthly_rate = (annual_rate / 100) / 12

    future_value = initial * ((1 + monthly_rate) ** months)
    future_value_contributions = monthly * \
        (((1 + monthly_rate) ** months - 1) / monthly_rate)

    total = future_value + future_value_contributions
    total_invested = initial + (monthly * months)
    total_interest = total - total_invested

    return total, total_invested, total_interest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project Investment Growth")
    parser.add_argument("--initial", type=float,
                        required=True, help="Initial Amount")
    parser.add_argument("--monthly", type=float,
                        required=True, help="Monthly Contribution")
    parser.add_argument("--rate", type=float, required=True,
                        help="Expected Annual Return %")
    parser.add_argument("--years", type=int, required=True,
                        help="Investment Horizon in Years")

    args = parser.parse_args()

    total, invested, interest = project_compound_interest(
        args.initial, args.monthly, args.rate, args.years)

    print(f"--- Investment Projection ({args.years} Years) ---")
    print(
        f"Inputs: {args.initial}€ start + {args.monthly}€/mo at {args.rate}%")
    print(f"\nFinal Balance: {total:,.2f} €")
    print(f"Total Invested: {invested:,.2f} €")
    print(f"Total Interest Earned: {interest:,.2f} €")
