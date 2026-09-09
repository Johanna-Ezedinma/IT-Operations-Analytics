"""
cleaning_utils.py

A reusable toolkit of data cleaning functions.
Import what you need into any project with:

    from cleaning_utils import check_missing_values, remove_duplicates, ...

Run help(function_name) in a notebook to see what each one does.

Suggested order of use on a new dataset:
1. Run pandas profiling (ydata-profiling) separately FIRST for a full overview.
2. check_dtypes, check_missing_values, check_duplicates  -> INSPECT
   (check_missing_values, check_duplicates, check_constant_columns and
   check_outliers_iqr live in profiling.py, not here - this file imports
   them so drop_constant_columns() and full_quality_check() below actually
   work standalone. Keep profiling.py in the same folder as this file.)
3. show_duplicates (review first!), remove_duplicate_keys (review first!),
   remove_duplicates, remove_orphaned_rows (review first!),
   standardize_categories, label_missing, strip_whitespace,
   fix_column_names, convert_dtype, convert_to_datetime, fill_missing,
   fill_missing_from_group, drop_missing, drop_constant_columns,
   flag_by_list, remove_rows (review first!), categorize_column,
   set_category_order, melt_to_long, split_datetime_parts   -> CLEAN
4. check_unique_values, check_outliers_iqr                 -> VALIDATE
5. full_quality_check                                      -> quick all-in-one re-check
"""

import pandas as pd
import numpy as np

# check_missing_values, check_duplicates, check_constant_columns and
# check_outliers_iqr are defined in profiling.py, not this file. They're
# imported here so drop_constant_columns() and full_quality_check() don't
# crash with a NameError if someone calls them without also having
# profiling.py's functions already in scope.
from profiling import check_missing_values, check_duplicates, check_constant_columns, check_outliers_iqr


def check_dtypes(df):
    """
    Print column data types.
    Useful for spotting numbers stored as text, dates stored as strings, etc.

    Example:
        check_dtypes(df)
    """
    print(df.dtypes)

# ---------- CLEAN ----------

def show_duplicates(df, subset=None, sort_by=None):
    """
    Show the actual duplicate rows before deciding to remove anything.
    Matching pairs are always sorted to appear side by side for easy review.

    subset:  list of columns to check duplicates on instead of the whole row
             e.g. ['customer_id', 'date']
    sort_by: list of columns to sort by so pairs sit next to each other.
             If not provided, defaults to subset columns (if given),
             otherwise sorts by all columns so identical rows group together.

    Use this BEFORE remove_duplicates to judge whether they're real
    duplicates or legitimate repeated events.
    """
    dupes = df[df.duplicated(subset=subset, keep=False)]

    # Decide sort order: explicit > subset > all columns
    sort_cols = sort_by or subset or list(df.columns)
    dupes = dupes.sort_values(by=sort_cols)

    print(f"Found {len(dupes)} rows involved in duplication (subset={subset}).")
    print(f"Sorted by: {sort_cols}")
    return dupes


def remove_duplicates(df, subset=None, confirm=False):
    """
    Drop duplicated rows.
    subset: optionally pass columns to check duplicates on, same as show_duplicates.
    confirm: must be set to True to actually delete anything. This is a safeguard,
             so you don't accidentally drop rows you haven't reviewed yet.
             Run show_duplicates(df) first to inspect before confirming.
    """
    if not confirm:
        print("No rows removed. Review with show_duplicates(df) first, "
              "then call remove_duplicates(df, confirm=True) once you're sure.")
        return df

    before = len(df)
    df = df.drop_duplicates(subset=subset)
    print(f"Removed {before - len(df)} duplicate rows.")
    return df


