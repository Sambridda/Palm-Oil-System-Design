# Palm Oil Melting & Retention System — Nebico

**Industrial thermal systems design and automation architecture for a multi-tank palm oil melting, storage, and trim-heating facility — Mechatronics Engineering Pvt. Ltd. (MEPL), Kathmandu.**

Grounded in the self-authored **VCH Sizing Framework (2nd Ed.)**, the system coordinates a passive solar thermal loop with an auxiliary electric immersion array through PLC automation to deliver demand-driven, high-efficiency process operations. The plant's control logic is formalised as the **Adaptive Demand Allocation Architecture (ADA)**.

> **Document History**
> | Document | Date | Status |
> | :--- | :--- | :--- |
> | Technical Proposal I | Prior to June 2026 | Archived — superseded |
> | Technical Proposal II | June 29, 2026 | Archived — superseded |
> | Technical Proposal III (Architectural Revision I) | July 10, 2026 | Archived — superseded |
> | Technical Proposal IV (Architectural Revision II — ADA) | July 12, 2026 | Archived — superseded |
> | ADA: System Overview (Revised) — True Three-Way Concurrency | July 16, 2026 | Archived — superseded |
> | **ADA Architecture 2.0.1** | **August 4, 2026** | **Current — For Review** |
> | **ADA: PLC Guide 1.1** (as-built companion) | **August 4, 2026** | **Current — For Review** |
> | **ADA: Thermodynamic Analysis** (worst/normal/best-case) | **July 25, 2026** | **Current — For Review** |
> | Ladder Logic (printed) | August 2026 | Current — For Review |
> | Electrical Schematic IV | August 2026 | Current — For Review |

The companion documents cover the following:

- **ADA Architecture 2.0.1** — Complete, self-contained description of the Automatic Dispatch Architecture as designed: the thermal control law for T5, heater staging, sensor filtering, tank scoring and selection, PO tank designation, oil-distribution scheme, dispense duration estimation, fault/E-Stop supervision, and operator override and information controls. Architecture only — physical I/O tags, ladder addresses, and PLC implementation detail are intentionally out of scope.
- **ADA: PLC Guide 1.1** — As-built documentation of the programmed ladder logic. A single walkthrough of the V1.0 baseline and all V1.1 changes, including: what changed and why, what each architecture open item resolved to in actual code, and a calibration register list of every constant currently standing in for a real, site-measured value.
- **ADA: Thermodynamic Analysis** — Worst, Normal, and Best-case evaluation of thermal throughput, coil power, solar coverage, and estimated savings under the full three-way-concurrent branch architecture. Uses the 2-inch coil bore / 1.2 m/s / 70°C constant supply basis from Architectural Revision II.
- **Ladder Logic** — Printed export of the complete PLC ladder as programmed. Source of truth for as-built program structure (2948 steps), used as the basis for the PLC Guide.
- **Electrical Schematic IV** — AutoCAD Electrical schematic, fourth revision. Sheet 6 of 10 confirms the I/O assignment cross-referenced in the PLC Guide.

---

## Table of Contents

