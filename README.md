# Palm Oil Melting & Retention System — Nebico

**Industrial thermal + control systems design for a multi-tank palm oil melting, storage, and trim-heating facility.**
Mechatronics Engineering Pvt. Ltd. (MEPL), Kathmandu — ongoing project, internship role: Junior Automation Design Architect.

A passive solar thermal loop and a 36 kW auxiliary electric immersion array are coordinated by a PLC-driven control architecture — the **Adaptive Demand Allocation Architecture (ADA)** — to melt and hold ≥2 tonnes/day of palm oil across three 10 kL vessels and one 5 kL trim-heating tank, in Kathmandu's 18.1°C ambient. The thermal sizing methodology is generalised into a self-authored, published framework, the **VCH Sizing Framework (2nd Ed.)** ([DOI: 10.5281/zenodo.21009246](https://doi.org/10.5281/zenodo.21009246)).

---

## What I Built

- **Thermal sizing methodology** — derived a closed-form ε-NTU coil-length inversion from a target heat duty, replacing trial-and-error coil sizing; identified that oil-side thermal resistance dominates >95% of total impedance, which redirected the whole design from mechanical tuning (pump velocity, coil bore) toward **algorithmic throughput recovery** — a smarter multi-tank dispatch queue instead of bigger pipes.
- **Control architecture (ADA)** — evolved the plant's control logic across five major revisions, from a simple priority ladder to a genuine three-way concurrent arbiter with a real-time thermal control law, dual-latch anti-chatter heater staging, and a unified tank-scoring formula. Formalised as a four-scheduler model (Operational / Priority / Mathematical / Fault) that cleanly separates *decision* from *action*.
- **PLC implementation** — programmed the full as-built ladder logic (2,948 steps) on a Mitsubishi FX3U: I/O mapping, register map, sensor filtering, thermal control, heater staging, tank scoring, Modbus round-robin communication to three satellite HMIs, and FIFO-based oil dispensing.
- **Validation** — ran worst/normal/best-case thermodynamic scenario analysis; confirmed throughput held within 1% variance across all three conditions, and quantified a peak-demand finding (≈1.7% over the rated auxiliary array) that was carried directly into electrical design.
- **Mathematical frugality** — favored closed-form, single-lookup expressions over multi-step or iterative logic wherever the PLC had to compute something live: a real-time water temperature target derived directly from tank level via a closed-form quadratic ($T_\text{target}(d)$), a dynamic upper thermal safety boundary computed from a weighted-mass energy balance ($T_f$), a single unified tank-scoring formula in place of two earlier ones, and a piecewise, commissioning-calibrated heat-demand function for the PO tank. Each was chosen so the controller produces an answer in one evaluation rather than a chain of dependent calculations.

---

## Engineering Judgment I'm Proud Of

- **Chose simplicity deliberately, not by default.** The architecture originally specified a 12-register-per-channel fault detection scheme — fully correct, fully tunable. I collapsed it to one ratio-based check repeated ten times, keeping adjustable registers only on the four channels (tank levels) where a bad reading actually cascades into mass, temperature, and priority decisions. Fewer places for a commissioning technician to introduce a bug, in exchange for tunability I judged wasn't earning its complexity.
- **Treated requirement volatility as a design constraint, not a disruption.** Across five-plus proposal revisions — a new product line, two coil-bore changes, a trunk upsize — I kept the VCH sizing methodology and priority-budget philosophy modular enough that each new requirement extended the framework rather than triggering a rebuild.
- **Went outside the datasheet when it ran out.** Modbus configuration across multiple Coolmay HMI stations failed silently with no documented diagnostic path; I resolved it by contacting the manufacturer's own engineer for the register-level configuration, rather than guessing.
- **Caught my own architecture's blind spots before they shipped.** Documenting the as-built PLC Guide against the architecture surfaced real gaps — a register collision (M40–M71 vs. M115–M146) that a live register map would have caught immediately, and several open items (E-Stop reset behavior, tie-break rules) now explicitly flagged rather than silently assumed.

---

## Status

Architecture, PLC implementation, and HMI are complete and internally documented (Architecture 2.0.1, PLC Guide 1.1, Thermodynamic Analysis). The project is now in the installation and manufacturing phase — control panel and tanks are being fabricated, with on-site testing coming up soon.

*Full technical documentation — architecture specification, PLC guide, thermodynamic analysis, and revision history — available on request.*