def remove_duplicate_keys(df, key_col, confirm=False):
    """
    Handle a column that SHOULD be a unique key (order_id, customer_id) but
    has duplicates - and handles the two cases differently, because they
    need different fixes:

    - EXACT duplicates (every other column also matches): safe to collapse
      to one row automatically. Nothing is lost.
    - CONFLICTING duplicates (same key, but other columns differ): NOT
      collapsed automatically. These get returned to you separately so you
      can decide - rename, drop, or check with the data source - rather
      than silently keeping one arbitrary row the way a plain
      "Remove Duplicates" button would.

    key_col: the column that should uniquely identify each row.
    confirm: must be True to actually drop the exact-duplicate rows.
             Review the printed summary first, then call again with
             confirm=True once you're sure.

    Returns: (cleaned_df, conflicting_rows)
        cleaned_df       - original df with exact duplicates collapsed
                            (only if confirm=True; otherwise unchanged)
        conflicting_rows - rows sharing a key with genuinely different data,
                            for you to review and handle separately. Empty
                            if none were found.

    Example:
        clean_orders, conflicts = remove_duplicate_keys(orders, 'order_id')
        print(conflicts)  # review what's actually different about these
        clean_orders, conflicts = remove_duplicate_keys(orders, 'order_id', confirm=True)
        # then decide what to do with `conflicts` yourself - this function
        # will never guess for you
    """
    dup_keys = df[key_col][df[key_col].duplicated(keep=False)].unique()
    if len(dup_keys) == 0:
        print(f"No duplicate values in '{key_col}'. Nothing to do.")
        return df, df.iloc[0:0]

    subset = df[df[key_col].isin(dup_keys)]
    other_cols = [c for c in df.columns if c != key_col]

    exact_keys, conflicting_keys = [], []
    for k, group in subset.groupby(key_col):
        (exact_keys if group[other_cols].nunique().max() == 1 else conflicting_keys).append(k)

    conflicting_rows = df[df[key_col].isin(conflicting_keys)].sort_values(key_col)

    print(f"'{key_col}': {len(exact_keys)} exact-duplicate key(s), {len(conflicting_keys)} conflicting key(s).")
    if conflicting_keys:
        print(f"  Conflicting keys are NOT auto-removed: {conflicting_keys[:10]}")
        print(f"  Review the returned `conflicting_rows` and decide yourself - "
              f"drop, rename, or check with the source system.")

    if not confirm:
        print("  No exact duplicates removed yet. Call again with confirm=True once you're sure.")
        return df, conflicting_rows

    before = len(df)
    df = df.drop_duplicates(subset=[key_col], keep='first') if exact_keys else df
    # only actually collapses rows where key was an EXACT duplicate;
    # conflicting-key rows are left untouched either way, since they were
    # never safe to auto-resolve
    if exact_keys:
        exact_mask = df[key_col].isin(exact_keys)
        first_of_exact = df[exact_mask].drop_duplicates(subset=[key_col], keep='first')
        df = pd.concat([df[~exact_mask], first_of_exact]).sort_index()
    print(f"  Removed {before - len(df)} exact-duplicate rows.")
    return df, conflicting_rows


def remove_orphaned_rows(df, key_col, valid_keys, confirm=False):
    """
    Remove rows whose key doesn't exist in a reference table - e.g. a
    customer_id in an orders table that has no matching row in customers.
    This is the "keep only what matches" side of a referential integrity
    check (the detection side is check_referential_integrity() in profiling.py).

    key_col:    the foreign key column to check, e.g. 'customer_id'
    valid_keys: the set/list of keys that ARE valid - usually
                parent_df['id_column'].unique()
    confirm:    must be True to actually drop anything. Review the printed
                orphan count and sample first, then call again with
                confirm=True once you're sure.

    Example:
        valid_ids = customers['customer_id'].unique()
        clean_usage = remove_orphaned_rows(product_usage, 'customer_id', valid_ids)
        # review the printout, then:
        clean_usage = remove_orphaned_rows(product_usage, 'customer_id', valid_ids, confirm=True)
    """
    valid_keys = set(valid_keys)
    orphan_mask = ~df[key_col].isin(valid_keys)
    n_orphans = orphan_mask.sum()

    if n_orphans == 0:
        print(f"No orphaned '{key_col}' values found. Nothing to do.")
        return df

    orphan_values = df.loc[orphan_mask, key_col].unique()
    print(f"{n_orphans} row(s) have a '{key_col}' value not found in the reference list.")
    print(f"  Orphaned values ({min(5, len(orphan_values))} shown): {list(orphan_values)[:5]}")

    if not confirm:
        print("  No rows removed. Review the orphaned rows first (df[~df[key_col].isin(valid_keys)]), "
              "then call again with confirm=True once you're sure.")
        return df

    df = df[~orphan_mask].reset_index(drop=True)
    print(f"  Removed {n_orphans} orphaned rows.")
    return df


