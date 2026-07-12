# Palm Oil Melting & Retention System

**Industrial thermal systems design and automation architecture for a multi-tank palm oil melting, storage, and trim-heating facility — Mechatronics Engineering Pvt. Ltd. (MEPL), Kathmandu.**

Grounded in the self-authored **VCH Sizing Framework (2nd Ed.)**, the system coordinates a passive solar thermal loop with an auxiliary electric immersion array through PLC automation to deliver demand-driven, high-efficiency process operations. As of Proposal IV, this automation logic is formalised as the **Adaptive Demand Allocation Architecture (ADA)** — see [Section 5.1](#51-the-adaptive-demand-allocation-architecture-ada).

> **Document History**
> | Version | Date | Status |
> | :--- | :--- | :--- |
> | Technical Proposal I | Prior to June 2026 | Archived — superseded |
> | Technical Proposal II | June 29, 2026 | Archived — superseded |
> | Technical Proposal III (Architectural Revision I) | July 10, 2026 | Archived — superseded |
> | Technical Proposal IV (Architectural Revision II — ADA) | July 12, 2026 | Current — For Review |

---

## Table of Contents

1. [Industrial Mandate & Constraints](#1-industrial-mandate--constraints)
2. [Engineering Journey & Design Challenges](#2-engineering-journey--design-challenges)
3. [System Architecture](#3-system-architecture)
4. [Core Technical Deep Dives](#4-core-technical-deep-dives)
5. [The VCH Sizing Framework & ADA](#5-the-vch-sizing-framework--ada)
6. [Headline Results & Validation Metrics](#6-headline-results--validation-metrics)
7. [Future Plan](#7-future-plan)
8. [My Contributions](#8-my-contributions)
9. [Changelog: Proposal I → Proposal II](#9-changelog-proposal-i--proposal-ii)
10. [Changelog: Proposal II → Proposal III (Architectural Revision I)](#10-changelog-proposal-ii--proposal-iii-architectural-revision-i)
11. [Changelog: Proposal III → Proposal IV (Architectural Revision II — ADA)](#11-changelog-proposal-iii--proposal-iv-architectural-revision-ii--ada)
12. [Appendix: Engineering Notebook](#appendix-engineering-notebook)

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

### Requirement Volatility Across Four Proposal Cycles

Between Proposal I and the current revision, the client's stated requirements changed substantially and more than once — the production window (see above), the supply/coil pipe cost preference, the introduction of a dedicated palm olein product line partway through, and most recently a hardware change (trunk upsizing) that reopened the entire priority and control-logic layer. None of these were anticipated at the outset.

Rather than treating each change as a disruption requiring a ground-up redesign, the architecture was deliberately kept modular enough to absorb them: the VCH thermal sizing methodology, the ε-NTU coil-length inversion, and the priority-budget control philosophy each proved reusable across revisions, with each new requirement extending the existing framework rather than replacing it. The PO tank introduction in Proposal III, for example, required restructuring the oil-side piping and adding a third priority tier — but did not require re-deriving the underlying thermal model, which carried forward unchanged.

**Takeaway:** A four-revision proposal history is not, on its own, a sign of a poorly-scoped project — it is a normal feature of iterative industrial design work done alongside a client who is still discovering their own requirements. The relevant engineering discipline is not preventing requirement change, but architecting a system whose core methodology survives it. That discipline is reflected directly in the changelog structure of this document (Sections 9–11), which exists specifically to make each revision's actual delta traceable against the last.

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
> **Proposal III update:** The coil bore variable is itself resolved into a **single standardised 2-inch bore across every tank** (T10, PO, and T5 alike), trading a small amount of thermal margin for a single procurement spec across the whole plant.
>
> **Proposal IV update:** The 2-inch coil bore and tank-level piping are unchanged. The variable reopened this revision is the **trunk main**, upsized from 1-inch to 1.5-inch specifically to enable dual-branch parallel flow — see [Section 11](#11-changelog-proposal-iii--proposal-iv-architectural-revision-ii--ada).

---

### Challenging the Water-Side Velocity Assumption

The initial hypothesis was that increasing water-side velocity through the submerged hydronic coils would be the primary lever for accelerating the melting phase. Applying the first-principles equations of the VCH Sizing Framework forced a critical course correction.

**The impedance bottleneck.** Modelling the two-phase overall heat transfer coefficient ($U$) revealed that the outer oil-side thermal resistance accounts for over **95%** of total system impedance. Increasing water velocity through a 1-inch bore coil (Case A.B) produced a very high inner-surface coefficient ($h_i = 19{,}594\ \text{W/m}^2\text{K}$), yet yielded a negligible change in the overall melting rate — while adding hydraulic pump stress and accelerated wear for a mathematically redundant gain.

### Shifting to Algorithmic Design

Once the solid-phase oil-side resistance was confirmed as an unyielding physical bottleneck, the design philosophy shifted from mechanical brute force to **algorithmic throughput recovery**. If a single tank's melting phase cannot be safely accelerated beyond its thermodynamic limit, total plant throughput must be reclaimed by orchestrating a smarter, time-staggered multi-tank queue.

This led directly to the demand-driven "pull" automation architecture. Real-time volume- and temperature-weighted priority matrices ($S_\text{casual}$ and $S_\text{immediate}$) allow the PLC to continuously prepare, melt, and hold oil across all three 10 kL vessels in an overlapping sequence — bypassing single-tank cycle limitations and securing an uninterrupted downstream process stream.

**Proposal IV extends this same philosophy one level further**: if a single *branch's* flow rate cannot be increased without a full hydraulic redesign, throughput can instead be recovered by allowing the trunk to serve *two branches in parallel* — see the Need-Array Priority Framework below.

---

### From a Shared Bunch to a Dedicated Palm Olein Tank (Proposal III)

Once the demand-driven multi-tank queue was validated, a new operational requirement emerged: one of the three T10 vessels needed to be carved out as dedicated palm olein storage rather than continuing to melt palm oil. Palm olein solidifies at a much lower temperature (≈24°C, versus palm oil's 36°C) and, once liquid, needs comparatively little energy to stay that way — so simply leaving it in the shared rotation would have distorted the tank-scoring system's assumptions, which were derived entirely around palm oil's higher-energy melt behaviour.

The fix required restructuring at the piping level, not just the control level — on the **oil side**, not the hydronic heating side. The original design drew all three tanks' oil off a **single shared feed pipe**; this revision gives each tank its **own dedicated oil pump and feed line**, gated by a manual ball valve in series with an automated control valve. The water/hydronic heating circuit itself is unchanged. This individualised oil feed is what makes it possible to designate one tank as a dedicated, isolated PO (palm olein) store — automatically excluded from the melting rotation, manually hard-isolated as a physical safeguard, and dispensed only via operator-triggered HMI pulses — without touching the piping or control logic of the other two tanks.

This single change cascaded into a full re-architecture of the plant's priority logic (see below) and its fault-detection philosophy (Section 4).

---

### A Three-Way Priority Ladder, Not a Fixed Split (Proposal III)

Introducing the PO tank meant the old two-tier logic (T5 master, T10 demand-pull) needed a third rung: **P1 — T5 trim-heating**, **P2 — PO tank temperature maintenance**, and **P3 — T10 palm oil melting**. The obvious approach — a strict P1 ≫ P2 ≫ P3 lockout — was rejected: it would mean P3 simply waits, indefinitely if necessary, whenever P1 or P2 has any demand at all, even though palm oil melting tolerates interruption far better than a live PO-tank dispense or T5's process-critical trim-heating.

Instead, arbitration was resolved as a **sequential daily energy budget**: P1's and P2's actual required duty periods are computed first, and P3 — by design the process that absorbs all of the system's slack — receives whatever remains of the 24-hour window. This ladder was retained as the basis for arbitration logic through Proposal III; Proposal IV reframes it into a parallel need-array rather than a strict sequence (Section 11), while keeping P3's role as the slack-absorbing process unchanged.

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

As of Proposal IV, each of the three T10 tanks has its own **dedicated oil pump and feed line**, with one T10 tank optionally designated by site technicians as the **PO tank** — automatically and manually isolated from the common palm-oil bunch and dispensed only via HMI-driven pulse logic. On the hydronic side, the trunk main has been upsized from 1-inch to **1.5-inch NPS**, enabling it to serve two 1-inch branches simultaneously at their full individual design flow. Water time across the plant is arbitrated by the **ADA need-array** — P1 (T5), P2 (PO tank), P3 (palm oil melt) — described in full in [Section 5.1](#51-the-adaptive-demand-allocation-architecture-ada) and [Section 11](#11-changelog-proposal-iii--proposal-iv-architectural-revision-ii--ada).

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

This algorithm protects high-pressure line components and prevents product degradation without operator intervention. It is retained unchanged through Proposal IV, governing T5's safety cutoff logic. Proposal IV's worst-case T5 loss calculation (Section 11) deliberately evaluates the tank at this boundary (55°C) as a conservative stress-test basis.

### Volume- and Temperature-Weighted Tank Scoring

Two independent PLC calculation blocks evaluate plant state and drive the staggered delivery queue:

- **$S_\text{casual}$ Block** — Manages solar thermal energy distribution to tanks requiring non-urgent pre-heating.
- **$S_\text{immediate}$ Block** — Prioritises auxiliary electric backup (36 kW) to the active processing tank when a downstream demand signal ($\delta$) is high, preventing line starvation.

Retained unchanged through Proposal IV, applied only across the two T10 tanks not designated as the PO tank.

### Coil Sizing: Inverted Design Logic

Proposal I fixed the coil at its geometric ceiling (90 m for T10) and asked what throughput results. Proposal II inverted this: a heat-duty target $Q_\text{target} = Q_\text{batch} + Q_\text{loss,max} = 9.17\ \text{kW}$ is defined from the mandate and worst-case standing loss, and the **minimum coil length required** is solved in closed form via the ε-NTU method.

Proposal III fixed the coil bore and length outright (2-inch bore, 30 m for T10/PO tanks, 10 m for T5) as a standardised, single-spec design across the whole plant. **Proposal IV retains this coil spec unchanged** — the throughput gain this revision comes entirely from trunk-level dual-branch operation, not from any further coil resizing.

### Batch-Side Modelling Correction: $C_\text{min} = C_w$

Proposal I's T5 analysis treated oil throughput as $C_\text{min}$, appropriate for continuous flow-through duty. Under the individualised-feed architecture, each tank is instead heated as a **well-mixed batch** whose bulk temperature changes slowly relative to a single pass of water through the coil — so the water side is $C_\text{min}$ ($C_w$) and the tank contents behave as $C_\text{max} \to \infty$ over one coil pass. Using the old throughput-rate model here would have predicted effectiveness in excess of 98% and near-instant temperature overshoot — physically inconsistent with a duty-cycled batch process. All NTU calculations from Proposal III onward use:

$$NTU = \frac{UA}{C_w}, \quad \varepsilon = 1 - e^{-NTU}, \quad Q(T_\text{tank}) = \varepsilon\, C_w\, (T_\text{hot} - T_\text{tank})$$

### Fault Detection: A Physics-Based Alarm Philosophy

An earlier iteration considered alarming whenever P1's duty cycle, measured over a short rolling window, exceeded twice its statistically expected value. This was rejected because P1's real-world demand is inherently bursty — legitimate operation naturally produces some windows with heavy, clustered activity and others with none, so a duty-percentage threshold can't distinguish a busy stretch of the day from an actual fault.

The revised philosophy alarms on **physics, not bookkeeping**: the PLC compares T5's observed heating and cooling rates against the maximum physically achievable rates given the coil's known heat-delivery capacity and the tank's own computed loss rate. Heating faster than the coil could physically produce, or cooling faster than the tank's own standing loss rate can account for, both indicate a sensor, valve, or leak fault — independent of how busy the day has been. Retained unchanged in Proposal IV.

---

## 5. The VCH Sizing Framework & ADA

This system is a full-scale industrial deployment of the **VCH Sizing Framework (2nd Edition)** — a methodology authored specifically for submerged hydronic coil thermal systems. The project served as a definitive verification platform, confirming that unifying coil heat transfer modeling with multi-phase thermal boundary calculations produces highly predictable, field-resilient industrial designs.

**DOI:** [10.5281/zenodo.21009246](https://doi.org/10.5281/zenodo.21009246)

### 5.1 The Adaptive Demand Allocation Architecture (ADA)

As of Proposal IV, the plant's control logic is formalised under a single name — the **Adaptive Demand Allocation Architecture (ADA)** — a responsive control framework for multi-load thermal distribution systems that replaces rigid sequential scheduling and static supply setpoints with real-time fluid-mechanics-aware, energy-budgeted, operator-centric governance. ADA rests on four pillars:

**1. The Need-Array Priority Framework.** Rather than a strict priority ladder that locks out lower-priority processes entirely whenever a higher-priority one is active, ADA evaluates active demand as a parallel need array with **three distinct tiers**, not two:
   - *Unbounded, guaranteed service* — T5 trim-heating (P1), the process master.
   - *Bounded, operator-supervised* — PO tank maintenance/dispense (P2), capped by daily throughput and layered governance rather than by priority lockout.
   - *Remainder-absorbing* — palm oil melting (P3), which by design receives whatever branch-time the array leaves available, and benefits directly whenever a second branch is free to run in parallel.

   When one process is active, the trunk runs at a reduced single-branch velocity; when two are active, it shifts to a high-velocity dual-branch posture, serving both concurrently at their full individual design flow — a direct consequence of upsizing the trunk main to 1.5-inch (Section 11.1).

**2. Demand-Driven Dynamic Thermal Sizing.** Rather than holding the utility loop at a fixed, energy-intensive maximum ceiling (70°C, constant, in Proposal III), ADA evaluates aggregate instantaneous demand ($E_\text{total}$) on a continuous 10-second refresh window and derives the water supply target from it directly. The control law is a **two-point anchored proportional relationship** — anchored specifically at system idle ($P=0\to40°C$) and at **T5's own established worst-case power draw** ($P\approx6.16\ \text{kW}\to70°C$), not a generic system-wide worst case. T5 is used as the anchor because it is the process master; the water supply is considered "fully hot" once demand reaches what T5 alone can draw at its own worst case. The underlying demand function explicitly tracks the physical discontinuity at the palm oil melting point (a genuine step in remaining energy demand, not a modelling artefact) and the distinct natural-convection loss behaviour of insulated (T5) versus uninsulated (PO tank) vessels.

**3. Load-Responsive Operational Postures.** System execution is governed by T5's own live level ($\alpha_S$) — not a fixed schedule, and not T10 tank level or temperature — since T5's level is the clearest available signal of how urgently the whole plant needs melted oil:
   - **Eco Mode** ($\alpha_S \geq 90\%$) — buffer nearly full, low-intensity maintenance rate.
   - **Efficiency Mode** ($90\% > \alpha_S \geq 50\%$) — steady-state operating tier.
   - **Full Throttle** ($\alpha_S < 50\%$) — aggressive demand pull, deliberately triggered at the same 50% threshold that already fires the batch-release logic, so the two mechanisms reinforce rather than disagree.

   Mode selection and the demand-driven water temperature are not competing signals to be resolved by taking whichever is "higher" — they sit in a cause-and-effect relationship. Mode decides how aggressively P3 pulls; that decision shapes $E_\text{total}$; $E_\text{total}$ decides how hot the water needs to be delivered to meet whatever was asked for.

**4. Layered Operator-Trust Governance.** For the PO tank's operator-initiated, operator-supervised dispensing, ADA replaces disruptive automatic hard-cutoffs with layered oversight: a **suspicion meter** ($S \in \{0,1,2,3\}$, resetting every 24 hours) that escalates from an HMI confirmation prompt through an alarm to autonomous feed isolation only at its highest tier (and only after a 5-minute no-response auto-escalation, never on a single long dispense), alongside an independent **soft-ceiling buffer** — supervised deviations up to 2× the operator-entered quantity are permitted before a warning is raised, and that ceiling is manual-shutoff only, so a live, supervised operation is never silently interrupted by a raw PLC timer.

> **Architectural impact.** By mapping a single hardware change — the upsized trunk cross-section — directly onto this four-pillar control framework, ADA lifts combined system throughput to **≈271%** of the original 2 t/day mandate (≈246% from palm oil melting alone, plus the PO tank's dispensed volume), without any change to individual coil sizing. It is a working example of software intelligence directly amplifying a fixed mechanical footprint's real capacity.

---

## 6. Headline Results & Validation Metrics

### Proposal IV Results (Current — Architectural Revision II / ADA)

Evaluated under a 1.5-inch trunk main (dual-branch capable), 1.2 m/s branch feed velocity cap, and the same standardised 2-inch coil bore as Proposal III (30 m for T10/PO tanks, 10 m for T5), with the need-array governing single- vs. dual-branch operation:

| Performance Metric | Result |
| :--- | :---: |
| **Trunk flow advantage over a single branch** | 2× |
| **T5 (P1) daily duty period, worst case (4 t/day basis)** | 3.67 hr (15.3%) |
| **PO tank (P2) daily duty period** | 0.59 hr (2.4%) |
| **P3 effective dual-branch energy budget** | ≈ 43.7 branch-hr/day |
| **Palm oil melted per day (P3, dual-delivery)** | ≈ 4,919.8 kg (4.92 t/day) |
| **Combined system throughput (P3 melt + PO tank)** | ≈ 5,419.8 kg (5.42 t/day) |
| **Fulfilment vs. 2 t/day mandate (melt only / combined)** | ≈ 246% / ≈ 271% |
| **Total daily thermal energy demand** | ≈ 1081.5 MJ |
| **Average continuous power demand** | ≈ 12.5 kW |

**Key findings:**
- **The trunk upsize is the single highest-leverage change in this revision** — without altering any coil, tank, or water temperature specification, enabling two branches to run in parallel roughly doubles P3's effective daily throughput.
- **P3's 48-branch-hour budget calculation is a deliberate conservative floor**, not a best case — it subtracts P1's and P2's full raw duty duration from the doubled daily pool regardless of how much of that time genuinely overlaps with P3's own access. A less conservative, overlap-credited model would recover most of the remaining gap toward the ≈6 t/day figure referenced during early scoping.
- **The PO tank's own standing heat loss still dominates its energy budget roughly 7:1** over its sensible duty, because it remains uninsulated — unchanged from Proposal III and still the single highest-leverage efficiency gain available.
- **This revision's T5 loss calculation deliberately evaluates the tank at its 55°C dynamic upper thermal boundary** (a worst-case stress-test basis), not at its typical operating mid-band — this distinction should be labelled explicitly wherever the figure is reused downstream.

### Archived: Proposal III Results (Architectural Revision I)

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

> Note: Proposal IV's figures are not directly comparable to Proposal III's on a like-for-like basis — Proposal IV introduces dual-branch trunk operation, a doubled T5 demand basis (4 t/day vs. 2 t/day), and a worst-case (55°C boundary) T5 loss evaluation rather than the typical mid-band used in Proposal III. See [Section 11](#11-changelog-proposal-iii--proposal-iv-architectural-revision-ii--ada) for the full basis-change breakdown.

### Archived: Proposal II Results

| Performance Metric | Design Target | Primary (75°C HTF) | Worst-Case (70°C HTF) |
| :--- | :---: | :---: | :---: |
| **Safety margin vs. 2 t/day (single tank)** | 1.0× | **3.0×** (at design point) | **3.0×** (by construction) |
| **3-tank staggered capacity** | ≥ 2.0 t/day | **6.0 t/day** | **6.0 t/day** |
| **Required coil length (1.5" bore)** | ≤ 90 m | **48.3 m** | **55.6 m** |
| **Solar Loop Thermal Coverage (ETC)** | Maximise | **61.46%** offset | Emergency electric override |
| **System Thermal Bottleneck** | Mitigate | Oil-side impedance (>95%) | Oil-side impedance (>95%) |
| **T5 coil length required (1.5" bore)** | — | **3.2 m** of 65 m ceiling | **4.1 m** of 65 m ceiling |

### Archived: Proposal I Results

| Performance Metric | Design Target | Primary (75°C HTF) | Worst-Case (70°C HTF) |
| :--- | :---: | :---: | :---: |
| **Daily Plant Throughput** | ≥ 2.0 t/day | **24.23 t/day** (staggered) | **20.48 t/day** (staggered) |
| **Single-Tank Safety Factor** | 1.0× | **3.63×** | **2.42×** |
| **Solar Loop Thermal Coverage** | Maximise | **61.46%** offset (ETC) | Emergency electric override |
| **System Thermal Bottleneck** | Mitigate | Oil-side impedance (>95%) | Oil-side impedance (>95%) |

---

## 7. Future Plan

With Proposal IV / ADA in place, the next phases are:

**Open Items Carried From This Revision**
- Confirm the 2°C / 24°C T10 outlet-temperature reference points against their intended design meaning (currently interpreted as extreme-cold and mild fill conditions).
- Confirm the 90% Eco/Efficiency mode threshold — the 50% Full Throttle line is fixed by the existing batch-release trigger, but the upper boundary is a proposed value pending sign-off.
- Consider the overlap-credited refinement to P3's dual-branch budget calculation (Section 6) if a less conservative throughput figure is wanted for planning purposes.

**PO Tank Insulation**
- Insulating the PO tank to T5's standard remains the identified highest-leverage, lowest-capital-cost efficiency gain — its uninsulated loss currently outweighs its sensible heating duty roughly 7:1, and every megajoule saved there returns directly to P3's melting window. Insulating it would also reduce the sensitivity of the PO tank's linearised loss term in the dynamic demand function to operating temperature, a secondary benefit for the ADA control law's accuracy.

**Electrical Design**
- Detailed electrical system design in AutoCAD, covering power distribution, protection coordination, and wiring layout strategies for the immersion array and pump drives.

**Controls Architecture**
- Discussion with the senior engineer to finalise the control philosophy — evaluating a PLC-based architecture against distributed individual controllers, and assessing the feasibility of PI control loops in place of hard on/off automation for improved stability and reduced thermal cycling.
- Formal review of the ADA framework itself with the senior engineer — this architecture has not yet been formally reviewed and is pending discussion.

**Instrumentation & HMI**
- Full sensor schedule: selection, specification, and placement of temperature, level, and flow instruments across all four tanks and the solar loop.
- HMI design for operator visibility, PO-tank designation/dispense workflow, suspicion-meter status display, and manual override capability.

**Hydraulics & Pump Selection**
- Head loss calculations for the coil circuits and the single-pump solar/primary loop, now including the upsized 1.5-inch trunk main. Hand calculations have been initiated; finalisation is deferred until site plumbing routing is confirmed.
- Pump selection based on the locked head loss and flow rate requirements, sized for dual-branch worst-case simultaneous draw.

---

## 8. My Contributions

This project was undertaken as a Junior Automation Design Architect during an internship at MEPL, working under the direction of the senior project lead. The scope of personal contributions is as follows:

**Thermal Sizing & Proposal Authorship**
All thermal calculations, coil sizing, case matrix analysis (A.A / A.B / B.A / B.B in Proposal I; unified 1-inch supply with 1–2 inch coil bore sweep in Proposal II; fixed 2-inch bore, individualised-feed, and three-way priority architecture in Proposal III; dual-branch trunk sizing, need-array reframing, and the ADA demand functions in Proposal IV), phase-change modelling, solar reliability analysis, and the full engineering proposal documents were produced independently, grounded in the self-authored VCH Sizing Framework (2nd Ed.).

**Process Architecture**
The single-pump solar feedback loop topology, the individualised T10 feed restructuring, the PO tank isolation logic, the P1/P2/P3 priority architecture (sequential-budget in Proposal III, need-array in Proposal IV), the demand-driven dynamic water temperature control law, and the Eco/Efficiency/Full Throttle mode logic were independently conceived and designed. The formalisation of this control logic under the ADA name is new to Proposal IV. This architecture has not yet been formally reviewed with the senior engineer and is pending discussion.

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

This section documents the technical changes introduced by the third revision.

### 10.1 Shared Oil Feed → Individualised Oil Feed per Tank

**Proposal II** retained a single shared oil feed pipe across the three T10 tanks, with tank selection handled entirely by the PLC's scoring logic. The hydronic water/heating circuit was, and remains, a separate system.

**Proposal III** replaces the shared oil feed with an **individualised feed per tank on the oil side** — each T10 vessel gets its own dedicated oil pump and feed line, gated by a manual ball valve in series with an automated control valve. The water-side hydronic circuit is unchanged. This oil-side restructuring is the structural prerequisite for designating one tank as a dedicated palm olein store without disturbing the piping or control logic of the other two.

### 10.2 New Tank Class: The PO (Palm Olein) Tank

One T10 tank may now be designated, via HMI input, as a dedicated palm olein store. Once designated, it is automatically excluded from the P3 melting rotation and the legacy tank-scoring system, manually hard-isolated via its ball valve as a PLC-independent safeguard, and dispensed only through operator-triggered HMI pulse logic (compute dispense time → run dispense valve → enter a 20 s-on/60 s pulse-hold to keep residual oil warm → clear on operator "process complete"). Proposal IV extends this tank's governance model further (Section 11.3).

### 10.3 Two-Tier → Three-Tier Priority Architecture

**Proposal II's** priority logic was effectively single-tier (T5 master, T10 demand-pull).

**Proposal III** introduces a three-way ladder — **P1 (T5 trim-heat)**, **P2 (PO tank maintenance)**, **P3 (T10 palm oil melt)** — resolved not by hard lockout but by a **sequential daily energy budget**: P1 and P2 take what their computed duty periods require, and P3 receives the remainder of the 24-hour window by design. P2 is additionally bounded by a 10-minute arbitration window (sized at 3× T5's worst-case heat-up time) with a flat 5-minute cap, so it cannot starve P3 indefinitely. This sequential model is superseded by the need-array in Proposal IV (Section 11.2).

### 10.4 Coil Bore and Length: From Swept Variable to Fixed Spec

**Proposal II** swept coil bore across 1", 1.25", 1.5", and 2" NPS to find a minimum-length design point (1.5" recommended, ≈56 m).

**Proposal III** fixes the bore at **2-inch NPS Sch. 10S across every tank** (T10, PO, and T5), with coil length fixed at **30 m** (T10/PO) and **10 m** (T5), and water supply fixed at a constant 70°C (previously 70–75°C, variable) with feed velocity reduced to 1.2 m/s (from 1.5 m/s). Because the oil-side film continues to dominate 1/U for the melting duty, standardising the bore for procurement simplicity costs almost nothing in thermal performance. This spec carries forward unchanged into Proposal IV.

### 10.5 NTU Model Correction: $C_\text{min} = C_w$, Not the Oil Throughput Rate

**Proposal I's** T5 analysis modelled oil throughput as $C_\text{min}$, appropriate for continuous flow-through duty.

**Proposal III** corrects this for the individualised-feed, batch-heated architecture: each tank is a well-mixed batch whose bulk temperature changes slowly relative to one coil pass, so **water is $C_\text{min}$** and tank contents behave as $C_\text{max} \to \infty$. The old model would have predicted >98% effectiveness and near-instant overshoot — physically inconsistent with batch heating.

### 10.6 Fault Detection: From Duty-Cycle Thresholds to Physics-Based Alarms

An interim design considered alarming when P1's duty cycle exceeded twice its statistically expected value over a rolling window — rejected because P1's demand is legitimately bursty, making a duty-percentage threshold unable to distinguish a busy day from a fault.

**Proposal III** instead alarms on **observed heating/cooling rates versus what is physically achievable** given the coil's known delivery capacity and the tank's own computed loss rate — decoupling fault detection from duty-cycle bookkeeping entirely. Retained unchanged in Proposal IV.

### 10.7 Headline Result Basis

Proposal III's throughput and safety-margin figures were reported against the **single-branch, sequential water-use case only** (P1, P2, P3 never draw simultaneously). Simultaneous-branch operation was outlined qualitatively as a future direction but explicitly out of scope for that revision's quantitative results — this is exactly what Proposal IV implements and quantifies.

---

## 11. Changelog: Proposal III → Proposal IV (Architectural Revision II — ADA)

This section documents the technical changes introduced by the current revision, in which the sequential single-branch architecture of Proposal III is replaced by the parallel, dual-branch **Adaptive Demand Allocation Architecture (ADA)**.

### 11.1 Trunk Upsize: Enabling Dual-Branch Flow

**Proposal III** used a 1-inch trunk main feeding 1-inch branches — structurally capable of serving only one branch at a time without starving it below design flow.

**Proposal IV** upsizes the trunk main to **1.5-inch NPS**. Sized to run at ≈1.021 m/s, the 1.5-inch trunk delivers exactly 2× the flow of a single 1-inch branch at its normal 1.2 m/s design velocity — enough to serve **two branches simultaneously**, each at full individual design flow, without either being starved. When only one branch is active, the trunk simply throttles down to ≈0.508 m/s. No branch-level, coil, or tank-level hardware changed; this is a single-fitting-scale intervention with outsized downstream effect.

### 11.2 Priority Ladder → Need Array

**Proposal III's** sequential daily energy budget assumed only one branch could ever be active, so P1 and P2 were served first, in full, before P3 received any remaining time.

**Proposal IV** reframes arbitration as a **need array**: however many of P1/P2/P3 currently have live demand determines whether the trunk runs single-branch or dual-branch. When two processes are concurrently active, both are served in full via the upsized trunk rather than one waiting on the other. P1 remains unbounded and effectively guaranteed; P2 remains capped (Section 11.3); P3 is the remainder-absorbing tier, now benefiting directly from dual-branch parallel operation whenever a second slot is free. P3's daily throughput is modelled conservatively as a **48 branch-hour pool** (2 branches × 24 hr) minus P1's and P2's full raw duty duration — a deliberate floor estimate, not a best case (see Section 6).

### 11.3 PO Tank Governance: From Hard Cap to Operator-Trust Model

**Proposal III** capped P2 with a flat 10-minute arbitration window and a 5-minute hard limit.

**Proposal IV** replaces this with a **suspicion meter** ($S \in \{0,1,2,3\}$, resetting every 24 hours): sustained draw beyond the expected 500 kg/day escalates from an HMI confirmation prompt ($S{=}1$) through an alarm ($S{=}2$) to autonomous feed isolation with alarm ($S{=}3$) — the only point in this pathway that forces a shutoff — with a 5-minute no-HMI-response auto-increment to prevent the escalation stalling on operator inaction. Independently, a **soft-ceiling buffer** permits draw up to 2× the operator-entered dispense quantity before issuing a warning; crossing it is manual-shutoff only, so a live, supervised dispense is never silently interrupted.

### 11.4 T5 Demand Basis and Worst-Case Loss Evaluation

**Proposal III** evaluated T5 against a 2 t/day throughput and its typical 42.5°C mid-band operating condition for the loss calculation.

**Proposal IV** doubles the T5 demand basis to **4 t/day**, reflecting the higher system-level throughput the dual-branch architecture now supports, and deliberately evaluates T5's standing loss at its **55°C dynamic upper thermal boundary** (the existing $T_f(x,y,m_p)$ safety limit) rather than the operating mid-band — a conservative worst-case stress test, not the typical daily figure.

### 11.5 Dynamic, Demand-Driven Water Temperature

**Proposal III** held the water supply at a constant, fixed 70°C regardless of actual instantaneous demand.

**Proposal IV** derives the water target from real-time aggregate demand ($E_\text{total}=E_\alpha+E_5+E_{C^\ast}$, summed on a 10-second refresh window) via a two-point anchored proportional law:

$$T_\text{water} = 40 + \frac{70-40}{6.16}\,P = 40 + 4.87\,P\ [\text{kW}], \quad \text{clamped to } [40,70]°\text{C}$$

anchored at system idle ($P=0\to40°C$) and T5's own worst-case draw ($P\approx6.16\ \text{kW}\to70°C$). Solar and auxiliary supply are then gated purely on whether each can meet this dynamic target, rather than running to a fixed schedule. Each demand term ($E_\alpha$, $E_5$, $E_{C^\ast}$) explicitly tracks the physical discontinuity at palm oil's melting point and the distinct (approximated, deliberately linearised) natural-convection loss behaviour of T5's insulated jacket versus the PO tank's uninsulated shell.

### 11.6 Load-Responsive Operating Modes

**Proposal III** had no load-responsive mode logic — P3 ran continuously whenever it held a branch.

**Proposal IV** introduces three operating postures for P3, governed by **T5's own live level** ($\alpha_S$) rather than tank temperature or T10 level: Eco Mode (≥90%), Efficiency Mode (90–50%), and Full Throttle (<50%) — the Full Throttle threshold deliberately matching the existing batch-release trigger, so the two mechanisms escalate together.

### 11.7 Headline Result Basis Change

Proposal IV's throughput figures are reported against the **dual-branch, need-array case**, evaluated as a deliberately conservative floor (Section 6). Combined system throughput rises to ≈5.42 t/day (≈271% of the original 2 t/day mandate), against Proposal III's ≈2.45 t/day (≈122%) — the entire gain attributable to the trunk upsize and need-array reframing described above, with no change to individual coil sizing.

---

## Appendix: Engineering Notebook

High-resolution scans of scratchpad derivations, geometric helical coil layout constraints, and early PLC state-machine routing matrices are located in the `engineering_notes/` directory.
