# Business Rules Update
## Sephora Case 3 — Brand Affinity Detection

This document captures the latest non-negotiable business rules and strategic directions following client discussions.

### 1. Generation as a Strategic Core
The `age_generation` variable is elevated to a core strategic variable. Analysis must track generation-based differences across:
- Basket value
- Frequency
- Openness to discovery
- Propensity to adopt new/emerging brands

### 2. Value-Justified Recommendations
Recommendations cannot simply state "bought X, will buy Y". They must justify the *value* of the recommendation:
- Higher basket potential
- Higher units potential
- Higher frequency
- Stronger brand discovery 
- Increased customer value potential

### 3. Activation Hierarchy
System outputs must be natively designed for the exact Sephora activation pipeline, in this priority order, prioritizing outbound targeted communication:
1. **Priority 1:** CRM / Email / Push Notifications
2. **Priority 2:** App / Website recommendation slots
3. **Priority 3:** Store advisor / In-store guidance

### 4. High-Frequency Profiling
High-frequency customers must be explicitly isolated and profiled. A dedicated workstream must compare them against the general base to determine if affinity quality and commercial value uniquely improve in that subgroup.

### 5. Brand-Family Arbitration
Recommendations must not assume identical value across brand families. Differences in Sephora Collection vs Exclusive vs Selective margins and strategic weights must remain a visible arbitration overlay in the final logic.

### 6. Anti-Triviality & Revenue Constraints
- **No Revenue-Only Conclusions:** All monetary interpretations must be paired with quantity or comparable unit metrics to prevent high-priced items from generating false affinity signals.
- **Filter Obvious Results:** Statistically strong but commercially trivial formulas must be systematically rejected.

### 7. Explicit Baseline Logic & Cold-start
Feature engineering must be structurally completed before modeling. A distinct logic stream must be created for cold-start (new/low-history) brands that breaks from historical co-occurrence reliance and leverages proxy similarity.