def standardize_categories(df, column, mapping):
    """
    Apply a mapping dict to collapse spelling/formatting variants of the
    same real-world value into one - e.g. "US", "USA", "United States" all
    becoming "United States". Prints a before/after summary so the effect
    is visible, not silent.

    column:  the column to standardize
    mapping: dict of {existing_value: standardized_value}. Values not in
             the mapping are left unchanged - this is deliberate, so an
             unmapped typo doesn't silently vanish into a null. Run
             check_fuzzy_categories() from profiling.py first to build
             this mapping, rather than guessing at it.

    Example:
        country_map = {
            'US': 'United States', 'USA': 'United States', 'United States': 'United States',
            'UK': 'United Kingdom', 'United Kingdom': 'United Kingdom',
        }
        df = standardize_categories(df, 'country', country_map)
    """
    df = df.copy()
    before = df[column].nunique(dropna=True)
    unmapped = set(df[column].dropna().unique()) - set(mapping.keys())
    df[column] = df[column].map(mapping).fillna(df[column])
    after = df[column].nunique(dropna=True)

    print(f"'{column}': {before} distinct value(s) -> {after} after standardizing.")
    if unmapped:
        print(f"  Not in mapping, left unchanged: {sorted(unmapped)}")
    return df


def label_missing(df, column, label='Unknown'):
    """
    Explicitly label missing values with a fixed string, e.g. 'Unknown'.

    This does the same mechanical thing as fill_missing(df, column, method=label)
    but exists as its own function because the two are different KINDS of
    decision: fill_missing's mean/median/mode options are statistical
    guesses, while label_missing is a business judgment call - "we don't
    know this value, and we're saying so explicitly" rather than
    estimating what it probably was. Keeping them separate makes that
    distinction visible in your own code later, not just in your head now.

    Example:
        df = label_missing(df, 'country', 'Unknown')
    """
    df = df.copy()
    n_missing = df[column].isna().sum()
    df[column] = df[column].fillna(label)
    print(f"'{column}': labeled {n_missing} missing value(s) as '{label}'.")
    return df


def remove_rows(df, mask, reason='', confirm=False):
    """
    Remove rows matching a boolean condition, with the same review-first
    safeguard as remove_duplicates.

    mask:    a boolean Series identifying the rows to remove, e.g.
             (df['quantity'] < 0) & (df['customer_id'].isna())
    reason:  a short note on why these rows are being removed, printed
             back to you so the intent is documented, not just the count.
    confirm: must be set to True to actually delete anything. Review the
             matched rows yourself first with df[mask], then call again
             with confirm=True once you're sure they aren't real events.

    Example:
        invalid_mask = (df['quantity'] < 0) & (~df['is_cancelled']) & (df['customer_id'].isna())
        print(df[invalid_mask])  # review first
        df = remove_rows(df, invalid_mask, reason='internal stock write-offs', confirm=True)
    """
    if not confirm:
        print(f"{mask.sum()} rows match this condition (reason: {reason or 'not specified'}).")
        print("No rows removed. Review df[mask] first, then call remove_rows(df, mask, confirm=True) once you're sure.")
        return df

    before = len(df)
    df = df[~mask].reset_index(drop=True)
    print(f"Removed {before - len(df)} rows (reason: {reason or 'not specified'}).")
    return df



