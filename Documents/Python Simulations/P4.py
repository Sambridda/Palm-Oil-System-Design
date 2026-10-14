import numpy as np

# ==========================================
# 1. CONSTANTS & GEOMETRY
# ==========================================
N = 100
R_tank_inner = 1.22
R_coil = 0.98
L_tank = 2.3
dr = R_tank_inner / N

# Steel Wall
t_steel = 0.005
R_tank_outer = R_tank_inner + t_steel
rho_steel = 7850.0
cp_steel = 500.0
M_steel = rho_steel * np.pi * (R_tank_outer**2 - R_tank_inner**2) * L_tank

# Oil
T_melt_start = 31.0
T_melt_end = 41.0
H_fusion = 65000.0
cp_solid = 1600.0
cp_liquid = 1900.0

# Coil
d_in = 0.0409
d_out = 0.04826
L_coil = 30.0
A_coil = np.pi * d_out * L_coil
k_ss = 16.0
R_f_out = 0.0004

# Water
T_water_in = 70.0

# ==========================================
# 2. INSULATION TOGGLE
# ==========================================
INSULATED = False
if INSULATED:
    U_tank_air = 0.7
    print("--- INSULATION: ON (U=0.7 W/m2K) ---")
else:
    U_tank_air = 10.0
    print("--- INSULATION: OFF (bare steel, U=10 W/m2K) ---")

A_tank_outer = 2 * np.pi * R_tank_outer * L_tank + 2 * np.pi * R_tank_outer**2

# ==========================================
# 3. ENTHALPY FUNCTIONS
# ==========================================
def temp_to_enthalpy(T):
    if T < T_melt_start:
        return cp_solid * T
    elif T <= T_melt_end:
        return cp_solid * T_melt_start + H_fusion * (T - T_melt_start) / 10.0
    else:
        return cp_solid * T_melt_start + H_fusion + cp_liquid * (T - T_melt_end)

def enthalpy_to_temp(H):
    H_solidus = cp_solid * T_melt_start
    H_liquidus = H_solidus + H_fusion
    if H < H_solidus:
        return H / cp_solid
    elif H <= H_liquidus:
        return T_melt_start + 10.0 * (H - H_solidus) / H_fusion
    else:
        return T_melt_end + (H - H_liquidus) / cp_liquid

def get_melt_fraction(T):
    if T < T_melt_start: return 0.0
    elif T > T_melt_end: return 1.0
    else: return (T - T_melt_start) / 10.0

def get_oil_k(T):
    if T < T_melt_start: return 0.180
    elif T > T_melt_end: return 0.170 * 5.0
    else:
        frac = get_melt_fraction(T)
        return 0.180 * (1 - frac) + (0.170 * 5.0) * frac

def get_oil_rho_cp(T):
    if T < T_melt_start:
        return 920.0, cp_solid
    elif T > T_melt_end:
        return 902.5 - 0.53 * T, 1750.0 + 2.9 * T
    else:
        frac = get_melt_fraction(T)
        rho = 920.0 * (1 - frac) + (902.5 - 0.53 * T) * frac
        cp = cp_solid * (1 - frac) + (1750.0 + 2.9 * T) * frac
        return rho, cp

# ==========================================
# 4. HEAT TRANSFER COEFFICIENTS
# ==========================================
def water_props(T):
    rho = 983.0; cp = 4185.0; mu = 0.000466; k = 0.654
    return rho, cp, mu, k, (mu * cp / k)

def h_internal(m_dot, T_water):
    rho, cp, mu, k, Pr = water_props(T_water)
    v = m_dot / (rho * np.pi * (d_in/2)**2)
    Re = rho * v * d_in / mu
    if Re > 10000:
        f = (0.79 * np.log(Re) - 1.64)**-2
        Nu = (f/8) * (Re - 1000) * Pr / (1 + 2.17 * np.sqrt(f/8) * (Pr**(2/3) - 1))
        Nu *= (1 + (d_in/1.96)**0.9)
    else:
        Nu = 4.36
    return Nu * k / d_in

def h_external(T_oil):
    rho, cp = get_oil_rho_cp(T_oil)
    if T_oil < T_melt_start: return 5.0
    mu = 1.85e-6 * np.exp(3080.0 / (T_oil + 273.15))
    k = get_oil_k(T_oil)
    beta = 0.0007; g = 9.81; d_coil = 1.96; dT = 5.0
    nu = mu / rho; alpha = k / (rho * cp); Pr = nu / alpha
    Ra = g * beta * dT * (d_coil**3) / (nu * alpha)
    Nu = (0.60 + (0.387 * Ra**(1/6)) / (1 + (0.559/Pr)**(9/16))**(8/27))**2
    return Nu * k / d_coil

def calc_Q_coil(m_dot, T_band, T_amb):
    if T_band >= 70.0: return 0.0
    T_water_avg = (T_water_in + T_band) / 2.0
    h_in = h_internal(m_dot, T_water_avg)
    h_out = h_external(T_band)
    R_in = 1.0 / h_in
    R_wall = (d_out * np.log(d_out/d_in)) / (2 * k_ss)
    U = 1.0 / (R_in + R_wall + R_f_out + 1.0/h_out)
    rho_w, cp_w, _, _, _ = water_props(T_water_avg)
    NTU = (U * A_coil) / (m_dot * cp_w)
    epsilon = 1 - np.exp(-NTU)
    return epsilon * m_dot * cp_w * (T_water_in - T_band)

