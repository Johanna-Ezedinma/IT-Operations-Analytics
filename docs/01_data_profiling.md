<table width="100%">
<tr>
<td><h1>Vectral</h1></td>
<td align="right">

[![Home](https://img.shields.io/badge/Home-5B6864?style=for-the-badge)](../README.md)
[![Data Profiling](https://img.shields.io/badge/Data_Profiling-5444F1?style=for-the-badge)](../vectral/docs/01_data_profiling.md)
[![Data Preparation](https://img.shields.io/badge/Data_Preparation-5B6864?style=for-the-badge)](../docs/02_data_preparation.md)
[![Analysis](https://img.shields.io/badge/Analysis-5B6864?style=for-the-badge)](../docs/03_analysis.md)

</td>
</tr>
</table>

What I found in each table before making any changes. One table at a time, checked independently before deciding what to do about anything, see [Data Preparation](02_data_preparation.md) for the decisions.

## Customers

**147 rows, 11 columns**

| Issue                                            | What was found                                                                                                                                        |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Different representations of the same country    | 9 real countries identified, but some are spelled differently — e.g. US, USA, United States are the same place; UK, United Kingdom are the same place |
| Missing country (2 rows)                         | 2 rows have no country listed. Both are real, active customers with real revenue                                                                      |
| Duplicate records (2 rows: CUST-0018, CUST-0064) | Checked against every other column — exactly identical in every field                                                                                 |

## Orders

**720 rows, 10 columns · Date range: 10 Jan 2025 to 4 Sep 2026**

| Issue                                               | What was found                                                                                                                                                                            |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Duplicate order_id, but conflicting orders (4 rows) | No identical duplicates, but 2 order IDs are each used twice. The two rows under each ID describe different orders — different customer, device, value                                    |
| Missing country (10 rows)                           | 10 rows have no country listed                                                                                                                                                            |
| Missing delivery date (105 rows)                    | All 105 belong to orders that are Cancelled, Failed, or still In Transit                                                                                                                  |
| Different representations of the same country       | Same spelling issue as customers.csv                                                                                                                                                      |
| device_model doesn't match device_type              | The same model name (e.g. "MacBook Air M3") shows up about equally often under every device_type — Monitor, Phone, Tablet, Desktop, Laptop — it doesn't reliably describe the real device |

## Sales

**430 rows, 11 columns**

| Issue                                         | What was found                                                                                                            |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Missing country (10 rows)                     | 10 rows have no country listed                                                                                            |
| Different representations of the same country | Same spelling issue as customers.csv                                                                                      |
| Missing lost_reason                           | 36 leads are marked Lost, but only 33 have a lost_reason filled in — 3 are blank                                          |
| date_converted blank                          | 334 blanks — all belong to leads with no outcome recorded yet                                                             |
| lost_reason blank for Won/open leads          | Expected — there's no "reason" for a deal that hasn't been lost                                                           |
| No shared key with Customers                  | Sales uses "Prospect 000N" naming, Customers uses "Customer 0NN" naming. Zero text overlap, and no ID field connects them |

## Vendors

**54 rows, 8 columns**

| Issue                                         | What was found                                                                                |
| --------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Different representations of the same country | Same spelling issue as the other tables (11 variants for 9 real countries)                    |
| No shared key with Orders                     | orders.csv has no vendor_id column, and vendors.csv has nothing that maps to a specific order |
| Everything else                               | No nulls, no duplicate vendor_id, no implausible numbers                                      |

## Product Usage

**2,500 rows, 6 columns · Date range: 1 Jan 2026 to 2 Sep 2026**

| Issue                                         | What was found                                                                                                                                                        |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Records that can't be matched across datasets | customer_id `CUST-9999` has 83 rows that don't exist anywhere in customers.csv. Confirmed with a Left Anti merge                                                      |
| active_users bigger than devices_in_scope     | Happens in 822 of 2,500 rows (~33%). One row shows 2 devices in scope but 61 active users — not logically possible                                                    |
| Data only covers ~8 months                    | Earliest date is Jan 2026 — doesn't go back to each customer's actual start date. September 2026 is also a partial month (only 21 rows vs. ~300-330 for a full month) |

## Experiment

**80 rows, 6 columns**

| Issue              | What was found                                                                                                                                                                                                                                                       |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Everything checked | No nulls anywhere. No duplicate experiment_id or customer_id. Every customer_id exists in customers.csv. Groups are perfectly even (40 Treatment, 40 Control). target_feature_adopted is a clean 0/1 flag. No negative values in baseline or post-experiment actions |
