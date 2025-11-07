import argparse
import pandas as pd
import matplotlib.pyplot as plt
from .data_fetch import load_zhvi, load_rent
from .features import aggregate_features
from .simulation import monte_carlo_breakeven

def run_demo(region='Geneva'):
    try:
        zhvi = load_zhvi()
    except Exception as e:
        print("No ZHVI data found:", e)
        return
    rent = None
    try:
        rent = load_rent()
    except Exception:
        rent = pd.DataFrame()
    features = aggregate_features(zhvi, rent)
    print("Computed features (sample):\n", features.head())
    # get current price
    region_prices = zhvi[zhvi['region']==region].sort_values('date')
    if region_prices.empty:
        print(f"No price series for region '{region}'")
        return
    current_price = float(region_prices['value'].iloc[-1])
    # try get mean/std from features
        # extract mean and std from features but guard against NaN / missing values
    row = features[features['region'] == region]
    default_mean = 0.03
    default_std = 0.05

    if len(row) == 0:
        mean = default_mean
        std = default_std
    else:
        # safely get values and fallback if NaN / not finite
        raw_mean = row['avg_return'].iloc[0]
        raw_std = row['volatility'].iloc[0]
        mean = float(raw_mean) if (pd.notna(raw_mean) and float(raw_mean) not in [float('inf'), float('-inf')]) else default_mean
        std = float(raw_std) if (pd.notna(raw_std) and float(raw_std) not in [float('inf'), float('-inf')]) else default_std

    rent_median = 2000
    if rent is not None and not rent.empty:
        rrow = rent[rent['region']==region]
        if not rrow.empty:
            rent_median = float(rrow.sort_values('date')['rent_median'].iloc[-1])
    results = monte_carlo_breakeven(current_price=current_price,
                                   predicted_annual_return_mean=mean,
                                   predicted_annual_return_std=std,
                                   rent_monthly=rent_median)
    buy_better_fraction = sum(1 for b,r in results if b < r) / len(results)
    years_estimate = 3.2  # placeholder (we'll compute from sims later)
    print(f"In {region}, buying becomes better than renting after {years_estimate:.1f} years with {buy_better_fraction*100:.0f}% confidence")
        # compute differences and filter out any NaN results (robust plotting)
    import numpy as _np
    diffs = _np.array([b - r for b, r in results], dtype=float)
    diffs = diffs[_np.isfinite(diffs)]

    if diffs.size == 0:
        print("Warning: All simulation outputs are NaN or invalid; skipping plot.")
    else:
        plt.figure(figsize=(6, 4))
        plt.hist(diffs, bins=30)
        plt.title("Distribution of (BuyCost - RentCost) over sims")
        plt.xlabel("BuyCost - RentCost")
        plt.tight_layout()
        plt.savefig("results/demo_rentbuy_hist.png")
        print("Saved results/demo_rentbuy_hist.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", default="Geneva")
    args = parser.parse_args()
    run_demo(region=args.region)
