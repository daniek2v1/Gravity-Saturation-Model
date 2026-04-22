import math

"""
DITM CORE ENGINE v2.1 - "Stability & Grid Viscosity"
A numerical framework for modeling gravity as an interaction within a 
dense spatial grid (The Bulk). 

Designed to address:
- Galaxy Rotation Curves (Propeller Effect)
- Kinetic Anomalies (Flyby/Pioneer)
- Singularity Prevention (Saturation)
"""

# --- FUNDAMENTAL GRID CONSTANTS ---
C = 299792.458  # Speed of light (km/s)
G_NEWTON = 6.67430e-11
EARTH_DENSITY = 5515.0
EARTH_RADIUS_KM = 6371.0

# ZETA: Grid viscosity constant. 
# Derived from Earth's density/geometry ratio as a baseline.
ZETA = (EARTH_DENSITY / (EARTH_RADIUS_KM * 1e6)) * G_NEWTON * 12.0 

# VC_LIMIT: The interaction ceiling of the spatial grid.
# Derived from the geometric ratio of linear propagation vs grid node topology.
VC_LIMIT = C / (1 + math.pi)  # Approx. 83424.62 km/s

def get_saturation_factor(mass, radius_km):
    """
    Grid Saturation Regulator (S).
    As field potential approaches the hardware limit (VC_LIMIT), 
    the grid's permeability for gravity begins to close smoothly.
    """
    r_m = radius_km * 1000
    phi = (G_NEWTON * mass) / r_m
    phi_crit = (VC_LIMIT * 1000)**2 
    
    # Saturation curve to prevent infinite acceleration values
    return 1 / (1 + (phi / phi_crit))

def get_interaction_ratio(velocity_kms):
    """
    Interaction Velocity Index (IV). 
    Protects the grid from velocity-induced 'overflow'.
    """
    ratio = velocity_kms / VC_LIMIT
    if ratio >= 1.0: return 0.0
    return math.sqrt(1 - ratio**2)

def calculate_gravity_force(mass, radius_km, distance_km, v_rot, v_orb, density_kgm3, mag_field_t=0):
    """
    Main DITM Gravitational Kernel.
    Formula: (Newton * Interaction Index * Grid Saturation) + Bulk Drag.
    """
    dist_m = distance_km * 1000
    total_v = math.sqrt(v_rot**2 + v_orb**2)
    
    # 1. BASE NEWTONIAN FORCE (Deformation component)
    g_base = (G_NEWTON * mass) / (dist_m**2)
    
    # 2. DITM CORE CORRECTIONS
    iv = get_interaction_ratio(total_v)
    s = get_saturation_factor(mass, radius_km)
    
    # 3. PROPELLER EFFECT (Bulk Grid Drag)
    # The rotating core 'stirs' the Bulk medium, providing extra orbital stability.
    # Scaled by intergalactic vacuum density coefficient (0.5e-13).
    spin_ratio = total_v / VC_LIMIT
    bulk_drift = ZETA * spin_ratio * dist_m * 0.5e-13
    
    # 4. AUXILIARY FACTORS (Magnetism and sync slip)
    sync = (v_rot * v_orb) / (VC_LIMIT**2)
    mag_slip = get_magnetic_shield_factor(mag_field_t, radius_km)
    
    # SYNTHESIS
    return (g_base * iv * s * (1 - sync) + bulk_drift) / (1 + mag_slip)

def get_magnetic_shield_factor(magnetic_field_tesla, radius_km):
    """Local grid relaxation induced by high-intensity magnetic fields."""
    if magnetic_field_tesla <= 0: return 0
    return math.log1p((magnetic_field_tesla * radius_km) / 1000.0) * 0.01

def get_time_dilation(g_accel, distance_km, velocity_kms):
    """Calculates time dilation based on gravity and Bulk-velocity interaction."""
    dist_m = distance_km * 1000
    phi = g_accel * dist_m
    c_m = C * 1000
    iv = get_interaction_ratio(velocity_kms)
    
    val = 1 - (2 * phi * iv / (c_m**2))
    return math.sqrt(max(0, val))

def get_event_horizon_radius(mass):
    """
    Event Horizon Radius (DITM Rip Radius).
    Defines the point where grid saturation reaches 99.9%.
    """
    phi_crit = (VC_LIMIT * 1000)**2
    rip_radius_m = (G_NEWTON * mass) / (999 * phi_crit)
    return rip_radius_m / 1000