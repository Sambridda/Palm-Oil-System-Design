# Nebico ADA — Engineering Archive

This is the full technical history behind the Nebico Oil Melting & Retention System: every proposal revision, the engineering journey and mistakes along the way, deep technical derivations, changelogs, open items, and results as they stood at each stage. **[README.md](./README.md)** is the short version for a reader who wants the headline; this document is for anyone who wants to see the reasoning underneath it.

Mechatronics Engineering Pvt. Ltd. (MEPL), Kathmandu. Internship role: Junior Automation Design Architect (architect, PLC programmer, and electrical designer), working under a senior project lead. Grounded throughout in the self-authored **VCH Sizing Framework, 2nd Edition** ([DOI: 10.5281/zenodo.21009246](https://doi.org/10.5281/zenodo.21009246)).

---

## Document History

| Document | Date | Status |
| :--- | :--- | :--- |
| Technical Proposal I | Prior to June 2026 | Archived — superseded |
| Technical Proposal II | June 29, 2026 | Archived — superseded |
| Technical Proposal III (Architectural Revision I) | July 10, 2026 | Archived — superseded |
| Technical Proposal IV (Architectural Revision II — ADA) | July 12, 2026 | Archived — superseded |
| ADA: System Overview (Revised) — True Three-Way Concurrency | July 16, 2026 | Archived — superseded |
| ADA: Thermodynamic Analysis (worst/normal/best-case) | July 25, 2026 | Archived — see §18 for the operating-condition finding that qualifies these figures |
| ADA Architecture 2.0.1 | August 4, 2026 | Archived — superseded by ADA 3.0 |
| ADA: PLC Guide 1.1 (as-built companion) | August 4, 2026 | Archived — superseded by PLC Guide V3.0 |
| Ladder Logic (printed, 2,948 steps) | August 2026 | Archived — superseded by Program 3.3 export |
| Electrical Schematic IV | August 2026 | Current |
| **ADA Architecture 3.0** | **September 9, 2026** | **Current — Final, Locked** |
| **ADA PLC Guide V3.0** (consolidated) | **September 9, 2026** | **Current — sole programming reference** |
| **Nebico Oil Retention — PLC Overview, Program 3.3** (as-built) | **September 9–15, 2026** | **Current — as-built on Coolmay L10S** |
| **ADA — Commissioning Verification Checklist, Rev. 3** | **September 2026** | **Current — in use on site** |
| **ADA — Site Testing & Calibration, v1.0** | **September 10, 2026** | **Current — in use on site** |
| **Full Analysis of ADA Architecture** (1D radial thermal model) | **September 18, 2026** | **Current — supersedes the 2-zone tank model used in the Thermodynamic Analysis** |

---

## Table of Contents

1. [Industrial Mandate & Constraints](#1-industrial-mandate--constraints)
2. [Engineering Journey & Design Challenges](#2-engineering-journey--design-challenges)
3. [System Architecture](#3-system-architecture)
4. [ADA: Four-Scheduler Model](#4-ada-four-scheduler-model)
5. [Core Technical Deep Dives](#5-core-technical-deep-dives)
6. [The VCH Sizing Framework](#6-the-vch-sizing-framework)
7. [Headline Results & Validation Metrics](#7-headline-results--validation-metrics)
8. [Open Items](#8-open-items)
9. [Commissioning & Site Calibration](#9-commissioning--site-calibration)
10. [Electrical Design, Panel Build & Wire Sizing](#10-electrical-design-panel-build--wire-sizing)
11. [My Contributions](#11-my-contributions)
12. [Changelog: Proposal I → Proposal II](#12-changelog-proposal-i--proposal-ii)
13. [Changelog: Proposal II → Proposal III](#13-changelog-proposal-ii--proposal-iii-architectural-revision-i)
14. [Changelog: Proposal III → Proposal IV](#14-changelog-proposal-iii--proposal-iv-architectural-revision-ii--ada)
15. [Changelog: Proposal IV → System Overview (Revised)](#15-changelog-proposal-iv--system-overview-revised-true-three-way-concurrency)
16. [Changelog: System Overview → Architecture 2.0.1 & Companions](#16-changelog-system-overview-revised--architecture-201--companions)
17. [Changelog: Architecture 2.0.1 → ADA 3.0](#17-changelog-architecture-201--ada-30)
18. [The Thermal Model Rebuild: Cold Start vs. Carryover](#18-the-thermal-model-rebuild-cold-start-vs-carryover)
19. [Appendix: Engineering Notebook](#appendix-engineering-notebook)

---

## 1. Industrial Mandate & Constraints

| Parameter | Specification |
| :--- | :--- |
| **Production Throughput** | ≥ 2 tonnes of fully processed liquid palm oil per day (4 t/day treated as the satisfactory mark) |
| **Thermal Transition** | Solid-state feedstock at 18.1 °C (Kathmandu annual ambient) → stable liquid process target |
| **Hardware Scope** | Three 10 kL storage/melting vessels (one optionally dedicated to palm olein), one 5 kL trim-heating replenishment tank, passive solar thermal loop, 36 kW auxiliary electric immersion array |
| **Climate Factor** | Kathmandu solar reliability: 75.9% annually |

The steady-state throughput figures in §7 satisfy this mandate several times over under every evaluated ambient/feedstock condition. §18 adds a distinct, later finding: throughput is contingent on how the tank is *started* — see that section before treating the §7 figures as unconditional.

---

## 2. Engineering Journey & Design Challenges

### Scope Misalignment: Production Window Clarification

The project initially proceeded under the assumption that the target throughput was 2 tonnes processed within a 4-hour window. The VCH methodology had not yet been extended to account for latent heat during phase change, causing the computed overall heat transfer coefficient (U) to appear unrealistically poor and prompting repeated proposals for mechanical agitation that the senior engineer consistently declined. The 24-hour daily target reframing brought thermal performance figures within acceptable bounds and removed the need for agitation entirely — until agitation resurfaced, on different grounds, in §18.

**Takeaway:** Requirement ambiguity compounds downstream. Early, explicit clarification of the production window prevented a fundamentally over-specified design from proceeding to detailed engineering.

### Requirement Volatility Across Five-Plus Proposal Cycles

Between Proposal I and ADA 3.0, stated requirements changed substantially and more than once: the production window, supply/coil pipe cost preferences, a dedicated palm olein product line introduced mid-project, a trunk upsize that reopened priority logic, a coil bore reduction paired with a valve-count reduction, and multiple control-architecture revisions as the PLC implementation revealed gaps in the architecture documents. Rather than treating each change as a disruption, the architecture was kept modular: the VCH thermal sizing methodology, the ε-NTU coil-length inversion, and the priority-budget control philosophy proved reusable across revisions, with each new requirement extending the existing framework rather than replacing it.

**Takeaway:** A multi-revision proposal history is a normal feature of iterative industrial design work done alongside a client still discovering their own requirements. The relevant discipline is not preventing requirement change, but architecting a system whose core methodology survives it.

### Modbus Round-Robin Configuration: The Lowest Point

Implementing satellite communication between the master PLC and the three destination HMIs via Modbus round-robin polling was the most difficult moment in the development phase. The challenge was not conceptual — the round-robin sequencer logic was straightforward once the structure was clear — but configurational: without prior experience setting up Modbus across multiple Coolmay devices, every attempt to get the ADPRW instruction talking to the satellite stations failed silently or returned junk, with no obvious diagnostic path. The breakthrough came from going directly to the source — contacting Coolmay's own engineer, who clarified the specific register and parameter configuration the protocol required.

**Takeaway:** Hardware-specific communication protocol configuration is rarely fully documented in the manual. When the datasheet runs out, the manufacturer's engineer is a legitimate engineering resource, not a last resort.

### Register Allocation: The Hidden Complexity of Memory Management

Distributing data coherently across the PLC's D, M, T, and counter registers — while simultaneously managing what the HMI reads from and writes to — proved more cognitively demanding than any single control block in the architecture. The difficulty was not any individual register assignment, but the cumulative effect of a large program: data written in one section was silently consumed elsewhere, hundreds of steps later, and without a continuously maintained register map, tracking down a wrong value meant tracing the entire chain from sensor input to output. The V1.1 addition of M115–M146 as the physical input mirror, for example, displaced an earlier speculative allocation of M40–M71 for the same purpose — a collision a live map would have caught immediately, but which only surfaced on cross-reference. The same discipline paid off again in ADA 3.0/PLC Guide V3.0: every collision between the old V1.1 guide and the new pointer-driven core (M4's meaning, the tank-scoring formula, the Dynamic Water Target source, rate/fault checking, oil-distribution mechanism, heater-output arbitration) is resolved explicitly in a Reconciliation Log rather than left ambiguous (§17).

**Takeaway:** For any PLC program beyond a few dozen rungs, a register map is not documentation overhead — it is a development tool. Maintain it alongside the program from the first rung, not after the fact.

### Simplicity as an Engineering Decision

A recurring temptation throughout the architecture's development was to build the most complete, most faithful implementation of every specified mechanism. The fault detection system is the clearest example: the architecture specified twelve individually-adjustable, per-direction limit registers across all ten sensor channels — technically correct and fully covering every tunability case. The as-built implementation collapsed this to a single ratio-based check per channel, repeated ten times, with adjustable registers only on the four level channels where a bad reading has the most severe cascade consequences. This was not a shortcut; it was a deliberate trade — simpler logic has fewer places to hide a bug, fewer registers for a commissioning technician to misconfigure, and a fault behaviour explainable in one sentence rather than twelve. The same philosophy drove the simplification of the oil-line fault path (no escalation, no auto-stop, just a flowmeter and an operator), the consolidation of the two-block tank-scoring system into a single formula, and — a full architectural generation later — ADA 3.0's entire premise: replace repeated per-channel rungs with pointer-driven indexed loops wherever the channels are structurally identical, and retire a mixed number convention for one consistent decimal representation.

**Takeaway:** Complex systems are efficient. Reliable systems are functional. When the two are in tension, the system a commissioning engineer can verify in an afternoon is worth more than the system that is theoretically optimal on paper.

### The A.A / A.B / B.A / B.B Case Matrix

Cost pressure from the senior engineer introduced a preference for 1-inch NPS pipe while sizing was developed around 1.5-inch. Rather than selecting arbitrarily under an unresolved production window, all four permutations of supply/coil NPS were calculated in full and published for transparency. This four-case matrix was progressively resolved across later revisions (§12–§16).

### Challenging the Water-Side Velocity Assumption

Modelling the two-phase overall heat transfer coefficient revealed that the outer oil-side thermal resistance accounts for over 95% of total system impedance — meaning increasing water velocity through the coil produces negligible change in overall melting rate. This finding redirected the design from mechanical optimisation toward **algorithmic throughput recovery**: orchestrating a smarter, time-staggered multi-tank queue to bypass single-tank thermodynamic limits. This philosophy extended, in Proposal IV, to a dual-branch trunk serving two processes in parallel, and in later revisions to true three-way concurrent service across all branches.

### From a Shared Queue to a Dedicated Palm Olein Tank

One T10 vessel was carved out as dedicated palm olein storage. Palm olein solidifies at ≈24 °C and needs comparatively little energy to stay liquid — leaving it in the shared rotation would have distorted the tank-scoring system's assumptions. The fix required an oil-side restructuring: each T10 gets its own dedicated oil pump and feed line, gated by a manual ball valve in series with an automated control valve. The water/hydronic heating circuit itself was unchanged.

### A Three-Way Priority Ladder, Then a Need Array, Then True Concurrency, Then a Sentinel

Introducing the PO tank required a third priority tier (P1 T5 trim-heat, P2 PO maintenance, P3 T10 melting). A strict lockout was rejected in favour of a sequential daily energy budget. Proposal IV reframed this as a parallel need array with dual-branch flow; the System Overview (Revised) expanded it to genuine three-way concurrent service. Architecture 2.0.1 finalised this at the architecture level (§4). ADA 3.0 then resolved *how the arbiter itself works in the ladder*: rather than a conditional branch excluding the designated PO tank from scoring, the three scores are copied into a scratch array each scan and the designated tank's slot is overwritten with a sentinel value guaranteed to lose whichever comparison direction is active — letting one uniform indexed loop handle both the "highest wins" (3 eligible) and "lowest wins" (2 eligible, urgency-prioritising) cases with a single direction bit. See §17.

### Scrapping My Own Calibration Data

The first round of RTD sensor calibration was logged while the raw value was still drifting toward its settled reading in the water bath, with no fixed protocol for how many readings to take or what counted as "settled." That informality is also how a transcription error on one sensor (72 °C logged against a raw value of 722, misread at the time as 122) survived undetected until it was found on inspection. Rather than patch the existing dataset, it was discarded outright and replaced with a protocol that leads with an explicit steady-state check before any logging begins, all six sensors re-measured from a blank sheet (§9).

**Takeaway:** A measurement taken before the system has settled is not a noisy version of the right answer — it's a different, unusable quantity. The fix for bad data discipline is a better protocol, not a correction factor.

### Cold Start vs. Carryover: The Biggest Single Finding

Rebuilding the tank thermal model (§18) surfaced a result that reframes everything in §7: a tank started cold produces effectively nothing in a working day, while the same tank carried over warm from the previous batch clears the satisfactory throughput mark several times over — for free, with no hardware change. This is now judged the single most valuable finding of the project, and is being written into the ladder as a threshold-triggered reheat routine rather than left as an operating habit.

---

## 3. System Architecture

> **P&ID III** (mechanical engineer's latest Piping & Instrumentation Diagram) is the authoritative process-routing reference. The original Process Flow Diagram is retained for historical context only.

Each of the three T10 tanks has its own dedicated oil pump and feed line, with one T10 optionally designated as the **PO tank** — isolated from the melting rotation and dispensed only via operator-triggered logic. On the hydronic side, the trunk main is 1.5-inch NPS. Two branches are permanently and continuously dedicated to T10 palm oil melting (P3); the third branch is shared between T5 (P1) and the PO tank (P2). Water allocation is arbitrated by the ADA need array — a genuine three-way concurrent arbiter, not a sequential lockout. Branch valve count is 6, coil bore across every tank is 1.5-inch NPS. The architecture is governed by the four-scheduler model (§4); the ladder implementing it now runs on ADA 3.0's pointer-driven, single-decimal-convention core (§17), on a Coolmay L10S under Program 3.3 (§9).

---

## 4. ADA: Four-Scheduler Model

Architecture 2.0.1 formalised the control system as exactly four functional schedulers — a conceptual grouping that clarifies which kind of job each block is doing, not a physical or programmatic boundary. ADA 3.0 changes none of this grouping; it only simplifies the internal implementation of two of the four (Priority and, partially, Mathematical — see §17).

**Operational Scheduler** — Reads sensors and drives outputs: solar routing, heater output state, branch valve state, destination valve routing, and the dispense pump. Acts on decisions made elsewhere; does not make them.

**Priority Scheduler** — Decides who gets served. On the water side: the Need Array/Need Scheduler, tank scoring, and PO tank designation. On the oil side, entirely separately: request handling across the dispense nodes, gated only by the plant-wide System-OK condition.

**Mathematical Core** — Computes the numbers the other three schedulers consume: the water target law, heater-count lookup and anti-chatter latches, sensor averaging, the dynamic thermal boundary, the PO heat-demand function, and the oil-line runtime estimate.

**Fault Scheduler** — Keeps the system safe and stops it when it isn't. E-Stop, the System-OK condition, and Trend Threshold Supervision (now the resolved Sensor Rate Error block, §17) all live here. The oil line has no fault path of its own by design.

> **Critical design decision:** The oil line and water line do not share decision logic. The Need Array/Need Scheduler, tank scoring, and PO tank designation govern water only. Oil distribution runs on its own trigger and its own flowmeter/Modbus-confirmed completion. The two systems share only the plant-wide System-OK condition.

---

## 5. Core Technical Deep Dives

### Multi-Phase Thermal Modeling

External natural convection profiles for the uninsulated vessels were constructed using the Churchill-Chu correlation (vertical tank walls), Morgan-McAdams plate equations (horizontal surfaces), and the Gnielinski correlation with Kubair-Kuloor enhancements for helical coil geometries. This isolated a 1.07 kW hold-phase thermal loss profile for the melt phase (uninsulated T10) — the basis later extended into the full 1D radial model of §18.

### Thermal Control Law: T_target(d)

$$T_\text{target}(d) = \begin{cases} 70 & d < 200 \\ 70 - \dfrac{3}{2560}(d-200)^2 & 200 \leq d < 360 \\ 40 & d \geq 360 \end{cases}$$

where d is the level division register (d=200 is 50% full, d=360 is 90% full). Below half-full, T5 is heated aggressively to 70 °C; between 50–90% full the target tapers quadratically; above 90% full it drops to a 40 °C holding value. Continuity is confirmed at both knots. This law is unchanged in shape from Architecture 2.0.1 through ADA 3.0 — only its number representation and comparison basis changed (§17).

### Heater Staging: Dual-Latch Anti-Chatter

Three 12 kW heater elements are staged from level alone, active band split into three equal thirds. Two independent latches prevent chatter: a **rounding latch** (filling direction only — holds a heater-count decrease until level reaches a slightly higher buffer point) and a **comfort latch** (temperature-driven — waits until measured temperature actually permits cutting heat). Both must clear before any state change. This block was specified at the architecture level from early revisions but was **not actually ladderised until PLC Guide V3.0** — it is now the sole driver of the three heater outputs, replacing the older auxiliary-stage-register arbitration to avoid a two-master conflict on the same coils (§17).

### Dynamic Upper Thermal Boundary (Tf)

$$T_f(x,\, y,\, m_p) = \frac{239.53\, x + m_p\, y}{239.53 + m_p}$$

where x is the water/steel structure temperature, y is the palm oil temperature, and m_p is the estimated remaining oil mass. When Tf > 55 °C, an interlock triggers. Unchanged in formula from early revisions through PLC Guide V3.0, where it is re-expressed in float arithmetic to remove a 16-bit overflow risk that had forced 32-bit scaling tricks.

### Sensor Averaging

A five-sample rolling average refreshing once every 5 seconds, applied to every channel feeding a calculation, rejects transient spikes from oil movement. Ten channels filtered: four level, six temperature-derived. Flow is excluded and kept real-time. Unchanged in concept since early revisions; re-implemented as a pointer-driven indexed loop in ADA 3.0.

### Tank Scoring, Selection, and the Retired Incumbent/Challenger Rule

The scoring formula has been stable since early revisions: score = 0.6 × level + 0.4 × temperature. What changed is how the winner is picked. Earlier revisions used an incumbent/challenger switching rule with a displacement threshold (challenger must exceed 2× or fall below 0.5× the incumbent, depending on eligible-candidate count) to prevent chatter. **This rule has since been scrapped.** ADA 3.0's Need Scheduler instead uses a sentinel-based single loop with strict (never ≥/≤) comparisons, so a tie is decided purely by scan-order index — ties keep whichever tank the loop reaches first, with no dedicated tie-break logic required. See §17 for the resolution and PLC Guide V3.0 §9.5 for an optional minimum-dwell debounce timer noted but not required.

### PO Tank Demand Function

$$D_\text{PO}(\theta_\text{tank}, m_\text{tank}, \theta_w) = \begin{cases} C_\text{cal,melt} \cdot A & \theta_\text{tank} < \theta_\text{melt} \\ C_\text{cal,liquid} \cdot B & \theta_\text{melt} \leq \theta_\text{tank} < \theta_\text{target} \\ 0 & \theta_\text{tank} \geq \theta_\text{target} \end{cases}$$

Calibration constants tuned at commissioning, not derived from first principles, so the demand check stays accurate as conditions drift. A demand watchdog timer clears a stale flag if demand never resolves. Reference constants and watchdog pattern unchanged in ADA 3.0/PLC Guide V3.0; the timer devices were renumbered to a 100 ms base in Program 3.3 (T5→T250, §9).

### Oil Distribution: From FIFO to Modbus-Node Request/Response

Earlier revisions specified a hardware FIFO (SFWR/SFRD) across three destinations, flowmeter-confirmed completion, and no fault path by design. This has since been **fully redesigned** around per-node Start/Stop/Reset hardware and closed-loop Modbus polling: an operator enters an amount and presses Start; the PLC checks line occupancy (busy nodes see "halted", not a queue position); on success the request is acknowledged and dispensed under an exclusive line lock; on failure, up to 5 Modbus retries are attempted before the line lock is **released unconditionally** — closing a deadlock risk the original design carried, where a node stuck on a failed poll could hold the lock indefinitely with no recovery path. Three outcomes now exist (dispensed / busy-elsewhere / comms-fault-retry), each with its own HMI message, and a persistent per-node failure counter gives visibility into a chronically flaky Modbus link. See §17.

### Fault Supervision → Sensor Rate Error (Resolved)

Trend Threshold Supervision's asymmetric tunability rationale — level channels adjustable, temperature channels fixed, because a bad level reading cascades into mass, Tf, scoring and priority far more severely — is unchanged since it was first specified. What ADA 3.0 resolved was the check's shape: a single two-sided band (max and min rate bound) per channel, run through one pointer loop across exactly ten channels, replacing what earlier revisions specified as a single-direction ratio check.

### Batch-Side Modelling Correction: Cmin = Cw

Under the individualised-feed, batch-heated architecture, each tank is a well-mixed batch whose bulk temperature changes slowly relative to one coil pass, so water is Cmin and tank contents behave as Cmax → ∞ over one pass:

$$NTU = \frac{UA}{C_w}, \quad \varepsilon = 1 - e^{-NTU}, \quad Q(T_\text{tank}) = \varepsilon\, C_w\, (T_\text{hot} - T_\text{tank})$$

All NTU calculations from Proposal III onward use this basis.

---

## 6. The VCH Sizing Framework

The system is a full-scale industrial deployment of the **VCH Sizing Framework** — a methodology authored specifically for submerged hydronic coil thermal systems, applied here across all eleven sizing steps (thermal target, NTU-ε analysis, hydraulic resistance, fouling correction, driver verification). The original edition is published on Zenodo (DOI: 10.5281/zenodo.20579394); the 2nd Edition — with 35 formal derivations and PLC/control logic scoped into separate appendices — carries its own DOI (10.5281/zenodo.21009246) and is the version cited throughout every ADA-family document from ADA 3.0 onward. The project served as the framework's original verification platform and surfaced two of its founding findings: an NPS 1" coil exceeding erosion velocity limits (upgraded to 1.5" Sch 10S SS304), and a specified 36 kW immersion heater found undersized once tank heat losses were properly accounted for — a finding since revisited and reversed by the 1D radial model (§18), which found the same heater materially oversized once cold-start dead time and real duty cycle were properly modelled.

---

## 7. Headline Results & Validation Metrics

*These figures assume steady-state operation at the stated ambient/feedstock condition. §18 adds a distinct finding about how the tank is started that materially changes daily output in practice — read both before treating a single number here as "the" throughput figure.*

### Thermodynamic Analysis (Worst / Normal / Best Case)

Evaluated under the 2-inch coil bore / 1.2 m/s / 70 °C constant supply basis, full three-way concurrent branch architecture. Worst = cold-start + cold-snap; Normal = Kathmandu weighted-average ambient and feedstock; Best = continuous-operation residual-heat feedstock.

| Metric | Worst | Normal | Best |
| :--- | :---: | :---: | :---: |
| T5 duty period | 4.70 hr | 4.03 hr | 3.64 hr |
| PO tank duty period | 0.91 hr | 0.45 hr | 0.00 hr |
| Palm oil melted | 5,457.8 kg/day | 5,439.3 kg/day | 5,490.8 kg/day |
| Fulfilment vs. 2 t/day mandate | ≈273% | ≈272% | ≈275% |
| Total daily energy demand | 1,247.5 MJ | 1,173.6 MJ | 1,133.6 MJ |
| Average coil power | 14.44 kW | 13.58 kW | 13.12 kW |
| Solar (FPC) coverage of demand | 6.45% | 9.15% | 9.46% |
| Estimated annual savings (NPR, FPC) | 75,125 | 100,243 | 100,094 |

**Key findings:** throughput variance across all three conditions is under 1% — worst case's larger specific energy per kg and smaller melting window largely offset each other. Best case genuinely requires zero PO tank duty (olein starts above its 30 °C target). Solar coverage (6.4–9.5%) is substantially lower than the 40–61% reported in earlier revisions — a smaller FPC array (10 panels, 19.0 m², vs. 15 panels/22.674 m²) against roughly 2–3× the demand basis, a direct and honestly-reported consequence of maximising throughput, not a sizing error. ETC is the more efficient collector at every condition (53–58% vs. 34–45%) and only needs to beat FPC on cost by a margin of ≈1.28–1.57× to also win on ROI. The savings estimate uses NEA's general industrial tariff, not the facility's actual metered rate, and is explicitly flagged as directional.

### Prior Revisions (archived)

| Revision | Melt output | Fulfilment vs. mandate |
| :--- | :---: | :---: |
| System Overview (Revised) — 1.5" bore, 6 valves | ≈4,453 kg/day (≈4,953 combined) | ≈223% / ≈248% combined |
| Proposal IV (Architectural Revision II — 2" bore, 8 valves) | ≈4,919.8 kg/day (≈5,419.8 combined) | ≈246% / ≈271% combined |
| Proposal III (Architectural Revision I, single-branch) | ≈2,447 kg/day | ≈122% |
| Proposal II (3-tank staggered, primary/worst-case HTF) | 6.0 t/day both cases | — |
| Proposal I (Primary / Worst-Case) | 24.23 / 20.48 t/day | 3.63× / 2.42× single-tank safety factor |

System Overview (Revised) also carried a peak instantaneous demand check: P_peak ≈ 36.61 kW, about 1.7% over the 36 kW rated auxiliary array — a finding carried into electrical design at the time. §18's 1D radial model later found the opposite in practice (the heater is comfortably oversized once real duty cycle is modelled), which does not overturn this steady-state instantaneous-peak calculation but does mean the two figures answer different questions and shouldn't be read against each other directly.

---

## 8. Open Items

### Resolved by ADA 3.0 / PLC Guide V3.0 (closed, listed for the record)

- Tie-break on equal scores — previously flagged as defaulting to execution order with no explicit design decision; now formally resolved as an inherent property of the sentinel loop's strict comparisons (§5, §17).
- Sensor Rate Error / Trend Threshold Supervision shape — previously a single-direction ratio check; now a resolved two-sided band per channel.
- Need Scheduler arbiter mechanism — previously described only at the architecture level; now a specified single indexed loop.
- Oil distribution deadlock risk on Modbus failure — previously unaddressed; now closed via unconditional lock release on the 5th failed try.
- Whether temperature channels warrant adjustable threshold registers — resolved as no; they remain hardwired, matching the original asymmetric-tunability rationale.

### Still Open — Architecture / PLC

- Dynamic Water Target's quadratic coefficient (E618) needs re-derivation for direct mm-domain comparison (was fit to an old 5 mm-division register domain).
- M_Serve_TA/TB/TC and the temp/level/mass channel registers need confirmation as genuinely contiguous 3-point blocks for Z1-indexing to work as written in the Etotal and Need Scheduler loops.
- ADPRW station/address/count parameters in the Oil Scheduler's Modbus poll are placeholders copied from the legacy periodic poll — each node needs its own values confirmed against the real Modbus map, and settle/timeout/cooldown timer values tuned against actual RS485 round-trip time.
- E-register pool's actual size on the target hardware needs confirming against the Coolmay L01S/L10S memory map before the guide can be trusted as complete.
- Rounding latch asymmetry (draining direction uses a plain nominal boundary with no buffer, filling direction has the buffer) — confirm this is still intentional before commissioning.
- E-Stop reset source and tie-break rules were flagged as open in earlier PLC review and are noted as explicitly unresolved in PLC Guide V3.0's own scope statement.

### Still Open — Commissioning (from Rev. 3 checklist)

- M51 (Run-or-Pause) withholding a paused tank from priority scheduling is confirmed as intended behaviour by the design authority but is still not written into the Program 3.3 PLC Guide's own walkthrough or register tables — the one item carried across three checklist revisions without closing.

### Still Open — From the 1D Radial Thermal Model (§18)

- Which threshold to use for a carryover reheat routine: the RTD sensor sits closer to the tank wall than to the modelled core, so what it reads and what the simulation calls "band" or "core" temperature aren't the same quantity — needs further work before a number from the simulation can be used directly.
- The pipe-resistance network behind the 44/47/50 Hz VFD frequency settings was only half-modelled (remaining run estimated, not measured, since piping wasn't fully laid out) — flagged for on-site verification by whoever commissions the VFD.
- Ttarget's heater-staging overshoot protection governs automatic mode only and can be bypassed entirely in manual mode — flagged as a live safety question given a 36 kW heater on a 400 L loop, not yet resolved.
- Thermal simulations in the Full Analysis were run at a fixed 1.17/1.65 m³/h rather than varying with tank count the way the pump section does — not yet explicitly checked at the single-tank 2.0 m³/h VFD point.

---

## 9. Commissioning & Site Calibration

### Commissioning Verification Checklist, Rev. 3

Worked through item-by-item with the commissioning technician against Program 3.3 on the live system (or a faithful bench/simulation rig). Tolerance policy is explicit and two-tier: **±5%** on calculated/analog quantities (temperatures, tank scores, durations, derived setpoints), and **exact match, no tolerance,** on anything digital or logical — valve state, latch behaviour, sequencing, mutual exclusivity, which branch of an IF/ELSE fires, HMI password gating. A third mark, **Unsatisfactory**, is reserved for test points the PLC Guide does not pin to an exact register or that describe a feature not yet in the ladder — keeping genuinely open questions visible instead of forcing them into a pass or fail.

Every PLC step reference was renumbered and individually re-checked against the Program 3.3 export (the offset between 3.2 and 3.3 grows through the programme rather than being a flat shift). Five items are new to 3.3 and collected in their own section for fast re-verification after an upgrade: the fault trigger-value snapshot, the T250/T251 100 ms-base timer renumbering, the M800 flowmeter-fitted toggle, the M65 master Oil Controller enable (sourced specifically from the supervisory HMI, independent of the three per-station units), and the Manual Pump Mode consolidation. One item remains open across three checklist revisions (§8).

### Site Testing & Calibration, v1.0

Five calibration jobs, each set out as a fill-in-on-site template with the fitted equation given alongside:

1. **RTD temperature sensors** — two-point ice-water/hot-water bath fit per sensor, with an explicit steady-state check before logging begins (the old dataset was scrapped for skipping this — §2). Per-sensor gain/offset averaged into one shared equation applied across all six channels; any sensor sitting noticeably off the shared line gets a repeat pair of baths before the shared equation is accepted as final.
2. **Ultrasonic level sensors** — calibrated directly against the tank at three real fill states (empty/half/full) rather than against a sighted proxy target, giving level directly with no separate geometric offset to subtract afterward.
3. **VFD-to-flowrate** — bucket-and-timer measurement (no flowmeter reference needed) to find the VFD frequencies producing 0.5 / 1.0 / 1.2 m/s for LSM/HSM/FSM.
4. **Tank geometry** — the empty-tank raw value for the level constant, and mass-per-mm from measured tank diameter and operating-temperature oil density.
5. **Oil-node dispense-volume calibration constant** — commanded-vs-measured dispense trials, iterated until error at 5 L settles at or below a 0.5 L ceiling, then checked across additional volumes (10 L, 15 L) to confirm linearity holds across the working range, not just at the calibration point.

---

## 10. Electrical Design, Panel Build & Wire Sizing

- Drew the full electrical schematic for the plant (Electrical Schematic IV, AutoCAD Electrical, 10 sheets — Sheet 6 confirms the I/O assignment cross-referenced in the PLC Guide), and walked the trickier connections through directly with the technician on site rather than handing over a drawing to be interpreted alone.
- Designed the control panel layout for the main enclosure and for the three substations.
- Sized the field wiring on site with a technician against real runs and loads: **0.75 mm² for all logic and 24 V, 1.5 mm² for the gear pump, 4 mm² for the heater circuit.**
- **The panel that came out too small.** The main control panel was the first enclosure designed on this project, and it came out smaller than it needed to be — a measurement and judgement error caught only after fabrication, with no chance to amend it. The senior engineer took the design and produced his own layout, switching the 24 V power supply to fit everything into the space available. Sheet metal doesn't forgive a sizing error the way a drawing revision does; enclosure sizing is now something to over-check before it goes to fabrication, not after.

---

## 11. My Contributions

**Thermal Sizing & Proposal Authorship** — All thermal calculations, coil sizing, the A.A/A.B/B.A/B.B case matrix (Proposal I); unified 1-inch supply bore sweep (Proposal II); fixed 2-inch bore, individualised-feed, three-tier priority architecture (Proposal III); dual-branch trunk, need-array reframing, ADA demand functions (Proposal IV); 1.5-inch bore reduction, six-valve reconfiguration, true three-way concurrency analysis (System Overview Revised); architectural consolidation and thermal control law revision (Architecture 2.0.1); worst/normal/best-case thermodynamic scenario analysis; the pointer-driven, decimal-convention simplification pass and resolution of the Sensor Rate Error, Need Scheduler and Oil Scheduler blocks (ADA 3.0); and the ground-up 1D radial enthalpy thermal-model rebuild, pump/piping circuit characterisation, and the cold-start/carryover operating finding (Full Analysis). All grounded in the self-authored VCH Sizing Framework.

**PLC Implementation** — Full ladder logic, as-built: I/O mapping, register map, safety gating, sensor averaging, thermal control law, heater staging (ladderised for the first time in PLC Guide V3.0), dynamic thermal boundary, tank scoring, the arbiter, oil distribution, fault supervision, and operator HMI interfaces — carried from the original 2,948-step V1.1 program through to the current ~3,300-step Program 3.3 export on a Coolmay L10S, with every register collision between successive guide revisions resolved explicitly in a reconciliation log rather than left ambiguous.

**Commissioning & Calibration** — Authored the Commissioning Verification Checklist (Rev. 3, tolerance-policy-based, worked live with the technician) and the Site Testing & Calibration procedure (RTD, ultrasonic, VFD, tank geometry, oil-node constant), including the decision to discard and re-take the original RTD dataset rather than patch it.

**Electrical Design** — Full electrical schematic, control panel layout for the main box and three substations, on-site field wiring sizing (0.75 / 1.5 / 4 mm²), and ownership of a panel-sizing mistake on the first enclosure design, resolved by the senior engineer's rework (§10).

**Process Architecture** — Single-pump solar feedback loop topology; individualised T10 oil-feed restructuring; PO tank isolation logic; the P1/P2/P3 priority architecture across its sequential-budget, dual-branch, true three-way concurrent, and four-scheduler forms; the demand-driven dynamic water temperature control law; Eco/Efficiency/Full Throttle mode logic; the oil-distribution independence principle.

**Tank Geometry (Collaborative)** — Initial vessel proportions and aspect ratio estimates as part of thermal sizing work; detailed manufacturable geometry and SolidWorks verification completed by the team's mechanical engineer.

**Status** — The plant is in its installation phase, roughly 30% complete: control panel and tanks fabricated, field wiring underway, site calibration and commissioning verification proceeding against the documents in §9.

---

## 12. Changelog: Proposal I → Proposal II

**Supply pipe simplification.** Proposal I evaluated two supply pipe sizes, producing a 2×2 case matrix. Proposal II standardises on a single 1-inch Schedule 40 CPVC supply pipe; the case matrix collapses to a single-axis coil bore sweep (1", 1.25", 1.5", 2").

**Coil sizing: inverted design logic.** Proposal I fixed the coil at its 90 m geometric ceiling and solved for throughput. Proposal II inverts this: a heat-duty target Q_target = Q_batch + Q_loss,max = 9.17 kW is defined from the mandate, and minimum coil length solved in closed form via ε-NTU inversion. Recommended: 1.5-inch coil at L ≈ 56 m — a 38% reduction from the original spec.

**Melt time and safety factor basis.** Proposal II sizes to the daily mandate floor, so single-tank margin is 1.0× by construction; the 3× system-level margin comes from three staggered tanks.

**T5 coil sizing quantified.** Even the smallest bore (1-inch) requires only ≈5.8 m of coil against a 65 m geometric ceiling — under 9% utilisation.

---

## 13. Changelog: Proposal II → Proposal III (Architectural Revision I)

**Shared → individualised oil feed.** Each T10 vessel gets its own dedicated oil pump and feed line, gated by a manual ball valve in series with an automated control valve — the structural prerequisite for a dedicated palm olein tank.

**New tank class: the PO tank.** One T10 tank may be designated via HMI as a dedicated palm olein store, excluded from the P3 melting rotation and dispensed only via operator-triggered logic.

**Two-tier → three-tier priority.** A three-way ladder — P1 (T5 trim-heat), P2 (PO tank maintenance), P3 (T10 melting) — resolved by a sequential daily energy budget.

**Coil bore fixed.** 2-inch NPS Sch. 10S across every tank; coil length 30 m (T10/PO), 10 m (T5); water supply fixed 70 °C; feed velocity 1.2 m/s.

**NTU model correction.** Cmin = Cw under the batch-heated architecture — the old throughput-rate model would have predicted >98% effectiveness, physically inconsistent with batch heating.

**Fault detection: duty-cycle → physics-based.** Alarming on observed heating/cooling rates versus what is physically achievable, decoupling fault detection from duty-cycle bookkeeping.

---

## 14. Changelog: Proposal III → Proposal IV (Architectural Revision II — ADA)

**Trunk upsize.** 1-inch → 1.5-inch NPS, enabling two branches simultaneously at full individual design flow.

**Priority ladder → need array.** Whichever of P1/P2/P3 had live demand determined single- or dual-branch operation; all active processes served in full rather than one waiting on the other.

**PO tank governance: hard cap → operator-trust model.** A flat 10-minute arbitration window replaced by a suspicion meter (S ∈ {0,1,2,3}, resetting every 24 hours) escalating from HMI prompt through alarm to autonomous feed isolation, plus an independent soft-ceiling buffer permitting draw up to 2× the entered quantity before a warning.

**Dynamic, demand-driven water temperature.** Fixed 70 °C supply replaced by a real-time demand-derived target (two-point anchored proportional law).

**Load-responsive operating modes.** Eco (≥90% T5 level), Efficiency (90–50%), Full Throttle (<50%).

---

## 15. Changelog: Proposal IV → System Overview (Revised) — True Three-Way Concurrency

**Coil bore reduced**, 2-inch → 1.5-inch across every tank (−20.0% coil surface area). **Branch valve count reduced**, 8 → 6 — two T10 branches permanently dedicated to P3, the third shared between P1 and P2. **Three-way concurrent arbiter** — the trunk serves all three branches concurrently by throttling flow; no priority is discarded under contention, which is the trunk's normal operating condition whenever P1 or P2 is active. **PO tank pulse-hold timer retired** — under the three-wide need array, PO demand is served normally for as long as it stays live. **Peak instantaneous demand check introduced**: P_peak ≈ 36.61 kW, ≈1.7% over the rated 36 kW array — a narrow, conservative, compounded worst-case finding carried into electrical design.

---

## 16. Changelog: System Overview (Revised) → Architecture 2.0.1 & Companions

Architecture 2.0.1 is the first document describing the ADA as *designed* rather than as *revised from the previous revision* — it introduces the four-scheduler model, consolidates all control logic into one self-contained reference, and separates architecture from implementation. It formalises the T_target(d) closed-form quadratic (replacing the two-point anchored proportional law), the dual-latch heater-staging model, the PO tank's piecewise demand function with its watchdog, the single tank-scoring formula with its inversion rule and score floor, and the oil-line/water-line independence principle as a first-class design decision.

PLC Guide 1.1 documented the gap between this specification and the as-built ladder — most consequentially, the 12-register fault-detection design simplified to a single ratio-based check repeated ten times, with only the four level channels made adjustable.

The Thermodynamic Analysis was the first document to evaluate performance across three distinct scenarios rather than a single design point, surfacing the <1% throughput variance, the best-case zero-PO-duty finding, and the corrected (lower, honestly-attributed) solar coverage figure — see §7.

---

## 17. Changelog: Architecture 2.0.1 → ADA 3.0

ADA 3.0 (final, locked, September 9, 2026) is a ground-up simplification pass over Architecture 2.0.1 and the as-built V1.1–V2.0 ladder, aimed at two things only: replacing repetitive per-channel rungs with pointer-driven loops wherever the underlying channels are structurally identical, and moving the whole program onto one consistent decimal data convention — real decimal values for temperature (1 dp), float for level (full precision, display rounded to the mm) and flow, and a fixed comparison tolerance (±1 mm, ±0.1 °C) used everywhere a setpoint is checked, replacing bare floating-point equality. This is a ladder-and-data-representation simplification, not a change to control philosophy — the thermal control law, tank scoring formula, and water/oil separation all carry forward unchanged in substance.

Two blocks left open in earlier revisions were resolved outright: **Sensor Rate Error**, now a two-sided band per channel across the ten monitored channels, flow excluded and kept real-time; and the **Need Scheduler**, now a single indexed loop, direction-gated by the PO-designation flag, using a sentinel value to exclude the designated tank instead of a conditional branch — replacing two separate hand-written comparison structures with one loop that scales to a fourth tank for free. The **Oil Scheduler** was fully redesigned around per-node Start/Stop/Reset hardware and closed-loop Modbus polling, closing the one deadlock risk in the original scheme: an unconditional release of the line-occupancy lock on the fifth failed poll.

**PLC Guide V3.0** then consolidated the full picture: every block ADA 3.0 resolved or simplified sits alongside every block ADA 3.0 was silent on and PLC Guide V1.1 had already specified (Heater Staging, Tf, Etotal/Dynamic Power, the Auxiliary Stage register) — carried forward and, where the shared register map required it, reconciled. Every collision is resolved explicitly in a **Reconciliation Log**, not left ambiguous:

| Conflict | Resolution |
| :--- | :--- |
| M4's meaning | Kept as the Tf interlock (V1.1); the aggregate PO-stored flag moves to a new address, M5_POStored, instead of reusing M4 as ADA 3.0 had proposed |
| Tank scoring formula | V1.1's two-variant (casual/immediate) formula and the old incumbent/challenger rule are dropped; the single 0.6×Level + 0.4×Temperature form is authoritative |
| Dynamic Water Target source | V1.1's linear D_Ptotal-based rung is dropped; the quadratic T_target(d) law is authoritative |
| Rate/fault checking, 10 sensor channels | V1.1's per-channel heat/cool rate limits inside Fault Detection are superseded by the resolved two-sided Sensor Rate Error block |
| Oil distribution mechanism | V1.1's direct valve-driving rungs from demand flags are dropped outright; the Oil Scheduler's Modbus-node model replaces it |
| Heater output arbitration | Heater Staging (ladderised for the first time) becomes the sole driver of the three heater coils; the Auxiliary Stage register is retained but demoted to informational-only, avoiding a two-master conflict |
| Number format | Every real-valued register moves to the float (E) pool, removing the 16-bit overflow risk that had forced 32-bit arithmetic throughout the energy and Tf blocks |

**Program 3.3** (the current as-built export on a Coolmay L10S) layered four genuinely new features on top of a renumbering pass from Program 3.2: a per-channel fault trigger-value snapshot (D750–D768, the HMI's "max value recorded"); the PO-melt watchdog and oil-dispense timers renumbered to 100 ms-base Coolmay devices (T5→T250, T100→T251); an M800 HMI toggle forcing the processed flow register to a fixed nominal value when no physical flowmeter is fitted at a site; and a master Oil Controller enable (M65) sourced specifically from the supervisory HMI, independent of the three per-station units. The separate "Manual Mode Scheduler" and "Manual Pump Mode" sections from 3.2 were also consolidated under one heading as part of an ongoing segmentation clean-up.

---

## 18. The Thermal Model Rebuild: Cold Start vs. Carryover

### Why the model was rebuilt

The tank thermal model went through the same evolution twice. **Version 1** (a single lump of oil at one uniform temperature) predicted 40 hours to 40 °C — fundamentally misleading, since solid palm oil's thermal conductivity (~0.18 W/mK, similar to wood) means heat cannot spread through a solid block that fast; a single-temperature model assumes a perfect mixing that solid oil can't do. **Version 2** (a Core/Shell split, 30/70) correctly revealed the "hot pocket" effect — the core melts while the shell stays cold — but the 30/70 split was arbitrary; the coil actually sits at 80% of the tank's radius, not in the middle. **Version 3**, used throughout the Full Analysis, slices the tank into 100 thin concentric shells from centre to wall, tracks each shell's enthalpy (not temperature — this keeps latent heat numerically stable across 100 coupled shells instead of inflating cp through the melt band) individually, and includes the 5 mm steel tank wall as its own thermal mass.

### The pump and piping circuit (unchanged conclusion, re-confirmed)

The CHL2-30 pump (0.37 kW motor) cannot reach the original 4.04 m³/h design target — 3.5 m³/h is a hard ceiling for this hardware. VFD settings: ~47 Hz for three tanks open (1.17 m³/h/coil), 50 Hz for two (1.65 m³/h/coil), 44 Hz for one (2.0 m³/h, targeted directly at 1.0 m/s). All three settings sit comfortably inside CPVC's velocity ceiling. These frequencies were calculated on a half-modelled pipe-resistance network (§8) and are flagged for on-site verification.

### The finding: how you start the batch matters more than the weather

| Start condition | Single-tank daily output | Time to 4 t (2 tanks) |
| :--- | :--- | :--- |
| Cold start, any Kathmandu ambient | 0 kg — no usable liquid inside a 24 h day at any evaluated ambient | ~14–40 h depending on ambient |
| Carryover (≈30 °C retained from prior batch) | ~4.0–4.4 t/day per tank | ~11–12 h regardless of ambient |
| Carryover, 3 tanks combined | ~12.2–12.8 t/day | ~7.6 h to clear the 4 t mark |

Starting a tank cold means the coil can only deliver ~1.4 kW into solid oil — a "dead time" of 6 to 40 hours (worse in colder ambient) before any oil melts at all, because the oil-side heat transfer coefficient is only ~5 W/m²K while the oil is solid (pure conduction) versus 50+ W/m²K once melting begins (a positive feedback loop: faster melting means more liquid right at the coil, which transfers heat better). Running three tanks at once doesn't triple output during this phase — all three sit through essentially the same dead time in parallel, giving a consistent 1.6× (not 3×) speed-up over a single tank across the whole run. Carrying the tank over at ~30 °C removes the dead time entirely: liquid production starts within the first hour, and the 2–22 °C ambient range then changes output by less than 10% — carryover, not weather, sets the outcome. This also makes the earlier-identified **13 °C threshold** (below which cold-start dead time stretches badly) disappear in carryover mode.

### What it means for the heater, solar coverage, and next steps

The 36 kW heater's spare capacity is larger than earlier reported once dead time and active melting are accounted for separately: ~3.9% duty during dead time, ~31–35% during active melting — nothing here calls for a different heater, only for when it gets useful work to do. Solar coverage recomputed against the new demand basis sits in a narrow 7.9–10.6% band in carryover mode (consistent with the Thermodynamic Analysis's 6.4–9.5% figure) but is *not* comparable to the misleadingly high 66.5% figure that a cold-start, near-zero-output day would otherwise produce — a small solar contribution covering a large share of almost no real demand is not solar performing well.

Two operational decisions follow directly: build a threshold-triggered carryover/reheat routine into the ladder itself rather than leaving "never let the tank go cold" as a manual habit (open item, §8); and don't reach for insulation as the fix — 50 mm of mineral wool only bought ~6% more cold-start production, which doesn't justify the cost. A slow impeller or even manual top-of-manhole agitation to disturb the solid mass looks like it could move the needle further, and stays on the table instead.

---

## Appendix: Engineering Notebook

High-resolution scans of scratchpad derivations, geometric helical coil layout constraints, and early PLC state-machine routing matrices are located in the `engineering_notes/` directory.
