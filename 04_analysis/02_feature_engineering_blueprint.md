# Feature Engineering Blueprint — Revision 2
## Sephora Case 3 — Brand Affinity Detection

### Document Control Confirmation
This blueprint was designed after a full re-read of:
- `07_data_audit_cleaning.md`: All features operate exclusively on `eligible_for_affinity_v1 = True` rows (385,879 valid interactions). Anomaly flags are respected. ID columns are used for grouping only. `UNKNOWN` brand/market fills are preserved.
- `08_business_rules_update.md`: Generation is a core conditioning dimension. All recommendations must be value-justified. Activation priority is CRM > App > Store. High-frequency customers are separately profiled. Brand-family arbitration is enforced. Anti-triviality and anti-revenue-only rules are active.
- `09_modeling_constraints.md`: The composite success score (w1–w5) governs recommendation ranking. Feature families must map to Sephora business objectives. External signals are narrative-only, never joined into the feature base.

---

## 0. Prediction-Time Design & Anti-Leakage Framework

### As-Of Date Logic
The dataset covers January 1 – December 31, 2025. We split time as follows:

| Window | Date Range | Purpose |
|---|---|---|
| **Feature Window** | Jan 1 – Sep 30, 2025 (9 months) | All features are computed exclusively from this period. |
| **Target Window** | Oct 1 – Dec 31, 2025 (3 months) | Used to evaluate whether a recommended brand was actually purchased. |

**Hard rule:** No feature may use any information from the target window. Every aggregation, lookup, and similarity computation is bounded by the as-of date of September 30, 2025.

### Target Definition
For each customer, the target is binary per candidate brand:
- `target = 1` if the customer purchased brand B at least once during Oct–Dec 2025 AND had never purchased brand B during Jan–Sep 2025.
- `target = 0` otherwise.

This directly operationalizes the Case 3 mission: "predict brands a customer has not yet purchased."

### Leakage Prevention Checklist
- Brand co-occurrence lift: computed from feature-window baskets only.
- Customer similarity: computed from feature-window brand vectors only.
- Generation/loyalty/RFM features: snapshot at or before Sep 30.
- Cold-start brand classification: based on feature-window transaction counts only.

---

## 1. Candidate-Generation Framework

For each customer, candidate brands are generated through four independent routes. The union of all routes forms the candidate set scored by the recommendation engine.

### Route 1 — Basket-Pair Route
- For each brand B the customer has purchased, find all brands that co-occur with B in other customers' baskets with `brand_cooccurrence_lift > threshold_lift`.
- Exclude brands the customer already purchased in the feature window.
- **Threshold:** `lift > 1.5` is a placeholder. Will be calibrated by testing lift thresholds [1.2, 1.5, 2.0, 3.0] against target-window hit rate.

### Route 2 — Lookalike-Customer Route
- Find the top-K most similar customers (by `profile_match_score` on feature-window brand vectors).
- Collect brands purchased by those similar customers but not by the target customer.
- **Threshold:** `K = 50` is a placeholder. Will be calibrated by testing K values [20, 50, 100] against recall in the target window.

### Route 3 — Axis/Market Expansion Route
- If the customer has high `cross_axis_discovery_propensity` or low `axis_concentration`, surface brands from adjacent axes they have not tried.
- If the customer shows `selective_to_exclusive_tradeup_score > 0`, surface Exclusive brands in their dominant axis.
- **Threshold:** Propensity thresholds are placeholders, calibrated against actual cross-axis adoption rates in the target window.

### Route 4 — Cold-Start Route
- For brands classified as cold-start (see Section 3 below), candidates are generated via `proxy_similarity_index` matching to established brands the customer already purchases.
- Filtered by `launch_readiness_score` of the customer to avoid targeting non-receptive users.

**Final candidate set** = Union(Route 1, Route 2, Route 3, Route 4), deduplicated.

---

## 2. Analytical Layer Architecture

### Layer 1 — Core Affinity Signal
Features that capture brand relationships, customer similarity, axis/market proximity, and purchase pattern structure.

### Layer 2 — Business Value Overlay
Features that estimate expected basket uplift, repeat potential, strategic brand-family value, and discovery upside.

