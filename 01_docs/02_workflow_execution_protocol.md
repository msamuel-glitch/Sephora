Workflow Execution Protocol
Sephora Case 3 — Brand Affinity Detection
Purpose
This protocol defines the exact order of work for Sephora Use Case 3 so that analysis remains business-aligned, technically rigorous, and activation-oriented.

Its role is to prevent scope drift, shallow pattern hunting, and premature modeling by forcing a disciplined sequence from business understanding to recommendation output.

Governing rule
01_case_mission.md must be checked before every major task.

If any planned analysis does not clearly improve brand affinity detection, recommendation quality, or activation logic for Case 3, it should be paused, challenged, or removed.

Phase 1
Scope confirmation
Before touching the dataset, restate the case in one sentence: identify which brands a customer is most likely to buy next, including brands never purchased before, in order to support cross-sell and recommendation actions.

Explicitly reject drift into full customer journey analysis, generic segmentation, churn modeling, or standalone LTV modeling.

Business interpretation
Translate the case into operational business questions:

What brand should be recommended?

To which customer or customer group?

On what behavioral basis?

Through which activation channel?

With what expected business value?

Innovation check
Before execution begins, propose at least 3 non-obvious analytical angles that still stay inside Case 3.

Allowed examples include switching behavior, discount dependence, trade-up signals, emerging-brand targeting, and margin-aware brand combinations.

Phase 2
File and data discipline
Confirm that:

raw CSV remains untouched in 02_data_raw/,

all transformed files go into 03_data_working/,

all notebooks/scripts go into 04_analysis/,

all outputs go into 05_outputs/.

Dataset inspection
Inspect the CSV before cleaning or modeling.

The agent must first understand:

row count and column count,

column types,

missing values,

duplicated rows,

cardinality of key fields,

date ranges,

whether tickets, customers, and products behave as expected.

Variable mapping
Map the raw columns to business meaning using the deck/schema, including customer ID, ticket ID, transaction date, spend, discount, quantity, brand, axis, market, channel, first purchase, loyalty status, and RFM-related fields.

No variable should be used in modeling until its business meaning is understood.

Phase 3
Case 3 filtering
Create a working Case 3 dataset from the raw CSV.

Keep only the variables needed for:

basket analysis,

customer-brand history,

brand similarity,

switching sequences,

activation scoring.

Data quality checks
Perform quality checks before feature creation:

missing or null brand names,

invalid or zero quantities,

negative or suspicious spend values,

discount inconsistencies,

duplicate transactions,

impossible dates,

inconsistent channel/store combinations.

Cleaning principle
Do not over-clean blindly.

Every cleaning decision must preserve business meaning and be logged with a short explanation of why it improves reliability for Case 3.

Phase 4
Feature engineering
Create new calculated fields because the most useful KPIs will not exist directly in the raw data.

At minimum, engineer features at four levels:

customer level,

basket level,

brand level,

customer-brand interaction level.

Core engineered features
The minimum first-pass feature set should include:

basket value,

basket quantity,

number of brands per basket,

number of axes per basket,

customer purchase frequency,

recency within 2025,

brand purchase count per customer,

share of spend by brand,

share of quantity by brand,

discount rate,

first purchase brand/axis/market,

channel usage mix,

market mix: Sephora / Exclusive / Selective.

Strategic engineered features
The protocol should also test more differentiating features:

repeat rate by brand,

brand switching rate,

next-brand transition counts,

full-price versus discounted brand affinity,

premium migration signals,

exploration score, meaning diversity of brands tried,

loyalty concentration score, meaning how concentrated a customer is on a small set of brands,

emerging-brand adjacency candidates.

Phase 5
Exploratory analysis
Before any advanced model, perform structured exploratory analysis.

This must include:

top brands by volume and spend,

market split across Sephora / Exclusive / Selective,

brand co-occurrence in baskets,

customer repeat concentration,

distribution of basket value and quantity,

discount behavior by brand and market type.

Obviousness filter
Any pattern that can be explained mainly by product expensiveness must be flagged as weak until validated with quantities, frequency, or comparable baselines.

The protocol must explicitly reject “expensive + expensive = insight” logic.

Baseline comparisons
Every important result should be compared to a baseline such as:

global average basket,

average quantity,

average repeat rate,

average brand adoption rate,

or average discount dependence.

Phase 6
Hypothesis testing
Convert marketing intuitions into explicit testable hypotheses rather than assumed truths.

