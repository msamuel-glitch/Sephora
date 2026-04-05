# Data Audit & Proposed Cleaning Plan
## Sephora Case 3 — Brand Affinity Detection

### A. Confirmed Cleaning Actions
- **Dropped exact row duplicates:** 892 perfectly identical rows were permanently removed, ensuring basket compositions are not artificially inflated.
- **Protected ID Types:** Cast `anonymized_card_code` and `anonymized_Ticket_ID` to strictly non-numeric strings to preserve them exclusively for grouping/joining.
- **Created Anomaly Flags:** Instead of destructive filtering, the following boolean flags were safely created to tag problematic rows:
  - `flag_negative_sales` (5,210 rows)
  - `flag_zero_sales` (8,008 rows)
  - `flag_negative_quantity` (4,979 rows)
  - `flag_zero_quantity` (5,676 rows)
  - `flag_discount_gt_sales` (14,571 rows)
- **Resolved Missing Categoricals:** Attempted deterministic recovery for `brand` and `Market_Desc` from `materialCode`. Zero values were recoverable (missing fields map to missing materials or new item codes). Remaining nulls (5,283 `brand` and 5,461 `Market_Desc`) were filled with `"UNKNOWN"`.

### B. Flagged but Deferred Issues
- **First Purchase missingness (74%):** No imputation or dummy-filling yet. The exact trigger will be investigated in EDA without modifying the raw structure.
- **Discounts exceeding sales:** `discountEUR` > `salesVatEUR` will not be dropped. We will investigate if this identifies 100% reward redemptions.
- **Ticket+Product Duplicates (104 rows):** These are kept intact. Profiling reveals they are mostly split lines or in-ticket return/exchanges (e.g., Qty: 1 and Qty: -1 for the exact same `materialCode` in one `anonymized_Ticket_ID`). These will naturally be handled by the eligibility rule.
- **Geographic Perimeters:** `countryIsoCode` is intact. Monaco and Luxembourg remain valid elements of the France database scope.

### C. Proposed `eligible_for_affinity_v1` Rule
**Logic:** A transaction line is eligible for brand affinity modeling *only if* it represents a mathematically valid, positive engagement with a product.
`eligible_for_affinity_v1 = ~(flag_negative_sales | flag_zero_sales | flag_negative_quantity | flag_zero_quantity)`
- **Impact:** 13,226 rows fail this test (returns, exchanges, zero-value samples).
- **Resulting Clean Base:** 385,879 true product interactions ready for feature engineering and recommendation logic.

---
### D. Post-Phase-4 Corrections
Two targeted fixes were implemented after the initial feature engineering run to resolve data quality flags:
1. **MAEK UP Typo:** Corrected the upstream data entry error by mapping "MAEK UP" to "MAKE UP" across all affected tables and re-deriving all axis-dependent metrics.
2. **Age Generation Gap Inference:** Approximately ~31% of the sample originally lacked an explicit generation label. Leveraging Sephora's own observed cohort boundaries, generation was systematically inferred for customers with a valid stated `age > 0`. Notably, this logic accurately populated the `genx` cohort spanning ages 46–60, bridging a major demographic gap in the raw cut, while properly isolating the remaining structurally missing users (age=0) explicitly as `"UNKNOWN"`.