### Layer 3 — Activation & Storytelling Overlay
Features that support activation routing by CRM/app/store, generation-conditioned interpretation, and post-scoring recommendation explanation.

---

## 3. Cold-Start: Two Distinct Cases

### Case A — Emerging Brands (Limited History)
Brands with **fewer than 50 unique purchasers** in the feature window (Jan–Sep 2025). These brands exist in the dataset but lack sufficient co-occurrence data for reliable lift computation.

**Strategy:** Use `proxy_similarity_index` to map them to established brands via shared (Axe_Desc, Market_Desc, top-generation purchaser profile). Score customers via the established brand's affinity patterns, discounted by an uncertainty factor.

### Case B — Truly Unseen New-Launch Brands
Brands with **zero transactions** in the feature window. These cannot be scored from transactional data at all.

**Strategy:** Define the new brand by its (Axe_Desc, Market_Desc, target generation, price tier) profile. Use `launch_readiness_score` and `novelty_receptiveness_score` to rank customers by their general openness to new brands in that axis/market/generation slot. This is a profile-matching approach, not a co-occurrence approach.

**Threshold note:** The 50-purchaser cutoff for "emerging" is a placeholder. Will be calibrated by testing cutoffs [20, 50, 100] and checking whether proxy recommendations for brands below each cutoff match actual target-window adoptions.

---

## 4. Full Feature Inventory

### A. Basket Co-occurrence (Layer 1)

| Feature | Hypothesis | Calculation | Grain | Type | Cold-Start? | Leakage Risk | Sephora Objective |
|---|---|---|---|---|---|---|---|
| `brand_cooccurrence_lift` | Brands bought together more than chance reveals structural affinity | P(A∩B) / (P(A)*P(B)) within feature-window baskets | brand-pair | Predictive | No | Low | Basket growth |
| `basket_complementarity_score` | True complementarity = adding distinct axes, not redundancy | Count distinct Axe_Desc in baskets containing both brands / max possible axes | brand-pair | Predictive | No | Low | Basket growth |
| `basket_axis_density` | Higher axis diversity in a basket signals cross-sell readiness | Count distinct axes per basket, averaged per customer | customer | Predictive | N/A | Low | Basket growth, Brand discovery |
| `promo_pairing_rate` | Co-occurrences under heavy discount are fragile affinities | Share of co-occurrences where combined discount rate > calibrated threshold | brand-pair | Guardrail | No | Low | Anti-obviousness |

### B. Customer Similarity (Layer 1)

| Feature | Hypothesis | Calculation | Grain | Type | Cold-Start? | Leakage Risk | Sephora Objective |
|---|---|---|---|---|---|---|---|
| `profile_match_score` | Customers with similar brand portfolios share hidden affinities | Cosine similarity on feature-window customer-brand purchase vectors, excluding target brand | customer-pair | Predictive | No | Medium: must exclude target brand | Customer value |
| `spend_decile_alignment` | Same-tier customers adopt similar brands | Assign customer to feature-window spend decile, compare brand adoption rates within decile | customer | Interpretive | Yes (proxy) | Low | CRM/push targeting |
| `loyalist_vs_explorer_index` | Concentrated vs diversified buying = different recommendation strategies | 1 - HHI(brand spend share). 0=pure loyalist, 1=pure explorer | customer | Predictive + Interpretive | N/A | Low | Customer value, Brand discovery |

### C. Axis Similarity (Layer 1)

| Feature | Hypothesis | Calculation | Grain | Type | Cold-Start? | Leakage Risk | Sephora Objective |
|---|---|---|---|---|---|---|---|
| `cross_axis_discovery_propensity` | Customers buying across multiple axes are more receptive to cross-sell | Distinct axes purchased / 5 | customer | Predictive | Yes (proxy) | Low | Brand discovery |
| `axis_concentration` | Heavy concentration reveals untapped adjacent territory | Max axis share of spend | customer | Interpretive | Yes (proxy) | Low | App/site recommendation |
| `axis_brand_penetration` | Within primary axis, how many brands tried? | Distinct brands / total distinct brands available in that axis (feature window) | customer-axis | Predictive | Partially | Low | Brand discovery |