1. [Industrial Mandate & Constraints](#1-industrial-mandate--constraints)
2. [Engineering Journey & Design Challenges](#2-engineering-journey--design-challenges)
3. [System Architecture](#3-system-architecture)
4. [ADA: Four-Scheduler Model](#4-ada-four-scheduler-model)
5. [Core Technical Deep Dives](#5-core-technical-deep-dives)
6. [The VCH Sizing Framework](#6-the-vch-sizing-framework)
7. [Headline Results & Validation Metrics](#7-headline-results--validation-metrics)
8. [Future Plan & Open Items](#8-future-plan--open-items)
9. [My Contributions](#9-my-contributions)
10. [Changelog: Proposal I → Proposal II](#10-changelog-proposal-i--proposal-ii)
11. [Changelog: Proposal II → Proposal III](#11-changelog-proposal-ii--proposal-iii-architectural-revision-i)
12. [Changelog: Proposal III → Proposal IV](#12-changelog-proposal-iii--proposal-iv-architectural-revision-ii--ada)
13. [Changelog: Proposal IV → System Overview (Revised)](#13-changelog-proposal-iv--system-overview-revised-true-three-way-concurrency)
14. [Changelog: System Overview → Architecture 2.0.1 & Companions](#14-changelog-system-overview-revised--architecture-201--companions)
15. [Appendix: Engineering Notebook](#appendix-engineering-notebook)

---

## 1. Industrial Mandate & Constraints

| Parameter | Specification |
| :--- | :--- |
| **Production Throughput** | ≥ 2 tonnes of fully processed liquid palm oil per day |
| **Thermal Transition** | Solid-state feedstock at 18.1°C (Kathmandu annual ambient) → 60°C stable liquid process target |
| **Hardware Scope** | Three 10 kL storage/melting vessels (one optionally dedicated to palm olein), one 5 kL trim-heating replenishment tank, passive solar thermal loop, 36 kW auxiliary electric immersion array |
| **Climate Factor** | Kathmandu solar reliability: **75.9% annually** |

---

## 2. Engineering Journey & Design Challenges

### Scope Misalignment: Production Window Clarification

The project initially proceeded under the assumption that the target throughput was 2 tonnes processed within a 4-hour window. The VCH methodology had not yet been extended to account for latent heat during phase change, causing the computed overall heat transfer coefficient ($U$) to appear unrealistically poor and prompting repeated proposals for mechanical agitation that the senior engineer consistently declined.

The misalignment was resolved through structured clarification. The 24-hour daily target reframing brought thermal performance figures within acceptable bounds and removed the need for agitation entirely.

**Takeaway:** Requirement ambiguity compounds downstream. Early, explicit clarification of the production window prevented a fundamentally over-specified design from proceeding to detailed engineering.

---

### Requirement Volatility Across Five-Plus Proposal Cycles

Between Proposal I and the current architecture, stated requirements changed substantially and more than once: the production window, supply/coil pipe cost preferences, a dedicated palm olein product line introduced mid-project, a trunk upsize that reopened priority logic, a coil bore reduction paired with a valve-count reduction, and multiple control-architecture revisions as the PLC implementation revealed gaps in the architecture documents.

Rather than treating each change as a disruption, the architecture was kept modular: the VCH thermal sizing methodology, the ε-NTU coil-length inversion, and the priority-budget control philosophy proved reusable across revisions, with each new requirement extending the existing framework rather than replacing it.

**Takeaway:** A multi-revision proposal history is a normal feature of iterative industrial design work done alongside a client still discovering their own requirements. The relevant discipline is not preventing requirement change, but architecting a system whose core methodology survives it. That discipline is reflected directly in the changelog structure of this document.

---

### Modbus Round-Robin Configuration: The Lowest Point

Implementing the satellite communication between the master PLC and the three destination HMIs via Modbus round-robin polling was the most difficult moment in the development phase. The challenge was not conceptual — the round-robin sequencer logic was straightforward once the structure was clear — but configurational. Without prior experience setting up Modbus across multiple Coolmay devices, every attempt to get the ADPRW instruction talking to the satellite stations failed silently or returned junk, with no obvious diagnostic path.

The breakthrough came from going directly to the source: contacting Coolmay's own engineer, who clarified the specific register and parameter configuration the protocol required. Once that was in hand, the round-robin sequencer (three stations, two ADPRW exchanges each, gated by timers T10–T61 and stepped by flags M0–M5) fell into place. The write-back exchange added in V1.1 — sending an acknowledgement back to each requesting satellite — was only possible because that initial configuration was correct.

**Takeaway:** Hardware-specific communication protocol configuration is rarely fully documented in the manual. When the datasheet runs out, the manufacturer's engineer is a legitimate engineering resource, not a last resort.

---

### Register Allocation: The Hidden Complexity of Memory Management

Distributing data coherently across the PLC's D, M, T, and counter registers — while simultaneously managing what the HMI reads from and writes to — proved more cognitively demanding than any single control block in the architecture. The difficulty was not any individual register assignment, but the cumulative effect of a large program: data written in one section was silently consumed in another three hundred steps later, and without a continuously maintained register map, tracking down a wrong value meant tracing the entire chain from sensor input to output.

The reconstructed register map in the PLC Guide (Section 5) exists because of this problem — it was built retrospectively from the ladder to serve as the reference the development phase lacked. The V1.1 addition of M115–M146 as the physical input mirror, for example, displaced the earlier speculative allocation of M40–M71 for that purpose — a collision that would have been caught immediately with a live map but only surfaced during the cross-reference exercise.

**Takeaway:** For any PLC program beyond a few dozen rungs, a register map is not documentation overhead — it is a development tool. Maintain it alongside the program from the first rung, not after the fact.

---

### Simplicity as an Engineering Decision

A recurring temptation throughout the architecture's development was to build the most complete, most faithful implementation of every specified mechanism. The fault detection system is the clearest example: the architecture specified twelve individually-adjustable, per-direction limit registers across all ten sensor channels — technically correct and fully covering every tunability case. The as-built implementation collapsed this to a single ratio-based check per channel, repeated ten times, with adjustable registers only on the four level channels where a bad reading has the most severe cascade consequences.

This was not a shortcut. It was a deliberate engineering trade: simpler logic has fewer places to hide a bug, fewer registers for a commissioning technician to misconfigure, and a fault behaviour that can be explained in one sentence rather than twelve. The same philosophy drove the simplification of the oil-line fault path — no escalation, no auto-stop, just a flowmeter and an operator — and the consolidation of the two-block tank-scoring system ($S_\text{casual}$ / $S_\text{immediate}$) into a single formula.

**Takeaway:** Complex systems are efficient. Reliable systems are functional. When the two are in tension, the system that a commissioning engineer can verify in an afternoon is worth more than the system that is theoretically optimal on paper.**
---

### The A.A / A.B / B.A / B.B Case Matrix

Cost pressure from the senior engineer introduced a preference for 1-inch NPS pipe while sizing was developed around 1.5-inch. Rather than selecting arbitrarily under an unresolved production window, all four permutations of supply/coil NPS were calculated in full and published for transparency. This four-case matrix was progressively resolved across later revisions (see changelogs).

---

### Challenging the Water-Side Velocity Assumption

Modelling the two-phase overall heat transfer coefficient revealed that the outer oil-side thermal resistance accounts for over **95%** of total system impedance — meaning increasing water velocity through the coil produces negligible change in overall melting rate. This finding redirected the design from mechanical optimisation toward **algorithmic throughput recovery**: orchestrating a smarter, time-staggered multi-tank queue to bypass single-tank thermodynamic limits.

This philosophy extended, in Proposal IV, to a dual-branch trunk serving two processes in parallel, and in the current architecture to true three-way concurrent service across all branches.

---

### From a Shared Queue to a Dedicated Palm Olein Tank

One T10 vessel was carved out as dedicated palm olein storage. Palm olein solidifies at ≈24°C and needs comparatively little energy to stay liquid — leaving it in the shared rotation would have distorted the tank-scoring system's assumptions. The fix required an **oil-side restructuring**: each T10 gets its own dedicated oil pump and feed line, gated by a manual ball valve in series with an automated control valve. The water/hydronic heating circuit itself was unchanged.

---

### A Three-Way Priority Ladder, Then a Need Array, Then True Concurrency

Introducing the PO tank required a third priority tier (P1 T5 trim-heat, P2 PO maintenance, P3 T10 melting). A strict lockout was rejected in favour of a sequential daily energy budget. Proposal IV reframed this as a parallel need array with dual-branch flow; the System Overview (Revised) expanded it to genuine three-way concurrent service. Architecture 2.0.1 finalises this model — see [Section 4](#4-ada-four-scheduler-model) and [Section 14](#14-changelog-system-overview-revised--architecture-201--companions).

---

### From Architecture Specification to As-Built Documentation

The PLC Guide 1.1 documents the gap between the architecture specification and the ladder as it was actually programmed. The most consequential simplification: the architecture's 12-register per-channel, per-direction fault-detection design was replaced by a simpler ratio-based check — one pattern repeated ten times. Only the four level channels (T5, TA, TB, TC) received adjustable registers in V1.1 (D500–D514); the six temperature channels remain hardcoded. This is explicitly a deliberate first-commissioning trade: simpler logic is easier to verify and less likely to hide a bug at the cost of per-direction tunability on temperature channels.

---

## 3. System Architecture

> **P&ID III** (mechanical engineer's latest Piping & Instrumentation Diagram) is the current authoritative process-routing reference. The original Process Flow Diagram is retained for historical context only.

Each of the three T10 tanks has its own **dedicated oil pump and feed line**, with one T10 optionally designated as the **PO tank** — isolated from the melting rotation and dispensed only via operator-triggered logic. On the hydronic side, the trunk main is **1.5-inch NPS**. Two branches are permanently and continuously dedicated to T10 palm oil melting (P3); the third branch is shared between T5 (P1) and the PO tank (P2). Water allocation is arbitrated by the **ADA need array** — a genuine three-way concurrent arbiter, not a sequential lockout.

Branch valve count is **6** (down from 8). Coil bore across every tank is **1.5-inch NPS** (down from 2-inch in Architectural Revision II). The architecture is governed by a **four-scheduler model** described in Section 4.

---

## 4. ADA: Four-Scheduler Model

Architecture 2.0.1 formalises the control system as exactly four functional schedulers — a conceptual grouping that clarifies which kind of job each block is doing, not a physical or programmatic boundary.

**Operational Scheduler** — Reads sensors and drives outputs. Solar routing, heater output state, branch valve state, X/Y/Z destination valve routing, and the dispense pump all live here. This scheduler *acts on decisions made elsewhere*; it does not make them. When Automation Mode is not selected, the three CP speed outputs can be driven from a dedicated panel input set, subject to the same E-Stop gating as the automatic path.

**Priority Scheduler** — Decides who gets served, across two fully independent domains. On the water side: the Need Array and its trigger-count-to-state mapping, tank scoring and the incumbent/challenger switching rule, and PO tank designation. On the oil side, entirely separately: the FIFO queue across X/Y/Z, gated only by the plant-wide System-OK condition. Water-side assignment can be held off entirely on operator command without stopping the system.

**Mathematical Core** — Computes the numbers the other three schedulers consume: the level division register, $T_\text{target}(d)$, heater-count lookup and both anti-chatter latches, sensor averaging, $T_f$, the P2 heat-demand function, and the oil-line pump runtime estimate. Nothing in this scheduler drives an output or arbitrates contention directly.

**Fault Scheduler** — Keeps the system safe and stops it when it isn't. Physical and Virtual E-Stop, the System-OK condition, and Trend Threshold Supervision all live here. The oil line has no fault path of its own by design — it is gated only by System-OK and the operator's oil-line disable, like every other output.

> **Critical design decision:** The oil line and water line **do not share decision logic**. The Need Array, tank scoring, and PO tank designation govern water only. Oil distribution runs on its own trigger (F2) and its own flowmeter-confirmed completion signal. The two systems share only the plant-wide System-OK condition.

---

## 5. Core Technical Deep Dives

### Multi-Phase Thermal Modeling

External natural convection profiles for the uninsulated vessels were constructed using:

- **Vertical tank walls** — Churchill-Chu correlation
- **Horizontal surfaces** — Morgan-McAdams plate equations
- **Internal coil fluid dynamics** — Gnielinski correlation with Kubair-Kuloor enhancements for helical geometries

This approach isolated a **1.07 kW** hold-phase thermal loss profile (melt phase, uninsulated T10).

### Thermal Control Law: $T_\text{target}(d)$

Rather than a fixed water supply temperature or a two-point anchored linear law, Architecture 2.0.1 derives the water target from T5's level in real time via a closed-form, three-region function:

$$T_\text{target}(d) = \begin{cases} 70 & d < 200 \\ 70 - \dfrac{3}{2560}(d-200)^2 & 200 \leq d < 360 \\ 40 & d \geq 360 \end{cases}$$

where $d = \text{height(mm)}/5 \in [0, 400]$ is the level division register ($d{=}200$ is 50% full, $d{=}360$ is 90% full). Below half-full, T5 is heated aggressively to 70°C. Between 50% and 90% full, the target tapers quadratically — steepest where the most heater capacity is still engaged, flattening as fewer heaters remain active. Above 90% full, the target drops to a 40°C holding value.

Continuity is confirmed at both knots. Solar assist is gated off the same function — no separate solar temperature target.

### Heater Staging: Dual-Latch Anti-Chatter

Three heater elements (12 kW each) are staged from level alone. The active band (50–90% full, d = 200–360) is split into three equal thirds, one heater dropping per third. Two independent latches prevent chatter:

- **Rounding latch** — when the tank is filling and a heater decrease nominally triggers, that decrease is held until d reaches a slightly higher buffer point (e.g., 3→2 heaters holds until d = 260 rather than 253). Filling direction only.
- **Comfort latch** — independent of the rounding latch. Governs when measured temperature actually permits cutting heat. For $T_\text{target}$ between 65–70°C, waits until θS reaches 70°C; for lower targets, waits until θS reaches $T_\text{target}+5$°C.

Both latches must clear before any change to heater state.

### Dynamic Upper Thermal Boundary ($T_f$)

The PLC continuously evaluates:

$$T_f(x,\, y,\, m_p) = \frac{239.53\, x + m_p\, y}{239.53 + m_p}$$

where $x$ is the water/steel structure temperature, $y$ is the palm oil temperature, and $m_p$ is the estimated remaining oil mass. When $T_f > 55°C$, an interlock triggers. Derived from $K = m_w c_w + m_{ss} c_{ss} \approx 479{,}060\ \text{J/°C}$ for the combined thermal capacitance; dividing through by 2000 gives the compact register-friendly form above. Confirmed exactly in the ladder at constant E239.53.

### Sensor Averaging

Raw analog readings are shown live on HMI displays. Everything feeding a calculation consumes a **5-second block-averaged value** — a five-sample rolling average that refreshes once every 5 seconds and holds steady between updates — to reject transient spikes from oil movement. Ten channels filtered in total: four level channels (T5, TA, TB, TC) and six temperature-derived channels. The same ten channels are what Trend Threshold Supervision watches.

### Tank Scoring and Selection

A single scoring formula is used for all ranking decisions:

$$\text{score} = 0.6\,\alpha + 0.4\,\theta$$

where $\alpha$ is the tank's level and $\theta$ its temperature. The switching rule depends on how many T10 tanks are eligible:

- **Three eligible (no PO tank designated):** highest-scoring tank wins; a challenger displaces the incumbent only once $\text{score}_\text{incumbent} \leq 0.5 \times \text{score}_\text{challenger}$. Optimises for throughput — finish the closest tank fastest.
- **Two eligible (a PO tank designated):** lowest-scoring tank wins; the other candidate displaces it only once it falls to $0.5\times$ the incumbent's score. Optimises for urgency — don't let the neediest tank fall further behind.

A score floor is enforced in both cases to prevent the inverted 0×0 comparison failure.

### PO Tank Demand Function

The PO tank's heat demand ($D_\text{PO}$, in seconds of pump runtime required) is a piecewise calibration-constant structure conditioned on phase:

$$D_\text{PO}(\theta_\text{tank}, m_\text{tank}, \theta_w) = \begin{cases} C_\text{cal,melt} \cdot A & \theta_\text{tank} < \theta_\text{melt} \\ C_\text{cal,liquid} \cdot B & \theta_\text{melt} \leq \theta_\text{tank} < \theta_\text{target} \\ 0 & \theta_\text{tank} \geq \theta_\text{target} \end{cases}$$

The two calibration constants ($C_\text{cal,melt}$, $C_\text{cal,liquid}$) are tuned at commissioning against real equipment behaviour — not hard-coded from first principles — so the demand check remains accurate as conditions drift over the installation's lifetime. A **demand watchdog timer** clears a stale P2 flag if demand never resolves, preventing a single unresolved condition from permanently occupying a Need Array slot.

### Oil Distribution

Oil can be dispensed to three destinations (X, Y, Z), each with its own satellite HMI. Key design decisions:

- **Single-destination, full-flow dispensing only** — no splitting or throttling between destinations.
- **Hardware FIFO (SFWR/SFRD)** — requests served strictly in arrival order. No manual ring buffer.
- **Flowmeter-confirmed completion** — the flowmeter is the sole authority on when a dispense ends; no timer-based cutoff. No fault path on the oil line by design.
- **Prime function** — each destination can isolate its line and manually run the pump to clear residual oil before a metered dispense.
- **Pump runtime estimate** — computed for HMI display only (estimated time remaining), never used as a completion signal. Calibration constants tuned at commissioning using a viscosity-temperature correction via DEXP exponential instruction.
- **Request acknowledgement and cancellation** — a handshake returns to each satellite on request receipt; cancellation clears the computed dispense amount to zero.

### Fault Supervision

Trend Threshold Supervision watches all ten filtered sensor channels at the same 5-second cadence as averaging. Each channel's current filtered value is compared against its own previous-cycle value; both a high-side and low-side ratio check are run. The architecture originally specified twelve individually-adjustable registers across all channels; the as-built design simplifies to:

- **Channels 1–4 (level channels T5, TA, TB, TC):** adjustable high-side (D500, D502, D504, D506) and low-multiplier (D508, D510, D512, D514) registers, tunable from V1.1 onward.
- **Channels 5–10 (temperature channels):** fixed K2/K1 constants. Whether these warrant their own adjustable registers is left as a commissioning decision.

Tunability is asymmetric by design: a bad level reading cascades into mass, into $T_f$, into tank scoring, and into priority decisions — the knock-on effects are immediate and can be severe. A temperature channel drifting is comparatively low-consequence over these timescales.

### Batch-Side Modelling Correction: $C_\text{min} = C_w$

Under the individualised-feed, batch-heated architecture, each tank is a well-mixed batch whose bulk temperature changes slowly relative to one coil pass — so water is $C_\text{min}$ and tank contents behave as $C_\text{max} \to \infty$ over one pass. All NTU calculations from Proposal III onward use:

$$NTU = \frac{UA}{C_w}, \quad \varepsilon = 1 - e^{-NTU}, \quad Q(T_\text{tank}) = \varepsilon\, C_w\, (T_\text{hot} - T_\text{tank})$$

---

## 6. The VCH Sizing Framework

This system is a full-scale industrial deployment of the **VCH Sizing Framework (2nd Edition)** — a methodology authored specifically for submerged hydronic coil thermal systems. The project served as a definitive verification platform, confirming that unifying coil heat transfer modelling with multi-phase thermal boundary calculations produces highly predictable, field-resilient industrial designs.

**DOI:** [10.5281/zenodo.21009246](https://doi.org/10.5281/zenodo.21009246)

---

## 7. Headline Results & Validation Metrics

### Current: Thermodynamic Analysis (Worst / Normal / Best Case)

Evaluated under the 2-inch coil bore / 1.2 m/s / 70°C constant supply basis (Architectural Revision II hydraulics), full three-way concurrent branch architecture. The three scenarios represent cold-start + cold-snap (Worst), Kathmandu weighted-average ambient and feedstock (Normal), and continuous-operation residual-heat feedstock (Best):

| Metric | Worst | Normal | Best |
| :--- | :---: | :---: | :---: |
| **T5 duty period** | 4.70 hr (19.6%) | 4.03 hr (16.8%) | 3.64 hr (15.2%) |
| **PO tank duty period** | 0.91 hr (3.8%) | 0.45 hr (1.9%) | **0.00 hr** |
| **Palm oil melted** | 5,457.8 kg/day | 5,439.3 kg/day | 5,490.8 kg/day |
| **Fulfilment vs. 2 t/day mandate** | **≈ 273%** | **≈ 272%** | **≈ 275%** |
| **Total daily energy demand** | 1,247.5 MJ | 1,173.6 MJ | 1,133.6 MJ |
| **Average coil power** | 14.44 kW | 13.58 kW | 13.12 kW |
| **Solar (FPC) coverage of demand** | 6.45% | 9.15% | 9.46% |
| **Estimated annual savings (NPR, FPC)** | 75,125 | 100,243 | 100,094 |

**Key findings from the Thermodynamic Analysis:**

- **Throughput variance across all three conditions is under 1%.** Despite worst case carrying the largest specific energy per kg (218 kJ/kg vs. 152 kJ/kg for best case) and the smallest melting window, these penalties largely offset each other — worst-case output (5,457.8 kg/day) is 99.4% of best case (5,490.8 kg/day).
- **Best case genuinely requires zero PO tank duty.** Starting at 35°C, palm olein is already above its 30°C target before any heat is applied. This is a real load-bearing finding, not a simplification.
- **Solar coverage is now 6.4–9.5% (FPC)**, substantially lower than the 40–61% figures reported in earlier revisions. Two compounding causes: the FPC array is smaller (10 panels, 19.0 m², vs. 15 panels / 22.674 m² in the base document), and total daily demand under the full three-way-concurrent throughput basis (1,134–1,248 MJ/day) is roughly 2–3× larger than earlier revisions were evaluated against. This is a direct, honest consequence of maximising throughput.
- **ETC is the more efficient collector at every condition.** At 53–58% efficiency vs. 34–45% for FPC, ETC only needs to win on cost by a margin of $c_\text{ETC}/c_\text{FPC} \leq \eta_\text{ETC}/\eta_\text{FPC} \approx 1.28$–$1.57$ for it to also win on ROI. This is the single number needed once both unit costs are priced.
- **The savings estimate is directional, not final.** The tariff used (≈ NPR 9.21/kWh) is Nepal Electricity Authority's general industrial/business rate, not this facility's actual metered rate.

### Archived: System Overview (Revised) — True Three-Way Concurrency (1.5" bore, 6 valves)

| Metric | Result |
| :--- | :---: |
| **Palm oil melted per day (P3)** | ≈ 4,453 kg/day |
| **Combined system throughput (P3 + PO tank)** | ≈ 4,953 kg/day |
| **Fulfilment vs. 2 t/day mandate (melt / combined)** | ≈ 222.7% / ≈ 247.7% |
| **Peak instantaneous demand (worst case)** | ≈ 36.61 kW (≈1.7% over 36 kW rated array) |
| **Branch valve count** | 6 |

### Archived: Proposal IV (Architectural Revision II — 2" bore, 8 valves, dual-branch)

| Metric | Result |
| :--- | :---: |
| **Palm oil melted per day (P3)** | ≈ 4,919.8 kg/day |
| **Combined system throughput** | ≈ 5,419.8 kg/day |
| **Fulfilment vs. 2 t/day mandate (melt / combined)** | ≈ 246% / ≈ 271% |

### Archived: Proposal III (Architectural Revision I — single-branch)

| Metric | Result |
| :--- | :---: |
| **Palm oil melted per day** | ≈ 2,447 kg/day |
| **Fulfilment vs. 2 t/day mandate** | ≈ 122% |

### Archived: Proposal II

| Metric | Design Target | Primary (75°C HTF) | Worst-Case (70°C HTF) |
| :--- | :---: | :---: | :---: |
| **3-tank staggered capacity** | ≥ 2.0 t/day | **6.0 t/day** | **6.0 t/day** |
| **Required coil length (1.5" bore)** | ≤ 90 m | **48.3 m** | **55.6 m** |

### Archived: Proposal I

| Metric | Design Target | Primary | Worst-Case |
| :--- | :---: | :---: | :---: |
| **Daily Plant Throughput** | ≥ 2.0 t/day | **24.23 t/day** | **20.48 t/day** |
| **Single-Tank Safety Factor** | 1.0× | **3.63×** | **2.42×** |

---

## 8. Future Plan & Open Items

### Architecture Open Items (carried from System Overview Revised and Architecture 2.0.1)

- Mode thresholds (Eco/Efficiency/Standard boundaries) remain provisional and may be adjusted at commissioning once live plant behaviour is observable. The 50% Full Throttle line is fixed by the existing batch-release trigger; other boundaries are not yet locked.
- Rounding latch asymmetry (draining direction not yet specified — assumed to use plain nominal boundaries with no buffer): confirm this is intentional before finalising.
- Branch flow area cross-reference: the branch flow area used in trunk-split calculations (6.069 × 10⁻⁴ m²) traces to project hand-derived sizing notes; the base VCH proposal's 1-inch supply pipe basis implies ≈5.575 × 10⁻⁴ m² — a ≈9% discrepancy affecting only reported branch velocity figures. Reconcile against as-built pipe specification before commissioning.
- PO tank insulation remains the highest-leverage, lowest-capital efficiency gain — its uninsulated loss outweighs its sensible heating duty roughly 7:1, and every megajoule saved returns directly to P3's melting window.
- The ≈36.61 kW peak instantaneous demand finding (≈1.7% over the 36 kW rated auxiliary array) should be carried explicitly into electrical design.

### PLC Open Items (from PLC Guide 1.1)

- E-STOP latch reset source not yet defined.
- Behaviour on a mid-operation switch from Automation Enabled to Disabled (abrupt stop vs. complete-current-step) not yet decided.
- Tie-break on equal $S_\text{immediate}$ scores currently defaults to execution order (TA-favoured); flagged for confirmation, not an explicit design decision.
- $D_\text{Mode}$ power-up default not yet specified.
- Whether the six temperature channels (5–10) should eventually get their own adjustable threshold registers (like channels 1–4) or remain fixed at K2/K1 is an open commissioning decision.
- T130 (PO-melt-demand reset timer) preset value is not present in the current program export — role confirmed, value still TBD.
- Write-back exchange to D550 payload meaning is not fully clear from the ladder alone; worth tracing through properly before commissioning.

### Calibration Items (from PLC Guide 1.1 — values requiring site-measured data)

| Location | Constant(s) | What's needed |
| :--- | :--- | :--- |
| Water Temperature Target Core | K200, K360 | Real level-range measurement at commissioning (50% / 90% of usable height) |
| Height-to-Mass Conversion | K1 (×4 channels) | Real height-to-mass factor per tank from geometry and product density |
| PO Melting Timer | E135, E30 | Check against actual palm-oil product phase-temperature specification |
| Heater Latching | K55, K80, K95, K85, K70, K45 | Confirm comfort/staging bands against actual tank and product |
| Heater Latch stability gate | T5/T6, E1 ratio threshold | Adjust once real sensor noise characteristics are known |
| Fault Analysis channels 5–10 | K2/K1 | Decide whether to registerise or leave fixed |
| AODD Pump | K30 threshold | Confirm against real tank levels and temperatures |
| Oil write-back exchange | T12/T13/T14 (K30 timeout) | Confirm against actual Modbus round-trip time to satellites |

### Electrical Design

Detailed electrical system design in AutoCAD Electrical (Electrical Schematic IV, 10 sheets) is complete after several iterations, informed by the peak instantaneous demand finding from the System Overview (Revised). Sheet 6 of 10 is the confirmed I/O assignment cross-referenced by the PLC Guide.

### Controls Architecture

Formal review of the ADA framework — including the current four-scheduler model and three-way concurrent arbiter — with the senior engineer is pending. The architecture has not yet been formally reviewed.

### Instrumentation

Full sensor schedule (selection, specification, and placement of temperature, level, and flow instruments across all four tanks and the solar loop) is complete, cross-referenced against the 11-channel analog input assignment in the PLC Guide.

### HMI (Remaining)

HMI design for operator visibility, PO-tank designation/dispense workflow, suspicion-meter status display, mode indicator, and manual override capability.

### Hydraulics & Pump Selection

Head loss calculations for the coil circuits and the single-pump solar/primary loop. Deferred until site plumbing routing is confirmed. Pump selection sized for three-way-concurrent worst-case simultaneous draw.

---

## 9. My Contributions

This project was undertaken as a Junior Automation Design Architect during an internship at MEPL, working under the direction of the senior project lead.

**Thermal Sizing & Proposal Authorship** — All thermal calculations, coil sizing, the A.A/A.B/B.A/B.B case matrix (Proposal I); unified 1-inch supply bore sweep (Proposal II); fixed 2-inch bore, individualised-feed, and three-tier priority architecture (Proposal III); dual-branch trunk, need-array reframing, and ADA demand functions (Proposal IV); 1.5-inch bore reduction, six-valve reconfiguration, and true three-way concurrency analysis (System Overview Revised); architectural consolidation and thermal control law revision (Architecture 2.0.1); worst/normal/best-case thermodynamic scenario analysis (Thermodynamic Analysis). All grounded in the self-authored VCH Sizing Framework (2nd Ed.).

**PLC Implementation** — Full ladder logic program (as-built, 2948 steps): I/O mapping, register map, safety gating, sensor averaging, thermal control law, heater staging, dynamic thermal boundary, tank scoring, need-array arbiter, oil distribution FIFO, fault supervision, and operator HMI interfaces. Documented in the companion PLC Guide 1.1. This architecture has not yet been formally reviewed with the senior engineer.

**Process Architecture** — Single-pump solar feedback loop topology; individualised T10 oil-feed restructuring; PO tank isolation logic; P1/P2/P3 priority architecture across its sequential-budget (Proposal III), dual-branch need-array (Proposal IV), true three-way concurrent (System Overview Revised), and four-scheduler (Architecture 2.0.1) forms; demand-driven dynamic water temperature control law; Eco/Efficiency/Full Throttle mode logic; oil distribution independence principle.

**Tank Geometry (Collaborative)** — Initial vessel proportions and aspect ratio estimates produced as part of thermal sizing work. Detailed manufacturable geometry and SolidWorks verification completed by the team's mechanical engineer.

**PFD vs. P&ID** — The original Process Flow Diagram is now superseded. P&ID III (mechanical engineer's latest revision) is the current authoritative process-routing reference. The oil distribution port (X/Y/Z) logic is confirmed directly against P&ID III.

**Note:** The project is ongoing. Physical commissioning, HMI development, and hydraulics/pump selection are planned for subsequent phases.

---

## 10. Changelog: Proposal I → Proposal II

### 10.1 Supply Pipe Simplification

**Proposal I** evaluated two supply pipe sizes (1-inch and 1.5-inch NPS), producing a 2×2 case matrix (A.A, A.B, B.A, B.B). **Proposal II** standardises on a single 1-inch Schedule 40 CPVC supply pipe, eliminating the supply pipe as a variable. The oil-side resistance dominates at >95% of total impedance regardless; the case matrix collapses to a single-axis coil bore sweep (1", 1.25", 1.5", 2").

### 10.2 Coil Sizing: Inverted Design Logic

**Proposal I** fixed the coil at its 90 m geometric ceiling and solved for throughput. **Proposal II** inverts this: a heat-duty target $Q_\text{target} = Q_\text{batch} + Q_\text{loss,max} = 4.30 + 4.87 = 9.17\ \text{kW}$ is defined from the mandate and worst-case standing loss, and the minimum coil length is solved in closed form via the ε-NTU inversion for a $C_r = 0$ heat exchanger. Recommended design point: **1.5-inch coil at L ≈ 56 m** — a 38% reduction from the original 90 m specification.

### 10.3 Melt Time and Safety Factor Basis

Proposal II sizes to the daily mandate floor (24-hour melt for 2 t at $Q_\text{batch}$), so the single-tank margin is 1.0× by construction. The 3× system-level margin is recovered from running all three T10 tanks staggered (3 × 2 t = 6 t/day).

### 10.4 T5 Coil Sizing Quantified

Even the smallest bore (1-inch) requires only ≈5.8 m of coil against a 65 m geometric ceiling — under 9% utilisation. T5 is not capacity-limiting under any evaluated scenario.

---

## 11. Changelog: Proposal II → Proposal III (Architectural Revision I)

### 11.1 Shared Oil Feed → Individualised Oil Feed

A single shared oil feed pipe across the three T10 tanks was replaced with an **individualised feed per tank** — each vessel gets its own dedicated oil pump and feed line, gated by a manual ball valve in series with an automated control valve. The water-side hydronic circuit is unchanged. This oil-side restructuring is the structural prerequisite for designating one tank as a dedicated palm olein store.

### 11.2 New Tank Class: The PO Tank

One T10 tank may be designated via HMI as a dedicated palm olein store — automatically excluded from the P3 melting rotation, manually hard-isolated, and dispensed only through operator-triggered HMI pulse logic.

### 11.3 Two-Tier → Three-Tier Priority Architecture

A three-way ladder — **P1 (T5 trim-heat), P2 (PO tank maintenance), P3 (T10 melting)** — resolved by a **sequential daily energy budget**: P1 and P2 take their computed duty periods first; P3 receives whatever remains of the 24-hour window.

### 11.4 Coil Bore: From Swept Variable to Fixed Spec

**Proposal II** swept coil bore across four NPS options. **Proposal III** fixes bore at **2-inch NPS Sch. 10S** across every tank (T10, PO, T5), coil length at 30 m (T10/PO) and 10 m (T5), water supply fixed at 70°C, feed velocity reduced to 1.2 m/s.

### 11.5 NTU Model Correction: $C_\text{min} = C_w$

Under the batch-heated architecture, water is $C_\text{min}$. The old throughput-rate model for T5 would have predicted >98% effectiveness — physically inconsistent with batch heating.

### 11.6 Fault Detection: From Duty-Cycle to Physics-Based Alarms

Alarming on observed heating/cooling rates versus what is physically achievable given the coil's known delivery capacity and the tank's own computed loss rate — decoupling fault detection from duty-cycle bookkeeping.

---

## 12. Changelog: Proposal III → Proposal IV (Architectural Revision II — ADA)

### 12.1 Trunk Upsize: Enabling Dual-Branch Flow

Trunk main upsized from 1-inch to **1.5-inch NPS**, running at ≈1.021 m/s. This delivered exactly 2× the flow of a single 1-inch branch at its 1.2 m/s design velocity — enabling **two branches simultaneously**, each at full individual design flow.

### 12.2 Priority Ladder → Need Array

Sequential daily energy budget replaced by a **parallel need array**: however many of P1/P2/P3 had live demand determined whether the trunk ran single- or dual-branch. All active processes were served in full rather than one waiting on the other.

### 12.3 PO Tank Governance: From Hard Cap to Operator-Trust Model

A flat 10-minute arbitration window replaced by a **suspicion meter** ($S \in \{0,1,2,3\}$, resetting every 24 hours), escalating from HMI confirmation prompt ($S=1$) through alarm ($S=2$) to autonomous feed isolation ($S=3$). Independently, a **soft-ceiling buffer** permitted draw up to 2× the operator-entered quantity before issuing a warning.

### 12.4 Dynamic, Demand-Driven Water Temperature

Fixed 70°C supply replaced by a real-time demand-derived target (two-point anchored proportional law, anchored at system idle → 40°C and T5's own worst-case draw → 70°C). Solar and auxiliary supply gated on whether each could meet this dynamic target.

### 12.5 Load-Responsive Operating Modes

Three operating postures governed by T5's live level ($\alpha_S$): **Eco Mode** (≥90%), **Efficiency Mode** (90–50%), **Full Throttle** (<50%) — the Full Throttle threshold matching the existing batch-release trigger.

---

## 13. Changelog: Proposal IV → System Overview (Revised) — True Three-Way Concurrency

### 13.1 Coil Bore Reduced: 2-inch → 1.5-inch

Bore reduced across every tank (T5, T10, PO), coil lengths unchanged (10 m for T5, 30 m for T10/PO). Coil surface area loss: **−20.0%** across all tanks. Delivered heat rate drops 16–19%, tracking the 20% area loss closely for the low-NTU duties.

### 13.2 Branch Valve Count Reduced: 8 → 6

Two T10 branches are now permanently and continuously dedicated to P3; the third branch is shared between P1 (T5) and P2 (PO tank).

### 13.3 Three-Way Concurrent Arbiter

The trunk (capped at 1.2 m/s) serves all three branches concurrently by throttling flow — no priority is discarded under three-way contention. Whenever P1 or P2 has live demand, P3 is necessarily also active (it always holds its two branches), so three-way contention is the trunk's normal operating condition under any P1/P2 activity.

### 13.4 PO Tank: Pulse-Hold Timer Retired

The 20 s-on/60 s pulse-hold timer (designed for branch scarcity under the two-branch architecture) is retired. Under the three-wide need array, PO demand is served normally for as long as it remains live.

### 13.5 Peak Instantaneous Demand Check

New in this revision: worst-case simultaneous demand across all three duties at their individual coldest/highest-draw conditions:

$$P_\text{peak} = Q_{T5,\max} + Q_{PO,\max} + 2 \times Q_{T10,\max} \approx 36.61\ \text{kW}$$

This exceeds the auxiliary array's rated 36 kW by ≈1.7% — a narrow, conservative, compounded worst-case finding carried into the electrical design phase.

---

## 14. Changelog: System Overview (Revised) → Architecture 2.0.1 & Companions

### 14.1 Architecture 2.0.1: Consolidated Specification

Architecture 2.0.1 is the first document that describes the ADA as *designed* rather than as *revised from the previous revision*. It introduces the **four-scheduler model** (Section 4 above) as a unifying conceptual framework, consolidates all control logic into one self-contained reference, and deliberately separates architecture from implementation — physical I/O tags and ladder addresses are intentionally out of scope.

### 14.2 Thermal Control Law Formalised: $T_\text{target}(d)$

Architecture 2.0.1 replaces the prior two-point anchored proportional law with the closed-form quadratic $T_\text{target}(d)$ — a direct, level-to-temperature function requiring no energy summation and no dynamic power evaluation. This allows the Mathematical Core to produce a water supply target in one lookup, not in a multi-step calculation. Continuity confirmed analytically at both knots.

### 14.3 Heater Staging Formalised: Dual-Latch Model

The prior architecture specified heater staging against level bands but did not formalise an anti-chatter mechanism. Architecture 2.0.1 introduces and specifies both the **rounding latch** (filling direction, holds off count-decrease until a buffer level is reached) and the **comfort latch** (temperature-driven, holds off count-decrease until the tank is genuinely warm enough) as independent, co-required conditions.

### 14.4 PO Tank Demand Function: Piecewise Calibration Structure

Earlier revisions described the PO tank's heat demand qualitatively. Architecture 2.0.1 specifies it as a piecewise function with independent calibration constants for the melting and liquid phases, paired with a **demand watchdog timer** that prevents a single unresolved demand from permanently occupying a Need Array slot. The exact combining functions and thresholds are left to commissioning calibration, not first-principles derivation.

### 14.5 Tank Scoring: Single Formula, Inversion Rule Formalised

Earlier revisions used two separate scoring formulas ($S_\text{casual}$ and $S_\text{immediate}$). Architecture 2.0.1 unifies these into a single formula (0.6α + 0.4θ) with an **inversion rule** for the two-eligible-candidate case, and formally specifies the **score floor** that prevents the inverted 0×0 comparison failure.

### 14.6 Oil Distribution: Independence Principle Formalised

Architecture 2.0.1 makes the oil-line / water-line independence a first-class architectural principle: explicitly named as a decision, not an assumption. The rationale — the oil line's completion signal is a direct physical measurement with no escalation path; the PLC surfaces information and the human decides — is documented alongside the design.

### 14.7 PLC Guide 1.1: As-Built vs. Architecture Gap Documentation

The PLC Guide 1.1 documents the following significant gaps between Architecture 2.0.1's specification and the as-built ladder:

| Architecture item | As-built resolution |
| :--- | :--- |
| 12-register per-channel fault detection | Simplified to ratio-based check; only level channels 1–4 adjustable |
| Manual ring buffer for FIFO | Replaced by real hardware SFWR/SFRD FIFO instruction |
| Assumed exponential block unavailable | DEXP exists and is used for viscosity correction |
| 24-hour rollover via T24H placeholder | Real M8014 minute-pulse counter |
| AODD pump duty unresolved (×2) | Tied to PO designation + K30 threshold |
| Satellite word packing (unconfirmed) | Confirmed via D0/D2/D4 bit-unpacking |
| 32-point input mirror (speculated) | Confirmed at M115–M146, V1.1 |
| Manual override provisions (unspecified) | Mode Adjuster section added, V1.1 |
| T1 as permanently-true permissive | Confirmed as genuinely self-resetting tick |

### 14.8 Thermodynamic Analysis: First Multi-Scenario Evaluation

The Thermodynamic Analysis is the first document in this project to evaluate performance across three distinct environmental and feedstock scenarios (Worst: 2°C cold-start; Normal: 18.1°C Kathmandu weighted average; Best: 35°C residual-heat feedstock) rather than at a single design point. Key new findings not present in any prior revision:

- Throughput variance across all conditions is under 1% — a direct consequence of the two penalties (larger specific energy per kg, smaller melting window) largely cancelling each other.
- Best case's zero PO-tank duty is a load-bearing finding: olein starting at 35°C is already above its 30°C target.
- Solar coverage (6.4–9.5%) is substantially lower than earlier reported (40–61%) — correctly attributed to simultaneous array downsizing and demand growth, not a solar sizing error.
- The ETC vs. FPC ROI break-even threshold is now fully characterised: ETC wins if $c_\text{ETC}/c_\text{FPC} \leq 1.28$–$1.57$.
- The PO tank loss-coefficient linearisation carries wider approximation error at worst-case ambient (2°C) than in any prior use — flagged for a full natural-convection recomputation if worst-case PO figures become load-bearing.

---

## Appendix: Engineering Notebook

High-resolution scans of scratchpad derivations, geometric helical coil layout constraints, and early PLC state-machine routing matrices are located in the `engineering_notes/` directory.
