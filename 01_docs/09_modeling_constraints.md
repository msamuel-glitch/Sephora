# Modeling Constraints & Operational Definitions
## Sephora Case 3 — Brand Affinity Detection

### 1. Proposed Composite Success Metric
The success of an affinity recommendation relies on a weighted composite score that explicitly balances conversion probability against strategic and monetary value.

**Proposed Formula (Weighted Affinity Success Score):**
`Composite Score = (w1 * conversion_propensity) + (w2 * expected_basket_uplift) + (w3 * expected_repeat_or_frequency_uplift) + (w4 * discovery_value) + (w5 * business_priority_overlay)`

*Component Justification:*
- **w1 * conversion_propensity**: The baseline statistical likelihood that the customer will adopt the recommended brand based on basket co-occurrence and similarity patterns.
- **w2 * expected_basket_uplift**: The direct monetary or unit turnover expected from the brand pairing. Focuses strictly on immediate basket growth.
- **w3 * expected_repeat_or_frequency_uplift**: The long-term capability of the proposed brand to generate recurrent purchases over time, building sustained customer value.
- **w4 * discovery_value**: A premium awarded if the recommendation introduces a customer to a brand they have never purchased before, accelerating portfolio penetration (as opposed to irrelevant new client acquisition).
- **w5 * business_priority_overlay**: An optional multiplier enforcing Sephora's strategic margin priorities (e.g., favoring Sephora Collection or Exclusive brands over Selective brands).

### 2. Feature Engineering Groups & Business Mapping
Features must be structurally mapped to Case 3 objectives prior to model training. 

#### Why each feature group exists in business terms:
| Feature Family | Corresponding Features | Sephora Business Objective |
|---|---|---|
| **Basket Co-occurrence** | `basket_brand_pairing`, `basket_axis_density`, `promo_pairing_rate` | **Basket growth:** Identifying natural cross-selling add-ons that increase average order value (e.g., in-store / app checkout check-out placement). |
| **Customer Similarity** | `profile_match_score`, `spend_decile_alignment` | **Customer value:** Finding lookalike customers to confidently pitch proven high-LTV brand paths via CRM/push targeting. |
| **Axis Similarity** | `cross_axis_propensity`, `axis_concentration` | **Brand discovery:** Identifying when a skincare buyer is ready to penetrate the makeup axis, serving App/Site recommendations. |
| **Market Similarity** | `market_desc_loyalty`, `premium_transition_rate` | **Customer value & Basket growth:** Mapping affinities between Selective and Exclusive tiers to encourage strategic trade-ups. |
| **Generation-Aware** | `gen_basket_index`, `gen_brand_appeal` | **CRM/push targeting:** Utilizing demographic segmentation to accurately pitch viral/trending brands to Gen Z vs. prestige brands to Gen X. |
| **Cold-Start Proxy** | `proxy_similarity_index`, `launch_receptiveness` | **Brand discovery:** Enabling recommendations for new or emerging brands with no history, crucial for app recommendation slots. |
| **High-Frequency/Value** | `velocity_score`, `loyalty_concentration` | **CRM/Push targeting & Store guidance:** Distinguishing the affinity patterns of highly engaged loyalists from opportunistic, low-frequency buyers. |

### 3. External Benchmark & Social-Trend Context
External market and social signals serve exclusively as a qualitative context layer. They will not be explicitly ingested into the quantitative recommendation engine to avoid contaminating the core structural logic of the dataset. Instead, they will be used to contextualize the narrative findings.
- **Primary Competitors:** Nocibé (direct primary benchmark), Yves Rocher (secondary comparison point).
- **Social Trend Constraints:**
  - **TikTok:** Critical qualitative overlay specifically for explaining viral Gen Z adoption patterns uncovered in the transactional data.
  - **X (Twitter):** Text-based monitor for broader brand sentiment to justify emerging shifts.
  - **Instagram:** Context for visual brand positioning, trailing behind TikTok's direct conversion dynamics.
