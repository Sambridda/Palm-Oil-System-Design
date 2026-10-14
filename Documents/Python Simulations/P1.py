import numpy as np

# ==========================================
# 1. CONSTANTS & GEOMETRY
# ==========================================
M_oil_total = 9200.0
M_core = M_oil_total * 0.45  
M_shell = M_oil_total * 0.55 

T_melt_start = 31.0
T_melt_end = 41.0
H_fusion = 65000.0   
T_core_max = 45.0    

L_coil = 30.0        
d_in = 0.0409        
d_out = 0.04826      
k_ss = 16.0          
R_f_out = 0.0004     

A_tank = 27.0        
U_tank = 10.0  # Uninsulated

A_interface = 2 * np.pi * 1.0 * 2.3  
r_gap = 0.4 

# ==========================================
# 2. FLUID PROPERTY FUNCTIONS
# ==========================================
def water_props(T):
    rho = 983.0; cp = 4185.0; mu = 0.000466; k = 0.654
    return rho, cp, mu, k, (mu * cp / k)

def oil_props(T):
    if T < T_melt_start:
        return 920.0, 1600.0, 0.1, 0.180
    elif T > T_melt_end:
        cp = 1750.0 + 2.9 * T
        k = 0.174 - 0.00008 * T
        rho = 902.5 - 0.53 * T
        mu = 1.85e-6 * np.exp(3080.0 / (T + 273.15))
        return rho, cp, mu, k
    else:
        cp = 1800.0 + H_fusion / (T_melt_end - T_melt_start)
        return 910.0, cp, 0.05, 0.175

# ==========================================
# 3. HEAT TRANSFER COEFFICIENTS
# ==========================================
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
    rho, cp, mu, k = oil_props(T_oil)
    if T_oil < T_melt_start: return 5.0 
    beta = 0.0007; g = 9.81; d_coil = 1.96; dT = 5.0 
    nu = mu / rho; alpha = k / (rho * cp); Pr = nu / alpha
    Ra = g * beta * dT * (d_coil**3) / (nu * alpha)
    Nu = (0.60 + (0.387 * Ra**(1/6)) / (1 + (0.559/Pr)**(9/16))**(8/27))**2
    return Nu * k / d_coil

def overall_U(m_dot, T_oil_core, T_water_avg):
    h_in = h_internal(m_dot, T_water_avg)
    h_out = h_external(T_oil_core)
    R_in = 1.0 / h_in
    R_wall = (d_out * np.log(d_out/d_in)) / (2 * k_ss)
    U = 1.0 / (R_in + R_wall + R_f_out + 1.0/h_out)
    return U

def oil_conduction_U(T_oil_core, T_oil_shell):
    _, _, _, k_core = oil_props(T_oil_core)
    _, _, _, k_shell = oil_props(T_oil_shell)
    k_avg = (k_core + k_shell) / 2.0
    if T_oil_core > T_melt_end and T_oil_shell > T_melt_end:
        k_eff = k_avg * 10.0 
    else:
        k_eff = k_avg 
    return k_eff / r_gap

# ==========================================
# 4. TRANSIENT SIMULATION LOOP
# ==========================================
def run_simulation(T_amb, flow_rate_m3h, target_time_hr):
    T_core = T_amb 
    T_shell = T_amb
    
    dt = 60.0 
    time_hr = 0.0
    
    m_dot = flow_rate_m3h * 1000 / 3600.0 
    T_water_in = 70.0
    
    total_energy_J = 0.0
    max_dT_water = 0.0
    max_power_kW = 0.0
    
    while time_hr < target_time_hr:
        T_water_avg = (T_water_in + T_core) / 2.0
        rho_w, cp_w, _, _, _ = water_props(T_water_avg)
        
        U_coil = overall_U(m_dot, T_core, T_water_avg)
        NTU = (U_coil * np.pi * d_out * L_coil) / (m_dot * cp_w)
        epsilon = 1 - np.exp(-NTU)
        Q_coil = epsilon * m_dot * cp_w * (T_water_in - T_core)
        
        current_power_kW = Q_coil / 1000.0
        if current_power_kW > max_power_kW: max_power_kW = current_power_kW
        total_energy_J += Q_coil * dt
        
        dT_water = Q_coil / (m_dot * cp_w)
        if dT_water > max_dT_water: max_dT_water = dT_water
        
        U_cond = oil_conduction_U(T_core, T_shell)
        Q_cond = U_cond * A_interface * (T_core - T_shell)
        
        _, cp_core, _, _ = oil_props(T_core)
        dT_core = (Q_coil - Q_cond) * dt / (M_core * cp_core)
        T_core_new = T_core + dT_core
        
        if T_core_new > T_core_max:
            Q_needed_for_cap = (T_core_max - T_core) * M_core * cp_core / dt
            Q_excess = (Q_coil - Q_cond) - Q_needed_for_cap
            T_core = T_core_max
            Q_cond += Q_excess
        else:
            T_core = T_core_new
            
        Q_loss = U_tank * A_tank * (T_shell - T_amb)
        _, cp_shell, _, _ = oil_props(T_shell)
        dT_shell = (Q_cond - Q_loss) * dt / (M_shell * cp_shell)
        T_shell += dT_shell
        
        time_hr += dt / 3600.0
        
    def calc_melted(T, M):
        if T < T_melt_start: return 0.0
        elif T > T_melt_end: return M
        else: return M * (T - T_melt_start) / (T_melt_end - T_melt_start)
        
    melted_core = calc_melted(T_core, M_core)
    melted_shell = calc_melted(T_shell, M_shell)
    total_melted = melted_core + melted_shell
    
    return T_core, T_shell, total_melted, total_energy_J / 3.6e6, max_power_kW, max_dT_water

# ==========================================
# 5. RUN FOR ALL 9 CASES
# ==========================================
conditions = []
for T_amb, time in [(2, 42.39), (18, 43.52), (22, 44.36)]:
    for flow in [1.17, 1.65, 2.0]:
        conditions.append((T_amb, flow, time))

print(f"--- 9-CASE SIMULATION (Capped Core at 45C) ---")
print(f"{'Amb':<4} | {'Flow':<6} | {'Time':<6} | {'Core T':<7} | {'Shell T':<8} | {'Melted (kg)':<12} | {'Total kWh':<10} | {'Max kW':<7} | {'Max dT_w':<8}")
print("-" * 105)

for T_amb, flow, target_time in conditions:
    Tc, Ts, melted, kWh, max_kW, max_dT = run_simulation(T_amb, flow, target_time)
    print(f"{T_amb:<4} | {flow:<6} | {target_time:<6.2f} | {Tc:<7.2f} | {Ts:<8.2f} | {melted:<12.1f} | {kWh:<10.2f} | {max_kW:<7.2f} | {max_dT:<8.2f}")