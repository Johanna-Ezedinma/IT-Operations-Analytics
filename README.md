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

Vectral's running motto is to turn IT disruptions into unstoppable growth. They provide infrastructure that helps companies manage their employees' devices and IT operations globally, handling the behind-the-scenes work of IT for growing businesses.
When a new employee starts, Vectral helps the company order, track, and manage their laptops, phones, and tablets. It keeps track of who owns what device, when equipment needs replacing, and whether software tools are being used.

As Vectral expanded, leadership shifted toward a fully data-driven strategy to align day-to-day decisions with real operational metrics across sales, operations, product, and customer success. To guide this next phase of growth, they needed answers to four core questions:

- Are we making more money over time, or does it just feel like it?
- Which types of customers bring in the most value?
- Why are orders failing or getting cancelled in certain regions?
- Is the new software feature we built actually helping customers stay active?

---

**How Vectral's Business Model Works**

Vectral groups its business clients into three distinct plan tiers: **Starter**, **Growth**, and **Enterprise**. These tiers are defined primarily by employee headcount and organizational complexity.

**Starter** plans serve small teams needing basic inventory tracking.

**Growth** plans support mid-sized companies with scaling onboarding flows.

**Enterprise** clients represent large organizations that require custom IT workflows, advanced security controls, and dedicated support, charging higher subscription rates to reflect that scale.

---

**End-to-End Business Performance & Insights**

To understand how Vectral performs, we follow the operational path a client takes: from initial sales outreach, to contract signing, hardware fulfillment, ongoing platform usage, and feature adoption.

```
Sales Lead  --->  Deal Closed  --->  Hardware Order  --->  Fulfilled / Delivered  --->  Active Usage & Feature Tests
```

### 1. Attracting & Closing Deals (Sales Pipeline)

