import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. CONSTANTS & GEOMETRY
# ==========================================
M_oil_total = 9200.0
N = 100                 # Number of radial shells for oil
R_tank_inner = 1.22     # m
R_coil = 0.98           # m
L_tank = 2.3            # m (cylinder height)
dr = R_tank_inner / N   # Shell thickness (0.0122 m)

# Steel Wall Properties
t_steel = 0.005         # 5mm
R_tank_outer = R_tank_inner + t_steel
rho_steel = 7850.0      # kg/m3
cp_steel = 500.0        # J/kgK
k_steel = 50.0          # W/mK
M_steel = rho_steel * np.pi * (R_tank_outer**2 - R_tank_inner**2) * L_tank

# Oil Properties & Phase Change
T_melt_start = 31.0
T_melt_end = 41.0
H_fusion = 65000.0      # J/kg
cp_solid = 1600.0
cp_liquid = 1900.0

# Coil Geometry
d_in = 0.0409; d_out = 0.04826
L_coil = 30.0
A_coil = np.pi * d_out * L_coil
k_ss = 16.0
R_f_out = 0.0004

# Ambient & Water
T_water_in = 70.0
U_tank_air = 10.0       # W/m2K (uninsulated)
A_tank_outer = 2 * np.pi * R_tank_outer * L_tank + 2 * np.pi * R_tank_outer**2

# ==========================================
# 2. ENTHALPY FUNCTIONS (Phase Change)
# ==========================================
def temp_to_enthalpy(T):
    if T < T_melt_start:
        return cp_solid * T
    elif T <= T_melt_end:
        return cp_solid * T_melt_start + H_fusion * (T - T_melt_start) / 10.0
    else:
        return (cp_solid * T_melt_start + H_fusion + 
                cp_liquid * (T - T_melt_end))

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
    # Effective thermal conductivity (enhanced for liquid natural convection)
    if T < T_melt_start: return 0.180
    elif T > T_melt_end: return 0.170 * 5.0  # x5 multiplier for natural convection
    else:
        frac = get_melt_fraction(T)
        return 0.180 * (1 - frac) + (0.170 * 5.0) * frac

def get_oil_rho_cp(T):
    if T < T_melt_start: return 920.0, cp_solid
    elif T > T_melt_end: 
        rho = 902.5 - 0.53 * T
        cp = 1750.0 + 2.9 * T
        return rho, cp
    else:
        frac = get_melt_fraction(T)
        rho = 920.0 * (1 - frac) + (902.5 - 0.53 * T) * frac
        cp = cp_solid * (1 - frac) + (1750.0 + 2.9 * T) * frac
        return rho, cp

# ==========================================
# 3. HEAT TRANSFER COEFFICIENTS
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

def h_external(T_oil, T_band_water_avg):
    rho, cp = get_oil_rho_cp(T_oil)
    if T_oil < T_melt_start: return 5.0 
    # Use Andrade viscosity for liquid
    mu = 1.85e-6 * np.exp(3080.0 / (T_oil + 273.15))
    k = get_oil_k(T_oil)
    beta = 0.0007; g = 9.81; d_coil = 1.96; dT = 5.0 
    nu = mu / rho; alpha = k / (rho * cp); Pr = nu / alpha
    Ra = g * beta * dT * (d_coil**3) / (nu * alpha)
    Nu = (0.60 + (0.387 * Ra**(1/6)) / (1 + (0.559/Pr)**(9/16))**(8/27))**2
    return Nu * k / d_coil

def calc_Q_coil(m_dot, T_band, T_amb):
    if T_band >= 70.0: return 0.0 # Cap at water inlet temp
    T_water_avg = (T_water_in + T_band) / 2.0
    h_in = h_internal(m_dot, T_water_avg)
    h_out = h_external(T_band, T_water_avg)
    
    R_in = 1.0 / h_in
    R_wall = (d_out * np.log(d_out/d_in)) / (2 * k_ss)
    U = 1.0 / (R_in + R_wall + R_f_out + 1.0/h_out)
    
    # Use NTU-Effectiveness
    rho_w, cp_w, _, _, _ = water_props(T_water_avg)
    NTU = (U * A_coil) / (m_dot * cp_w)
    epsilon = 1 - np.exp(-NTU)
    Q = epsilon * m_dot * cp_w * (T_water_in - T_band)
    return Q

