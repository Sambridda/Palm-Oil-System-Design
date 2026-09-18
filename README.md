# Palm Oil Melting & Retention System — Nebico

**Industrial thermal + control systems design for a multi-tank palm oil melting, storage, and trim-heating facility.**
Mechatronics Engineering Pvt. Ltd. (MEPL), Kathmandu — internship role: Junior Automation Design Architect (architect and programmer).

A passive solar thermal loop and a 36 kW auxiliary electric immersion array are coordinated by a PLC-driven control architecture — the **Adaptive Demand Allocation Architecture (ADA)** — to melt and hold palm oil across three 10 kL vessels and one 5 kL trim-heating tank, in Kathmandu's 18.1 °C ambient. The thermal sizing methodology is generalised into a self-authored, published framework, the **VCH Sizing Framework (2nd Ed.)** ([DOI: 10.5281/zenodo.21009246](https://doi.org/10.5281/zenodo.21009246)).

The system is built, programmed and in commissioning. The work below spans thermal modelling, control architecture, as-built ladder logic on a Coolmay L10S, and the commissioning and site-calibration procedures used to bring it up.

---

## System at a Glance

| | |
|---|---|
| Plant | 3 × 10 kL retention tanks, 1 × 5 kL trim-heating tank (T5), shared hydronic water loop |
| Heat sources | 10-panel FPC solar array (19.0 m²) + 36 kW electric immersion array, 400 L water loop |
| Controller | Coolmay L10S, ~3,300-step ladder program (GX Works2), 11 analog channels |
| HMI | TK8100H supervisory × 1, TK8050H per-station × 3, Modbus RS485 |
| Distribution | Three oil dispense nodes, one-at-a-time line lock, flowmeter-confirmed |
| Design output | Target 2 t/day, satisfactory 4 t/day — see *Thermal Modelling* below |

---

## What I Built

### Thermal sizing and modelling
- Derived a closed-form ε-NTU coil-length inversion from a target heat duty, replacing trial-and-error coil sizing; found that oil-side thermal resistance dominates the impedance stack, which redirected the design from mechanical tuning (pump velocity, coil bore) toward **algorithmic throughput recovery** — a smarter multi-tank dispatch queue instead of bigger pipes.
- Ran a worst/normal/best-case scenario analysis on the water-side basis (2″ bore, 1.2 m/s, 70 °C supply), which showed daily melt throughput holding within ~1% across all three ambient/feedstock conditions, and quantified solar coverage honestly at 6.4–9.5% — a **downward correction of the 40–61% figure earlier revisions reported**, caused by a smaller array against a much larger throughput basis, and flagged as such to stakeholders rather than left to be discovered later.
- Rebuilt the tank thermal model from scratch when the earlier one stopped being trustworthy: **1D radial, 100-shell enthalpy model** including the steel wall's own thermal mass, replacing a 2-zone core/shell model whose 30/70 split was arbitrary. Tracking specific enthalpy rather than temperature keeps latent heat numerically stable across 100 coupled shells instead of inflating cₚ through the melt band.

### Control architecture (ADA)
- Evolved the plant's control logic across five major revisions to **ADA 2.0.1**, from a simple priority ladder to a three-way concurrent arbiter with a real-time thermal control law, dual-latch anti-chatter heater staging, and a unified tank-scoring formula — formalised as a four-scheduler model (Operational / Priority / Mathematical / Fault) separating *decision* from *action*.
- Then ran a deliberate simplification pass, **ADA 3.0 (final, locked)**, which changed no control philosophy but closed the gap between the architecture and a maintainable ladder: repetitive per-channel rungs replaced by pointer-driven indexed loops, and the old mixed float / ×10 fixed-point convention retired for one decimal representation with a single comparison tolerance (±1 mm, ±0.1 °C) used everywhere.
- Resolved the three blocks earlier revisions had left open:
  - **Sensor rate error** — a two-sided band per channel across exactly 10 channels (flow excluded and kept real-time), with level bounds operator-adjustable and temperature bounds PLC-hardwired, matching where a bad reading actually cascades.
  - **Need Scheduler** — one indexed arbiter loop, direction-gated by the PO-designation flag, using a **sentinel value** to exclude the designated tank rather than a conditional branch. This replaced two separate hand-written comparison structures, inherits lowest-index tie-breaking for free from strict comparisons, and scales to a fourth tank at no cost.
  - **Oil Scheduler** — redesigned around per-node Start/Stop and Reset hardware, with a hard, unconditional release of the line-occupancy lock on the fifth failed Modbus poll. The original scheme could hold the lock indefinitely with no recovery path; the redesign turns two outcomes into three (dispensed / busy-elsewhere / comms-fault-retry), each with its own operator-facing message.

### PLC implementation
- Programmed and documented the full as-built ladder (Program 3.3, Coolmay L10S): I/O mapping, register banding, pointer/subroutine mechanism (Z0–Z5 / P0–P5), sensor scaling and 5-sample averaging, rate-of-change fault detection, the quadratic water-temperature target, heater staging, height-to-mass and Tf thermal blending, tank scoring, LSM/HSM/FSM scheduling, Modbus round-robin to three satellite HMIs, and FIFO-free oil dispensing under a shared line lock.
- Wrote **PLC Guide V3.0**, a single consolidated programming reference merging every block of the V1.1 guide with ADA 3.0's simplified core — with a **Reconciliation Log that resolves every register and logic collision between the two explicitly, rather than flagging it**: M4 keeps its Tf-interlock meaning and the PO-stored flag moves to a new address; the single 0.6 × Level + 0.4 × Temperature scoring formula supersedes the old two-variant incumbent/challenger rule; the quadratic Ttarget law supersedes V1.1's linear rung; Heater Staging becomes the sole driver of the three heater coils, avoiding a two-master conflict with the auxiliary stage register.
- Moved all real-valued arithmetic into the float register family, which removed the 16-bit overflow risk that had forced 32-bit scaling tricks throughout the energy and Tf blocks — same formulas, no scaling.

