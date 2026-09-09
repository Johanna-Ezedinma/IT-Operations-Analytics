"""
clean_vectral_data.py

Runs the full cleaning recipe for the Vectral dataset, start to finish,
with no manual review steps - every decision below was already made and
reviewed in the project's Data Profiling & Cleaning writeup. This script
just re-executes those exact decisions so the raw data can be cleaned
again from scratch at any time (e.g. if the source files change).

This is NOT the toolkit - cleaning_utils.py and profiling.py are the
reusable toolkit. This script is the one-time "recipe" for THIS dataset,
built out of that toolkit.

Usage:
    python clean_vectral_data.py --raw-dir data/raw --out-dir data/clean

Input:  customers.csv, orders.csv, sales.csv, vendors.csv,
        product_usage.csv, experiment.csv  (in --raw-dir)
Output: the same six filenames, cleaned, written to --out-dir
"""

import argparse
import sys
import pandas as pd


from .cleaning_utils import (
    remove_duplicates,
    remove_duplicate_keys,
    remove_orphaned_rows,
    standardize_categories,
    label_missing,
)

COUNTRY_MAP = {
    'US': 'United States', 'USA': 'United States', 'United States': 'United States',
    'UK': 'United Kingdom', 'United Kingdom': 'United Kingdom',
    'Australia': 'Australia', 'Canada': 'Canada', 'France': 'France', 'Germany': 'Germany',
    'Netherlands': 'Netherlands', 'Nigeria': 'Nigeria', 'Singapore': 'Singapore',
}


def clean_customers(raw_dir):
    print("\n=== customers.csv ===")
    df = pd.read_csv(f"{raw_dir}/customers.csv")
    start = len(df)

    # 2 exact-duplicate rows (CUST-0018, CUST-0064) -> keep one copy
    df, conflicts = remove_duplicate_keys(df, 'customer_id', confirm=True)
    assert len(conflicts) == 0, "Unexpected conflicting customer_id found - stop and investigate, don't silently proceed."

    # 12 country spellings -> 9 real countries
    df = standardize_categories(df, 'country', COUNTRY_MAP)

    # 2 missing country values, both real active customers -> label, don't delete
    df = label_missing(df, 'country', 'Unknown')

    print(f"customers.csv: {start} -> {len(df)} rows")
    return df


def clean_orders(raw_dir):
    print("\n=== orders.csv ===")
    df = pd.read_csv(f"{raw_dir}/orders.csv")
    start = len(df)

    # 2 order_ids, 4 rows total, each pair describes two DIFFERENT orders
    # (different customer/device/value) sharing one ID - can't tell which
    # is real, so both rows in each pair are dropped, not just one.
    df, conflicts = remove_duplicate_keys(df, 'order_id', confirm=True)
    if len(conflicts) > 0:
        conflicting_ids = conflicts['order_id'].unique().tolist()
        df = df[~df['order_id'].isin(conflicting_ids)].reset_index(drop=True)
        print(f"  Also removed {len(conflicts)} rows under conflicting IDs {conflicting_ids} "
              f"(both rows in each pair, per the reviewed decision - not a guess made here).")

    df = standardize_categories(df, 'country', COUNTRY_MAP)
    df = label_missing(df, 'country', 'Unknown')

    # delivery_date: left blank on purpose. All blanks belong to orders that
    # are Cancelled, Failed, or still In Transit - nothing to fill in, this
    # is a correct blank, not missing data. No action needed here.

    # Fulfilment Days: derived column (delivery_date - order_date), built
    # the same way as the Power Query version, including the same
    # try/otherwise-null handling for orders with no delivery_date yet.
    order_dt = pd.to_datetime(df['order_date'], errors='coerce')
    delivery_dt = pd.to_datetime(df['delivery_date'], errors='coerce')
    df['fulfilment_days'] = (delivery_dt - order_dt).dt.days

    # device_model: NOT cleaned or trusted. It doesn't reliably correspond
    # to device_type (confirmed during profiling), so it's left as-is in
    # the data but should not be used in any analysis without confirming
    # with the data owner first.

    print(f"orders.csv: {start} -> {len(df)} rows")
    return df