Examples:

customers buying celebrity-led brands are less likely to switch,

sustainable-brand buyers show tighter affinity patterns,

some exclusive-brand buyers transition more naturally into Sephora Collection than selective-brand buyers,

some brands attract low-discount customers and are more activation-efficient.

Evidence standard
Each hypothesis must be classified as:

supported,

partially supported,

unsupported,

or inconclusive.

Statistical caution
Where possible, test whether differences are meaningful rather than anecdotal, and remain careful about correlation versus causation.

The goal is not to prove perfect causality, but to avoid overclaiming.

Phase 7
Modeling strategy
V1 must use one primary recommendation engine, not several equally developed model families.

The chosen engine should be the one most capable of identifying non-purchased but likely brands at customer level, because this is central to Sephora Case 3.

Primary engine rule
The default V1 recommendation engine should be a customer-brand affinity model, such as collaborative filtering, implicit feedback matrix factorization, or another scalable user-item propensity approach.

This primary engine is preferred because the case is not only about basket completion, but also about discovery, hidden affinity, and future brand adoption.

Benchmark rule
A simpler baseline model must still be built for comparison, but only as a benchmark, not as the main engine.

This baseline can be based on:

brand co-occurrence within baskets,

top brand transitions,

or simple purchaser similarity rules.

Business-rule overlay
Final recommendations must not come from model scores alone.

They should be filtered or re-ranked using business logic such as:

axis relevance,

market type fit,

discount dependence,

strategic value for Sephora Collection / Exclusive / Selective,

and activation feasibility by CRM, app, e-merchandising, or store usage.

Model selection discipline
Do not build multiple advanced recommenders in parallel unless early evidence clearly shows the primary engine is failing.

The sequence should be:

Build the benchmark.

Build the primary engine.

Compare them on recommendation quality and business usefulness.

Add business-rule re-ranking.

Stop unless there is strong evidence that a second advanced model is necessary.

Explainability rule
The chosen V1 engine must remain explainable enough for a business presentation.

Each recommendation should still be interpretable through supporting signals such as similar purchasers, related brands, basket adjacency, switching patterns, or market compatibility.

Innovation rule
Innovation is encouraged in feature design, scoring logic, and activation strategy more than in multiplying model families.

A technically simpler model with stronger activation logic is preferred over a complex system that is difficult to justify commercially.
Phase 8
Activation framing
No recommendation is complete unless it is paired with an activation use case.

Each recommendation should indicate whether it is better suited for:

eCRM,

app feed,

website recommendation,

store advisor support,

launch targeting,

or bundle/promo logic.

Business ranking
Rank findings not only by model score but also by business usefulness.

A recommendation may be deprioritized if it is:

too obvious,

too discount-dependent,

too low-volume,

too hard to activate,

or too weakly evidenced.

Margin-aware interpretation
Where useful, discuss differences between Sephora Collection, Exclusive, and Selective because Sephora explicitly signals that their business value and margins differ.

Do this carefully without replacing affinity logic with pure margin logic.

Phase 9
Output creation
The required output is not only an analysis file but a business-ready decision set.

The workflow must produce:

a ranked list of strongest affinity insights,

candidate recommendation rules,

high-value customer-brand opportunities,

weak or rejected hypotheses,

and risks/limitations.

Deliverable structure
Every major insight should be formatted as:

observation,

evidence,

why it matters,

recommended activation,

confidence level,

caveats.

Minimum “showable” outputs
Before final presentation work begins, the project must have at least:

1 customer-brand scoring table,

1 brand-to-brand affinity table,

1 switching matrix or sequential transition summary,

1 discount-sensitivity summary,

1 prioritized recommendation shortlist.

Phase 10
Review gate
Before moving into presentation mode, challenge the analysis with these questions:

Is this still clearly Case 3?

Is the finding non-obvious?

Is it based on comparable measures?

Is it actionable?

Is the evidence strong enough to present confidently?

Would Sephora’s marketing or merchandising team know what to do next with it?

Stop conditions
Pause or reject an analysis branch if:

it mainly answers a Case 1 or Case 2 question,

it depends on unavailable data,

it produces only descriptive output with no action,

it is impressive technically but weak commercially,

or it cannot be explained simply.

Final principle
The goal is not to produce the most complex model.

The goal is to produce the most credible, creative, and activation-ready brand affinity recommendations within the real limits of the dataset and the case brief.