### Commissioning and calibration
- Authored a **Commissioning Verification Checklist (Rev. 3)** worked through item-by-item with the technician on the live system, with an explicit tolerance policy: ±5% on calculated and analog quantities, **exact match on anything logical** — valve state, latch behaviour, sequencing, which branch fires — because there is no such thing as a 5% correct interlock. A third mark, *Unsatisfactory*, is reserved for test points the PLC Guide does not pin to an exact register, so open questions stay visible instead of being forced into a pass or a fail.
- Authored the **Site Testing & Calibration** procedure covering RTD, ultrasonic level, VFD-to-flowrate, tank geometry, and oil-node dispense-volume calibration — every table written as a template to travel to site and come back filled in.

---

## Engineering Judgment I'm Proud Of

**Scrapped my own data rather than patching it.** The first round of RTD calibration was taken while the sensor value was still drifting toward its settled reading, with no fixed protocol for what counted as "settled" — which is also how a transcription error on one sensor survived to be found later. That data is discarded, not revised. The replacement protocol leads with an explicit steady-state check, and all six sensors are being re-measured from a blank sheet.

**Let the model overrule the previous version of the model.** The 1D radial rebuild showed the coil sits at 80% of the tank radius, not in the middle, and that a cold-started tank spends 6–40 hours in a *dead time* where only ~1.4 kW of a 36 kW heater can reach solid oil — producing **zero usable liquid in a 24-hour winter day**. Carrying the tank over warm from the previous batch removes that dead time entirely and takes ambient temperature almost out of the picture. That finding — that *how the plant is operated* matters more than the weather or the hardware — costs nothing to implement and is now being written into the ladder as a threshold-triggered reheat routine.

**Chose simplicity deliberately, not by default.** The architecture originally specified a 12-register-per-channel fault detection scheme — fully correct, fully tunable. I collapsed it to one ratio-based check repeated ten times, keeping adjustable registers only on the four channels where a bad reading cascades into mass, temperature and priority decisions. Fewer places for a commissioning technician to introduce a bug, in exchange for tunability I judged wasn't earning its complexity.

**Said no to the intuitive fix.** Insulation looks like the obvious answer to a cold tank; my own numbers gave it about 6% more production at cold start, which doesn't justify the cost, so I didn't recommend it. What the simulations kept pointing at instead was the solid oil layer itself — so a slow impeller or even manual agitation stays on the table, and insulation sits below it.

**Treated requirement volatility as a design constraint, not a disruption.** Across five-plus proposal revisions — a new product line, two coil-bore changes, a trunk upsize — the VCH sizing methodology and priority-budget philosophy stayed modular enough that each new requirement extended the framework rather than triggering a rebuild.

**Went outside the datasheet when it ran out.** Modbus configuration across multiple Coolmay HMI stations failed silently with no documented diagnostic path; I resolved it by contacting the manufacturer's own engineer for the register-level configuration rather than guessing.

**Wrote down what I got wrong, and what I can't yet stand behind.** Every document carries its own limitations section: the pipe-resistance network behind the VFD frequencies was only half-modelled when those figures were calculated, and is flagged for on-site verification by whoever commissions it; the PO tank's loss coefficient was linearised around a narrow ΔT and is noted as carrying wider error at the worst-case extreme; the best-case feedstock temperature is labelled an engineering assumption rather than a computed value. Most importantly, I flagged that the heater-staging protection governs automatic mode only and can be bypassed entirely in manual — a 36 kW heater on a 400 L loop leaves very little margin for operator error, and that is better raised as a foreseen problem than a live one.

---

## Documentation Set

| Document | Role |
|---|---|
| ADA — Architecture 3.0 | Control architecture specification (final, locked) |
| ADA — PLC Guide V3.0 | Consolidated programming reference, incl. reconciliation log |
| Nebico Oil Retention — PLC Overview (Program 3.3) | As-built ladder documentation, register map, calibration placeholders |
| ADA — Commissioning Verification Checklist, Rev. 3 | Section-by-section sign-off against the live system |
| ADA — Site Testing & Calibration v1.0 | RTD, ultrasonic, VFD, geometry and oil-node calibration procedure |
| ADA — Thermodynamic Analysis | Worst/normal/best-case throughput, power and solar coverage |
| ADA — Full Analysis (1D Radial Thermal Model) | Pump/circuit characterisation and rebuilt tank thermal model |
| VCH Sizing Framework, 2nd Ed. | Published, generalised sizing methodology ([Zenodo](https://doi.org/10.5281/zenodo.21009246)) |

---

## Status

Architecture locked, PLC program and HMI complete, and the plant is in installation and commissioning — control panel and tanks fabricated, site calibration and verification in progress against the checklist above.

*Full technical documentation available on request.*