def strip_whitespace(df, columns=None):
    """Remove leading/trailing whitespace from text columns.
    Preserves real null values instead of converting them to the string 'nan'.
    """
    columns = columns or df.select_dtypes(include='object').columns
    for col in columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def fix_column_names(df):
    """
    Standardize column names to snake_case:
    - Converts to lowercase
    - Replaces spaces with underscores
    - Removes special characters (@, #, $, %, etc.)
    - Strips leading and trailing underscores from the result

    Examples:
        'Invoice No'  -> 'invoice_no'
        'Unit@Price'  -> 'unitprice'
        '% Growth'    -> 'growth'
        'Total $'     -> 'total'
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace(r'[^a-z0-9_]', '', regex=True)
        .str.strip('_')
    )
    return df


def convert_dtype(df, column, dtype):
    """
    Convert a column to a specified type, e.g. convert_dtype(df, 'price', float).
    Handles common symbols like $ and , automatically for numeric conversions.
    """
    if dtype in (float, int):
        df[column] = (
            df[column].astype(str)
            .str.replace('$', '', regex=False)
            .str.replace(',', '', regex=False)
        )
    df[column] = df[column].astype(dtype)
    return df




def convert_to_datetime(df, column, fmt=None):
    """
    Convert a column to datetime type and handle extra spaces and messy formats.
    fmt: optional date format string, e.g. '%m/%d/%Y %H:%M' or '%Y-%m-%d'.
         If not provided, pandas will infer the format automatically.
    Example:
        df = convert_to_datetime(df, 'invoice_date', fmt='%m/%d/%Y %H:%M')
    """
    # Create a copy to prevent SettingWithCopyWarning
    df = df.copy()

    #  Trim leading/trailing spaces if string data exists
    if df[column].dtype == 'object':
        df[column] = df[column].astype(str).str.strip()

    #  Convert to datetime using errors='coerce' to turn unparseable values to NaT
    if not fmt:
        print(f"No format given for '{column}', pandas will infer it row by row. "
              "This is slower on large datasets and can occasionally parse ambiguous "
              "dates inconsistently. Pass fmt='%m/%d/%Y %H:%M' (or similar) if you know the format.")
    df[column] = pd.to_datetime( df[column], 
        format=fmt if fmt else 'mixed', errors='coerce'
    )
    
    print(f"'{column}' converted to datetime. Sample: {df[column].iloc[0]}")
    return df




def fill_missing(df, column, method='mean', add_flag=False):
    """
    Fill missing values in a column with mean, median, mode, or a custom string/value.
    method:   'mean', 'median', 'mode', or any fixed value (e.g. 0, 'Unknown').
    add_flag: if True, adds a companion boolean column '{column}_missing' marking
              which rows were originally missing, BEFORE they get filled. Missingness
              is often informative on its own (a guest checkout, an unrated title),
              so this preserves that signal instead of erasing it once the gap is filled.

    Example:
        df = fill_missing(df, 'country', method='Unknown', add_flag=True)
        # df['country'] is now filled; df['country_missing'] shows which rows were
    """
    # Create a copy to modify safely
    df = df.copy()

    # Make sure literal 'nan' strings are converted to true null values first
    df[column] = df[column].replace(['nan', 'NaN', 'None', ''], np.nan)

    if add_flag:
        df[f'{column}_missing'] = df[column].isna()

    # Warn if method looks like a typo of a recognized keyword, rather than
    # silently using it as a literal fill value
    recognized = {'mean', 'median', 'mode'}
    if isinstance(method, str) and method not in recognized:
        close_matches = [r for r in recognized if abs(len(r) - len(method)) <= 2
                          and sum(a != b for a, b in zip(r, method)) <= 2]
        if close_matches:
            print(f"Warning: method='{method}' isn't a recognized keyword "
                  f"(did you mean {close_matches[0]!r}?). Using '{method}' as a literal fill value.")

    # 3. Apply missing value replacement
    if method == 'mean':
        fill_val = df[column].mean()
    elif method == 'median':
        fill_val = df[column].median()
    elif method == 'mode':
        fill_val = df[column].mode()[0]
    else:
        fill_val = method  # Custom input like 'Not Specified'

    # 4. Fill NaNs with the determined value
    df[column] = df[column].fillna(fill_val)

    return df





def fill_missing_from_group(df, column, group_col, fallback='UNKNOWN'):
    """
    Fill missing values in a column using the most frequent value already
    recorded for the same key elsewhere in the data, rather than a single
    dataset-wide fill. Useful when a column should be near-constant within
    a group (e.g. a product's description should match its stock code).

    column:     the column with missing values to fill.
    group_col:  the reliable key to group by (e.g. a product code or ID).
                Should be a fixed identifier, not another free-text field,
                since free text is exactly the kind of thing you're trying
                to fix here.
    fallback:   value used when a group has no known value anywhere to
                borrow from (e.g. 'UNKNOWN', 'UNKNOWN ITEM').

    Example:
        df = fill_missing_from_group(df, 'description', 'stock_code', fallback='UNKNOWN ITEM')
    """
    df = df.copy()
    lookup = (df.dropna(subset=[column])
                .groupby(group_col)[column]
                .agg(lambda x: x.value_counts().index[0]))

    missing_before = df[column].isna().sum()
    df[column] = df.apply(
        lambda r: lookup.get(r[group_col], fallback) if pd.isna(r[column]) else r[column],
        axis=1
    )
    print(f"Filled {missing_before} missing '{column}' values using '{group_col}' as the lookup key. "
          f"Remaining unresolved: {df[column].isna().sum()}.")
    return df


def flag_by_list(df, column, values, flag_name):
    """
    Add a boolean flag column marking whether each row's value is IN a
    known, verified list, rather than deleting or altering those rows.

    column:    the column to check (e.g. 'stock_code').
    values:    a list of known values to match against. This should be a
               list you've verified yourself (e.g. by reading the actual
               descriptions behind each value), not a guess based on what
               the values look like, pattern-based rules can misclassify
               real data that just happens to look unusual.
    flag_name: name for the new boolean column. It will be True for rows
               NOT in the list (i.e. the "normal"/default case), matching
               the is_product-style convention of flagging exceptions as False.

    Example:
        non_product_codes = ['POST', 'DOT', 'M', 'C2', 'D', 'BANK CHARGES', 'S', 'AMAZONFEE', 'CRUK', 'PADS']
        df = flag_by_list(df, 'stock_code', non_product_codes, flag_name='is_product')
    """
    df = df.copy()
    df[flag_name] = ~df[column].isin(values)
    print(f"{(~df[flag_name]).sum()} rows flagged under '{flag_name}' (matched the provided list).")
    return df


def categorize_column(df, column, categories=None, ordered=False):
    """
    Convert a column to pandas Categorical dtype.
    This is useful before modelling or plotting to control sort order,
    reduce memory usage, and signal to pandas that this is a fixed set of values.

    categories: optional list specifying the order of categories.
                If not provided, pandas infers them from the unique values.
    ordered:    set True if the categories have a meaningful order
                (e.g. ['Low', 'Medium', 'High']).

    Examples:
        df = categorize_column(df, 'rating')
        df = categorize_column(df, 'rating', categories=['G', 'PG', 'PG-13', 'R', 'NC-17'], ordered=True)
        df = categorize_column(df, 'country')
    """
    df = df.copy()
    df[column] = pd.Categorical(df[column], categories=categories, ordered=ordered)
    n_cats = df[column].cat.categories.tolist()
    print(f"'{column}' converted to Categorical. {len(n_cats)} categories: {n_cats}")
    return df


def set_category_order(df, column, order):
    """
    Set a custom display order for a categorical column.
    Affects how the column is sorted in plotnine charts and groupby operations.

    Use this when the column is already categorical but the default sort order
    (alphabetical) isn't what you want in your charts.
    Use categorize_column() instead if the column isn't categorical yet.

    order: list of category values in the order you want them displayed.
           Every value in the column should appear in this list.

    Examples:
        df = set_category_order(df, 'rating', ['G', 'PG', 'PG-13', 'R', 'NC-17'])
        df = set_category_order(df, 'priority', ['Low', 'Medium', 'High', 'Critical'])
        df = set_category_order(df, 'month_name', ['January', 'February', 'March',
                                                    'April', 'May', 'June', 'July',
                                                    'August', 'September', 'October',
                                                    'November', 'December'])
    """
    df = df.copy()
    df[column] = pd.Categorical(df[column], categories=order, ordered=True)
    print(f"'{column}' order set to: {order}")
    return df


def melt_to_long(df, id_vars, value_vars=None, var_name='variable', value_name='value'):
    """
    Reshape a dataframe from wide format to long format (equivalent to pivot_longer in R).
    Each row in the output represents one observation of one variable.

    This follows the principle of tidy data: each variable in its own column,
    each observation in its own row.

    id_vars   : columns to keep as identifier variables (they stay as columns).
    value_vars : columns to unpivot into rows. If not provided, uses all columns
                 not listed in id_vars.
    var_name  : name for the new column that holds the old column names (default 'variable').
    value_name: name for the new column that holds the values (default 'value').

    Example — wide format:
        country  2019  2020  2021
        Nigeria  100   120   140

    After melt_to_long(df, id_vars=['country'], var_name='year', value_name='sales'):
        country  year  sales
        Nigeria  2019  100
        Nigeria  2020  120
        Nigeria  2021  140

    Examples:
        df_long = melt_to_long(df, id_vars=['country', 'category'])
        df_long = melt_to_long(df, id_vars=['id'], value_vars=['2019', '2020', '2021'],
                               var_name='year', value_name='sales')
    """
    df_long = df.melt(id_vars=id_vars, value_vars=value_vars,
                      var_name=var_name, value_name=value_name)
    print(f"Reshaped from {df.shape} (wide) to {df_long.shape} (long).")
    print(f"New columns: '{var_name}' (variable names) and '{value_name}' (values).")
    return df_long


def split_datetime_parts(df, column, parts=None):
    """
    Split a datetime column into separate tidy columns following tidy data principles.
    Each extracted component gets its own column.

    column: the datetime column to split. Must already be converted to datetime dtype
            (run convert_to_datetime first if needed).
    parts:  list of components to extract. Options:
            'year', 'month', 'month_name', 'day', 'day_name',
            'quarter', 'week', 'hour', 'minute'
            If not provided, extracts year, month, month_name, and day by default.

    Examples:
        df = split_datetime_parts(df, 'invoice_date')
        df = split_datetime_parts(df, 'date_added', parts=['year', 'month', 'day'])
        df = split_datetime_parts(df, 'invoice_date', parts=['year', 'month', 'day', 'day_name', 'quarter'])
    """
    df = df.copy()

    if not pd.api.types.is_datetime64_any_dtype(df[column]):
        print(f"Warning: '{column}' is not datetime. Run convert_to_datetime(df, '{column}') first.")
        return df

    parts = parts or ['year', 'month', 'month_name', 'day']
    extracted = []

    part_map = {
        'year'      : lambda c: c.dt.year,
        'month'     : lambda c: c.dt.month,
        'month_name': lambda c: c.dt.month_name(),
        'day'       : lambda c: c.dt.day,
        'day_name'  : lambda c: c.dt.day_name(),
        'quarter'   : lambda c: c.dt.quarter,
        'week'      : lambda c: c.dt.isocalendar().week.astype(int),
        'hour'      : lambda c: c.dt.hour,
        'minute'    : lambda c: c.dt.minute,
    }

    for part in parts:
        if part not in part_map:
            print(f"Warning: '{part}' is not a recognised part. Skipping.")
            continue
        col_name = f'{column}_{part}'
        df[col_name] = part_map[part](df[column])
        extracted.append(col_name)

    print(f"Extracted from '{column}': {extracted}")
    return df


def drop_missing(df, columns=None):
    """
    Drop rows where values are missing.
    columns: a single column name or list of column names to check.
             If not provided, drops any row with ANY missing value.

    Use check_missing_values(df) first to decide which columns
    actually need rows dropped vs filled.

    Examples:
        drop_missing(df)                          # drop rows with any null
        drop_missing(df, columns='description')   # drop where description is null
        drop_missing(df, columns=['name', 'date'])# drop where either is null
    """
    before = len(df)
    df = df.dropna(subset=columns if columns else None)
    print(f"Dropped {before - len(df)} rows with missing values in: {columns or 'any column'}.")
    return df


def drop_constant_columns(df):
    """Drop columns where every value is identical."""
    constant_cols = check_constant_columns(df)
    return df.drop(columns=constant_cols)


# ---------- ALL-IN-ONE ----------

def full_quality_check(df):
    """
    Run all basic inspection checks at once. A quick first-pass audit.
    Covers: data types, missing values, duplicates, constant columns,
    and outliers across all numeric columns.
    """
    print("--- Data types ---")
    check_dtypes(df)
    print("\n--- Missing values ---")
    check_missing_values(df)
    print("\n--- Duplicates ---")
    check_duplicates(df)
    print("\n--- Constant columns ---")
    check_constant_columns(df)
    print("\n--- Outliers (all numeric columns) ---")
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) == 0:
        print("No numeric columns found.")
    else:
        for col in numeric_cols:
            check_outliers_iqr(df, col)