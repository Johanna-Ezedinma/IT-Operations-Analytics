<table width="100%">
<tr>
<td><h1>Vectral</h1></td>
<td align="right">

[![Home](https://img.shields.io/badge/Home-5B6864?style=for-the-badge)](../README.md)
[![Data Profiling](https://img.shields.io/badge/Data_Profiling-5B6864?style=for-the-badge)](01_data_profiling.md)
[![Data Preparatin](https://img.shields.io/badge/Data_Preparation-5444F1?style=for-the-badge)](02_data_preparation.md)
[![Analysis](https://img.shields.io/badge/Analysis-5B6864?style=for-the-badge)](03_analysis.md)

</td>
</tr>
</table>

What I did about each issue found in [Data Profiling](01_data_profiling.md), the options I considered, and why.

## Customers — 147 → 145 rows

| Issue                       | Options considered                                    | Decision                                                                         | Reason                                                                                                |
| --------------------------- | ----------------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Different country spellings | Standardise spelling · Leave as-is                    | **Standardise to one full name per country** ("United States", "United Kingdom") | Without this, the same country would split into 2-3 separate bars/slices on any chart                 |
| Missing country (2 rows)    | Delete the rows · Label "Unknown" · Guess the country | **Label "Unknown"**                                                              | Both are real, active customers with real revenue. Deleting them would mean losing real business data |
| Duplicate records (2 rows)  | Keep one copy · Keep both · Tag as duplicate but keep | **Keep one copy, delete the repeat**                                             | The two rows are identical, so nothing is lost                                                        |

## Orders — 720 → 716 rows

| Issue                                           | Options considered                                                               | Decision                              | Reason                                                                                                                                                                      |
| ----------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Duplicate order_id, conflicting orders (4 rows) | Rename the second one with a new ID · Delete both rows in each pair · Keep as-is | **Delete all 4 rows**                 | Can't tell which order (if either) is real, so keeping or renaming would be a guess. Losing 4 of 720 orders is safer than guessing                                          |
| Missing country (10 rows)                       | Delete the rows · Label "Unknown"                                                | **Label "Unknown"**                   | Same reasoning as customers.csv                                                                                                                                             |
| Different country spellings                     | Standardise spelling · Leave as-is                                               | **Standardise spelling**              | Keeps each country as one category instead of several                                                                                                                       |
| Missing delivery date (105 rows)                | Fill with a guess · Leave blank                                                  | **Leave blank**                       | Not an error. These orders haven't been delivered, so there's genuinely nothing to fill in                                                                                  |
| device_model doesn't match device_type          | Keep both fields as-is · Delete device_model · Keep device_type                  | **Use device_type for this analysis** | device_type's average price per unit corresponds with real-world prices. In a real-world scenario, I wouldn't fully trust either field until confirming with the data owner |

## Sales — 430 → 430 rows

| Issue                                     | Options considered                                     | Decision                                                                 | Reason                                                                                                                                               |
| ----------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Missing country (10 rows)                 | Delete the rows · Label "Unknown"                      | **Label "Unknown"**                                                      | Same reasoning as customers.csv                                                                                                                      |
| Different country spellings               | Standardise spelling · Leave as-is                     | **Standardise spelling**                                                 | Keeps each country as one category instead of several                                                                                                |
| lost_reason blank for 3 Lost deals        | Delete the rows · Label "Unknown" · Leave blank        | **Label "Unknown"**                                                      | "Unknown" already exists as a real category in this column, so this isn't inventing anything new — it just puts them in a bucket that already exists |
| date_converted / outcome blank (334 rows) | Fill with a guess · Leave blank                        | **Leave blank**                                                          | These leads simply haven't closed yet — there's no outcome or conversion date to record. A real business state, not missing data                     |
| No shared key with Customers              | Try to text-match company names · Leave as a known gap | **Leave as a known gap; recommend adding a converted_customer_id field** | A won lead cannot currently be traced to the customer record it became. Guessing a match would be worse than admitting the gap                       |

## Vendors — 54 → 54 rows

| Issue                       | Options considered                                                                        | Decision                                                  | Reason                                                                                                                                                                                                           |
| --------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Different country spellings | Standardise spelling · Leave as-is                                                        | **Standardise spelling**                                  | Keeps each country as one category instead of several                                                                                                                                                            |
| No shared key with Orders   | Spread vendor performance evenly across orders in the same country · Leave as a known gap | **Leave as is; recommend adding vendor_id to orders.csv** | Vendor performance (rating, fulfilment days) can only ever be viewed vendor-by-vendor — it can't be cross-cut by customer, country, or device type. This is a data-modelling gap, not something cleaning can fix |

## Product Usage — 2,500 → 2,417 rows

| Issue                                         | Options considered                                                    | Decision                                                                          | Reason                                                                                                                                                       |
| --------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| CUST-9999 (83 rows, no match in Customers)    | Keep the rows · Delete the rows                                       | **Delete the 83 rows**                                                            | These rows can't be attached to any real customer info (country, plan, industry), so they can't contribute to any customer-based chart or metric             |
| active_users > devices_in_scope (822 rows)    | Leave numbers as-is · Swap the two columns · Delete the affected rows | **Left exactly as they are**                                                      | The contradiction shows up in a third of all rows, so the ratio can't be trusted as a metric — but the raw numbers themselves aren't something I'd guess-fix |
| Data covers ~8 months only, partial September | —                                                                     | **Noted; excluded/footnoted the partial September in any month-over-month chart** | Not a cleaning fix, just a limitation to flag so a partial month doesn't look like a sudden drop                                                             |

## Experiment — 80 → 80 rows

No changes needed. Every check — nulls, duplicate keys, orphaned customer_id, group balance, value ranges — came back clean.