# ==========================================
# 4. TRANSIENT SIMULATION LOOP
# ==========================================
def run_simulation(T_amb, flow_rate_m3h, target_time_hr):
    dt = 60.0 # seconds
    time_hr = 0.0
    m_dot = flow_rate_m3h * 1000 / 3600.0
    
    # Initialize Grid
    T_oil = np.ones(N) * T_amb
    H_oil = np.array([temp_to_enthalpy(t) for t in T_oil])
    T_steel = T_amb
    
    # Coil index
    coil_idx = int(R_coil / dr)
    
    while time_hr < target_time_hr:
        # 1. Calculate Heat from Coil
        Q_coil = calc_Q_coil(m_dot, T_oil[coil_idx], T_amb)
        
        # 2. Distribute 50/50 Inward and Outward
        # Inward goes to coil_idx - 1, Outward goes to coil_idx + 1
        # (We add to enthalpy directly)
        dH_in = (0.5 * Q_coil * dt) / (np.pi * ((coil_idx*dr)**2 - ((coil_idx-1)*dr)**2) * L_tank * 920.0)
        dH_out = (0.5 * Q_coil * dt) / (np.pi * (((coil_idx+1)*dr)**2 - (coil_idx*dr)**2) * L_tank * 920.0)
        
        H_oil[coil_idx - 1] += dH_in
        H_oil[coil_idx + 1] += dH_out
        
        # 3. Radial Conduction between Oil Shells
        # Using explicit finite difference
        for i in range(1, N-1):
            k_i = get_oil_k(T_oil[i])
            k_ip1 = get_oil_k(T_oil[i+1])
            k_avg = (k_i + k_ip1) / 2.0
            
            r_face = i * dr
            A_face = 2 * np.pi * r_face * L_tank
            
            # Fourier's Law
            Q_cond = k_avg * A_face * (T_oil[i] - T_oil[i+1]) / dr
            
            # Update Enthalpy (Q_in - Q_out)
            # Mass of shell i
            m_shell = np.pi * (((i+0.5)*dr)**2 - ((i-0.5)*dr)**2) * L_tank * 920.0
            H_oil[i] -= (Q_cond * dt) / m_shell
            H_oil[i+1] += (Q_cond * dt) / m_shell
            
        # 4. Center Boundary (r=0) - Insulated
        # No heat flow at i=0
        
        # 5. Outer Boundary (Oil to Steel)
        # Conduction from last oil shell to steel wall
        k_last = get_oil_k(T_oil[-1])
        A_outer_oil = 2 * np.pi * R_tank_inner * L_tank
        Q_oil_to_steel = k_last * A_outer_oil * (T_oil[-1] - T_steel) / (dr/2)
        
        m_last = np.pi * (((N-0.5)*dr)**2 - ((N-1.5)*dr)**2) * L_tank * 920.0
        H_oil[-1] -= (Q_oil_to_steel * dt) / m_last
        
        # 6. Steel Wall Energy Balance
        Q_steel_to_air = U_tank_air * A_tank_outer * (T_steel - T_amb)
        dT_steel = (Q_oil_to_steel - Q_steel_to_air) * dt / (M_steel * cp_steel)
        T_steel += dT_steel
        
        # 7. Convert Enthalpy back to Temperature
        for i in range(N):
            T_oil[i] = enthalpy_to_temp(H_oil[i])
            
        time_hr += dt / 3600.0
        
    # ==========================================
    # 5. POST-PROCESSING: MASS & TEMP CLASSIFICATION
    # ==========================================
    solid_mass, slurry_mass, liquid_mass = 0.0, 0.0, 0.0
    solid_T_sum, slurry_T_sum, liquid_T_sum = 0.0, 0.0, 0.0
    
    for i in range(N):
        # Mass of shell i
        m_shell = np.pi * (((i+0.5)*dr)**2 - ((i-0.5)*dr)**2) * L_tank * 920.0
        T = T_oil[i]
        if T < T_melt_start:
            solid_mass += m_shell
            solid_T_sum += T * m_shell
        elif T <= T_melt_end:
            slurry_mass += m_shell
            slurry_T_sum += T * m_shell
        else:
            liquid_mass += m_shell
            liquid_T_sum += T * m_shell
            
    avg_solid_T = solid_T_sum / solid_mass if solid_mass > 0 else 0
    avg_slurry_T = slurry_T_sum / slurry_mass if slurry_mass > 0 else 0
    avg_liquid_T = liquid_T_sum / liquid_mass if liquid_mass > 0 else 0
    
    return (solid_mass, avg_solid_T, 
            slurry_mass, avg_slurry_T, 
            liquid_mass, avg_liquid_T, 
            T_steel, T_oil)

# ==========================================
# 6. RUN FOR THE SPECIFIED CASES
# ==========================================
cases = [
    (2, 1.65, 24.0, "Tank 1 (24 hrs)"),
    (2, 1.65, 18.39, "Tank 2 (18.39 hrs)"),
    (18, 1.65, 24.0, "Tank 1 (24 hrs)"),
    (18, 1.65, 19.52, "Tank 2 (19.52 hrs)"),
    (22, 1.65, 24.0, "Tank 1 (24 hrs)"),
    (22, 1.65, 20.36, "Tank 2 (20.36 hrs)")
]

print(f"--- 1D RADIAL ENTHALPY MODEL (100 Shells + Steel Wall) ---")
print(f"{'Case':<20} | {'Solid (kg)':<12} | {'Slurry (kg)':<12} | {'Liquid (kg)':<12} | {'T_steel':<8}")
print("-" * 80)

for T_amb, flow, time_hr, label in cases:
    sm, st, slm, slt, lm, lt, T_steel, T_profile = run_simulation(T_amb, flow, time_hr)
    print(f"{label:<20} | {sm:<12.0f} | {slm:<12.0f} | {lm:<12.0f} | {T_steel:<8.2f}")
    print(f"  {'':<20} | Avg T: {st:<5.1f}C | Avg T: {slt:<5.1f}C | Avg T: {lt:<5.1f}C |")
    print("-" * 80)