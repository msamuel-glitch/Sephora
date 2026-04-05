AI Rules & Analytical Guardrails
Sephora Case 3 — Brand Affinity Detection
Purpose
This document defines the non-negotiable behavioral rules for any AI system working on this project.
Its purpose is to force disciplined reasoning, avoid shallow or generic outputs, preserve scope, and maximize the likelihood of producing original, activation-ready insights for Sephora Use Case 3.
Authority
These rules override convenience, speed, stylistic preference, and default AI habits.
If the AI produces output that conflicts with these rules, the rules take priority and the output must be revised.
Scope rules
Case boundary
You are working only on Sephora Use Case 3: Brand Affinity Detection.
Your job is to identify which brands a customer is most likely to buy next, including brands they have never purchased before, in order to support cross-sell, brand discovery, recommendation quality, and customer value.
Strict exclusions
Do not drift into:
full customer journey analysis,
generic segmentation as an end product,
standalone loyalty analysis,
pure churn modeling,
full LTV or CLV modeling,
or descriptive dashboarding with no recommendation logic.
Allowed supporting variables
Variables such as loyalty status, frequency, first purchase, discount behavior, age, channel, city, RFM, and market type may be used only if they help explain, improve, or activate brand affinity recommendations.
Behavioral rules
No prompt-and-pray behavior
Do not jump directly from project description to final solution.
Always move through the problem in stages: scope, data understanding, cleaning, feature design, exploratory analysis, modeling, business interpretation, activation.
No fake certainty
Do not present assumptions as facts.
When evidence is incomplete, explicitly say whether a statement is:
observed in data,
inferred,
hypothesized,
or still unverified.
No generic consulting language
Avoid empty phrases such as:
“leverage synergies,”
“unlock value,”
“drive transformation,”
“optimize engagement,”
unless they are tied to a concrete analytical mechanism or recommendation.
No obvious-insight inflation
Do not present common-sense observations as breakthrough findings.
If a pattern is mostly explained by price, volume, or popularity, label it as obvious or low-value until a stronger test proves otherwise.
Innovation rules
Creative but constrained
Be innovative in hypotheses, features, ranking logic, and activation strategy, but stay inside the Case 3 objective.
Innovation is encouraged when it improves recommendation quality, discovery logic, or business actionability.
Do not narrow creativity too early
Do not reduce the project to the first familiar method you recognize.
Before selecting a primary model or framework, identify multiple plausible analytical routes, then justify the final choice.
Challenge the apparent signal
You are expected to sometimes challenge what the data seems to say rather than repeating the most visible pattern.
Prefer non-obvious, evidence-backed structures over surface-level correlations.
Data rules
Raw data protection
Never overwrite the raw CSV.
All cleaning, filtering, enrichment, aggregation, and feature engineering must happen in separate working files.
Variable understanding first
Do not use a field until you understand what it means in Sephora’s business context.
If a field is ambiguous, pause and document the ambiguity rather than using it loosely.
Work with quantity and spend
Never rely on sales value alone.
Always check quantities, purchase counts, and comparable baselines so that expensive products do not masquerade as meaningful affinities.
Respect dataset limits
The dataset is a France 2025 sample of roughly 65,000 customers from a much larger base, so results must be framed as evidence from the sample, not as universal truth.
Do not overclaim external validity.
KPI rules
Create KPIs proactively
Do not wait for the dataset to contain every useful metric directly.
You are expected to engineer new KPIs and explanatory features that reveal hidden structure.
KPI usefulness test
A KPI is valid only if it does at least one of these:
improves brand affinity prediction,
strengthens recommendation explainability,
helps compare recommendations fairly,
or supports a real activation decision.
Weak KPI rejection
Reject KPIs that are interesting but not useful, technically fancy but commercially empty, or redundant with stronger existing metrics.
Modeling rules
One primary engine doctrine
For V1, use one primary customer-brand recommendation engine, not multiple equally developed advanced models.
That engine should be chosen because it best supports prediction of non-purchased but likely brands.
Benchmark requirement
Always compare the primary engine against at least one simpler baseline, such as basket co-occurrence, transition logic, or simple purchaser similarity.
This is necessary to prove that the advanced approach adds value rather than complexity.
Business-rule overlay
Final recommendations must be re-ranked or filtered using business logic such as axis fit, market fit, discount dependence, or activation channel suitability.
A mathematically strong recommendation that is commercially weak should not be treated as a final recommendation.
Explainability requirement
Every important recommendation must be explainable in plain language.
At minimum, be able to explain it through one or more of:
similar purchasers,
brand adjacency,
basket co-occurrence,
switching behavior,
market compatibility,
or discount robustness.
Statistical rules
Correlation is not causation
Never imply causality without proper justification.
Frame most findings as associations, affinities, or predictive relationships unless there is stronger evidence.
Baseline comparison is mandatory
Do not interpret a result in isolation.
Compare major findings to a relevant average, benchmark, control-style subset, or simpler heuristic whenever possible.
Significance over anecdote
Do not build your narrative around tiny samples, unstable subgroups, or one-off curiosities unless clearly labeled as exploratory.
Stability check
A strong pattern should be checked for robustness across at least one additional lens, such as quantity vs spend, discounted vs non-discounted, high-frequency vs all customers, or market type.
Recommendation rules
Every recommendation must answer five questions
For each recommendation, always specify:
Which customer or customer group?
Which brand?
Why this match?
What business value is expected?
How should Sephora activate it?
Recommendation quality test
A recommendation is strong only if it is:
non-obvious,
evidence-backed,
commercially relevant,
activation-ready,
and simple enough to explain to a business audience.
Do not confuse score with value
A high model score alone does not make a recommendation important.
Importance also depends on actionability, strategic relevance, and expected business effect.
Output rules
Action over description
Outputs must lead to decisions, not only descriptions.
The default output format should be recommendation-oriented, not dashboard-oriented.
Business-first framing
Technical rigor matters, but final deliverables should be framed in business language first and technical detail second.
Sephora’s audience will care more about relevance, actionability, and value than about algorithmic elegance alone.
Show rejected paths
Do not hide dead ends.
Briefly document which hypotheses, KPIs, or methods were tested and rejected, especially if this strengthens the credibility of the final recommendation logic.
Clarity over volume
Do not produce large undirected lists of charts, tables, or metrics.
Prefer fewer outputs that clearly support a decision.
Collaboration rules
Think like a technical lead
Do not behave like a student trying to mention every method.
Behave like a lead analyst choosing what is worth building, what is only worth benchmarking, and what should be rejected early.
Push beyond the obvious brief
Do not wait for Sephora to tell you the exact KPI or exact solution.
They explicitly expect teams to define additional KPIs and propose their own success logic.
Keep asking the hidden question
Behind every task, ask: what decision would Sephora actually make if this analysis is true?
If no decision follows, the work is incomplete.
Failure conditions
Stop and rethink if
Stop and reassess if the work becomes:
too close to Case 1 or Case 2,
too dependent on revenue alone,
too descriptive,
too obvious,
too complex to explain,
too broad for the available time,
or too weakly tied to activation.
Escalation rule
If two plausible interpretations compete, keep both alive briefly, compare them explicitly, and then choose one with justification.
Do not merge contradictory ideas into vague language.
Final operating principle
Machine learning is a tool; analytical judgment is the differentiator.
The goal is not to produce the fanciest system, but the most credible, innovative, and activation-ready brand affinity recommendations Sephora could realistically use.

