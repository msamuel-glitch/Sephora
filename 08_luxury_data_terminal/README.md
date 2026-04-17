# Sephora Luxury Data Terminal
### Live Interactive 14-Slide Findings Deck

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20Deck-black?style=for-the-badge)](https://sephora-luxury-terminal.onrender.com)

This folder contains the full source code for the interactive presentation built to communicate the Brand Affinity Detection findings to Sephora France and Albert School evaluators.

## Live Deployment

**[sephora-luxury-terminal.onrender.com](https://sephora-luxury-terminal.onrender.com)**

The deck is deployed as a public web application. No login required. Navigate using the slide number buttons at the bottom of the screen.

## What the Deck Covers

| Slide | Title | Key Content |
|---|---|---|
| 01 | The Hook | +EUR 11.49 per customer business case |
| 02 | The Winning Formula | 3-scenario bake-off, Balanced scenario wins at 3.27% |
| 03 | Dataset Command | 385,879 transactions, anti-leakage architecture |
| 04 | The Explorer Effect | Explorer Index, loyalty vs. value paradox |
| 05 | Top 11 Pairs | 8,357 rules filtered to 11 guardrail-clean pairs |
| 06 | The Action Playbook | In-store, CRM, and app deployment channels |
| 07 | The Proof Engine | Three-stage filtration methodology |
| 08 | 894 Behavioral Rules | Profile-level transition rules by segment |
| 09 | Gen Z Persona | Explorer Index 0.73, EUR 208 total spend |
| 10 | Boomer Persona | EUR 46.11 avg basket, 3,176 single-visit reactivations |
| 11 | Cost of Being Wrong | Do-Not-Recommend Layer, EUR 491,476 LTV protected |
| 12 | Acquisition Strategy | Deploy 217 pairs, automate Sephora Collection rebounds |
| 13 | Protection Strategy | VIP lock-down, A/B test framework |
| 14 | Final Verdict | +EUR 11.49 delivered, 659 sales validated, 80M scale |

## Technical Stack

- **Framework:** React + Vite
- **Styling:** CSS3 with Sephora-coded luxury editorial design
- **Navigation:** Custom slide dot navigator with keyboard support
- **Deployment:** Render (continuous deployment from main branch)
- **Design system:** UI/UX Professional skill (GitHub-sourced) applied throughout

## Design Principles

Every slide follows three rules:
1. Lead with a business decision, not a data point
2. One insight, one action, one Monday Morning directive
3. Numbers only appear if traceable to a source file in `04_analysis/`
