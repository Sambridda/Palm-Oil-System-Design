# Palm Oil Melting & Retention System

**Industrial thermal systems design and automation architecture for a multi-tank palm oil melting, storage, and trim-heating facility — Mechatronics Engineering Pvt. Ltd. (MEPL), Kathmandu.**

Grounded in the self-authored **VCH Sizing Framework (2nd Ed.)**, the system coordinates a passive solar thermal loop with an auxiliary electric immersion array through PLC automation to deliver demand-driven, high-efficiency process operations.

> **Document History**
> | Version | Date | Status |
> | :--- | :--- | :--- |
> | Technical Proposal I | Prior to June 2026 | Archived — superseded |
> | Technical Proposal II | June 29, 2026 | Archived — superseded |
> | Technical Proposal III (Architectural Revision I) | July 10, 2026 | Current — For Review |

---

## Table of Contents

1. [Industrial Mandate & Constraints](#1-industrial-mandate--constraints)
2. [Engineering Journey & Design Challenges](#2-engineering-journey--design-challenges)
3. [System Architecture](#3-system-architecture)
4. [Core Technical Deep Dives](#4-core-technical-deep-dives)
5. [The VCH Sizing Framework](#5-the-vch-sizing-framework)
6. [Headline Results & Validation Metrics](#6-headline-results--validation-metrics)
7. [Future Plan](#7-future-plan)
8. [My Contributions](#8-my-contributions)
9. [Changelog: Proposal I → Proposal II](#9-changelog-proposal-i--proposal-ii)
10. [Changelog: Proposal II → Proposal III (Architectural Revision I)](#10-changelog-proposal-ii--proposal-iii-architectural-revision-i)
11. [Appendix: Engineering Notebook](#appendix-engineering-notebook)

---

## 1. Industrial Mandate & Constraints

The objective was to design, size, and architect the automation logic for a raw palm oil processing infrastructure under strict operational and environmental parameters.

| Parameter | Specification |
| :--- | :--- |
| **Production Throughput** | ≥ 2 tonnes of fully processed liquid palm oil per day |
| **Thermal Transition** | Solid-state feedstock at 18.1°C (Kathmandu annual ambient) → 60°C stable liquid process target |
| **Hardware Scope** | Three 10 kL storage/melting vessels (one now dedicated to palm olein storage), one 5 kL trim-heating replenishment tank, passive solar thermal loop, 36 kW auxiliary electric immersion array |
| **Climate Factor** | Kathmandu solar reliability: **75.9% annually** |

---

## 2. Engineering Journey & Design Challenges

### Scope Misalignment: Production Window Clarification

The project initially proceeded under the assumption that the target throughput was 2 tonnes processed within a 4-hour window — a significantly more demanding brief than what was ultimately intended. At that stage, the VCH methodology had not yet been extended to account for latent heat during phase change, which caused the computed overall heat transfer coefficient ($U$) to appear unrealistically poor. The apparent shortfall prompted repeated proposals to introduce mechanical agitation (an impeller) to compensate, which the senior engineer consistently declined on practical and cost grounds.

The misalignment was resolved through structured clarification: revisiting the original brief with targeted questions until the envisioned system — a daily throughput target, not a 4-hour batch — was confirmed unambiguously. This reframing immediately brought the thermal performance figures within acceptable bounds and removed the need for agitation entirely.

**Takeaway:** Requirement ambiguity compounds downstream. Early, explicit clarification of the production window prevented a fundamentally over-specified design from proceeding to detailed engineering.

---

### Solar Loop Integration: Single-Pump Architecture

The standard two-loop passive solar integration approach — where the solar circuit operates independently and dumps heat into the primary loop only when capacity permits — would have required a dedicated secondary circulation pump. To reduce capital cost and system complexity, the loop topology was redesigned so that a single high-pressure pump handles full circulation duties across both the solar collectors and the primary process loop.

The trade-off is a heavier-duty pump selection and a significantly higher system head loss, both of which are documented and will be finalised once site plumbing and pipe routing are confirmed. The architectural logic underpinning this single-pump design is reflected in the Process Flow Diagram.

---

### Pipe & Coil Sizing: The A.A / A.B / B.A / B.B Case Matrix

Cost pressure from the senior engineer introduced a preference for 1-inch NPS pipe at a stage when all sizing calculations had been developed around 1.5-inch. Reworking the analysis while the production throughput question was still unresolved made a definitive single-configuration recommendation premature. Rather than selecting arbitrarily, all four permutations of supply pipe NPS and coil bore NPS were calculated in full:

| Case | Supply Pipe | Coil Bore |
| :---: | :---: | :---: |
| **A.A** | 1" NPS | 1" NPS |
| **A.B** | 1" NPS | 1.5" NPS |
| **B.A** | 1.5" NPS | 1" NPS |
| **B.B** | 1.5" NPS | 1.5" NPS |

Publishing all four cases in the proposal preserves full transparency for the client and allows the final pipe selection to be made on cost and availability grounds without requiring a redesign.

> **Proposal II update:** The four-case supply/coil matrix has been resolved into a **single standardised supply pipe** (1-inch Schedule 40 CPVC throughout the loop), eliminating the supply pipe as an independent variable. The coil bore remains a design variable and is now evaluated across 1-inch, 1.25-inch, 1.5-inch, and 2-inch NPS in SS 304 Schedule 10S.
>
> **Proposal III update:** The coil bore variable is itself resolved into a **single standardised 2-inch bore across every tank** (T10, PO, and T5 alike), trading a small amount of thermal margin for a single procurement spec across the whole plant. See [Section 10](#10-changelog-proposal-ii--proposal-iii-architectural-revision-i) for detail.

---

### Challenging the Water-Side Velocity Assumption

The initial hypothesis was that increasing water-side velocity through the submerged hydronic coils would be the primary lever for accelerating the melting phase. Applying the first-principles equations of the VCH Sizing Framework forced a critical course correction.

**The impedance bottleneck.** Modelling the two-phase overall heat transfer coefficient ($U$) revealed that the outer oil-side thermal resistance accounts for over **95%** of total system impedance. Increasing water velocity through a 1-inch bore coil (Case A.B) produced a very high inner-surface coefficient ($h_i = 19{,}594\ \text{W/m}^2\text{K}$), yet yielded a negligible change in the overall melting rate — while adding hydraulic pump stress and accelerated wear for a mathematically redundant gain.

### Shifting to Algorithmic Design

Once the solid-phase oil-side resistance was confirmed as an unyielding physical bottleneck, the design philosophy shifted from mechanical brute force to **algorithmic throughput recovery**. If a single tank's melting phase cannot be safely accelerated beyond its thermodynamic limit, total plant throughput must be reclaimed by orchestrating a smarter, time-staggered multi-tank queue.

This led directly to the demand-driven "pull" automation architecture. Real-time volume- and temperature-weighted priority matrices ($S_\text{casual}$ and $S_\text{immediate}$) allow the PLC to continuously prepare, melt, and hold oil across all three 10 kL vessels in an overlapping sequence — bypassing single-tank cycle limitations and securing an uninterrupted downstream process stream.

---

### From a Shared Bunch to a Dedicated Palm Olein Tank (New in Proposal III)

Once the demand-driven multi-tank queue was validated, a new operational requirement emerged: one of the three T10 vessels needed to be carved out as dedicated palm olein storage rather than continuing to melt palm oil. Palm olein solidifies at a much lower temperature (≈24°C, versus palm oil's 36°C) and, once liquid, needs comparatively little energy to stay that way — so simply leaving it in the shared rotation would have distorted the tank-scoring system's assumptions, which were derived entirely around palm oil's higher-energy melt behaviour.

The fix required restructuring at the piping level, not just the control level: the original **shared water header** across the three T10 tanks was replaced with an **individualised feed per tank**, gated by a manual ball valve in series with an automated control valve. This is what makes it possible to designate one tank as a dedicated, isolated PO (palm olein) store — automatically excluded from the melting rotation, manually hard-isolated as a physical safeguard, and dispensed only via operator-triggered HMI pulses — without touching the piping or control logic of the other two tanks.

This single change cascaded into a full re-architecture of the plant's priority logic (see below) and its fault-detection philosophy (Section 4).

---

### A Three-Way Priority Ladder, Not a Fixed Split (New in Proposal III)

Introducing the PO tank meant the old two-tier logic (T5 master, T10 demand-pull) needed a third rung: **P1 — T5 trim-heating**, **P2 — PO tank temperature maintenance**, and **P3 — T10 palm oil melting**. The obvious approach — a strict P1 ≫ P2 ≫ P3 lockout — was rejected: it would mean P3 simply waits, indefinitely if necessary, whenever P1 or P2 has any demand at all, even though palm oil melting tolerates interruption far better than a live PO-tank dispense or T5's process-critical trim-heating.

Instead, arbitration was resolved as a **sequential daily energy budget**: P1's and P2's actual required duty periods are computed first, and P3 — by design the process that absorbs all of the system's slack — receives whatever remains of the 24-hour window. P2 itself is bounded within a 10-minute arbitration window (sized off T5's own worst-case heat-up time) and flat-capped at 5 of every 10 minutes, so it cannot starve P3 indefinitely even on a heavy dispense day.

**Takeaway:** Adding a third demand source didn't call for a more complex real-time scheduler — it called for recognising which processes can tolerate deferral and encoding that directly into a daily budget rather than a live priority fight.

---

### Ambient Data: Weighted-Average Design Philosophy

Kathmandu's solar irradiance and ambient temperature data are not available from a single authoritative instrument record for this site. Rather than anchoring the design on a single "average good day" figure — which would leave the system undersized for adverse conditions — weighted annual averages were compiled across multiple sources and applied consistently throughout the sizing work. This methodology appears across solar reliability factors, ambient baseline temperature (18.1°C), and the tank priority scoring matrices ($S_\text{casual}$, $S_\text{immediate}$).

The limitation is acknowledged: weighted averages characterise typical behaviour, not extremes. The worst-case 70°C HTF scenario in the validation table is the explicit hedge against adverse conditions.

---

### Tank Geometry & Manufacturability

Initial vessel proportioning followed the aspect ratio guidance in the VCH Sizing Framework. Translating those proportions into manufacturable steel vessels — balancing height, diameter, conical cap geometry, plate utilisation, and weld seam minimisation — proved more iterative than the thermal calculations themselves. Once the senior engineer introduced a manufacturability constraint tied to standard plate dimensions, the detailed vessel geometry was handed to the team's mechanical engineer, who modelled the tanks in SolidWorks and confirmed material utilisation and weldability before the dimensions were locked.

---

## 3. System Architecture

> *Process Flow Diagram (PFD) is available in the repository. Detailed architectural data to be added.*

As of Proposal III, the plant is organised around **individualised feeds** to each of the three T10 tanks (rather than a shared header), with one T10 tank optionally designated by site technicians as the **PO tank** — automatically and manually isolated from the common palm-oil bunch and dispensed only via HMI-driven pulse logic. Water time across the plant is arbitrated by the **P1 (T5) → P2 (PO tank) → P3 (palm oil melt)** priority ladder described in Section 2.

---

## 4. Core Technical Deep Dives

### Multi-Phase Thermal Modeling

External natural convection profiles for the uninsulated vessels were constructed using rigorous engineering correlations:

- **Vertical tank walls** — Churchill-Chu correlation
- **Horizontal surfaces** — Morgan-McAdams plate equations
- **Internal coil fluid dynamics** — Gnielinski correlation with Kubair-Kuloor enhancements for helical geometries

This approach isolated a **1.07 kW** hold-phase thermal loss profile.

### Dynamic Upper Thermal Boundary ($T_f$)

Rather than a static high-limit cutoff — which risks thermal degradation and pressure transients — the PLC dynamically computes the real-time thermodynamic equilibrium boundary from the instantaneous mass interaction of water, steel, and palm oil:

$$T_{f}(x,\, y,\, m_p) = \frac{239.53\, x + m_p\, y}{239.53 + m_p}$$

| Symbol | Definition |
| :---: | :--- |
| $x$ | Instantaneous temperature of the thermal buffer tank |
| $y$ | Instantaneous temperature of the target melting tank |
| $m_p$ | Estimated remaining mass of solid/liquid oil phase |

This algorithm protects high-pressure line components and prevents product degradation without operator intervention. It is retained unchanged in Proposal III, governing T5's safety cutoff logic.

### Volume- and Temperature-Weighted Tank Scoring

Two independent PLC calculation blocks evaluate plant state and drive the staggered delivery queue:

- **$S_\text{casual}$ Block** — Manages solar thermal energy distribution to tanks requiring non-urgent pre-heating.
- **$S_\text{immediate}$ Block** — Prioritises auxiliary electric backup (36 kW) to the active processing tank when a downstream demand signal ($\delta$) is high, preventing line starvation.

Retained unchanged in Proposal III, now applied only across the two T10 tanks not designated as the PO tank.

### Coil Sizing: Inverted Design Logic

Proposal I fixed the coil at its geometric ceiling (90 m for T10) and asked what throughput results. Proposal II inverted this: a heat-duty target $Q_\text{target} = Q_\text{batch} + Q_\text{loss,max} = 9.17\ \text{kW}$ is defined from the mandate and worst-case standing loss, and the **minimum coil length required** is solved in closed form via the ε-NTU method.

Proposal III fixes the coil bore and length outright (2-inch bore, 30 m for T10/PO tanks, 10 m for T5) as a standardised, single-spec design across the whole plant — see Section 10 for why this costs almost nothing in thermal performance.

### Batch-Side Modelling Correction: $C_\text{min} = C_w$ (New in Proposal III)

Proposal I's T5 analysis treated oil throughput as $C_\text{min}$, appropriate for continuous flow-through duty. Under the individualised-feed architecture, each tank is instead heated as a **well-mixed batch** whose bulk temperature changes slowly relative to a single pass of water through the coil — so the water side is $C_\text{min}$ ($C_w$) and the tank contents behave as $C_\text{max} \to \infty$ over one coil pass. Using the old throughput-rate model here would have predicted effectiveness in excess of 98% and near-instant temperature overshoot — physically inconsistent with a duty-cycled batch process. All NTU calculations from Proposal III onward use:

$$NTU = \frac{UA}{C_w}, \quad \varepsilon = 1 - e^{-NTU}, \quad Q(T_\text{tank}) = \varepsilon\, C_w\, (T_\text{hot} - T_\text{tank})$$

### Fault Detection: A Physics-Based Alarm Philosophy (New in Proposal III)

An earlier iteration considered alarming whenever P1's duty cycle, measured over a short rolling window, exceeded twice its statistically expected value. This was rejected because P1's real-world demand is inherently bursty — legitimate operation naturally produces some windows with heavy, clustered activity and others with none, so a duty-percentage threshold can't distinguish a busy stretch of the day from an actual fault.

The revised philosophy alarms on **physics, not bookkeeping**: the PLC compares T5's observed heating and cooling rates against the maximum physically achievable rates given the coil's known heat-delivery capacity and the tank's own computed loss rate. Heating faster than the coil could physically produce, or cooling faster than the tank's own standing loss rate can account for, both indicate a sensor, valve, or leak fault — independent of how busy the day has been.

---

## 5. The VCH Sizing Framework

This system is a full-scale industrial deployment of the **VCH Sizing Framework (2nd Edition)** — a methodology authored specifically for submerged hydronic coil thermal systems. The project served as a definitive verification platform, confirming that unifying coil heat transfer modeling with multi-phase thermal boundary calculations produces highly predictable, field-resilient industrial designs.

**DOI:** [10.5281/zenodo.21009246](https://doi.org/10.5281/zenodo.21009246)

---

## 6. Headline Results & Validation Metrics

### Proposal III Results (Current — Architectural Revision I)

Evaluated under a constant 70°C water supply, 1.2 m/s feed velocity cap, and standardised 2-inch coil bore throughout (30 m for T10/PO tanks, 10 m for T5), with sequential (single-branch) water-time arbitration across P1/P2/P3:

| Performance Metric | Result |
| :--- | :---: |
| **T5 (P1) daily duty period** | 2.05 hr (8.5%) |
| **PO tank (P2) daily duty period** | 0.59 hr (2.4%) |
| **Palm oil melting (P3) daily window** | 21.37 hr (89.0%) |
| **Palm oil melted per day (P3)** | ≈ 2,447 kg (2.45 t/day) |
| **Fulfilment vs. 2 t/day mandate** | ≈ 122% |
| **Total daily thermal energy demand** | 568.3 MJ |
| **Average continuous power demand** | 6.58 kW |
| **Solar (ETC) contribution to demand** | ≈ 40% |
| **Auxiliary (36 kW) headroom vs. average demand** | > 5× |

**Key findings:**
- The system is **not heat-limited** — P1 and P2 together consume only 10.9% of the day's coil availability. The true constraint on P3's throughput is the ≈77.8 hr melt time of a full 10 kL tank, not available thermal power.
- The PO tank's own standing heat loss, not its sensible duty, dominates its energy budget (roughly 7:1) because it remains uninsulated — identified as the single highest-leverage efficiency gain in this revision.
- The mandate is still comfortably exceeded (≈122% fulfilment) even after diverting a full tank's worth of capacity to palm olein and giving P1/P2 priority ahead of P3.

### Archived: Proposal II Results

| Performance Metric | Design Target | Primary (75°C HTF) | Worst-Case (70°C HTF) |
| :--- | :---: | :---: | :---: |
| **Safety margin vs. 2 t/day (single tank)** | 1.0× | **3.0×** (at design point) | **3.0×** (by construction) |
| **3-tank staggered capacity** | ≥ 2.0 t/day | **6.0 t/day** | **6.0 t/day** |
| **Required coil length (1.5" bore)** | ≤ 90 m | **48.3 m** | **55.6 m** |
| **Solar Loop Thermal Coverage (ETC)** | Maximise | **61.46%** offset | Emergency electric override |
| **System Thermal Bottleneck** | Mitigate | Oil-side impedance (>95%) | Oil-side impedance (>95%) |
| **T5 coil length required (1.5" bore)** | — | **3.2 m** of 65 m ceiling | **4.1 m** of 65 m ceiling |

> Note: Proposal III's headline figures are not directly comparable to Proposal II's on a like-for-like basis — Proposal III introduces a fixed 2-inch bore across all tanks, a dedicated PO tank (removing one T10 tank from the palm-oil rotation), sequential rather than purely throughput-optimised water-time allocation, and reports against the single-branch case only (see Section 10 of the Architectural Revision I document for the simultaneous-branch outlook).

### Archived: Proposal I Results

| Performance Metric | Design Target | Primary (75°C HTF) | Worst-Case (70°C HTF) |
| :--- | :---: | :---: | :---: |
| **Daily Plant Throughput** | ≥ 2.0 t/day | **24.23 t/day** (staggered) | **20.48 t/day** (staggered) |
| **Single-Tank Safety Factor** | 1.0× | **3.63×** | **2.42×** |
| **Solar Loop Thermal Coverage** | Maximise | **61.46%** offset (ETC) | Emergency electric override |
| **System Thermal Bottleneck** | Mitigate | Oil-side impedance (>95%) | Oil-side impedance (>95%) |

---

## 7. Future Plan

With the revised (Proposal III) architecture in place, the next phases are:

**Simultaneous-Branch Operation (Architectural Outlook, Not Yet Calculated)**
- All Proposal III analysis assumes sequential, single-branch water use. The coil sizing itself (2-inch bore throughout, with margins well above what P1 and P2 actually require) suggests the trunk main — not the branch coils — is the limiting element for a future upgrade.
- A future revision could upsize the trunk main to allow P1/P2/P3 branches to draw simultaneously (P3 becoming a permanently-valved bypass branch rather than one gated behind P1/P2 completion), shortening P3's effective wait per P1 event and pushing throughput closer to the coil-delivery ceiling rather than the arbitration-window ceiling. No flow-split or trunk-sizing math has been carried out for this yet.

**PO Tank Insulation**
- Insulating the PO tank to T5's standard is the identified highest-leverage, lowest-capital-cost efficiency gain — its uninsulated loss currently outweighs its sensible heating duty roughly 7:1, and every megajoule saved there returns directly to P3's melting window.

**Electrical Design**
- Detailed electrical system design in AutoCAD, covering power distribution, protection coordination, and wiring layout strategies for the immersion array and pump drives.

**Controls Architecture**
- Discussion with the senior engineer to finalise the control philosophy — evaluating a PLC-based architecture against distributed individual controllers, and assessing the feasibility of PI control loops in place of hard on/off automation for improved stability and reduced thermal cycling.

**Instrumentation & HMI**
- Full sensor schedule: selection, specification, and placement of temperature, level, and flow instruments across all four tanks and the solar loop.
- HMI design for operator visibility, PO-tank designation/dispense workflow, and manual override capability.

**Hydraulics & Pump Selection**
- Head loss calculations for the coil circuits and the single-pump solar/primary loop. Hand calculations have been initiated; finalisation is deferred until site plumbing routing and the pipe NPS selection are confirmed.
- Pump selection based on the locked head loss and flow rate requirements.

---

## 8. My Contributions

This project was undertaken as a Junior Automation Design Architect during an internship at MEPL, working under the direction of the senior project lead. The scope of personal contributions is as follows:

**Thermal Sizing & Proposal Authorship**
All thermal calculations, coil sizing, case matrix analysis (A.A / A.B / B.A / B.B in Proposal I; unified 1-inch supply with 1–2 inch coil bore sweep in Proposal II; fixed 2-inch bore, individualised-feed, and three-way priority architecture in Proposal III), phase-change modelling, solar reliability analysis, and the full engineering proposal documents were produced independently, grounded in the self-authored VCH Sizing Framework (2nd Ed.).

**Process Architecture**
The single-pump solar feedback loop topology, the individualised T10 feed restructuring, the PO tank isolation logic, and the P1/P2/P3 sequential-budget priority ladder were independently conceived and designed. This architecture has not yet been formally reviewed with the senior engineer and is pending discussion.

**Tank Geometry (Collaborative)**
Initial vessel proportions and aspect ratio estimates were produced as part of the thermal sizing work. Detailed manufacturable geometry and SolidWorks verification were completed by the team's mechanical engineer, who refined the dimensions to minimise plate waste and weld seam count.

**PFD vs. P&ID**
The Process Flow Diagram was produced as part of this proposal. The team's mechanical engineer has produced a separate P&ID; the two documents are currently not fully aligned and reconciliation is in progress.

**Note:** The project is ongoing. The contributions documented here reflect the proposal stage. Electrical design, instrumentation, and controls work are planned for subsequent phases.

---

## 9. Changelog: Proposal I → Proposal II

This section documents the technical changes between the first two proposal revisions for traceability.

### 9.1 Supply Pipe Simplification

**Proposal I** evaluated two supply pipe sizes (1-inch and 1.5-inch NPS) as an independent design variable, producing a 2×2 case matrix (A.A, A.B, B.A, B.B) for the combination of supply bore and coil bore.

**Proposal II** standardises on a **single 1-inch Schedule 40 CPVC supply pipe** throughout the entire loop. This eliminates the supply pipe as a design variable without any material effect on U-value or NTU performance — the oil-side resistance dominates at >95% of total impedance regardless of supply pipe selection. The case matrix collapses from four supply/coil combinations to a single-axis coil bore sweep (1", 1.25", 1.5", 2").

### 9.2 Coil Sizing Methodology: Inverted Design Logic

**Proposal I** fixed the coil at its maximum geometric length ($L_\text{max} = 90\ \text{m}$ for T10) and solved for the resulting throughput capacity.

**Proposal II** inverts this: the minimum coil length required to meet a defined heat-duty target is solved in closed form. The target is:

$$Q_\text{target} = Q_\text{batch} + Q_\text{loss,max} = 4.30 + 4.87 = 9.17\ \text{kW}$$

where $Q_\text{batch}$ is the average power needed to melt 2 t of palm oil over 24 hours, and $Q_\text{loss,max}$ is the conservative worst-case standing loss at the 75°C PLC high-limit. Using the ε-NTU closed-form inversion for a Cr = 0 heat exchanger, the required lengths are:

| Coil bore | $L_\text{required}$ at 75°C drive | $L_\text{required}$ at 70°C drive | % of 90 m ceiling (worst case) |
| :---: | :---: | :---: | :---: |
| 1-inch | 69.4 m | 80.1 m | 89% |
| 1.25-inch | 55.1 m | 63.6 m | 71% |
| **1.5-inch** | **48.3 m** | **55.6 m** | **62%** |
| 2-inch | 38.8 m | 44.7 m | 50% |

**Recommended design point:** 1.5-inch coil at L ≈ 56 m — a 38% reduction from the original 90 m specification.

### 9.3 Melt Time and Safety Factor Basis

**Proposal I** reported single-tank safety factors of 3.63× (primary) and 2.42× (worst case) derived from the ratio of actual coil output (at 90 m) to the 2 t/day minimum requirement.

**Proposal II** sizes to exactly the daily mandate floor (24-hour melt time for 2 t at $Q_\text{batch}$), so the single-tank margin against the mandate is 1.0× by construction at the coil design point. The 3× system-level margin is recovered from running all three T10 tanks in a staggered sequence (3 × 2 t = 6 t/day). Actual single-tank performance will exceed the design floor whenever the tank is below its 75°C high-limit — which is most of the melt cycle.

### 9.4 T5 Coil Sizing (Quantified)

**Proposal I** identified T5 as thermally over-specified and noted that a duty-cycle loop or mixing valve would be required, but did not quantify the degree of over-specification.

**Proposal II** quantifies it explicitly: even the smallest bore (1-inch) requires only **≈ 5.8 m** of coil (against a 65 m geometric ceiling — under 9% utilisation) to guarantee the 60°C process target. The recommended 1.5-inch bore requires only 4.1 m at the 70°C worst-case drive. This confirms that T5 is not capacity-limiting under any evaluated scenario.

---

## 10. Changelog: Proposal II → Proposal III (Architectural Revision I)

This section documents the technical changes introduced by the current revision.

### 10.1 Shared Header → Individualised Feeds

**Proposal II** retained a shared water header across the three T10 tanks, with tank selection handled entirely by the PLC's scoring logic.

**Proposal III** replaces the shared header with an **individualised feed per tank** — each T10 vessel is gated by its own manual ball valve in series with its own automated control valve. This is the structural prerequisite for designating one tank as a dedicated palm olein store without disturbing the piping or control logic of the other two.

### 10.2 New Tank Class: The PO (Palm Olein) Tank

One T10 tank may now be designated, via HMI input, as a dedicated palm olein store. Once designated, it is automatically excluded from the P3 melting rotation and the legacy tank-scoring system, manually hard-isolated via its ball valve as a PLC-independent safeguard, and dispensed only through operator-triggered HMI pulse logic (compute dispense time → run dispense valve → enter a 20 s-on/60 s pulse-hold to keep residual oil warm → clear on operator "process complete").

### 10.3 Two-Tier → Three-Tier Priority Architecture

**Proposal II's** priority logic was effectively single-tier (T5 master, T10 demand-pull).

**Proposal III** introduces a three-way ladder — **P1 (T5 trim-heat)**, **P2 (PO tank maintenance)**, **P3 (T10 palm oil melt)** — resolved not by hard lockout but by a **sequential daily energy budget**: P1 and P2 take what their computed duty periods require, and P3 receives the remainder of the 24-hour window by design. P2 is additionally bounded by a 10-minute arbitration window (sized at 3× T5's worst-case heat-up time) with a flat 5-minute cap, so it cannot starve P3 indefinitely.

### 10.4 Coil Bore and Length: From Swept Variable to Fixed Spec

**Proposal II** swept coil bore across 1", 1.25", 1.5", and 2" NPS to find a minimum-length design point (1.5" recommended, ≈56 m).

**Proposal III** fixes the bore at **2-inch NPS Sch. 10S across every tank** (T10, PO, and T5), with coil length fixed at **30 m** (T10/PO) and **10 m** (T5), and water supply fixed at a constant 70°C (previously 70–75°C, variable) with feed velocity reduced to 1.2 m/s (from 1.5 m/s). Because the oil-side film continues to dominate 1/U for the melting duty, standardising the bore for procurement simplicity costs almost nothing in thermal performance.

### 10.5 NTU Model Correction: $C_\text{min} = C_w$, Not the Oil Throughput Rate

**Proposal I's** T5 analysis modelled oil throughput as $C_\text{min}$, appropriate for continuous flow-through duty.

**Proposal III** corrects this for the individualised-feed, batch-heated architecture: each tank is a well-mixed batch whose bulk temperature changes slowly relative to one coil pass, so **water is $C_\text{min}$** and tank contents behave as $C_\text{max} \to \infty$. The old model would have predicted >98% effectiveness and near-instant overshoot — physically inconsistent with batch heating.

### 10.6 Fault Detection: From Duty-Cycle Thresholds to Physics-Based Alarms

An interim design considered alarming when P1's duty cycle exceeded twice its statistically expected value over a rolling window — rejected because P1's demand is legitimately bursty, making a duty-percentage threshold unable to distinguish a busy day from a fault.

**Proposal III** instead alarms on **observed heating/cooling rates versus what is physically achievable** given the coil's known delivery capacity and the tank's own computed loss rate — decoupling fault detection from duty-cycle bookkeeping entirely.

### 10.7 Headline Result Basis Change

Proposal III's throughput and safety-margin figures are reported against the **single-branch, sequential water-use case only** (P1, P2, P3 never draw simultaneously). A simultaneous-branch upgrade is outlined qualitatively as a future direction (Section 7) but is explicitly out of scope for the quantitative results in this revision.

---

## Appendix: Engineering Notebook

High-resolution scans of scratchpad derivations, geometric helical coil layout constraints, and early PLC state-machine routing matrices are located in the `engineering_notes/` directory.
