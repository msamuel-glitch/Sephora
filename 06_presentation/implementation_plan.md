# Sephora Case 3: Advanced Strategic Pitch Application

## Critique & Course Correction

You are entirely correct to call out the short-sightedness. Looking at the failed `sephora-dashboard-failed` attempt, all it did was lazily port static HTML into React components. That doesn't add value; it's just a tech change. 

To achieve a true **McKinsey-grade strategic asset**, we cannot just build a static scrolling website. We must build a **data-driven interactive application**. It needs to natively integrate the mandates from `08_business_rules_update.md`, specifically the focus on **Generational Arbitration**, **High-Frequency Profiling**, and the **Activation Hierarchy**, while leveraging advanced UI visualization to communicate complexity intuitively.

---

## User Review Required

> [!WARNING]
> Please review the expanded technical scope below. I am proposing the inclusion of **D3.js / React-Three-Fiber** for interactive data mapping and a real-time parsing engine for your CSV outputs. 

## Proposed Changes: Unlocking the Real UI/UX

### 1. Technology Infrastructure (The Engine Room)
#### [NEW] Vite + React + Advanced Visualization Stack
- **Framework:** Vite + React + TypeScript.
- **Styling & Motion:** Tailwind CSS, Shadcn UI, and GSAP + ScrollTrigger for the core narrative spine (using the cinematic styling you admire).
- **Advanced Visualization:** We will integrate **D3.js** (or a React wrapper like Recharts/Nivo) and **React-Three-Fiber (WebGL)** to build the Brand Affinity Network, ensuring the visual experience blows away standard bar charts.
- **Data Layer:** Instead of hardcoded strings, we will use `papaparse` to dynamically load `top10_store_brand_pairs_presentable.csv` and `store_brand_pairing_guide.csv` directly into the app state.

### 2. Narrative Arc & Interactive Components
We will structure the application around the exact business rules you defined:

#### A. The Hero / Business ROI (Rule 6: Anti-Triviality)
- **Data:** The $583K incremental basket opportunity upfront, backed by volume parameters.
- **UI:** A cinematic, WebGL-enhanced or heavily GSAP-animated entry sequence.

#### B. The Machine & Cold-Start Logic (Rule 7)
- **Data:** The bake-off (LightGBM vs. Ensemble).
- **UI:** Interactive "Tech vs. Business" toggle. Users can see how LightGBM wins on raw P@3 (5.26%), but why the Ensemble is required for the Cold-Start new brands.

#### C. The Brand Affinity Network (Rule 5 & Market Types)
- **Data:** `top10_store_brand_pairs_presentable.csv`
- **UI:** A **3D or Physics-based D3 Force Graph**. Brands are nodes. Sephora Collection, Exclusive, and Selective markets are color-coded (Brand-Family Arbitration). When a user hovers over the connection (e.g., KIEHLS -> LANCOME), the line glows, and the specific "Pairing Story" tooltip is revealed, alongside the 2.15x lift.

#### D. Generational & High-Frequency Profiling (Rules 1 & 4)
- **UI:** An **Interactive Control Panel**. The jury can interact with sliders/toggles to filter the cohort. 
- **Action:** Toggle between "High-Frequency" and "Base" to see the Explorer Index shift dynamically. Switch between "Gen Z" and "Baby Boomer" to see how the Haircare recommendation gets suppressed (Rule 14 from the safeguard). 

#### E. The Activation Pipeline (Rule 3)
- **Data:** CRM, App Feed, and In-Store.
- **UI:** A cascading visual pipeline showing exactly *how* a data point flows from the model score into a concrete CRM output.

## Open Questions

> [!IMPORTANT]
> 1. **Data Source Integration:** Should I build a local data fetcher that reads your `.csv` files inside the `05_outputs` folder upon loading, or do you have a specific Stitch API instance or cloud database you want me to hook up to?
> 2. **3D UI Capabilities:** Are you comfortable with me utilizing `react-three-fiber` or `d3-force` to handle the Brand Affinity pairs dynamically? This is exponentially more impressive than a static table but requires careful data shaping.
> 3. **Design Tokens:** Moving forward with the cinematic black/silver/red aesthetic, unless directed otherwise.

## Verification Plan
1. **Interactive Demo:** Deploy a local dev server that allows you to click through the Data Graph and filter by Generation.
2. **Data Parity Check:** Ensure the numbers displayed in the Generational chart matches the business rules perfectly.
