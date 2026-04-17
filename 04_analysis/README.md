# Analysis Pipeline

This folder contains the complete end-to-end analysis pipeline for the Sephora Brand Affinity Detection project.

## Pipeline Overview

The pipeline runs in sequential stages. Each script is numbered to reflect execution order.

| Script | Purpose |
|---|---|
| `01_cleaning_script.py` | Removes 892 duplicates from 399,997 raw rows, validates schema, produces 385,879 clean transactions |
| `03_feature_engineering_script.py` | Builds 19 customer-level behavioral features including the Explorer Index |
| `05_generate_final_outputs.py` | Produces scored recommendation outputs for all 50,805 customers |
| `06_model_bakeoff.py` | Runs three-scenario ML bake-off (Margin-First / Balanced / Discovery-First) |
| `07_suppression_layer_analysis.py` | Builds the Do-Not-Recommend Layer; protects 6,995 VIPs and 491,476 EUR LTV |
| `step3_4_hf_profiling_scoring.py` | Scores customers against brand affinity profiles; generates 894 behavioral rules |
| `analysis_c_verification.py` | Independent verification pass on Analysis C outputs |
| `populate_guardrails.py` | Populates commercial guardrail rules from brand constraint document |

## Key Output Files

| File | What It Contains |
|---|---|
| `step3_4_report.txt` | **Primary validated output.** Source of all metrics used in the final presentation. |
| `suppression_logic.txt` | Full suppression decision log with brand-level rationale |
| `06_model_bakeoff_results.txt` | Model bake-off scores: Balanced wins at 3.27% vs 3.10% and 2.89% |
| `feature_engineering_log.txt` | Full audit log of all 19 features computed per customer |
| `leakage_audit.txt` | Anti-leakage verification: confirms time-split was applied correctly |
| `validation_report.txt` | End-to-end validation report confirming all metrics are traceable |

## Data Integrity Policy

Every number used in the final deliverable is traceable to a specific file and line in this folder. Three figures were identified as incorrect during development and corrected before inclusion:

- Explorer Index: AI-generated value of 0.671 corrected to 0.578 per `feature_engineering_log.txt`
- Suppression coverage: 94.82% removed as base-rate artifact per `suppression_diagnostic.py`
- AVNE to BIODERMA lift of 65.4x excluded as unverifiable

## Anti-Leakage Architecture

All feature computation uses **January to September** transaction data only. Model validation runs on **October to December** holdout data. This prevents any information from the evaluation period leaking into the training features.