### D. Market Similarity (Layer 1 + Layer 2)

| Feature | Hypothesis | Calculation | Grain | Type | Cold-Start? | Leakage Risk | Sephora Objective |
|---|---|---|---|---|---|---|---|
| `market_desc_loyalty` | Some customers are locked into one market type | Share of spend in dominant Market_Desc | customer | Interpretive | Yes (proxy) | Low | Brand-family arbitration |
| `selective_to_exclusive_tradeup_score` | Rising Exclusive share signals migration readiness | (Exclusive spend share in months 7–9) - (Exclusive spend share in months 1–3) | customer | Predictive | Yes (proxy) | Low | Customer value, Strategic arbitration |
| `exclusive_to_sephora_migration_score` | Trending toward Sephora Collection = highest-margin path | Same logic for Sephora Collection share trend | customer | Predictive | Yes (proxy) | Low | Strategic arbitration |
| `sephora_collection_attach_potential` | Non-buyers matching buyer profiles = untapped margin targets | Binary: profile similarity to Sephora Collection buyers (excluding SC from similarity input) | customer | Predictive | Yes (proxy) | Medium: exclude target from similarity | Basket growth, Strategic arbitration |

### E. Generation-Aware Behavior (Layer 1 + Layer 3)

| Feature | Hypothesis | Calculation | Grain | Type | Cold-Start? | Leakage Risk | Sephora Objective |
|---|---|---|---|---|---|---|---|
| `gen_basket_index` | Basket behavior differs by generation | Customer avg basket / generation avg basket (feature window) | customer | Interpretive | Yes | Low | CRM/push targeting |
| `gen_brand_appeal` | Some brands over-index in specific generations | Brand purchase rate within generation / global brand purchase rate (feature window) | brand-generation | Predictive | Partially | Low | CRM/push targeting |
| `generation_discovery_gap` | Gen Z discovers more brands faster | Distinct brands in first 3 months of feature window, conditioned by generation | customer | Predictive + Wow | Yes | Low | Brand discovery |
| `generation_brand_loyalty_index` | Older generations exhibit stickier brand loyalty | Repeat rate of top brand, segmented by generation | customer-generation | Interpretive + Wow | Yes | Low | Customer value |

### F. Cold-Start / New-Brand Proxy Logic (Layer 1 + Layer 2)

| Feature | Hypothesis | Calculation | Grain | Type | Cold-Start? | Leakage Risk | Sephora Objective |
|---|---|---|---|---|---|---|---|
| `proxy_similarity_index` | New brands match existing brands via axis + market + generation overlap | Jaccard similarity of (Axe, Market, top-generation purchasers) between emerging and established brands | brand-pair | Predictive | **Yes — designed for this** | Low | Brand discovery |
| `novelty_receptiveness_score` | Some customers consistently adopt low-history brands | Share of purchases going to brands with < calibrated purchaser threshold in feature window | customer | Predictive + Wow | Yes | Low | Brand discovery |
| `launch_readiness_score` | Composite launch-targeting signal | Weighted: `novelty_receptiveness_score` * 0.4 + `loyalist_vs_explorer_index` * 0.3 + generation_weight * 0.3. Weights are placeholders; will be calibrated against target-window new-brand adoption | customer | Predictive + Activation | Yes | Low | App/site recommendation |
| `brand_history_depth` | Classifies brands into Established / Emerging / Unseen for routing | Count of unique purchasers in feature window: ≥50 = Established, 1–49 = Emerging, 0 = Unseen. Threshold is placeholder | brand | Routing | Yes | None | Cold-start routing |

### G. High-Frequency / Loyalty Value (Layer 2)