# ==========================================
# 5. SIMULATION WITH 4-TON TRACKING
# ==========================================
def run_simulation(T_amb, flow_rate_m3h, max_time_hr, T_initial=None, target_liquid_kg=None):
    if T_initial is None:
        T_initial = T_amb

    dt = 60.0
    time_hr = 0.0
    m_dot = flow_rate_m3h * 1000 / 3600.0

    T_oil = np.ones(N) * T_initial
    H_oil = np.array([temp_to_enthalpy(t) for t in T_oil])
    T_steel = T_initial

    coil_idx = int(R_coil / dr)

    # Track time to reach target liquid mass
    time_to_target = None

    while time_hr < max_time_hr:
        # --- Coil Heat ---
        Q_coil = calc_Q_coil(m_dot, T_oil[coil_idx], T_amb)

        m_in = np.pi * (((coil_idx*dr)**2 - ((coil_idx-1)*dr)**2)) * L_tank * 920.0
        m_out = np.pi * (((coil_idx+1)*dr)**2 - (coil_idx*dr)**2) * L_tank * 920.0
        H_oil[coil_idx - 1] += (0.5 * Q_coil * dt) / m_in
        H_oil[coil_idx + 1] += (0.5 * Q_coil * dt) / m_out

        # --- Radial Conduction ---
        for i in range(1, N-1):
            k_i = get_oil_k(T_oil[i])
            k_ip1 = get_oil_k(T_oil[i+1])
            k_avg = (k_i + k_ip1) / 2.0
            r_face = i * dr
            A_face = 2 * np.pi * r_face * L_tank
            Q_cond = k_avg * A_face * (T_oil[i] - T_oil[i+1]) / dr
            m_shell = np.pi * (((i+0.5)*dr)**2 - ((i-0.5)*dr)**2) * L_tank * 920.0
            H_oil[i] -= (Q_cond * dt) / m_shell
            H_oil[i+1] += (Q_cond * dt) / m_shell

        # --- Outer Boundary ---
        k_last = get_oil_k(T_oil[-1])
        A_outer_oil = 2 * np.pi * R_tank_inner * L_tank
        Q_oil_to_steel = k_last * A_outer_oil * (T_oil[-1] - T_steel) / (dr/2)
        m_last = np.pi * (((N-0.5)*dr)**2 - ((N-1.5)*dr)**2) * L_tank * 920.0
        H_oil[-1] -= (Q_oil_to_steel * dt) / m_last

        # --- Steel Wall ---
        Q_steel_to_air = U_tank_air * A_tank_outer * (T_steel - T_amb)
        T_steel += (Q_oil_to_steel - Q_steel_to_air) * dt / (M_steel * cp_steel)

        # --- Enthalpy → Temp ---
        for i in range(N):
            T_oil[i] = enthalpy_to_temp(H_oil[i])

        time_hr += dt / 3600.0

        # --- Check if target liquid mass reached ---
        if target_liquid_kg is not None and time_to_target is None:
            liquid_mass_now = 0.0
            for i in range(N):
                if T_oil[i] > T_melt_end:
                    m_shell = np.pi * (((i+0.5)*dr)**2 - ((i-0.5)*dr)**2) * L_tank * 920.0
                    liquid_mass_now += m_shell
            if liquid_mass_now >= target_liquid_kg:
                time_to_target = time_hr

    # --- Final State ---
    solid_mass, slurry_mass, liquid_mass = 0.0, 0.0, 0.0
    solid_T_sum, slurry_T_sum, liquid_T_sum = 0.0, 0.0, 0.0
    for i in range(N):
        m_shell = np.pi * (((i+0.5)*dr)**2 - ((i-0.5)*dr)**2) * L_tank * 920.0
        T = T_oil[i]
        if T < T_melt_start:
            solid_mass += m_shell; solid_T_sum += T * m_shell
        elif T <= T_melt_end:
            slurry_mass += m_shell; slurry_T_sum += T * m_shell
        else:
            liquid_mass += m_shell; liquid_T_sum += T * m_shell

    return (solid_mass, solid_T_sum/solid_mass if solid_mass > 0 else 0,
            slurry_mass, slurry_T_sum/slurry_mass if slurry_mass > 0 else 0,
            liquid_mass, liquid_T_sum/liquid_mass if liquid_mass > 0 else 0,
            T_steel, time_to_target)

# ==========================================
# 6. RUN CARRYOVER CASES (NO INSULATION)
# ==========================================
print("\n--- CARRYOVER START (30C) - NO INSULATION ---")
print(f"{'Case':<20} | {'Solid':<8} | {'Slurry':<8} | {'Liquid':<8} | {'T_steel':<8} | {'Time to 4 tons':<15}")
print("-" * 90)

cases = [
    (2,  1.17, 48.0, "Carry 2C"),
    (8,  1.17, 48.0, "Carry 8C"),
    (10, 1.17, 48.0, "Carry 10C"),
    (13, 1.17, 48.0, "Carry 13C"),
    (18, 1.17, 48.0, "Carry 18C"),
    (22, 1.17, 48.0, "Carry 22C"),
]

for T_amb, flow, max_hr, label in cases:
    (sm, st, slm, slt, lm, lt, T_steel, t_4t) = run_simulation(
        T_amb, flow, max_hr, T_initial=30.0, target_liquid_kg=4000.0
    )
    t_str = f"{t_4t:.2f} hrs" if t_4t is not None else "Not reached"
    print(f"{label:<20} | {sm:<8.0f} | {slm:<8.0f} | {lm:<8.0f} | {T_steel:<8.2f} | {t_str:<15}")
    print(f"{'':<20} | AvgT:{st:<4.1f}C | AvgT:{slt:<4.1f}C | AvgT:{lt:<4.1f}C |")
    print("-" * 90)