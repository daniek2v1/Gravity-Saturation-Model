import sys
import os
import math

# 1. Setup paths to include the engine directory
bench_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(bench_dir)
sys.path.insert(0, os.path.join(project_root, 'engine'))

try:
    import engine_up as engine
    print(f"--- DITM ENGINE LOADED SUCCESSFULLY (v2.1 Propeller) ---")
    print(f"VC_LIMIT (Grid Interaction Ceiling): {engine.VC_LIMIT:.2f} km/s")
except ModuleNotFoundError:
    print("\n--- IMPORT ERROR: engine_up.py not found in the same directory ---")
    sys.exit()

# --- CELESTIAL OBJECTS TEST ---
subjects = [
    {"name": "Sun (DITM Star)", "mass": 1.989e30, "radius": 696340, "density": 1408, "v_rot": 1.997, "v_orb": 220.0, "mag_field": 0.0001},
    {"name": "Earth", "mass": 5.972e24, "radius": 6371, "density": 5515, "v_rot": 0.465, "v_orb": 29.78, "mag_field": 0.000032},
    {"name": "Jupiter", "mass": 1.898e27, "radius": 69911, "density": 1326, "v_rot": 12.6, "v_orb": 13.07, "mag_field": 0.000427},
    {"name": "Mars", "mass": 6.39e23, "radius": 3389, "density": 3933, "v_rot": 0.241, "v_orb": 24.07, "mag_field": 0.0},
    {"name": "Dense Earth (0.5x Radius)", "mass": 5.972e24, "radius": 3185, "density": 44120, "v_rot": 10.0, "v_orb": 29.78},
    {"name": "Neutron Star (DITM)", "mass": 1.989e30 * 1.4, "radius": 10, "density": 4e17, "v_rot": 70000.0, "v_orb": 200.0, "mag_field": 1000000.0}
]

print(f"\n{'Object':<30} | {'Saturation %':<12} | {'Gravity (m/s²)'}")
print("-" * 75)
for obj in subjects:
    s_factor = engine.get_saturation_factor(obj["mass"], obj["radius"])
    g = engine.calculate_gravity_force(obj["mass"], obj["radius"], obj["radius"], obj["v_rot"], obj["v_orb"], obj["density"])
    print(f"{obj['name']:<30} | {s_factor*100:<12.4f} | {g:.4f}")

# --- GALAXY ROTATION TEST ---
def simulate_galaxy_rotation(distance_ly):
    dist_km = distance_ly * 9.461e+12
    galaxy_mass_inside = 1.0e11 * 1.989e30 * (distance_ly / 50000)
    v_newton = math.sqrt((engine.G_NEWTON * galaxy_mass_inside) / (dist_km * 1000)) / 1000
    
    g_ditm = engine.calculate_gravity_force(galaxy_mass_inside, dist_km * 0.1, dist_km, 250.0, 220.0, 1000)
    v_ditm = math.sqrt(g_ditm * dist_km * 1000) / 1000
    return v_newton, v_ditm

dist = 50000
vn, vd = simulate_galaxy_rotation(dist)
print(f"\n--- GALAXY ROTATION SIMULATION ({dist} ly) ---")
print(f"Newtonian Velocity (No DM): {vn:.2f} km/s")
print(f"DITM Velocity (Bulk Drag):   {vd:.2f} km/s | Boost: +{((vd-vn)/vn)*100:.2f}%")

# --- PROBE ANOMALY BENCHMARK ---
def simulate_probe(name, alt_km, v_kms):
    e_mass = 5.972e24
    e_r = 6371
    dist_m = (e_r + alt_km) * 1000
    g_newton = (engine.G_NEWTON * e_mass) / (dist_m**2)
    g_ditm = engine.calculate_gravity_force(e_mass, e_r, e_r + alt_km, 0.465, v_kms, 5515)
    
    # Anomaly is the difference in acceleration expressed in mm/s^2
    return (g_ditm - g_newton) * 1000

probes = [
    {"name": "Pioneer 10 (Deep Space)", "alt": 1000000, "v": 12.0},
    {"name": "NEAR Shoemaker (Flyby)", "alt": 539, "v": 12.7},
    {"name": "Galileo (Flyby I)", "alt": 960, "v": 13.7},
    {"name": "Rosetta (Flyby)", "alt": 1954, "v": 10.5}
]

print(f"\n--- HISTORICAL PROBE ANOMALIES (DITM REPLICATION) ---")
print(f"{'Probe Name':<25} | {'Altitude':<10} | {'DITM Drift (mm/s²)'}")
print("-" * 75)
for p in probes:
    drift = simulate_probe(p["name"], p["alt"], p["v"])
    print(f"{p['name']:<25} | {p['alt']:<10} | {drift:.10f}")