| Feature | Hypothesis | Calculation | Grain | Type | Cold-Start? | Leakage Risk | Sephora Objective |
|---|---|---|---|---|---|---|---|
| `velocity_score` | Days between purchases reveals engagement intensity | Median inter-purchase gap in days (feature window) | customer | Predictive | N/A | Low | CRM/push targeting |
| `loyalty_concentration` | Spend share in top brand reveals lock-in vs opportunity | Spend on top brand / total spend (feature window) | customer | Interpretive | N/A | Low | Customer value |
| `repeat_potential_proxy` | Brands with high repeat rate among similar customers signal sticky affinity | Repeat rate of brand within customer's spend decile + generation (feature window) | brand-customer | Predictive | Partially | Low | Repeat/frequency |
| `brand_volatility_index` | Brands with high customer churn are riskier recommendations | 1 - (customers repurchasing / customers who ever purchased) in feature window | brand | Guardrail | No | Low | Anti-obviousness |
| `high_frequency_flag` | Isolate top-quartile purchasers for separate profiling | Binary: velocity_score < 25th percentile of inter-purchase gap. Threshold is placeholder, calibrated from distribution | customer | Segmentation | N/A | Low | CRM/push targeting |

### H. Sephora-Native Differentiator Features (Layer 1 + Layer 2)

| Feature | Hypothesis | Calculation | Grain | Type | Cold-Start? | Leakage Risk | Sephora Objective |
|---|---|---|---|---|---|---|---|
| `loyalty_status_at_snapshot` | Status at as-of date captures engagement tier | Last observed `status` value ≤ Sep 30. Mapped: 1=NoFid, 2=Bronze, 3=Silver, 4=Gold | customer | Interpretive | N/A | Low | CRM/push targeting |
| `loyalty_trajectory` | Rising status = growing engagement, sharper affinity | (Max status in months 7–9) - (Max status in months 1–3). Positive = upgrading | customer | Predictive | N/A | Low | Customer value |
| `rfm_segment_snapshot` | RFM segment at as-of date stratifies customer value | Last observed `RFM_Segment_ID` ≤ Sep 30 | customer | Interpretive | N/A | Low | CRM/push targeting |
| `rfm_trajectory` | Improving RFM = customer becoming more valuable | (Last RFM in months 7–9) - (First RFM in months 1–3). Lower = improving for segments 1–3 | customer | Predictive | N/A | Low | Customer value |
| `first_purchase_axis_imprint` | First axis purchased may shape long-term affinity | Axe_Desc of first purchase (from `Axe_Desc_first_purchase` where available) | customer | Interpretive | N/A (where available) | Low | Brand discovery |
| `first_purchase_market_imprint` | First market type may anchor brand-family preference | Market_Desc of first purchase (from `Market_Desc_first_purchase` where available) | customer | Interpretive | N/A (where available) | Low | Strategic arbitration |
| `recruitment_channel` | Channel of first purchase signals digital vs physical affinity | `channel_recruitment` value where available | customer | Activation | N/A (where available) | Low | Channel activation |
| `omnichannel_behavior_score` | Customers using multiple store_type_app values are omnichannel | Count of distinct `store_type_app` values used in feature window | customer | Activation | N/A | Low | Channel activation |
| `click_and_collect_propensity` | Click & collect users bridge digital and physical — hybrid activation | Share of transactions where channel = 'estore' AND store_code_name ≠ ESTORE pattern (per deck rule) | customer | Activation | N/A | Low | Channel activation |

### I. Brand-Family Arbitration (Layer 2)

| Feature | Hypothesis | Calculation | Grain | Type | Cold-Start? | Leakage Risk | Sephora Objective |
|---|---|---|---|---|---|---|---|
| `brand_family_switch_tolerance` | Some customers naturally cross market types; others don't | Entropy of Market_Desc distribution per customer | customer | Interpretive | Yes (proxy) | Low | Strategic arbitration |
| `market_priority_scenario` | Business priority varies by strategic context | Not a fixed constant. Three scenario overlays computed in parallel — see Section 5 below | brand | Activation | Yes | None | Strategic arbitration |

### J. Activation-Readiness (Layer 3)

| Feature | Hypothesis | Calculation | Grain | Type | Cold-Start? | Leakage Risk | Sephora Objective |
|---|---|---|---|---|---|---|---|
| `crm_push_eligibility_proxy` | High-frequency, multi-brand customers respond best to outbound push | velocity_score < calibrated_threshold AND loyalist_vs_explorer > calibrated_threshold | customer | Activation | Yes | Low | CRM/push targeting |
| `app_recommendation_affinity_proxy` | Customers with high digital channel share are best served via app | Share of feature-window purchases via APP/ESTORE/MOBILE/WEB | customer | Activation | Yes | Low | App/site recommendation |
| `store_guidance_affinity_proxy` | Customers with dominant in-store channel need beauty-advisor routing | Share of feature-window purchases via STORE channel | customer | Activation | Yes | Low | Store guidance |
| `channel_activation_fit_score` | Assigns best activation channel per customer | argmax of (crm_proxy, app_proxy, store_proxy) | customer | Activation | Yes | Low | Channel activation |

