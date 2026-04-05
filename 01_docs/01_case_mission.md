Case Mission Document
Sephora Case 3 — Brand Affinity Detection
Project title
Sephora Case 3 — Brand Affinity Detection for Cross-Sell Activation
Core objective
Identify which brands each customer is most likely to buy next, including brands they have never purchased before, in order to identify cross-sell opportunities, accelerate brand discovery, improve personalized recommendations, and increase basket and customer value.
Business problem
Customers show implicit brand affinities through basket composition, repeat behavior, product mix, market type, channel behavior, and profile similarity, but these signals remain underexploited. Sephora wants these hidden signals transformed into actionable recommendations that can support CRM, e-merchandising, app experiences, and store activation.
Strict scope
This work is limited to Use Case 3: Brand Affinity Detection.
Variables such as purchase frequency, basket size, loyalty status, first purchase, axis, market type, channel, discount behavior, and customer profile may be used only if they improve brand affinity scoring, recommendation quality, or activation logic.
What this is not
This project is not:
a full customer journey analysis,
a pure segmentation project,
a standalone loyalty or LTV study,
or a descriptive dashboard with no activation logic.
Strategic extensions allowed
To make the brand-affinity system more intelligent and less obvious, the analysis may test structured hypotheses about:
brand identity alignment, such as celebrity-led, sustainable, premium, or Sephora-owned positioning,
switching behavior, such as whether customers stay within a brand logic or move across brands over sequential purchases,
trade-up patterns, such as whether some customers appear ready to migrate toward more premium brands,
and discount dependence, such as whether an observed affinity holds mainly under promotion.
These extensions are valid only if they remain in service of the main Case 3 question: which brand should Sephora recommend next to which customer, and why?
Main analytical questions
The project must answer the following:
Which brands tend to co-occur within baskets in meaningful, non-obvious ways?
Which customers resemble the purchasers of a target brand closely enough to justify a recommendation, even if they have never purchased it?
Which non-purchased brands have the highest adoption potential per customer or customer group?
Which affinities are stable versus promotional, persistent versus switchable, weak versus activation-ready?
Which recommendations are most likely to improve basket value, customer value, brand discovery, or recommendation relevance?
Business value standard
A finding is valuable only if it can support a real Sephora action such as:
CRM targeting,
app recommendation,
e-merchandising placement,
store-selling guidance,
cross-sell bundling,
or launch targeting for emerging brands.
If an insight is interesting but not actionable, it is incomplete.
Success definition
Sephora did not provide one fixed success metric and expects the team to propose a defensible success definition based on the analysis.
Acceptable success dimensions include:
increase in average basket value,
increase in quantity or diversity of products per basket,
stronger first-time adoption of recommended brands,
improved recommendation relevance,
and stronger contribution to customer value or loyalty potential through better cross-sell logic.
Technical evaluation metrics may be used internally to assess model quality, but the final framing should remain business-led.
Analytical standard
The work must go beyond obvious associations and quantify value where possible against relevant averages or baselines.
The analysis must avoid confusing high-priced products with true affinity, must use quantities alongside revenue, and must remain cautious about correlation versus causation.
Machine learning is a tool, but analytical judgment is the real differentiator.
Data context
The analysis will use an anonymized France 2025 sample of roughly 65,000 customers, shared across all three use cases.
The project must therefore:
filter for Case 3 relevant fields,
engineer new KPIs and features,
acknowledge sample limits,
and avoid overclaiming generalizability beyond the sample.
Decision philosophy
The project must not optimize for “interesting analysis.”
It must optimize for reliable, non-obvious, activation-ready brand affinity recommendations under evidence constraints.
Working principle
Every recommendation should answer five things:
Which customer or customer group?
Which brand?
Why this match?
What business value is expected?
How should Sephora activate it?

