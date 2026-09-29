<table width="100%">
<tr>
<td><h1>Vectral</h1></td>
<td align="right">

[![Home](https://img.shields.io/badge/Home-5444F1?style=for-the-badge)](../README.md)
[![Data Profiling](https://img.shields.io/badge/Data_Profiling-5B6864?style=for-the-badge)](docs/01_data_profiling.md)
[![Data Preparatin](https://img.shields.io/badge/Data_Preparation-5B6864?style=for-the-badge)](docs/02_data_preparation.md)
[![Analysis](https://img.shields.io/badge/Analysis-5B6864?style=for-the-badge)](docs/03_analysis.md)
[![Recommendations](https://img.shields.io/badge/Recommendations-5B6864?style=for-the-badge)](#key-recommendations)

</td>
</tr>
</table>

The company's running motto is to turn IT disruptions into unstoppable growth. It provides infrastructure that helps companies manage their employees' devices and IT operations globally, handling the behind-the-scenes work of IT for growing businesses.
When a new employee starts, it helps the company order, track, and manage their laptops, phones, and tablets. It keeps track of who owns what device, when equipment needs replacing, and whether software tools are being used.

As the company expanded, leadership shifted toward a fully data-driven strategy to align day-to-day decisions with real operational metrics across sales, operations, product, and customer success. To guide this next phase of growth, they needed answers to four core questions:

- Are we making more money over time, or does it just feel like it?
- If we are making money, which types of customers are bringing in the most value?
- What is the current state of our orders? Are deliveries succeeding, failing, or getting cancelled in certain regions?
- How did our experiment perform? Should the new feature be rolled out now?

---

**How The Company's Business Model Works**

They group their business clients into three distinct plan tiers: **Starter**, **Growth**, and **Enterprise**. These tiers are defined primarily by `employee headcount` and `organizational complexity`.

**Starter** plans serve small teams needing basic inventory tracking.

**Growth** plans support mid-sized companies with scaling onboarding flows.

**Enterprise** clients represent large organizations that require custom IT workflows, advanced security controls, and dedicated support, charging higher subscription rates to reflect that scale.

---

**End-to-End Business Performance & Insights**

To understand their current performance, we follow the operational path a client takes: from initial sales outreach, to contract signing, hardware fulfillment, ongoing platform usage, and feature adoption.

```
Sales Lead  --->  Deal Closed  --->  Hardware Order  --->  Fulfilled / Delivered  --->  Active Usage & Feature Tests
```

### 1. Attracting & Closing Deals (Sales Pipeline)

Their pipeline moves leads through distinct stages:
**Lead** (newly logged lead),
**Qualified** (meeting basic criteria),
**Discovery** (a deep-dive conversation to uncover the client's specific IT infrastructure needs), **Proposal**,
**Negotiation**, and finally
**Closed Won** or **Closed Lost**.

- **Deal Conversion:** `63%` of deals that reach a `final decision`, representing `60 won` versus `36 lost` out of `96 decided deals`. However, `334 deals` totaling `$7.91M in total value remain open` in earlier stages, with `166 sitting in Lead and Qualified alone`.

- **Lead Source Dynamics:** `Outbound sales calls` and `Referrals` close most reliably with `69% and 68% win rates`. `Inbound` web leads generate significantly larger contract sizes, bringing in roughly `$280K in total revenue` — the highest of any channel, despite converting only half the time.

![Growth & Sales](<dashboard/Growth and Sales.jpg>)

> _This view tracks total annual recurring revenue ($1.01M), sales pipeline progression across stages, win rates by lead channel, and monthly client growth trends._

---

### 2. Monetization & Revenue Realization (Customers)

Once deals close and clients join the platform, subscription revenue activates across the customer tiers.

- **Revenue Distribution:** They have generated `$1.01M in total Annual Recurring Revenue across 122 active accounts`. `Growth clients` generate the largest total pool of revenue `($434K across 57 accounts)`. `Enterprise clients` bring in the highest average revenue per client at `$11,158 per year` compared to `Starter's $5,597 per year`.
- **Hardware vs. Subscription Spending:** Big subscription clients were not actually buying more hardware. While Enterprise clients pay double the annual subscription cost of Starter clients, all three tiers place similarly sized physical device orders, averaging roughly $14K-$15K per order.

---

### 3. Delivering the Devices (Operations & Logistics)

After a client signs on, they place orders for laptops, phones, and tablets that must be fulfilled and shipped locally.

- **Order Volumes:** The company processed 716 total device orders, averaging 36 orders per month with an average fulfillment time of 7 days for delivered orders.
- **Regional Delivery Bottlenecks:** Geography heavily impacts fulfillment reliability. In Singapore, only 6% of orders fail or get cancelled. In contrast, orders shipped to France (23%) and Australia (22%) fail or cancel nearly four times as often, signaling likely regional vendor or courier issues.

![Customers and Operations](<dashboard/Customers and Operations.jpg>)

> _This view monitors order fulfillment speeds, monthly order spikes, client retention mixes, and regional failure/cancellation rates._

---

### 4. Long-Term Engagement & The Product Experiment (Product & Platform)

After onboarding and device delivery, clients use the platform daily to manage IT support tickets, track asset health, and offboard departing staff. Overall, platform usage stays fairly steady at around 12,000 monthly active users. Looking at total usage across the full 8-month window, IT Support (15.2K active-user-instances) and Employee Offboarding (14.6K) see the most use of any feature.

#### Why and How the Experiment Was Conducted

A product experiment was recently run to find out whether automated, proactive notifications could drive higher long-term engagement on the platform. The product team noticed that many clients only logged in when something broke. They hypothesized that if clients received proactive alerts about device health, such as dying laptop batteries, expiring warranties, or overdue security patches, they would log in more frequently and rely more heavily on the platform.

To test this idea, a controlled experiment was run:

- **The Method:** A group of 80 total clients was split into two cohorts: a **Treatment group** (40 clients), which was given access to the new **Fleet Health Alerts** feature, and a **Control group** (40 clients), which was kept on the standard platform without alerts.
- **The Goal:** Baseline weekly platform activity was measured before the feature rollout, along with post-experiment weekly activity, and whether clients actively adopted the new alerts tool.

#### What the Experiment Result Showed

- **The Initial Signal:** On the surface, the feature looked like a strong success. The Treatment group increased their average weekly platform activity by 57%, jumping from 3.6 to 5.7 actions per week. The Control group's activity slightly declined by 2.8%, dropping from 3.5 to 3.4 actions per week. 53% of Treatment customers actively adopted the feature, compared to just 25% in Control.
- **A Real Imbalance, Checked Rather Than Assumed:** Looking deeper into how the groups were set up revealed a genuine imbalance worth flagging. The Control group skewed heavily toward smaller **Starter** clients (19 Starter vs. 6 Enterprise). The Treatment group contained significantly more large **Enterprise** clients (16 Enterprise vs. 7 Starter). That's a real design weakness worth naming on its own.
- **The Test:** Rather than assume this explains the result, it was tested directly. If bigger companies naturally grow more active regardless of any feature, Control's own Enterprise customers should show that growth on their own, without any alerts. They didn't: their activity actually dropped slightly (-0.17). The biggest jump inside Treatment also came from Starter clients (+4.14), not Enterprise (+2.06), the opposite of what the imbalance theory would predict.
- **The Conclusion:** The group imbalance is real and worth naming as a design flaw. But it doesn't explain away the result, if anything, the lift looking strongest in the tier that got _fewer_ Treatment slots makes the feature's effect look more genuine, not less. The honest caveat left is sample size: some of these group-and-plan breakdowns have as few as 6 or 7 people in them, so none of the individual numbers should be treated as fully reliable on their own.

![Product and Experiment](<dashboard/Product and Experiment.jpg>)

> _This view analyzes feature adoption trends, monthly active user distribution, baseline vs. post-test action lifts, and client tier distribution across the experiment._

---

## Summary

**Are we making more money over time, or does it just feel like it?**
Genuinely growing; $1.01M in real ARR, not a mirage. But it's not a smooth climb. Some months bring in a dozen new customers, others just one or two, so month to month it can feel less steady than the total number suggests.

**If we are making money, which types of customers are bringing in the most value?**
Depends what you mean by "value." Enterprise customers pay the most per account ($11,158/year vs. Starter's $5,597), but Growth tier brings in the most money overall, simply because it has more customers (57 accounts, $434K total). None of that revenue difference shows up in hardware spend, either, all three tiers order similarly-sized batches. Plan tier tells you about contract value, not device demand.

**What is the current state of our orders? Are deliveries succeeding, failing, or getting cancelled in certain regions?**
Most orders go through fine, 716 processed, averaging 7 days to fulfil. But failure isn't evenly spread: France and Australia fail around 22-23% of orders, versus 6% in Singapore, a real, sizable pattern. We can tell you _where_ the problem concentrates, not fully _why_ yet, without a way to trace an order back to the specific vendor that handled it, we can't say whether the cause is vendor coverage, shipping distance, customs, or something else specific to those markets. That gap is exactly why fixing the Vendors-to-Orders link is one of the recommendations below.

**How did our experiment perform? Should the new feature be rolled out now?**
Not yet, but the signal is genuinely encouraging. Treatment customers' activity rose 57% while Control barely moved, and adoption was roughly double. The one real design flaw, an uneven split by company size, was tested directly rather than assumed, and it doesn't explain the result away. Still, this isn't the same as proof: no significance test has been run, and the sample is small. Worth a controlled re-check before betting a full rollout on it, not a reason to shelve it.

---

## Key Recommendations

**1. Hold off on further sales push into France and Australia, until Operations investigates the order failure rate there.**
At 22-23%, roughly 1 in 5 orders in these two markets fails or gets cancelled, about four times the rate in the best-performing market (Singapore, 6%). Pushing harder into these markets without knowing _why_ the failure rate is high risks scaling the problem right alongside the growth. An immediate vendor swap in these markets was considered instead, but ruled out, there's currently no way to confirm which vendor is even responsible, so swapping first would be a guess, not a fix.

**2. Re-check the Fleet Health Alerts result before rolling it out company-wide.**
The 57% activity lift looks like a clear win at face value, and testing the plan-tier imbalance directly didn't undercut that result. Even so, this isn't the same as a properly run significance test. Rolling out to every customer on the strength of a single before/after comparison is a bigger bet than the current evidence supports, an actual significance test, not just comparing averages, should come first.

**3. Add a `converted_customer_id` field to Sales, and a `vendor_id` field to Orders.**
Both are small, one-column schema changes, but they unlock real answers that can't currently be reached: true cost-per-channel (is Inbound's bigger deal size actually worth its lower conversion rate, once cost is factored in?), and true vendor accountability (which vendor is actually behind the France/Australia problem?). A workaround was considered, fuzzy-matching leads to customers by country and industry, or spreading vendor performance evenly across orders in the same country, and both were ruled out. Either would produce a number, but an invented one dressed up as data is more likely to mislead a decision-maker than an honest "we can't answer this yet."

**4. Get eyes on the 166 leads still sitting in Lead and Qualified.**
This is a related but separate ask from #3, it's a sales-process question, not a data-model one. Right now there's no way to tell whether these are healthy, recently-created pipeline or leads that have gone quiet for months, because the data doesn't track how long a lead has sat in its current stage. "Add stage-aging data" is worth treating as a companion fix to the two schema changes above, small to implement, and it turns a real blind spot into an answerable question the next time this kind of review happens.

---

**Data Limitations & Technical Gaps**

- **Untraceable Lead Acquisition Costs:** Sales lead records (`sales.csv`) and Customer account records (`customers.csv`) do not share a unified customer tracking ID. This prevents direct calculation of Customer Acquisition Cost (CAC) for won clients.
- **Missing Vendor-to-Order Connections:** Order records (`orders.csv`) lack a `vendor_id` reference. No order can be tied to the vendor that fulfilled it, meaning vendor performance numbers can only be viewed in aggregate.
- **Truncated Usage & Sample Scale:** Product usage data covers only the last 8 months rather than full account histories. The overall customer dataset is relatively small (145 customers), meaning observed patterns are directional rather than statistically proven.

---

**Core Business Metrics Framework**

To move from reactive monitoring to proactive decision-making, a 15-metric operational framework was established across Sales, Operations, Product, and Finance.
Key indicators such as **Win Rate by Lead Channel**, **Regional Fail/Cancel Rate**, and **Experiment Action Lift** are surfaced directly in the executive dashboard above.

_(For the complete 15-metric definition list, including business ownership and decision rationale, see [Analysis](docs/03_analysis.md).
For detailed technical documentation on initial data profiling, duplicate handling, schema mapping, and cleaning steps, see [Data Profiling](docs/01_data_profiling.md) and
[Data Preparation](docs/02_data_preparation.md).)_
