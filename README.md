# Sephora Brand Affinity Intelligence
### Predicting the Next Brand a Customer Will Buy — Built for Sephora France

[![Live Demo](https://img.shields.io/badge/Live%20Demo-sephora--luxury--terminal-black?style=for-the-badge&logo=vercel)](https://sephora-luxury-terminal.onrender.com)
[![Python](https://img.shields.io/badge/Python-48%25-3776AB?style=for-the-badge&logo=python)](./04_analysis)
[![JavaScript](https://img.shields.io/badge/JavaScript-46%25-F7DF1E?style=for-the-badge&logo=javascript)](./08_luxury_data_terminal)
[![Albert School](https://img.shields.io/badge/Albert%20School-Case%203-FF0058?style=for-the-badge)](https://albert-school.fr)

> **"Customers who discover just one new brand spend €84.02 vs €72.53 for non-discoverers. That's +€11.49 per customer — across 50,805 customers."**

---

## What This Project Does

This project answers one question that Sephora's CRM team faces every day:

**Which brand will your customer buy next — even if they have never bought it before?**

Using 385,879 validated transactions from Sephora France FY2025, this project builds a full end-to-end Brand Affinity Detection system: from raw data cleaning through machine learning model selection, to a deployed interactive presentation used in a live business competition.

---

## Key Results

| Metric | Value |
|---|---|
| Customers analyzed | 50,805 |
| Brands mapped | 239 |
| Behavioral rules generated | 894 |
| Brand pairs validated (guardrail-clean) | 217 |
| Top actionable pairs deployed | 11 |
| Average basket lift (discoverers vs non) | +15.8% |
| LTV protected via suppression layer | €491,476 |
| VIP customers shielded from bad recs | 6,995 |
| Bad recommendations eliminated | 53.6% |

---

## The Explorer Index — A Proprietary Signal

The single most important innovation in this project is a metric we built from scratch: the **Explorer Index**.

Every customer is scored from 0 (purely brand-loyal) to 1 (purely exploratory) based on three behavioral signals: number of distinct brands purchased, cross-axis purchase rate, and share of transactions in the training window. The median Explorer Index across 50,805 customers is **0.41**.

The counterintuitive finding: **the less loyal a customer, the more valuable they are as a recommendation target.** Customers with Explorer Index above the median who received a cross-brand recommendation spent €84.02 on average. Those who did not: €72.53.

This metric is proprietary. Competitors like Nocibe recommend the same brand 90% of the time because they never measure willingness to explore.

---

## The Do-Not-Recommend Layer

Most recommendation systems optimize for mathematical affinity. This one also optimizes for commercial safety.

A three-stage filtration pipeline (Raw Basket Mining → ML Validation → Business Guardrails) reduced 8,357 candidate rules to 217 guardrail-clean pairs. A dedicated suppression layer shields 6,995 VIP customers from recommendations that are mathematically strong but commercially inappropriate — protecting €491,476 in estimated LTV.

---

## Live Interactive Presentation

The full 14-slide findings deck is deployed as an interactive web application:

**[sephora-luxury-terminal.onrender.com](https://sephora-luxury-terminal.onrender.com)**

Built with HTML/CSS/JavaScript. Deployed via Render. Covers: Explorer Effect, Top 11 Brand Pairs, CRM Action Playbook, Persona Cards (Gen Z / Boomers), Suppression Layer, and the Winning Formula bake-off.

---

## Repository Structure

```
Sephora/
├── 00_admin/           # Project governance: rubric alignment, context documents
├── 01_docs/            # Feature engineering blueprint, methodology notes
├── 04_analysis/        # Full analysis pipeline (37 scripts + audit logs)
│   ├── 01_cleaning_script.py          # Data cleaning: 399,997 → 385,879 rows
│   ├── 03_feature_engineering_script.py  # 19 customer-level features
│   ├── 06_model_bakeoff.py            # 3-scenario ML bake-off
│   ├── 07_suppression_layer_analysis.py  # Do-Not-Recommend Layer
│   ├── step3_4_report.txt             # Core validated output (source of all metrics)
│   └── suppression_logic.txt          # Full suppression decision log
├── 05_outputs/         # Final scored recommendation outputs
├── 07_archive/         # Iteration history and deprecated scripts
├── 08_luxury_data_terminal/  # Interactive HTML/JS presentation source
├── claude-skills/      # AI governance: injected skill sets (UI/UX + Business Strategy)
├── picture/            # Persona photography assets
├── generate_speaker_notes.py  # Auto-generates speaker script from slide data
├── render.yaml         # Render deployment configuration
└── speaker.ipynb       # Speaker notes notebook
```

---

## Technical Stack

- **Data pipeline:** Python (pandas, numpy, mlxtend for association rules)
- **ML models:** Three-scenario bake-off — Margin-First, Balanced (winner: 3.27% lift), Discovery-First
- **Validation:** Time-split anti-leakage (Jan–Sep features / Oct–Dec holdout), 385,879-row dataset
- **Presentation:** HTML5, CSS3, JavaScript — deployed on Render
- **AI governance:** Four mandatory context documents + GitHub-sourced skill injections (UI/UX Pro + Business Strategy Consulting)

---

## Why This Project Stands Out

**1. Production-grade data integrity.**
Every number in the output is traceable to a named source file and line. Three AI-generated figures were identified as incorrect and corrected before any deliverable was produced.

**2. Business-first, not technique-first.**
The goal was never to maximize model accuracy. It was to identify the 11 brand pairs that a Sephora in-store team could act on Monday morning. The model serves the business decision, not the other way around.

**3. A working suppression layer.**
Building a Do-Not-Recommend system is harder than building a recommendation system. It requires domain judgment about brand positioning, LTV risk modeling, and commercial hierarchy — none of which come from the data alone.

**4. End-to-end delivery.**
This project goes from raw CSV to a live deployed web application. The same codebase powers the analysis, the speaker notes generator, and the interactive deck.

---

## Methodology in Brief

1. **Cleaning** — 399,997 raw rows → 892 duplicates removed → 385,879 eligible transactions
2. **Feature Engineering** — 19 customer-level behavioral features including Explorer Index, brand axis diversity, and recency-frequency-monetary signals
3. **Candidate Generation** — FP-Growth association rule mining on Jan–Sep training window (anti-leakage)
4. **Model Bake-off** — Three scenarios evaluated on Oct–Dec holdout; Balanced scenario wins at 3.27% composite score vs 3.10% (Margin-First) and 2.89% (Discovery-First)
5. **Guardrail Filtration** — 8,357 → 3,998 → 217 → 11 pairs through confidence, ML validation, and business guardrails
6. **Suppression Layer** — 6,995 VIPs protected, €491,476 LTV shielded, 53.6% bad recommendations eliminated
7. **Deployment** — Interactive 14-slide HTML deck deployed on Render; speaker notes auto-generated via Python

---

## About

Built by **Mugisha Samuel** — Data Science student at [Ecole des Mines / PSL](https://mines-paristech.fr), Paris.

This project was developed as Case 3 of the Albert School x Sephora France data competition, April 2026.

[![GitHub](https://img.shields.io/badge/GitHub-msamuel--glitch-181717?style=flat-square&logo=github)](https://github.com/msamuel-glitch)
