import argparse


def calculate_capital_gains_tax(profit, asset_type="general", years_held=0):
    """
    Calculates tax on capital gains in Portugal.
    Default: 28%
    PPR: sliding scale based on years.
    """
    rate = 0.28

    if asset_type.lower() == "ppr":
        if years_held < 5:
            rate = 0.215
        elif 5 <= years_held <= 8:
            rate = 0.172
        else:
            rate = 0.086

    tax = profit * rate
    net_profit = profit - tax
    return tax, net_profit, rate


def estimate_net_salary(gross_monthly):
    """
    Very rough estimate of Portuguese Net Salary (Single, No Dependents).
    Includes 11% SS + Estimated IRS retention.
    NOT LEGAL ADVICE.
    """
    ss_tax = gross_monthly * 0.11

    # Rough IRS brackets 2024 approximation for retention
    irs_rate = 0.0
    if gross_monthly < 820:
        irs_rate = 0.0
    elif gross_monthly < 1000:
        irs_rate = 0.13
    elif gross_monthly < 1500:
        irs_rate = 0.18
    elif gross_monthly < 2000:
        irs_rate = 0.22
    elif gross_monthly < 2500:
        irs_rate = 0.26
    elif gross_monthly < 3500:
        irs_rate = 0.30
    else:
        irs_rate = 0.35  # capped for estimation

    irs_tax = gross_monthly * irs_rate
    net = gross_monthly - ss_tax - irs_tax
    return net, ss_tax, irs_tax


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Portuguese Tax Estimator")
    parser.add_argument(
        "--mode", choices=["capital_gains", "salary"], required=True)

    # Capital Gains args
    parser.add_argument("--profit", type=float,
                        help="Profit amount for capital gains")
    parser.add_argument("--type", default="general",
                        choices=["general", "ppr"], help="Asset type")
    parser.add_argument("--years", type=int, default=0,
                        help="Years held (for PPR)")

    # Salary args
    parser.add_argument("--gross", type=float, help="Gross Monthly Salary")

    args = parser.parse_args()

    if args.mode == "capital_gains":
        if args.profit is None:
            print("Error: --profit required for capital_gains mode")
        else:
            tax, net, rate = calculate_capital_gains_tax(
                args.profit, args.type, args.years)
            print(f"--- Capital Gains Tax ({args.type.upper()}) ---")
            print(f"Profit: {args.profit:.2f} €")
            print(f"Tax Rate: {rate*100:.1f}%")
            print(f"Tax to Pay: {tax:.2f} €")
            print(f"Net Profit: {net:.2f} €")

    elif args.mode == "salary":
        if args.gross is None:
            print("Error: --gross required for salary mode")
        else:
            net, ss, irs = estimate_net_salary(args.gross)
            print(f"--- Net Salary Estimate (Rough) ---")
            print(f"Gross: {args.gross:.2f} €")
            print(f"Social Security (11%): -{ss:.2f} €")
            print(f"Est. IRS Retention: -{irs:.2f} €")
            print(f"Est. Net: {net:.2f} €")