### K. Anti-Obviousness / Guardrails (Layer 2 + Layer 3)

| Feature | Hypothesis | Calculation | Grain | Type | Cold-Start? | Leakage Risk | Sephora Objective |
|---|---|---|---|---|---|---|---|
| `not_just_popularity_penalty` | Globally popular brands should not dominate recommendations | 1 / log(brand total feature-window transactions + 1) | brand | Guardrail | Yes | None | Anti-obviousness |
| `high_price_artifact_flag` | Co-occurrences driven by both items being expensive are false signals | Flag pairs where both brands' median price > 75th pctl AND quantity correlation < calibrated threshold. Threshold is placeholder | brand-pair | Guardrail | Yes | None | Anti-obviousness |
| `discount_dependency_ratio` | Affinities under heavy discount are fragile | Share of co-occurrences where combined discount rate > calibrated threshold | brand-pair | Guardrail | No | Low | Anti-obviousness |
| `trivial_association_flag` | Reject lift < calibrated_threshold among top-N brands by volume | Boolean. Threshold and N are placeholders. Calibrate by testing [1.2, 1.5, 2.0] and [10, 20, 30] | brand-pair | Guardrail | No | None | Anti-obviousness |
| `quantity_revenue_divergence` | Pattern in revenue but not quantity = price artifact | abs(rank_by_revenue - rank_by_quantity) per brand-pair | brand-pair | Guardrail | No | None | Anti-obviousness |

### Post-Scoring Interpretive Label

| Feature | Hypothesis | Calculation | Grain | Type | Cold-Start? | Leakage Risk | Sephora Objective |
|---|---|---|---|---|---|---|---|
| `recommendation_reason_code` | Human-readable explanation of the top-scoring route | Categorical: "similar_purchasers" / "basket_adjacency" / "axis_expansion" / "generation_fit" / "market_migration" / "cold_start_proxy". **Strictly post-scoring:** assigned after the composite score is computed, based on which candidate route and feature contributed most to the final score. Not a model input. | customer-brand | Interpretive (post-scoring only) | Yes | None | Storytelling |

---

## 5. Business-Priority Scenario Overlays

Instead of fixed constants, we define three parallel business-priority scenarios. The final presentation can show results under each scenario, letting Sephora choose.

| Scenario | Sephora Collection Weight | Exclusive Weight | Selective Weight | Rationale |
|---|---|---|---|---|
| **Margin-First** | 1.0 | 0.6 | 0.3 | Maximizes high-margin Sephora Collection recommendations |
| **Balanced Growth** | 0.7 | 0.8 | 0.6 | Balances margin with portfolio breadth |
| **Discovery-First** | 0.5 | 1.0 | 0.5 | Prioritizes Exclusive brand discovery and differentiation |

These weights are applied as the `w5 * business_priority_overlay` component in the composite success score. The final choice belongs to Sephora.

---

## 6. Threshold Calibration Protocol

Every threshold used in this blueprint is a **placeholder** unless stated otherwise. Calibration will follow this protocol:

1. **Define the threshold parameter** (e.g., lift cutoff, K neighbors, purchaser count for cold-start).
2. **Test multiple values** against the target-window hit rate (Oct–Dec 2025 actual purchases).
3. **Choose the value** that maximizes a combination of precision (recommendation quality) and coverage (candidate pool breadth).
4. **Robustness check:** Verify that the chosen threshold produces stable results when tested on a random 50/50 split of the feature-window data.

