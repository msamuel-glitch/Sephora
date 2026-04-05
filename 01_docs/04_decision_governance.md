Decision Governance & Definition of Done
Sephora Case 3 — Brand Affinity Detection
Purpose
This document defines how decisions are made during the project, how findings are judged, when analysis is considered sufficient, and what standard a recommendation must meet before it is considered presentation-ready.

Its role is to prevent endless analysis, weak conclusions, premature stopping, and technically impressive but commercially empty outputs.

Governing principle
The project is done not when every possible analysis is exhausted, but when the strongest insights are sufficiently evidenced, non-obvious, activation-ready, and clearly superior to simpler alternatives.

Decision hierarchy
First priority
Priority 1 is Case 3 relevance.

If a result does not directly improve brand affinity understanding, customer-brand recommendation quality, or activation logic, it is secondary at best and should not dominate time or presentation space.

Second priority
Priority 2 is business actionability.

A finding matters only if Sephora could reasonably use it in CRM, e-merchandising, app feeds, store guidance, launch targeting, or bundle logic.

Third priority
Priority 3 is evidence quality.

A strong idea with weak evidence is exploratory; a moderately exciting idea with strong evidence and clear activation may be more valuable.

Fourth priority
Priority 4 is novelty after control for obviousness.

Findings that merely restate high sales, high prices, or high popularity are weaker than findings that reveal hidden brand relationships, switching structures, or well-justified discovery opportunities.

Classification system
Exploratory finding
A finding is exploratory if it is directionally interesting but still incomplete.

Typical reasons:

insufficient baseline comparison,

weak sample size,

unclear actionability,

limited stability checks,

or unresolved alternative explanations.

Validated insight
A finding becomes a validated insight when it:

is clearly within Case 3,

has been compared against a relevant baseline,

survives at least one robustness check,

avoids an obvious price-only explanation,

and supports a plausible Sephora action.

Presentation-ready recommendation
A finding becomes presentation-ready only when it is translated into a recommendation answering:

who,

what brand,

why,

expected value,

and activation route.

It must also be simple enough to explain to a business audience in a short verbal explanation.

Evidence thresholds
Minimum evidence standard
A finding cannot be treated as strong unless it has:

a clear definition,

measurable evidence,

a baseline or comparison point,

and a business interpretation.

Baseline requirement
Where possible, compare findings to:

global average basket behavior,

global brand adoption behavior,

simple baseline recommendation logic,

average quantity or frequency,

or another clearly justified benchmark.

Robustness requirement
A high-priority finding must be checked through at least one additional lens, such as:

spend versus quantity,

discounted versus full-price behavior,

high-frequency customers versus all customers,

Sephora / Exclusive / Selective split,

or repeat versus first-time purchase dynamics.

Weak evidence warning
A finding should remain provisional if it depends mainly on:

very rare brands,

extremely small customer subsets,

one unstable metric,

or an interpretation that changes sharply with a minor assumption.

Obviousness filter
Low-hanging fruit rule
If the finding is basically “popular brands are purchased together” or “expensive categories increase revenue,” it is not enough by itself.

It may remain in supporting analysis, but it should not be positioned as a headline insight.

Value-over-obviousness rule
A weaker-looking but genuinely non-obvious insight may deserve more emphasis than a statistically larger but trivial one.

The project should privilege hidden, decision-useful structure over superficial size.

Escalation rule
If an insight looks obvious at first glance, continue only if deeper analysis reveals a more nuanced mechanism, such as:

discount dependence,

asymmetric switching,

market-type differences,

brand discovery potential,

or strong divergence from average behavior.

Stop rules
Stop an analysis branch if
Stop or deprioritize a branch when one or more of these are true:

it mainly answers Case 1 or Case 2,

it produces only descriptive outputs,

it does not improve recommendations,

it cannot be activated,

it is too obvious,

it depends on data not available,

or it adds complexity without clear business gain.

Stop digging deeper if
A line of analysis is sufficiently explored when:

the main mechanism is clear,

additional iterations produce little new business value,

and the current insight is already strong enough to defend.

Continue deeper if
Continue exploring only if:

the current result still has unresolved ambiguity,

the pattern may still be explained by a trivial factor,

the action is unclear,

or one more check could materially strengthen the final story.

Model governance
Model choice rule
The chosen primary model is acceptable only if it beats or meaningfully complements a simpler benchmark on either recommendation quality, interpretability, or activation usefulness.

No complexity premium
A more advanced model does not automatically deserve selection.

If a simpler method is nearly as good and easier to explain, the simpler method may be the better business choice.

Promotion to final model
A model may be treated as the final engine only when:

its objective matches Case 3,

it performs credibly against baseline logic,

it supports non-purchased brand discovery,

and its outputs can be translated into concrete actions.

Recommendation ranking
Ranking dimensions
All candidate recommendations should be scored qualitatively or quantitatively on:

relevance to customer or segment,

strength of evidence,

non-obviousness,

activation feasibility,

expected business value,

strategic fit for Sephora,

and explainability.

Final recommendation tiers
Use this three-tier ranking:

Tier A: strongest, presentation-ready, highly actionable,

Tier B: promising and useful, but still needs one more check or clearer activation framing,

Tier C: exploratory, interesting, not yet strong enough for headline use.

Presentation focus rule
Only Tier A insights should dominate the final storyline.

Tier B can support the appendix or backup slides, while Tier C should mostly remain internal unless it explains why a more obvious route was rejected.

Definition of done
Analytical done
The analysis is “done enough” when:

the team has a clear primary engine,

at least one meaningful benchmark exists,

the main recommendation logic has been validated,

weak paths have been rejected,

and additional analysis is no longer likely to change the top recommendations materially.

Business done
The project is business-ready when the team can clearly answer:

what Sephora should recommend,

to whom,

through which channel,

with what expected business rationale,

and why this is better than a simpler alternative.

Presentation done
The work is presentation-ready when:

the top insights are not obvious,

the evidence is defensible,

the recommendations are activation-ready,

the limitations are acknowledged,

and the narrative is simple enough for business stakeholders to remember.

Required outputs before declaring done
Minimum analytical package
Before declaring the project complete, there must be:

one defined primary recommendation engine,

one baseline comparison,

one customer-brand recommendation table,

one brand-to-brand or basket-level affinity summary,

one activation mapping,

one limitations section,

and one shortlist of top recommendations.

Minimum storytelling package
Before declaring presentation readiness, there must be:

a clear problem statement,

a clear modeling logic,

3 to 5 headline insights,

2 to 4 prioritized recommendation examples,

and a short explanation of why these are valuable for Sephora.

Tie-break rules
When two insights compete
Choose the one that is more actionable, more robust, and easier to explain.

If still tied, prefer the one that better supports non-purchased brand discovery, since that is central to Case 3.

When two models compete
Prefer:

better alignment to Case 3,

stronger benchmark outperformance,

better explainability,

easier activation,

lower complexity.

When time runs short
If time becomes the main constraint, prioritize:

validating the strongest existing insights,

tightening the recommendation logic,

and improving activation framing,
rather than opening new exploratory branches.

Failure conditions
The project is not done if
The project is not done if:

it still reads like broad exploration,

the main recommendation logic is unclear,

the top insights are obvious,

the model is technically interesting but commercially vague,

or Sephora would still have to guess what action to take.

The project has gone too far if
The project has gone too far if:

complexity now exceeds explainability,

the team is still adding analyses with diminishing value,

or the final message becomes less clear rather than more convincing.

Final rule
“Done” means strong enough to defend, useful enough to act on, and focused enough to present.

It does not mean perfect, exhaustive, or maximally complex