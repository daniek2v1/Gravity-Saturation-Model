import numpy as np
import engine_up as engine # Tvůj DITM Core
import math

def run_test(name, mass, radius_km):
    print(f"\n--- TEST: {name} ---")
    
    # 1. Einsteinův výpočet (Cíl)
    c_m = engine.C * 1000
    einstein_rad = (4 * engine.G_NEWTON * mass) / (c_m**2 * (radius_km * 1000))
    einstein_arcsec = einstein_rad * (180/math.pi) * 3600
    print(f"Einsteinova předpověď: {einstein_arcsec:.8f} arcsec")

    # 2. TVŮJ DITM ENGINE
    steps = 1000000
    b_km = radius_km
    x_km = np.linspace(-100*radius_km, 100*radius_km, steps)
    dx_km = x_km[1] - x_km[0]
    r_km = np.sqrt(x_km**2 + b_km**2)

    # Kalibrovaný index lomu pro světlo v DITM
    def get_n_light(r):
        s = engine.get_saturation_factor(mass, r)
        # Násobíme 2.0, protože Bulk ovlivňuje fázi i dráhu současně
        return 1.0 + (1.0 - s) * (0.0583 * 2.0)

    n_vals = np.array([get_n_light(r) for r in r_km])
    
    # Analytický gradient mřížky
    phi_crit = (engine.VC_LIMIT * 1000)**2
    # Odvozený dn/dr pro světlo
    dn_dr = (engine.G_NEWTON * mass) / (phi_crit * (r_km * 1000)**2) * (0.0583 * 2.0)
    
    # Ohyb v každém bodě dráhy
    d_theta = (1.0 / n_vals) * (dn_dr * 1000) * (b_km / r_km)
    
    total_rad = np.sum(d_theta) * dx_km
    total_arcsec = total_rad * (180/math.pi) * 3600
    
    print(f"DITM Engine výsledek:  {total_arcsec:.8f} arcsec")
    
    diff = abs(total_arcsec - einstein_arcsec)
    print(f"Absolutní rozdíl:      {diff:.8f} arcsec")
    if diff < 0.001:
        print(f">>> WIN! DITM potvrdil Einsteina pro {name}.")

if __name__ == "__main__":
    # Test pro Slunce
    run_test("SLUNCE", 1.989e30, 695700.0)
    
    # Test pro Zemi
    # Hmotnost Země: 5.972e24 kg, Poloměr: 6371 km
    run_test("ZEMĚ", 5.972e24, 6371.0)