| Threshold | Placeholder Value | Calibration Range | Robustness Test |
|---|---|---|---|
| Co-occurrence lift cutoff | 1.5 | [1.2, 1.5, 2.0, 3.0] | 50/50 split stability |
| Lookalike K neighbors | 50 | [20, 50, 100] | Hit-rate variance across splits |
| Cold-start emerging cutoff | 50 purchasers | [20, 50, 100] | Proxy hit-rate for emerging brands |
| Discount dependency threshold | 30% combined rate | [20%, 30%, 40%] | Sensitivity of flagged pairs |
| High-price artifact qty correlation | 0.1 | [0.05, 0.1, 0.2] | Flagged pair stability |
| Trivial association lift floor | 1.5 among top-20 | lift [1.2, 1.5, 2.0], N [10, 20, 30] | False-rejection rate |
| High-frequency velocity percentile | 25th percentile | [10th, 25th, 33rd] | Subgroup size stability |

---

## 7. Output Table Design (Feature Mart)

The feature engineering phase will produce **four explicit output tables**, not one monolithic file.

### Table 1 — `dim_customer` (Customer-Level Features)
**Grain:** One row per `anonymized_card_code`.
**Contents:** All customer-level features from families B, C, E, G, H, I, J.
**Key columns:** `anonymized_card_code`, `loyalist_vs_explorer_index`, `cross_axis_discovery_propensity`, `velocity_score`, `loyalty_concentration`, `gen_basket_index`, `generation_discovery_gap`, `loyalty_status_at_snapshot`, `loyalty_trajectory`, `rfm_segment_snapshot`, `rfm_trajectory`, `omnichannel_behavior_score`, `click_and_collect_propensity`, `crm_push_eligibility_proxy`, `app_recommendation_affinity_proxy`, `store_guidance_affinity_proxy`, `channel_activation_fit_score`, `high_frequency_flag`, `novelty_receptiveness_score`, `launch_readiness_score`, `age_generation`.

### Table 2 — `dim_brand` (Brand-Level Features)
**Grain:** One row per `brand`.
**Contents:** All brand-level features from families A (aggregated), F, G, K.
**Key columns:** `brand`, `Market_Desc`, `Axe_Desc`, `not_just_popularity_penalty`, `brand_volatility_index`, `brand_history_depth`, `market_priority_scenario_margin`, `market_priority_scenario_balanced`, `market_priority_scenario_discovery`, `gen_brand_appeal_genz`, `gen_brand_appeal_millennial`, `gen_brand_appeal_genx`.

### Table 3 — `dim_brand_pair` (Brand-Pair Features)
**Grain:** One row per (brand_A, brand_B) pair where lift > minimum threshold.
**Contents:** All brand-pair features from families A, K.
**Key columns:** `brand_a`, `brand_b`, `brand_cooccurrence_lift`, `basket_complementarity_score`, `promo_pairing_rate`, `high_price_artifact_flag`, `discount_dependency_ratio`, `trivial_association_flag`, `quantity_revenue_divergence`, `proxy_similarity_index` (for cold-start pairs).

### Table 4 — `fact_customer_brand_candidate` (Candidate Scoring Table)
**Grain:** One row per (customer, candidate_brand) pair.
**Contents:** Merged features from Tables 1–3 plus candidate-generation route label.
**Key columns:** `anonymized_card_code`, `candidate_brand`, `candidate_route` (basket_pair / lookalike / axis_market / cold_start), all relevant features joined from dim tables, `eligible_for_scoring` flag.
**Note:** `recommendation_reason_code` is NOT included here. It is assigned strictly post-scoring, after the composite score ranks candidates.

---

## Features Most Likely to Create a Wow Moment in Final Presentation

1. **`generation_discovery_gap`** — "Gen Z discovers 3× more brands in 3 months than Gen X."
2. **`launch_readiness_score`** — "Here are the 5,000 customers to target for a brand that doesn't exist yet."
3. **`sephora_collection_attach_potential`** — "X% of high-value customers match the SC profile but have never bought it."
4. **`basket_complementarity_score`** — "This pair adds a new axis to the basket, not just another product."
5. **`loyalty_trajectory`** — "Customers upgrading from Bronze to Silver adopt 2× more new brands."
6. **`selective_to_exclusive_tradeup_score`** — "These customers are migrating toward Exclusive — intercept them now."
7. **`click_and_collect_propensity`** — "Omnichannel customers have X% higher brand diversity."
8. **`recommendation_reason_code`** — Every recommendation has a visible, human-readable *why*.
9. **`generation_brand_loyalty_index`** — "Brand stickiness is generation-dependent — CRM strategy must adapt."
10. **`brand_family_switch_tolerance`** — "Which customers naturally cross market boundaries?"

