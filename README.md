# Palm Oil Melting & Retention System

**Industrial thermal systems design and automation architecture for a multi-tank palm oil melting, storage, and trim-heating facility — Mechatronics Engineering Pvt. Ltd. (MEPL), Kathmandu.**

Grounded in the self-authored **VCH Sizing Framework (2nd Ed.)**, the system coordinates a passive solar thermal loop with an auxiliary electric immersion array through PLC automation to deliver demand-driven, high-efficiency process operations. As of Proposal IV, this automation logic is formalised as the **Adaptive Demand Allocation Architecture (ADA)** — see [Section 5.1](#51-the-adaptive-demand-allocation-architecture-ada). As of the System Overview (Revised) document, ADA is expanded to true three-way concurrent flow — see [Section 12](#12-changelog-proposal-iv--system-overview-revised-true-three-way-concurrency).

> **Document History**
> | Version | Date | Status |
> | :--- | :--- | :--- |
> | Technical Proposal I | Prior to June 2026 | Archived — superseded |
> | Technical Proposal II | June 29, 2026 | Archived — superseded |
> | Technical Proposal III (Architectural Revision I) | July 10, 2026 | Archived — superseded |
> | Technical Proposal IV (Architectural Revision II — ADA) | July 12, 2026 | Archived — superseded |
> | ADA: System Overview (Revised) — True Three-Way Concurrency | July 16, 2026 | Current — For Review |
> | ADA: PLC Implementation — Full Replacement (companion doc) | July 16, 2026 | Current — For Review |

Full PLC ladder logic, register maps, and I/O tables are documented separately in the companion document, **ADA: PLC Implementation — Full Replacement**, and are only summarised here where they affect system-level behavior.

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
12. [Changelog: Proposal IV → System Overview (Revised) — True Three-Way Concurrency](#12-changelog-proposal-iv--system-overview-revised-true-three-way-concurrency)
13. [PLC Implementation (Companion Document)](#13-plc-implementation-companion-document)
14. [Appendix: Engineering Notebook](#appendix-engineering-notebook)

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

### Requirement Volatility Across Five Proposal Cycles

Between Proposal I and the current revision, the client's stated requirements changed substantially and more than once — the production window (see above), the supply/coil pipe cost preference, the introduction of a dedicated palm olein product line partway through, a hardware change (trunk upsizing) that reopened the entire priority and control-logic layer, and most recently a coil bore reduction paired with a valve-count reduction that reopened the need-array arbiter itself. None of these were anticipated at the outset.

Rather than treating each change as a disruption requiring a ground-up redesign, the architecture was deliberately kept modular enough to absorb them: the VCH thermal sizing methodology, the ε-NTU coil-length inversion, and the priority-budget control philosophy each proved reusable across revisions, with each new requirement extending the existing framework rather than replacing it. The PO tank introduction in Proposal III, for example, required restructuring the oil-side piping and adding a third priority tier — but did not require re-deriving the underlying thermal model, which carried forward unchanged. The three-way concurrency expansion in the current revision required a new arbiter (Section 12) but no change at all to the underlying thermal sizing methodology or the PO tank's governance model.

**Takeaway:** A five-revision proposal history is not, on its own, a sign of a poorly-scoped project — it is a normal feature of iterative industrial design work done alongside a client who is still discovering their own requirements. The relevant engineering discipline is not preventing requirement change, but architecting a system whose core methodology survives it. That discipline is reflected directly in the changelog structure of this document (Sections 9–12), which exists specifically to make each revision's actual delta traceable against the last.

---

### Solar Loop Integration: Single-Pump Architecture

The standard two-loop passive solar integration approach — where the solar circuit operates independently and dumps heat into the primary loop only when capacity permits — would have required a dedicated secondary circulation pump. To reduce capital cost and system complexity, the loop topology was redesigned so that a single high-pressure pump handles full circulation duties across both the solar collectors and the primary process loop.

The trade-off is a heavier-duty pump selection and a significantly higher system head loss, both of which are documented and will be finalised once site plumbing and pipe routing are confirmed. The architectural logic underpinning this single-pump design is reflected in P&ID III, which supersedes the original Process Flow Diagram as the authoritative routing reference.

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
>
> **System Overview (Revised) update:** The coil bore is reopened one more time and reduced from **2-inch to 1.5-inch across every tank** (T5, T10, PO), trading roughly 16–19% of delivered heat rate for a further procurement/cost simplification, paired with a branch valve count reduction (8 → 6) and true three-way concurrent flow — see [Section 12](#12-changelog-proposal-iv--system-overview-revised-true-three-way-concurrency).

---

### Challenging the Water-Side Velocity Assumption

The initial hypothesis was that increasing water-side velocity through the submerged hydronic coils would be the primary lever for accelerating the melting phase. Applying the first-principles equations of the VCH Sizing Framework forced a critical course correction.

**The impedance bottleneck.** Modelling the two-phase overall heat transfer coefficient ($U$) revealed that the outer oil-side thermal resistance accounts for over **95%** of total system impedance. Increasing water velocity through a 1-inch bore coil (Case A.B) produced a very high inner-surface coefficient ($h_i = 19{,}594\ \text{W/m}^2\text{K}$), yet yielded a negligible change in the overall melting rate — while adding hydraulic pump stress and accelerated wear for a mathematically redundant gain.

### Shifting to Algorithmic Design

Once the solid-phase oil-side resistance was confirmed as an unyielding physical bottleneck, the design philosophy shifted from mechanical brute force to **algorithmic throughput recovery**. If a single tank's melting phase cannot be safely accelerated beyond its thermodynamic limit, total plant throughput must be reclaimed by orchestrating a smarter, time-staggered multi-tank queue.

This led directly to the demand-driven "pull" automation architecture. Real-time volume- and temperature-weighted priority matrices ($S_\text{casual}$ and $S_\text{immediate}$) allow the PLC to continuously prepare, melt, and hold oil across all three 10 kL vessels in an overlapping sequence — bypassing single-tank cycle limitations and securing an uninterrupted downstream process stream.

**Proposal IV extended this same philosophy one level further**: if a single *branch's* flow rate cannot be increased without a full hydraulic redesign, throughput can instead be recovered by allowing the trunk to serve *two branches in parallel*. **The current revision extends it once more**: rather than discarding a priority under three-way contention, the trunk now throttles and serves *all three branches concurrently* whenever demand is genuinely three-way — see [Section 12](#12-changelog-proposal-iv--system-overview-revised-true-three-way-concurrency).

---

### From a Shared Bunch to a Dedicated Palm Olein Tank (Proposal III)

Once the demand-driven multi-tank queue was validated, a new operational requirement emerged: one of the three T10 vessels needed to be carved out as dedicated palm olein storage rather than continuing to melt palm oil. Palm olein solidifies at a much lower temperature (≈24°C, versus palm oil's 36°C) and, once liquid, needs comparatively little energy to stay that way — so simply leaving it in the shared rotation would have distorted the tank-scoring system's assumptions, which were derived entirely around palm oil's higher-energy melt behaviour.

The fix required restructuring at the piping level, not just the control level — on the **oil side**, not the hydronic heating side. The original design drew all three tanks' oil off a **single shared feed pipe**; this revision gives each tank its **own dedicated oil pump and feed line**, gated by a manual ball valve in series with an automated control valve. The water/hydronic heating circuit itself is unchanged. This individualised oil feed is what makes it possible to designate one tank as a dedicated, isolated PO (palm olein) store — automatically excluded from the melting rotation, manually hard-isolated as a physical safeguard, and dispensed only via operator-triggered HMI pulses — without touching the piping or control logic of the other two tanks.

This single change cascaded into a full re-architecture of the plant's priority logic (see below) and its fault-detection philosophy (Section 4).

---

### A Three-Way Priority Ladder, Not a Fixed Split (Proposal III)

Introducing the PO tank meant the old two-tier logic (T5 master, T10 demand-pull) needed a third rung: **P1 — T5 trim-heating**, **P2 — PO tank temperature maintenance**, and **P3 — T10 palm oil melting**. The obvious approach — a strict P1 ≫ P2 ≫ P3 lockout — was rejected: it would mean P3 simply waits, indefinitely if necessary, whenever P1 or P2 has any demand at all, even though palm oil melting tolerates interruption far better than a live PO-tank dispense or T5's process-critical trim-heating.

Instead, arbitration was resolved as a **sequential daily energy budget**: P1's and P2's actual required duty periods are computed first, and P3 — by design the process that absorbs all of the system's slack — receives whatever remains of the 24-hour window. This ladder was retained as the basis for arbitration logic through Proposal III; Proposal IV reframed it into a parallel need-array rather than a strict sequence (Section 11); the current revision expands that need-array further into genuine three-way concurrent service (Section 12), retiring the "discard the lowest priority" contention rule entirely.

**Takeaway:** Adding a third demand source didn't call for a more complex real-time scheduler — it called for recognising which processes can tolerate deferral and encoding that directly into a daily budget rather than a live priority fight.

---

### Ambient Data: Weighted-Average Design Philosophy

Kathmandu's solar irradiance and ambient temperature data are not available from a single authoritative instrument record for this site. Rather than anchoring the design on a single "average good day" figure — which would leave the system undersized for adverse conditions — weighted annual averages were compiled across multiple sources and applied consistently throughout the sizing work. This methodology appears across solar reliability factors, ambient baseline temperature (18.1°C), and the tank priority scoring metric ($S_\text{immediate}$).

The limitation is acknowledged: weighted averages characterise typical behaviour, not extremes. The worst-case 70°C HTF scenario in the validation table is the explicit hedge against adverse conditions, extended in the current revision by an explicit worst-case simultaneous-demand check (Section 12).

---

### Tank Geometry & Manufacturability

Initial vessel proportioning followed the aspect ratio guidance in the VCH Sizing Framework. Translating those proportions into manufacturable steel vessels — balancing height, diameter, conical cap geometry, plate utilisation, and weld seam minimisation — proved more iterative than the thermal calculations themselves. Once the senior engineer introduced a manufacturability constraint tied to standard plate dimensions, the detailed vessel geometry was handed to the team's mechanical engineer, who modelled the tanks in SolidWorks and confirmed material utilisation and weldability before the dimensions were locked.

---

## 3. System Architecture

> **The original Process Flow Diagram (PFD) is now superseded and no longer authoritative.** The current source of truth for process routing is **P&ID III**, the latest revision of the mechanical engineer's Piping & Instrumentation Diagram. The PFD is retained in the repository for historical reference only.

As of the current revision, each of the three T10 tanks has its own **dedicated oil pump and feed line**, with one T10 tank optionally designated by site technicians as the **PO tank** — automatically and manually isolated from the common palm-oil bunch and dispensed only via HMI-driven pulse logic. On the hydronic side, the trunk main is **1.5-inch NPS**, capped at a safe 1.2 m/s rated velocity; two of the three branches are now permanently and continuously dedicated to T10 palm oil melting (P3), while the third branch is shared between T5 (P1) and the PO tank (P2). Branch valve count has been reduced from 8 to 6, and the coil bore across every tank (T5, T10, PO) is now **1.5-inch**, down from 2-inch. Water time across the plant is arbitrated by the **ADA need-array**, now expanded to true three-way concurrent service — see [Section 5.1](#51-the-adaptive-demand-allocation-architecture-ada) and [Section 12](#12-changelog-proposal-iv--system-overview-revised-true-three-way-concurrency).

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

This algorithm protects high-pressure line components and prevents product degradation without operator intervention. It is retained unchanged through the current revision, governing T5's safety cutoff logic. The full 32-bit fixed-point PLC implementation of this register is documented in the companion PLC document, Section 1.7.

### Volume- and Temperature-Weighted Tank Scoring

The tank-scoring system has been consolidated to a **single metric**. The original two-block design ($S_\text{casual}$ for non-urgent solar pre-heating, $S_\text{immediate}$ for urgent auxiliary-backup prioritisation) is retired in favour of one scoring block used for all arbitration decisions:

$$S_\text{immediate} = 0.6\,(\text{mass fraction}) + 0.4\,(\theta_\text{norm})$$

applied only across the two T10 tanks not designated as the PO tank, with the **higher-scoring tank winning** priority for both solar and auxiliary delivery. This is a deliberate re-weighting from the original two-block scheme, which split $S_\text{casual}$ (0.6·level + 0.4·temperature) and $S_\text{immediate}$ (0.4·level + 0.6·temperature) into separate mass-weighted and temperature-weighted variants for different demand sources; a single mass-weighted score is now judged sufficient for both.

### Coil Sizing: Inverted Design Logic

Proposal I fixed the coil at its geometric ceiling (90 m for T10) and asked what throughput results. Proposal II inverted this: a heat-duty target $Q_\text{target} = Q_\text{batch} + Q_\text{loss,max} = 9.17\ \text{kW}$ is defined from the mandate and worst-case standing loss, and the **minimum coil length required** is solved in closed form via the ε-NTU method.

Proposal III fixed the coil bore and length outright (2-inch bore, 30 m for T10/PO tanks, 10 m for T5) as a standardised, single-spec design across the whole plant. Proposal IV retained this coil spec unchanged. **The current revision reduces the coil bore to 1.5-inch across every tank while keeping coil lengths unchanged** (10 m for T5, 30 m for T10/PO) — see [Section 12](#12-changelog-proposal-iv--system-overview-revised-true-three-way-concurrency) for the full thermal-performance impact of this bore reduction.

### Batch-Side Modelling Correction: $C_\text{min} = C_w$

Proposal I's T5 analysis treated oil throughput as $C_\text{min}$, appropriate for continuous flow-through duty. Under the individualised-feed architecture, each tank is instead heated as a **well-mixed batch** whose bulk temperature changes slowly relative to a single pass of water through the coil — so the water side is $C_\text{min}$ ($C_w$) and the tank contents behave as $C_\text{max} \to \infty$ over one coil pass. Using the old throughput-rate model here would have predicted effectiveness in excess of 98% and near-instant temperature overshoot — physically inconsistent with a duty-cycled batch process. All NTU calculations from Proposal III onward use:

$$NTU = \frac{UA}{C_w}, \quad \varepsilon = 1 - e^{-NTU}, \quad Q(T_\text{tank}) = \varepsilon\, C_w\, (T_\text{hot} - T_\text{tank})$$

### Fault Detection: A Physics-Based Alarm Philosophy

An earlier iteration considered alarming whenever P1's duty cycle, measured over a short rolling window, exceeded twice its statistically expected value. This was rejected because P1's real-world demand is inherently bursty — legitimate operation naturally produces some windows with heavy, clustered activity and others with none, so a duty-percentage threshold can't distinguish a busy stretch of the day from an actual fault.

The revised philosophy alarms on **physics, not bookkeeping**: the PLC compares T5's observed heating and cooling rates against the maximum physically achievable rates given the coil's known heat-delivery capacity and the tank's own computed loss rate. Heating faster than the coil could physically produce, or cooling faster than the tank's own standing loss rate can account for, both indicate a sensor, valve, or leak fault — independent of how busy the day has been. Retained unchanged in the current revision; the full ladder implementation, including live-mass rate calculation and activity-gated level/mass anomaly detection, is in the companion PLC document, Section 1.15.

---

## 5. The VCH Sizing Framework & ADA

This system is a full-scale industrial deployment of the **VCH Sizing Framework (2nd Edition)** — a methodology authored specifically for submerged hydronic coil thermal systems. The project served as a definitive verification platform, confirming that unifying coil heat transfer modeling with multi-phase thermal boundary calculations produces highly predictable, field-resilient industrial designs.

**DOI:** [10.5281/zenodo.21009246](https://doi.org/10.5281/zenodo.21009246)

### 5.1 The Adaptive Demand Allocation Architecture (ADA)

As of Proposal IV, the plant's control logic is formalised under a single name — the **Adaptive Demand Allocation Architecture (ADA)** — a responsive control framework for multi-load thermal distribution systems that replaces rigid sequential scheduling and static supply setpoints with real-time fluid-mechanics-aware, energy-budgeted, operator-centric governance. As of the current revision, ADA's first pillar is expanded to true three-way concurrency (see below and Section 12). ADA rests on four pillars:

**1. The Need-Array Priority Framework.** Rather than a strict priority ladder that locks out lower-priority processes entirely whenever a higher-priority one is active, ADA evaluates active demand as a parallel need array with **three distinct tiers**, not two:
   - *Unbounded, guaranteed service* — T5 trim-heating (P1), the process master.
   - *Bounded, operator-supervised* — PO tank maintenance/dispense (P2), capped by daily throughput and layered governance rather than by priority lockout.
   - *Continuous, dedicated* — palm oil melting (P3), now permanently allocated two of the trunk's three branches, with no scenario in which it is fully idle.

   As of the current revision, all three tiers can be genuinely concurrent: the trunk, capped at its own safe 1.2 m/s rated velocity, serves whichever combination of branches has live demand by throttling flow rather than excluding a process — a direct consequence of the six-valve, 1.5-inch trunk reconfiguration (Section 12).

**2. Demand-Driven Dynamic Thermal Sizing.** Rather than holding the utility loop at a fixed, energy-intensive maximum ceiling (70°C, constant, in Proposal III), ADA evaluates aggregate instantaneous demand ($E_\text{total}$) on a continuous 10-second refresh window and derives the water supply target from it directly. The control law is a **two-point anchored proportional relationship** — anchored specifically at system idle ($P=0\to40°C$) and at **T5's own established worst-case power draw** ($P\approx6.16\ \text{kW}\to70°C$), not a generic system-wide worst case. T5 is used as the anchor because it is the process master; the water supply is considered "fully hot" once demand reaches what T5 alone can draw at its own worst case. The current revision adds an explicit peak-instantaneous-wattage coincidence check (Section 12) stress-testing this control law against the worst physically-plausible simultaneous draw across all three duties.

**3. Load-Responsive Operational Postures.** System execution is governed by T5's own live level ($\alpha_S$) — not a fixed schedule, and not T10 tank level or temperature — since T5's level is the clearest available signal of how urgently the whole plant needs melted oil:
   - **Eco Mode** ($\alpha_S \geq 90\%$) — buffer nearly full, low-intensity maintenance rate.
   - **Efficiency Mode** ($90\% > \alpha_S \geq 50\%$) — steady-state operating tier.
   - **Full Throttle** ($\alpha_S < 50\%$) — aggressive demand pull, deliberately triggered at the same 50% threshold that already fires the batch-release logic, so the two mechanisms reinforce rather than disagree.

   Unchanged in the current revision; fully laddered in the companion PLC document, Section 1.6.3.

**4. Layered Operator-Trust Governance.** For the PO tank's operator-initiated, operator-supervised dispensing, ADA replaces disruptive automatic hard-cutoffs with layered oversight: a **suspicion meter** ($S \in \{0,1,2,3\}$, resetting every 24 hours) that escalates from an HMI confirmation prompt through an alarm to autonomous feed isolation only at its highest tier (and only after a 5-minute no-response auto-escalation, never on a single long dispense), alongside an independent **soft-ceiling buffer** — supervised deviations up to 2× the operator-entered quantity are permitted before a warning is raised, and that ceiling is manual-shutoff only, so a live, supervised operation is never silently interrupted by a raw PLC timer. Unchanged in the current revision; the pulse-hold timer originally paired with this pillar (20 s-on/60 s pulse-hold) has been retired now that true three-way concurrency removes the branch-scarcity condition it existed to manage (Section 12).

> **Architectural impact.** As of the current revision, ADA delivers **≈247.7%** of the original 2 t/day mandate (≈222.7% from palm oil melting alone, plus the PO tank's dispensed volume) — down from Architectural Revision II's 271%, but achieved with two fewer control valves and an arbiter that no longer needs to discard any priority under contention. See [Section 12](#12-changelog-proposal-iv--system-overview-revised-true-three-way-concurrency) for the full basis of this trade-off.

---

## 6. Headline Results & Validation Metrics

### Current Revision Results (System Overview — Revised, True Three-Way Concurrency)

Evaluated under a 1.5-inch trunk main capped at 1.2 m/s, a 1.5-inch coil bore across every tank (10 m for T5, 30 m for T10/PO), six branch valves (down from eight), and the need-array expanded to genuine three-way concurrent service:

| Performance Metric | Result |
| :--- | :---: |
| **Coil area lost to the bore reduction (all tanks)** | −20.0% |
| **T5 (P1) daily duty period** | 4.47 hr (18.6%) |
| **PO tank (P2) daily duty period** | 0.71 hr (2.96%) |
| **Shared-branch active fraction of the day** | 21.0% |
| **Palm oil melted per day (P3)** | ≈ 4,453 kg/day |
| **Combined system throughput (P3 + PO tank)** | ≈ 4,953 kg/day |
| **Fulfilment vs. 2 t/day mandate (melt / combined)** | ≈ 222.7% / ≈ 247.7% |
| **Total daily thermal energy demand** | ≈ 990.7 MJ |
| **Average continuous power demand** | ≈ 11.47 kW |
| **Peak instantaneous demand (worst case)** | ≈ 36.61 kW |
| **Auxiliary array rated capacity** | 36.0 kW |

**Key findings:**
- **The bore reduction and the concurrency expansion are thermally separable, and only one of them is expensive.** The 2-inch → 1.5-inch bore change costs 16–19% of delivered heat rate across every duty — tracking the 20% coil area loss closely for the low-NTU duties (T5, T10 melt). Adding genuine three-way concurrency on top of that costs under 2% further for every duty.
- **Combined throughput falls by ≈8.6%** relative to Architectural Revision II (the prior 2-inch, two-priority revision), but still clears the original 2 t/day mandate by ≈2.5×.
- **At the single worst-case instant where every process is simultaneously at its coldest, highest-draw condition** — T5 at 40°C, the PO tank at 24°C, both melting branches at the 36°C melt point — peak demand (≈36.61 kW) marginally exceeds the auxiliary array's rated 36 kW by ≈1.7%. This is a deliberately conservative, compounded worst-case figure; the 300 L active thermal buffer would absorb a brief coincidence as a temperature dip rather than a shortfall, but the margin is narrow enough to carry into the electrical design phase.
- **The three-way need-array arbiter is architecturally simpler than Architectural Revision II's, not more complex** — flow-sharing under a velocity cap replaces the "discard the lowest priority" contention rule entirely, and the PO tank's pulse-hold timer is retired as a result (no scarcity condition remains to justify it).

### Archived: Proposal IV Results (Architectural Revision II)

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

> Note: current-revision figures are not directly comparable to Proposal IV's on a like-for-like basis — the current revision trades coil area (bore reduction) and two fewer valves for a simpler, genuinely concurrent arbiter. See [Section 12](#12-changelog-proposal-iv--system-overview-revised-true-three-way-concurrency) for the full before/after comparison.

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

With the current revision in place, the next phases are:

**Open Items Carried Forward**
- Mode thresholds (Eco/Efficiency/Standard boundaries) remain provisional and may be adjusted at commissioning time once live plant behaviour is observable — the 50% Full Throttle line is fixed by the existing batch-release trigger, but the other boundaries are not yet locked.
- Reconcile the ≈9% branch flow area discrepancy between the project's hand-derived trunk/branch sizing notes and the base VCH proposal's original 1-inch supply pipe basis (Section 12) against the as-built pipe specification.
- Carry the ≈36.61 kW peak instantaneous demand finding (≈1.7% over the 36 kW rated auxiliary array) into the electrical design phase explicitly.
- Confirm the VFD-01 RUN/FWD terminal logic (independent command vs. combined with speed-select) with the manufacturer's documentation before finalising the interlock wiring.

**Open Items Carried From the PLC Implementation Document**
- E-STOP latch reset source not yet defined.
- Behaviour on a mid-operation switch from Automation Enabled to Disabled (abrupt stop vs. complete-current-step) not yet decided.
- Tie-break behaviour on equal $S_\text{immediate}$ scores currently defaults to execution order (TA-favoured); flagged for confirmation, not an explicit design decision.
- $D_\text{Mode}$ power-up default not yet specified.
- Auxiliary staging hysteresis thresholds (26/22, 14/10, 0/2 kW, ±2 kW) are proposed, not independently confirmed.
- Access level on the PO tank designation confirm input (standard tap vs. supervisor PIN) remains open.

**Resolved Since Last Revision**
- $m_p$ (remaining oil-phase mass) for the $T_f$ register is acquired from the ultrasonic level sensor and converted to mass via the height-to-mass constants (Section 1.6.7 of the companion PLC document) — no longer an open item.
- Manual-mode trunk speed selection is confirmed as intended: the physical panel button drives a fixed HSM only, with no LSM/FSM selection on hardware — this is accepted behaviour, not a gap to close.

**PO Tank Insulation**
- Insulating the PO tank to T5's standard remains the identified highest-leverage, lowest-capital-cost efficiency gain — its uninsulated loss currently outweighs its sensible heating duty roughly 7:1, and every megajoule saved there returns directly to P3's melting window. Insulating it would also reduce the sensitivity of the PO tank's linearised loss term in the dynamic demand function to operating temperature, a secondary benefit for the ADA control law's accuracy.

**Electrical Design — Complete**
- Detailed electrical system design in AutoCAD, covering power distribution, protection coordination, and wiring layout strategies for the immersion array and pump drives, is now finished after several iterations — informed by the current revision's peak instantaneous demand finding.

**Controls Architecture**
- Discussion with the senior engineer to finalise the control philosophy — evaluating a PLC-based architecture against distributed individual controllers, and assessing the feasibility of PI control loops in place of hard on/off automation for improved stability and reduced thermal cycling.
- Formal review of the ADA framework itself, including its current three-way concurrent arbiter, with the senior engineer — this architecture has not yet been formally reviewed and is pending discussion.

**Instrumentation — Complete**
- The full sensor schedule — selection, specification, and placement of temperature, level, and flow instruments across all four tanks and the solar loop — is finished, cross-referenced against the confirmed 11-channel analog input assignment in the companion PLC document.

**HMI (Remaining)**
- HMI design for operator visibility, PO-tank designation/dispense workflow, suspicion-meter status display, and manual override capability.

**Hydraulics & Pump Selection**
- Head loss calculations for the coil circuits and the single-pump solar/primary loop, now including the 1.5-inch trunk main capped at 1.2 m/s under three-way concurrency. Hand calculations have been initiated; finalisation is deferred until site plumbing routing is confirmed.
- Pump selection based on the locked head loss and flow rate requirements, sized for three-way-concurrent worst-case simultaneous draw.

---

## 8. My Contributions

This project was undertaken as a Junior Automation Design Architect during an internship at MEPL, working under the direction of the senior project lead. The scope of personal contributions is as follows:

**Thermal Sizing & Proposal Authorship**
All thermal calculations, coil sizing, case matrix analysis (A.A / A.B / B.A / B.B in Proposal I; unified 1-inch supply with 1–2 inch coil bore sweep in Proposal II; fixed 2-inch bore, individualised-feed, and three-way priority architecture in Proposal III; dual-branch trunk sizing, need-array reframing, and the ADA demand functions in Proposal IV; the 1.5-inch bore reduction, six-valve reconfiguration, and true three-way concurrency analysis in the current revision), phase-change modelling, solar reliability analysis, and the full engineering proposal documents were produced independently, grounded in the self-authored VCH Sizing Framework (2nd Ed.).

**Process Architecture**
The single-pump solar feedback loop topology, the individualised T10 feed restructuring, the PO tank isolation logic, the P1/P2/P3 priority architecture (sequential-budget in Proposal III, dual-branch need-array in Proposal IV, true three-way concurrent need-array in the current revision), the demand-driven dynamic water temperature control law, and the Eco/Efficiency/Full Throttle mode logic were independently conceived and designed. The full PLC ladder logic implementation — I/O mapping, register map, safety gating, and all control blocks — is documented in the companion PLC Implementation document. This architecture has not yet been formally reviewed with the senior engineer and is pending discussion.

**Tank Geometry (Collaborative)**
Initial vessel proportions and aspect ratio estimates were produced as part of the thermal sizing work. Detailed manufacturable geometry and SolidWorks verification were completed by the team's mechanical engineer, who refined the dimensions to minimise plate waste and weld seam count.

**PFD vs. P&ID**
The Process Flow Diagram was produced as part of an earlier proposal but is now superseded — **P&ID III**, the mechanical engineer's latest Piping & Instrumentation Diagram revision, is the current authoritative process-routing reference, and the PFD is retained only for historical context. The oil distribution port (x/y/z) logic in the current revision is confirmed directly against P&ID III and taken as accurate as given, not re-derived from first principles.

**Note:** The project is ongoing. The contributions documented here reflect the proposal and PLC-implementation stage. Detailed electrical design and physical commissioning are planned for subsequent phases.

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

One T10 tank may now be designated, via HMI input, as a dedicated palm olein store. Once designated, it is automatically excluded from the P3 melting rotation and the legacy tank-scoring system, manually hard-isolated via its ball valve as a PLC-independent safeguard, and dispensed only through operator-triggered HMI pulse logic. Proposal IV extended this tank's governance model further (Section 11.3); the current revision retires the pulse-hold aspect of that logic entirely (Section 12.5) now that three-way concurrency removes the scarcity condition it existed to manage.

### 10.3 Two-Tier → Three-Tier Priority Architecture

**Proposal II's** priority logic was effectively single-tier (T5 master, T10 demand-pull).

**Proposal III** introduces a three-way ladder — **P1 (T5 trim-heat)**, **P2 (PO tank maintenance)**, **P3 (T10 palm oil melt)** — resolved not by hard lockout but by a **sequential daily energy budget**: P1 and P2 take what their computed duty periods require, and P3 receives the remainder of the 24-hour window by design. P2 is additionally bounded by a 10-minute arbitration window (sized at 3× T5's worst-case heat-up time) with a flat 5-minute cap, so it cannot starve P3 indefinitely. This sequential model is superseded by the two-branch need-array in Proposal IV (Section 11) and expanded to true three-way concurrency in the current revision (Section 12).

### 10.4 Coil Bore and Length: From Swept Variable to Fixed Spec

**Proposal II** swept coil bore across 1", 1.25", 1.5", and 2" NPS to find a minimum-length design point (1.5" recommended, ≈56 m).

**Proposal III** fixes the bore at **2-inch NPS Sch. 10S across every tank** (T10, PO, and T5), with coil length fixed at **30 m** (T10/PO) and **10 m** (T5), and water supply fixed at a constant 70°C (previously 70–75°C, variable) with feed velocity reduced to 1.2 m/s (from 1.5 m/s). Because the oil-side film continues to dominate 1/U for the melting duty, standardising the bore for procurement simplicity costs almost nothing in thermal performance. This spec carried forward unchanged into Proposal IV and is revised again in the current revision (Section 12.2), where the bore is reduced to 1.5-inch while lengths remain unchanged.

### 10.5 NTU Model Correction: $C_\text{min} = C_w$, Not the Oil Throughput Rate

**Proposal I's** T5 analysis modelled oil throughput as $C_\text{min}$, appropriate for continuous flow-through duty.

**Proposal III** corrects this for the individualised-feed, batch-heated architecture: each tank is a well-mixed batch whose bulk temperature changes slowly relative to one coil pass, so **water is $C_\text{min}$** and tank contents behave as $C_\text{max} \to \infty$. The old model would have predicted >98% effectiveness and near-instant overshoot — physically inconsistent with batch heating.

### 10.6 Fault Detection: From Duty-Cycle Thresholds to Physics-Based Alarms

An interim design considered alarming when P1's duty cycle exceeded twice its statistically expected value over a rolling window — rejected because P1's demand is legitimately bursty, making a duty-percentage threshold unable to distinguish a busy day from a fault.

**Proposal III** instead alarms on **observed heating/cooling rates versus what is physically achievable** given the coil's known delivery capacity and the tank's own computed loss rate — decoupling fault detection from duty-cycle bookkeeping entirely. Retained unchanged through the current revision; fully laddered, including live-mass-derived rate ceilings, in the companion PLC document.

### 10.7 Headline Result Basis

Proposal III's throughput and safety-margin figures were reported against the **single-branch, sequential water-use case only** (P1, P2, P3 never draw simultaneously). Simultaneous-branch operation was outlined qualitatively as a future direction but explicitly out of scope for that revision's quantitative results — Proposal IV implemented and quantified two-branch concurrency; the current revision implements and quantifies true three-way concurrency (Section 12).

---

## 11. Changelog: Proposal III → Proposal IV (Architectural Revision II — ADA)

This section documents the technical changes introduced by Architectural Revision II, in which the sequential single-branch architecture of Proposal III was replaced by the parallel, dual-branch **Adaptive Demand Allocation Architecture (ADA)**.

### 11.1 Trunk Upsize: Enabling Dual-Branch Flow

**Proposal III** used a 1-inch trunk main feeding 1-inch branches — structurally capable of serving only one branch at a time without starving it below design flow.

**Proposal IV** upsized the trunk main to **1.5-inch NPS**. Sized to run at ≈1.021 m/s, the 1.5-inch trunk delivered exactly 2× the flow of a single 1-inch branch at its normal 1.2 m/s design velocity — enough to serve **two branches simultaneously**, each at full individual design flow, without either being starved. When only one branch was active, the trunk simply throttled down to ≈0.508 m/s. No branch-level, coil, or tank-level hardware changed in this revision; it was a single-fitting-scale intervention with outsized downstream effect. The trunk bore introduced here (1.5-inch) is retained unchanged into the current revision, now operating under a different velocity cap and branch count (Section 12).

### 11.2 Priority Ladder → Need Array

**Proposal III's** sequential daily energy budget assumed only one branch could ever be active, so P1 and P2 were served first, in full, before P3 received any remaining time.

**Proposal IV** reframed arbitration as a **need array**: however many of P1/P2/P3 currently had live demand determined whether the trunk ran single-branch or dual-branch. When two processes were concurrently active, both were served in full via the upsized trunk rather than one waiting on the other. P1 remained unbounded and effectively guaranteed; P2 remained capped (Section 11.3); P3 was the remainder-absorbing tier, benefiting directly from dual-branch parallel operation whenever a second slot was free, modelled conservatively as a **48 branch-hour pool** (2 branches × 24 hr) minus P1's and P2's full raw duty duration. This two-branch need-array — including its "discard the lowest priority" three-way contention rule — is retired in the current revision in favour of genuine three-way concurrent service (Section 12.4).

### 11.3 PO Tank Governance: From Hard Cap to Operator-Trust Model

**Proposal III** capped P2 with a flat 10-minute arbitration window and a 5-minute hard limit.

**Proposal IV** replaced this with a **suspicion meter** ($S \in \{0,1,2,3\}$, resetting every 24 hours): sustained draw beyond the expected 500 kg/day escalated from an HMI confirmation prompt ($S{=}1$) through an alarm ($S{=}2$) to autonomous feed isolation with alarm ($S{=}3$) — the only point in this pathway that forces a shutoff — with a 5-minute no-HMI-response auto-increment to prevent the escalation stalling on operator inaction. Independently, a **soft-ceiling buffer** permitted draw up to 2× the operator-entered dispense quantity before issuing a warning; crossing it was manual-shutoff only. This suspicion-meter and soft-ceiling model is unchanged in the current revision; only the pulse-hold timer that originally accompanied it is retired (Section 12.5).

### 11.4 T5 Demand Basis and Worst-Case Loss Evaluation

**Proposal III** evaluated T5 against a 2 t/day throughput and its typical 42.5°C mid-band operating condition for the loss calculation.

**Proposal IV** doubled the T5 demand basis to **4 t/day**, reflecting the higher system-level throughput the dual-branch architecture then supported, and deliberately evaluated T5's standing loss at its **55°C dynamic upper thermal boundary** (the existing $T_f(x,y,m_p)$ safety limit) rather than the operating mid-band — a conservative worst-case stress test, not the typical daily figure. This 4 t/day basis and 55°C evaluation point are both retained unchanged into the current revision's P1 duty-period calculation (Section 12.3).

### 11.5 Dynamic, Demand-Driven Water Temperature

**Proposal III** held the water supply at a constant, fixed 70°C regardless of actual instantaneous demand.

**Proposal IV** derived the water target from real-time aggregate demand ($E_\text{total}=E_\alpha+E_5+E_{C^\ast}$, summed on a 10-second refresh window) via a two-point anchored proportional law:

$$T_\text{water} = 40 + \frac{70-40}{6.16}\,P = 40 + 4.87\,P\ [\text{kW}], \quad \text{clamped to } [40,70]°\text{C}$$

anchored at system idle ($P=0\to40°C$) and T5's own worst-case draw ($P\approx6.16\ \text{kW}\to70°C$). Solar and auxiliary supply were then gated purely on whether each could meet this dynamic target, rather than running to a fixed schedule. This control law is unchanged in the current revision, which adds an explicit peak-instantaneous-demand stress test on top of it (Section 12.6).

### 11.6 Load-Responsive Operating Modes

**Proposal III** had no load-responsive mode logic — P3 ran continuously whenever it held a branch.

**Proposal IV** introduced three operating postures for P3, governed by **T5's own live level** ($\alpha_S$) rather than tank temperature or T10 level: Eco Mode (≥90%), Efficiency Mode (90–50%), and Full Throttle (<50%) — the Full Throttle threshold deliberately matching the existing batch-release trigger, so the two mechanisms escalate together. Unchanged in the current revision.

### 11.7 Headline Result Basis Change

Proposal IV's throughput figures were reported against the **dual-branch, need-array case**, evaluated as a deliberately conservative floor. Combined system throughput rose to ≈5.42 t/day (≈271% of the original 2 t/day mandate), against Proposal III's ≈2.45 t/day (≈122%) — the entire gain attributable to the trunk upsize and need-array reframing described above, with no change to individual coil sizing. The current revision reports against a different, non-directly-comparable basis (Section 12.7).

---

## 12. Changelog: Proposal IV → System Overview (Revised) — True Three-Way Concurrency

This section documents the technical changes introduced by the current revision, in which the two-branch dual-priority architecture of Proposal IV is replaced by a genuine three-way concurrent arbiter across all three priorities.

### 12.1 Scope and Motivation

Architectural Revision II fixed the coil at 2-inch bore across every tank and allowed the need array to serve at most two branches at once. Two further hardware changes are introduced in this revision:

1. **Coil bore reduced to 1.5-inch across every tank** (T5, T10, PO), coil lengths unchanged (10 m for T5, 30 m for T10/PO).
2. **Branch valve count reduced from 8 to 6**, and the need array is expanded so that all three priorities can draw simultaneously, not just two — the trunk is capped at a safe 1.2 m/s rather than sized to guarantee every branch its individual full design flow under three-way concurrency.

The second change is the more consequential one architecturally: it retires the three-way "discard the lowest priority" contention rule from the prior PLC arbiter in favour of genuine three-way service, at a throttled flow rate, whenever all three priorities have live demand at once.

### 12.2 Revised Coil Geometry

| | T5 (10 m) 2-inch | T5 (10 m) 1.5-inch | T10/PO (30 m) 2-inch | T10/PO (30 m) 1.5-inch |
| :--- | :---: | :---: | :---: | :---: |
| $d_o$ (mm) | 60.33 | 48.26 | 60.33 | 48.26 |
| $d_i$ (mm) | 54.79 | 42.72 | 54.79 | 42.72 |
| Coil surface area (m²) | 1.895 | 1.516 | 5.685 | 4.549 |
| **Area change** | | **−20.0%** | | **−20.0%** |

### 12.3 Trunk Reconfiguration: True Three-Way Concurrent Flow

The 1.5-inch trunk (area 1.433 × 10⁻³ m²) is capped at its own safe rated velocity of 1.2 m/s:

$$F_\text{trunk} = 1.433\times10^{-3} \times 1.2 = 1.7196\times10^{-3}\ \text{m}^3\text{s}^{-1}$$

Under three-way concurrency, this splits three ways to ≈0.944 m/s per branch. Single- and dual-branch operation are **unaffected** — a single active branch or two active branches together still draw within the trunk's 1.2 m/s ceiling and continue to receive their full individual 1.2 m/s design rate exactly as in Architectural Revision II. The throttled regime applies only to the moment all three branches draw simultaneously.

Two of the three branches are now **permanently and continuously dedicated to T10 palm oil melting (P3)** — there is no longer a scenario in which P3 is fully idle. The third branch is shared between P1 (T5) and P2 (PO tank). The structural consequence: any time P1 or P2 has live demand, the trunk is necessarily supplying all three branches at once — **P1 and P2 never see the better single/dual-branch rate; they always operate under the throttled triple-branch condition.**

$$t_{P1} \approx 4.47\ \text{hr}\ (18.6\%), \qquad t_{P2} \approx 0.71\ \text{hr}\ (2.96\%)$$

$$t_\text{shared,active} \approx t_{P1} + t_{P2} - \frac{t_{P1}\times t_{P2}}{24} \approx 5.05\ \text{hr}\ (21.0\%)$$

### 12.4 Priority Ladder / Need Array → True Three-Way Concurrent Arbiter

**Proposal IV's** need array served at most two of the three destinations at once, resolving genuine three-way contention by discarding the lowest-priority demand.

**The current revision** retires that contention rule entirely. It is now obsolete: three-way contention is the trunk's *normal* operating condition whenever P1 or P2 is active, resolved by **flow-sharing** (all three branches throttled together), not by discarding a priority. The PLC arbiter becomes a genuine four-destination model (T5, TA, TB, TC competing for the trunk's three branches), with T5 and a designated, demanding PO tank guaranteed their slots and $S_\text{immediate}$ resolving four-way contention when it occurs (full ladder logic in the companion PLC document, Section 1.10).

### 12.5 PO Tank Governance: Pulse-Hold Timer Retired

**Proposal IV's** P2 block used a 20 s-on/60 s pulse-hold timer, designed to accommodate branch scarcity under the two-branch architecture.

**The current revision** retires this timer, not the governance model around it. Under the three-wide need array, PO demand can simply be served normally by the arbiter for as long as it remains live — there is no scarcity constraint left to justify throttling. Dispense stops and the demand flag clears on operator confirmation, not on a duty-cycled hold. The suspicion meter and soft-ceiling buffer (Proposal IV, Section 11.3) are otherwise unchanged.

### 12.6 Revised U-Values, NTU, and the Peak Instantaneous Demand Check

Reducing the bore to 1.5-inch drops delivered heat rate ($\varepsilon C_w$) by roughly 16–19% across every duty relative to the 2-inch baseline, tracking the 20% coil-area loss closely for T5 and T10 melt (both low-NTU). The PO tank, at meaningfully higher NTU, is structurally buffered and loses proportionally less. Moving from single/dual-branch to triple-branch flow, isolated from the bore change, costs under 2% further for every duty — the two effects are cleanly separable, and only the bore reduction is thermally expensive.

This revision adds a new check not present in any prior revision: the **worst-case simultaneous demand** across all three duties, evaluated at the single instant every process could plausibly draw its individual maximum at once (T5 at 40°C, PO tank at 24°C, both melting branches at the 36°C melt point — all necessarily in the throttled triple-branch regime since P1 and P2 are both active):

$$P_\text{peak} = Q_{T5,\max} + Q_{PO,\max} + 2\times Q_{T10,\max} \approx 5{,}048 + 21{,}602 + 9{,}957 \approx 36{,}607\ \text{W}\ (36.61\ \text{kW})$$

This exceeds the auxiliary array's rated 36 kW capacity by ≈1.7% — a genuine, if narrow, finding. It is a deliberately conservative, compounded worst case; the 300 L active thermal buffer would likely absorb a brief coincidence as a temperature dip rather than an outright shortfall, but the margin is worth an explicit check in the electrical design phase.

### 12.7 Headline Result Basis Change

| Metric | Architectural Revision II (2", 2-priority) | Current revision (1.5", 3-priority) |
| :--- | :---: | :---: |
| T5 duty period | 3.67 hr (15.3%) | 4.47 hr (18.6%) |
| PO tank duty period | 0.585 hr (2.4%) | 0.71 hr (2.96%) |
| P3 melt output | 4,919.8 kg/day | 4,453 kg/day (−9.5%) |
| Combined throughput | 5,419.8 kg/day | 4,953 kg/day (−8.6%) |
| Fulfilment (melt/combined) | 246% / 271% | 222.7% / 247.7% |
| Total daily thermal energy | 1,081.5 MJ | 990.7 MJ (−8.4%) |
| Average power demand | 12.5 kW | 11.47 kW (−8.2%) |
| Peak instantaneous demand | Not evaluated | 36.61 kW |
| Branch valve count | 8 | 6 |
| Max concurrent priorities | 2 | 3 |

The current revision's throughput figures are **not directly comparable** to Proposal IV's on a like-for-like basis: this revision trades coil area (bore reduction) and two fewer valves for a simpler, genuinely concurrent arbiter and a new peak-demand safety finding. The ≈8.6% combined-throughput reduction is spent almost entirely on the bore reduction, not on the concurrency expansion, which was thermally "free" (Section 12.6).

### 12.8 Open Item: Branch Flow Area Cross-Reference

The branch flow area used in the trunk-split calculation (6.069 × 10⁻⁴ m²) traces to the project's own hand-derived trunk/branch sizing notes; the base VCH proposal's original 1-inch supply pipe basis instead implies ≈5.575 × 10⁻⁴ m² (26.64 mm ID) — a ≈9% discrepancy. This affects only the reported branch velocity figure; every thermal result in this revision is derived from volumetric flow rate at the trunk split, which is unaffected. Worth reconciling against as-built pipe specification before commissioning.

### 12.9 Correction to an Earlier Working Figure

The PO tank's single/dual-branch U-value was previously stated as 128.7 W/m²K in intermediate working — an arithmetic slip. The correct value is 115.55 W/m²K, essentially identical to T5's own value. This affects only the single/dual-branch comparison row for the PO tank; all duty-period, throughput, and energy figures in Section 6 were already built from the correct triple-branch value.

---

## 13. PLC Implementation (Companion Document)

Full PLC ladder logic, register assignments, AI/DI/DO tables, safety gating, and every control block described architecturally above are documented in the companion document: **Adaptive Demand Allocation Architecture (ADA): PLC Implementation — Full Replacement** (MEPL, Sambridda Ranabhat). It is structured in dependency order — foundational blocks first, blocks that consume their outputs after — and includes:

- **Analog/Digital I/O** — 11-channel AI assignment (level, temperature, flow); X0–X10 digital inputs and Y0–Y25 digital outputs, confirmed against the panel's AutoCAD Electrical schematic (sheet 6 of 10).
- **Safety and Mode Control** — hardwired E-STOP caveat (IEC 60204-1), System OK flag, Automation Enable, and the manual/auto mutual-exclusion gating pattern used throughout.
- **Calculated Registers** — the 10 s refresh oscillator; the $T_\text{water}$ target law; the four-tier mode hysteresis ladder; the suspicion score; auxiliary staging; the consolidated $S_\text{immediate}$ tank scoring; and height-to-mass conversion (density back-derived to 957.0 kg/m³ from the base document's own full-tank figures).
- **$T_f$ Thermal Blending Register** — the 32-bit fixed-point ladder implementation of the dynamic upper thermal boundary, including the open item on $m_p$ acquisition.
- **P1/P2 Blocks and the Need-Array Arbiter** — now a genuine four-destination model (T5, TA, TB, TC) mapping directly to Section 12 above.
- **Fault Detection** — physics-based temperature rate-of-change alarms (using live mass, not fixed constants), activity-gated level/mass rate anomaly detection, and the T10 high-limit hard alarm.
- **Two Operator Interfaces** — the physical panel (E-STOP, Automation Enable/Disable, 4 manual pump buttons, Loop Exit) and the touchscreen HMI (PO tank designation, dispense entry, suspicion meter, mode indicator, fault stop/continue, diagnostics, trend logging).

All register addresses (D, T, M ranges) in the companion document are illustrative placeholders, chosen only to avoid collisions with each other — final addressing must be coordinated as one complete map before programming.

---

## Appendix: Engineering Notebook

High-resolution scans of scratchpad derivations, geometric helical coil layout constraints, and early PLC state-machine routing matrices are located in the `engineering_notes/` directory.