Vectral's pipeline moves leads through distinct stages:
**Lead** (newly logged lead),  
**Qualified** (meeting basic criteria),  
**Discovery** (a deep-dive conversation to uncover the client's specific IT infrastructure needs), **Proposal**,  
**Negotiation**, and finally  
**Closed Won** or **Closed Lost**.

- **Deal Conversion:** Vectral `wins 63%` of deals that reach a `final decision`, representing `60 won` versus `36 lost` out of `96 decided deals`. However, `334 deals` totaling `$7.91M in total value remain open` in earlier stages, with `166 sitting in Lead and Qualified alone`.

- **Lead Source Dynamics:** `Outbound sales` calls and `Referrals` close most reliably with `69% and 68% win rates`. `Inbound` web leads generate significantly larger contract sizes, bringing in roughly `$280K in total revenue` — the highest of any channel, despite converting only half the time.

![Growth & Sales](<dashboard/Growth and Sales.jpg>)

> _This view tracks total annual recurring revenue ($1.01M), sales pipeline progression across stages, win rates by lead channel, and monthly client growth trends._

---

### 2. Monetization & Revenue Realization (Customers)

Once deals close and clients join the platform, subscription revenue activates across the customer tiers.

- **Revenue Distribution:** Vectral generates `$1.01M in total Annual Recurring Revenue across 122 active accounts`. `Growth clients` generate the largest total pool of revenue `($434K across 57 accounts)`. `Enterprise clients` bring in the highest average revenue per client at `$11,158 per year` compared to `Starter's $5,597 per year`.
- **Hardware vs. Subscription Spending:** Their big subscription clients were not actually buying more hardware. While Enterprise clients pay double the annual subscription cost of Starter clients, all three tiers place similarly sized physical device orders, averaging roughly $14K-$15K per order.

---

### 3. Delivering the Devices (Operations & Logistics)

After a client signs on, they place orders for laptops, phones, and tablets that must be fulfilled and shipped locally.

- **Order Volumes:** Vectral processed 716 total device orders, averaging 36 orders per month with an average fulfillment time of 7 days for delivered orders.
- **Regional Delivery Bottlenecks:** Geography heavily impacts fulfillment reliability. In Singapore, only 6% of orders fail or get cancelled. In contrast, orders shipped to France (23%) and Australia (22%) fail or cancel nearly four times as often, signaling likely regional vendor or courier issues.

![Customers and Operations](<dashboard/Customers and Operations.jpg>)

> _This view monitors order fulfillment speeds, monthly order spikes, client retention mixes, and regional failure/cancellation rates._

---

### 4. Long-Term Engagement & The Product Experiment (Product & Platform)

After onboarding and device delivery, clients use Vectral's platform daily to manage IT support tickets, track asset health, and offboard departing staff. Overall, platform usage stays fairly steady at around 12,000 monthly active users. Looking at total usage across the full 8-month window, IT Support (15.2K active-user-instances) and Employee Offboarding (14.6K) see the most use of any feature.

#### Why and How the Experiment Was Conducted

Vectral recently conducted a product experiment to find out whether automated, proactive notifications could drive higher long-term engagement on the platform. The product team noticed that many clients only logged in when something broke. They hypothesized that if clients received proactive alerts about device health, such as dying laptop batteries, expiring warranties, or overdue security patches, they would log in more frequently and rely more heavily on Vectral's tools.

To test this idea, Vectral ran a controlled experiment:

- **The Method:** They split a group of 80 total clients into two cohorts: a **Treatment group** (40 clients), which was given access to the new **Fleet Health Alerts** feature, and a **Control group** (40 clients), which was kept on the standard platform without alerts.
- **The Goal:** They measured baseline weekly platform activity before the feature rollout, post-experiment weekly activity, and whether clients actively adopted the new alerts tool.

#### What the Experiment Result Showed

- **The Initial Signal:** On the surface, the feature looked like a strong success. The Treatment group increased their average weekly platform activity by 57%, jumping from 3.6 to 5.7 actions per week. The Control group's activity slightly declined by 2.8%, dropping from 3.5 to 3.4 actions per week. 53% of Treatment customers actively adopted the feature, compared to just 25% in Control.
- **The Hidden Flaw:** Looking deeper into how the groups were set up revealed a selection imbalance worth flagging. The Control group skewed heavily toward smaller **Starter** clients (19 Starter vs. 6 Enterprise). The Treatment group contained significantly more large **Enterprise** clients (16 Enterprise vs. 7 Starter).
- **The Insight:** Larger Enterprise clients naturally run more weekly IT tasks simply because they have more employees and devices. As a result, some of the recorded activity surge may reflect company size rather than the new feature alone.

![Product and Experiment](<dashboard/Product and Experiment.jpg>)

> _This view analyzes feature adoption trends, monthly active user distribution, baseline vs. post-test action lifts, and client tier distribution across the experiment._

---

## Summary

**Are we making more money over time, or does it just feel like it?**
Genuinely growing; $1.01M in real ARR, not a mirage. But it's not a smooth climb. Some months bring in a dozen new customers, others just one or two, so month to month it can feel less steady than the total number suggests.

**Which types of customers bring in the most value?**
Depends what you mean by "value." Enterprise customers pay the most per account ($11,158/year vs. Starter's $5,597) but Growth tier brings in the most money overall, simply because it has more customers (57 accounts, $434K total). None of that revenue difference shows up in hardware spend, either all three tiers order similarly-sized batches. Plan tier tells you about contract value, not device demand.

**Why are orders failing or getting cancelled in certain regions?**
Honestly, we can tell you _where_, not fully _why_ yet. France and Australia fail around 22-23% of orders, versus 6% in Singapore a real, sizable pattern. But without a way to trace an order back to the specific vendor that handled it, we can't say whether the cause is vendor coverage, shipping distance, customs, or something else specific to those markets. That gap is exactly why fixing the Vendors-to-Orders link is one of the recommendations below.

**Is the new software feature we built actually helping customers stay active?**
The early signal says yes, Treatment customers' activity rose 57% while Control barely moved, and adoption was roughly double. But because Treatment and Control weren't evenly matched by company size going in, this isn't proof yet, just a promising direction worth testing more rigorously before betting a full rollout on it.

---

## Key Recommendations

**1. Hold off on further sales push into France and Australia, until Operations investigates the order failure rate there.**
At 22-23%, roughly 1 in 5 orders in these two markets fails or gets cancelled, about four times the rate in Vectral's best-performing market (Singapore, 6%). Pushing harder into these markets without knowing _why_ the failure rate is high risks scaling the problem right alongside the growth. I considered recommending an immediate vendor swap in these markets instead, but ruled it out, there's currently no way to confirm which vendor is even responsible, so swapping first would be a guess, not a fix.

**2. Re-check the Fleet Health Alerts result before rolling it out company-wide.**
The 57% activity lift looks like a clear win at face value, but Treatment and Control weren't evenly split by plan tier, Control skewed Starter, Treatment skewed Enterprise. Rolling this out to every customer based on the raw number risks overstating the feature's actual effect, since some of that lift may just be "bigger customers were more likely to end up in Treatment." I considered recommending an immediate full rollout, since the direction is genuinely promising, but ruled it out until the result is checked controlling for plan tier, and run through an actual significance test rather than a simple before/after comparison.

**3. Add a `converted_customer_id` field to Sales, and a `vendor_id` field to Orders.**
Both are small, one-column schema changes, but they unlock real answers Vectral can't currently get: true cost-per-channel (is Inbound's bigger deal size actually worth its lower conversion rate, once cost is factored in?), and true vendor accountability (which vendor is actually behind the France/Australia problem?). I considered a workaround, fuzzy-matching leads to customers by country and industry, or spreading vendor performance evenly across orders in the same country and ruled both out. Either would produce a number, but an invented one dressed up as data is more likely to mislead a decision-maker than an honest "we can't answer this yet."

**4. Get eyes on the 166 leads still sitting in Lead and Qualified.**
This is a related but separate ask from #3. it's a sales-process question, not a data-model one. Right now there's no way to tell whether these are healthy, recently-created pipeline or leads that have gone quiet for months, because the data doesn't track how long a lead has sat in its current stage. I'd treat "add stage-aging data" as a companion fix to the two schema changes above. small to implement, and it turns a real blind spot into an answerable question the next time this kind of review happens.

---

**Data Limitations & Technical Gaps**

- **Untraceable Lead Acquisition Costs:** Sales lead records (`sales.csv`) and Customer account records (`customers.csv`) do not share a unified customer tracking ID. This prevents direct calculation of Customer Acquisition Cost (CAC) for won clients.
- **Missing Vendor-to-Order Connections:** Order records (`orders.csv`) lack a `vendor_id` reference. No order can be tied to the vendor that fulfilled it, meaning vendor performance numbers can only be viewed in aggregate.
- **Truncated Usage & Sample Scale:** Product usage data covers only the last 8 months rather than full account histories. The overall customer dataset is relatively small (145 customers), meaning observed patterns are directional rather than statistically proven.

---

**Core Business Metrics Framework**

To help Vectral move from reactive monitoring to proactive decision-making, a 15-metric operational framework was established across Sales, Operations, Product, and Finance.  
Key indicators such as **Win Rate by Lead Channel**, **Regional Fail/Cancel Rate**, and **Experiment Action Lift** — are surfaced directly in the executive dashboard above.

_(For the complete 15-metric definition list, including business ownership and decision rationale, see [Analysis](docs/03_analysis.md).  
For detailed technical documentation on initial data profiling, duplicate handling, schema mapping, and cleaning steps, see [Data Profiling](docs/01_data-profiling.md) and  
[Data Preparation](docs/02_data-preparation.md).)_