---

## Features Designed to Reject Weak Recommendations

1. **`not_just_popularity_penalty`** — Log-dampened inverse frequency suppressing dominant brands.
2. **`high_price_artifact_flag`** — Catches false co-occurrence driven by both brands being expensive.
3. **`trivial_association_flag`** — Rejects low-lift pairs among top brands by volume.
4. **`discount_dependency_ratio`** — Filters affinities that vanish at full price.
5. **`quantity_revenue_divergence`** — Catches patterns that hold in EUR but not in units.

---

## What Weaker Teams Would Probably Do

- Build a basic brand co-occurrence matrix using only basket overlap counts.
- Use raw purchase counts as the only affinity signal with no time-split discipline.
- Ignore generation entirely or treat age as a filter.
- Have no cold-start logic — new brands get no recommendations.
- Use revenue as the primary metric without quantity controls.
- Present a list of "top co-purchased brands" without explaining *why* or *for whom*.
- Have no candidate-generation framework — score all brands for all customers equally.
- Have no activation routing and no reason codes.
- Treat all market types identically.
- Use a single KPI without composite weighting.
- Hard-code thresholds without calibration.

## How Our Feature Layer Goes Beyond That

- **Formal prediction-time split** with explicit as-of date and target window preventing all leakage.
- **Four candidate-generation routes** ensuring coverage of co-occurrence, similarity, expansion, and cold-start.
- **Three analytical layers:** Signal → Value → Activation, not a flat feature table.
- **Four output tables** with clean grain definitions for reproducibility.
- **Dual cold-start handling:** Emerging brands (limited history) vs truly unseen brands (zero history).
- **Sephora-native features** exploiting loyalty trajectory, RFM trajectory, channel recruitment, first-purchase imprint, omnichannel behavior, and click-and-collect logic.
- **Generation-conditioned interpretation** at every level.
- **Five dedicated guardrail features** to systematically reject weak, obvious, or price-driven recommendations.
- **Scenario-based business priority overlays** instead of fixed constants.
- **Calibration protocol** for every threshold with robustness testing.
- **Post-scoring reason codes** for full explainability without model contamination.

---

## Leakage-Risk Audit

| Feature | Risk Level | Mitigation |
|---|---|---|
| `profile_match_score` | **Medium** | Exclude target brand from both profiles before computing similarity. |
| `sephora_collection_attach_potential` | **Medium** | Exclude Sephora Collection from similarity input. |
| All co-occurrence features | **Low** | Computed from feature-window population data only. |
| All customer-level features | **Low** | Computed from feature-window history only, bounded by as-of date. |
| All brand-level features | **Low** | Aggregated from feature-window population statistics. |
| `recommendation_reason_code` | **None** | Post-scoring label, never a model input. |
| Loyalty/RFM trajectory | **Low** | Uses only status values observed ≤ Sep 30. |

---

## Proposed Script Plan

1. **Load** `sephora_audit_labeled_base.csv`, filter to `eligible_for_affinity_v1 == True`.
2. **Apply time split:** feature window (Jan–Sep) vs target window (Oct–Dec).
3. **Compute Layer 1** on feature-window data: basket co-occurrence, customer similarity vectors, axis/market/generation features, Sephora-native features.
4. **Compute Layer 2** on feature-window data: cold-start proxies, brand-family scores, repeat potential, guardrails.
5. **Compute Layer 3** on feature-window data: channel proxies, activation fit scores.
6. **Build output tables:** `dim_customer`, `dim_brand`, `dim_brand_pair`, `fact_customer_brand_candidate`.
7. **Save** all four tables to `03_data_working/`. Do not overwrite `sephora_audit_labeled_base.csv`.
8. **Log** feature counts, distributions, null checks, and threshold placeholder values to `04_analysis/feature_engineering_log.txt`.
9. **Post-scoring only:** `recommendation_reason_code` will be assigned after composite scoring in a later phase.