def clean_sales(raw_dir):
    print("\n=== sales.csv ===")
    df = pd.read_csv(f"{raw_dir}/sales.csv")
    start = len(df)

    df = standardize_categories(df, 'country', COUNTRY_MAP)
    df = label_missing(df, 'country', 'Unknown')

    # lost_reason: only the 3 blanks that belong to Lost deals get labeled.
    # Blanks for Won/open leads are correct as-is (there's no "reason" for
    # a deal that hasn't been lost) and must NOT be touched.
    lost_and_blank = (df['outcome'] == 'Lost') & (df['lost_reason'].isna())
    n_fixed = lost_and_blank.sum()
    df.loc[lost_and_blank, 'lost_reason'] = 'Unknown'
    print(f"'lost_reason': labeled {n_fixed} blank value(s) as 'Unknown' (Lost deals only).")

    # outcome / date_converted blanks (334 open leads), and lost_reason
    # blanks for Won/open leads: left exactly as-is. These represent a
    # real "not decided yet" state, not missing data - no action needed.

    print(f"sales.csv: {start} -> {len(df)} rows")
    return df


def clean_vendors(raw_dir):
    print("\n=== vendors.csv ===")
    df = pd.read_csv(f"{raw_dir}/vendors.csv")
    start = len(df)

    df = standardize_categories(df, 'country', COUNTRY_MAP)
    # No missing values, no duplicate vendor_id, no implausible numbers -
    # this table needed nothing else.

    print(f"vendors.csv: {start} -> {len(df)} rows")
    return df


def clean_product_usage(raw_dir, valid_customer_ids):
    print("\n=== product_usage.csv ===")
    df = pd.read_csv(f"{raw_dir}/product_usage.csv")
    start = len(df)

    # 83 rows reference CUST-9999, which doesn't exist anywhere in
    # customers.csv - these can never be attached to real customer info,
    # so they're dropped rather than kept as unexplainable rows.
    df = remove_orphaned_rows(df, 'customer_id', valid_customer_ids, confirm=True)

    # active_users / devices_in_scope: left exactly as-is. active_users
    # exceeds devices_in_scope in ~33% of rows, so this ratio can't be
    # trusted as a literal "adoption rate" - flagged in the writeup, not
    # something to silently fix or guess at here.

    # Is Full Month flag: September 2026 only has 2 days of data in this
    # dataset, which would look like a fake engagement crash on any
    # month-over-month chart if not excluded.
    df['usage_date'] = pd.to_datetime(df['usage_date'])
    df['is_full_month'] = df['usage_date'] < pd.Timestamp('2026-09-01')
    n_partial = (~df['is_full_month']).sum()
    print(f"'is_full_month': flagged {n_partial} row(s) in the partial September window as False.")

    print(f"product_usage.csv: {start} -> {len(df)} rows")
    return df


def clean_experiment(raw_dir):
    print("\n=== experiment.csv ===")
    df = pd.read_csv(f"{raw_dir}/experiment.csv")
    # Nothing to clean - no nulls, no duplicate keys, no orphaned
    # customer_id, groups perfectly balanced 40/40, no implausible values.
    # Loaded as-is.
    print(f"experiment.csv: {len(df)} rows, no changes needed")
    return df


def main():
    parser = argparse.ArgumentParser(description="Clean the Vectral dataset end to end.")
    parser.add_argument('--raw-dir', default='data/raw', help="Folder containing the 6 raw CSVs")
    parser.add_argument('--out-dir', default='data/clean', help="Folder to write cleaned CSVs to")
    args = parser.parse_args()

    import os
    os.makedirs(args.out_dir, exist_ok=True)

    customers = clean_customers(args.raw_dir)
    orders = clean_orders(args.raw_dir)
    sales = clean_sales(args.raw_dir)
    vendors = clean_vendors(args.raw_dir)
    product_usage = clean_product_usage(args.raw_dir, customers['customer_id'].unique())
    experiment = clean_experiment(args.raw_dir)

    outputs = {
        'customers.csv': customers,
        'orders.csv': orders,
        'sales.csv': sales,
        'vendors.csv': vendors,
        'product_usage.csv': product_usage,
        'experiment.csv': experiment,
    }

    print("\n=== Writing cleaned files ===")
    for filename, df in outputs.items():
        path = f"{args.out_dir}/{filename}"
        df.to_csv(path, index=False)
        print(f"  {path}  ({len(df)} rows)")

    print("\nDone.")


if __name__ == '__main__':
    main()