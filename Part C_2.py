import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Given constants
D = 0.2  # outer diameter in meters
t = 0.01  # wall thickness in meters
ri = D / 2 - t  # inner radius in meters
ro = D / 2  # outer radius in meters
K_IC = 90e6  # fracture toughness in Pa * sqrt(m)
C = 1e-36  # Paris law constant in m/cycle (Pa sqrt(m))^m
m = 4  # Paris' law exponent
a0 = 0.00422  # assumed detection parameter from appendix in meters (example value)
nu = 0.3  # Poisson's ratio
target_failure_prob = 0.01 # target probability of failure

# stress and crack sizes
a_min = (-np.log(1-0.99))**0.25 * a0
def a_max(p):
    return (K_IC / sigma(p)) ** 2 / np.pi

def sigma(p):
    return (p * ri ** 2) / (ro ** 2 - ri ** 2)

# Stress intensity factor range calculation function
def delta_k(a, p):
    if a <= t:
        Y = 0.728 + 0.373 * (a / t) ** 2 - 0.029 * (a / t) ** 4
    else:
        Y = 1
    return Y * sigma(p) * np.sqrt(np.pi * a)

# Crack growth rate function (da/dN)
def crack_growth_rate(a, p):
    return C * (delta_k(a, p) ** m)

# Paris' law integration for a given initial crack size and inspection interval
def crack_growth(a_initial, a_final, p):
    def integrand(a):
        return (1 / crack_growth_rate(a, p))
    cycles, _ = quad(integrand, a_initial, a_final)
    return cycles

# Probability of Detection function
def probability_of_detection(a):
    return 1 - np.exp(-(a / a0) ** 4)

def LEFM_limit(a):
    return K_IC / delta_k(a)

def plot_crack_growth():
    a_initial = a_min  # initial crack size in meters
    a_final_1 = t  # first final crack size in meters
    a_final_2 = a_max  # second final crack size in meters

    # Create arrays for plotting
    a_values_1 = np.linspace(0.001, a_final_1, 200)
    a_values_2 = np.linspace(0.001, a_final_2, 200)
    cycles_values_1 = [crack_growth(a, a_final_1) for a in a_values_1]
    cycles_values_2 = [crack_growth(a, a_final_2) for a in a_values_2]

    # Plotting first graph
    plt.figure(figsize=(7, 6))
    plt.plot(a_values_1 * 1e3, cycles_values_1, color='blue')
    plt.xlabel('Existing crack Size (mm)')
    plt.ylabel('Cycles')
    plt.grid(True)
    plt.show()

    # Plotting second graph
    plt.figure(figsize=(7, 6))
    plt.plot(a_values_2 * 1e3, cycles_values_2, color='red')
    plt.xlabel('Existing crack Size (mm)')
    plt.ylabel('Cycles')
    plt.grid(True)
    plt.show()

def plot_crack_growth_probability():
    a_initial = a_min  # initial crack size in meters
    a_final_1 = t  # first final crack size in meters
    a_final_2 = a_max  # second final crack size in meters

    # Create arrays for plotting
    a_values_1 = np.linspace(0.001, a_final_1, 200)
    a_values_2 = np.linspace(0.001, a_final_2, 200)
    cycles_values_1 = [crack_growth(a, a_final_1) for a in a_values_1]
    cycles_values_2 = [crack_growth(a, a_final_2) for a in a_values_2]
    prob_values_1 = [1 - probability_of_detection(a) for a in a_values_1]
    prob_values_2 = [1 - probability_of_detection(a) for a in a_values_2]

    # Find intersection points
    intersection_1 = next((cycles for cycles, prob in zip(cycles_values_1, prob_values_1) if prob <= target_failure_prob), None)
    intersection_2 = next((cycles for cycles, prob in zip(cycles_values_2, prob_values_2) if prob <= target_failure_prob), None)

    print(f"Intersection point for Leak: {intersection_1} cycles")
    print(f"Intersection point for Fracture: {intersection_2} cycles")

    # Plotting combined graph with flipped axes
    plt.figure(figsize=(7, 6))
    plt.plot(cycles_values_1, prob_values_1, label='Leak', color='blue')
    plt.plot(cycles_values_2, prob_values_2, label='Fracture', color='red')
    plt.axhline(y=target_failure_prob, color='green', linestyle='--', label='0.01 probability of failure')
    plt.ylabel('Probability of failure')
    plt.xlabel('Cycles (Inspection Interval)')
    plt.legend()
    plt.show()

    # Plotting second graph with adjusted limits
    plt.figure(figsize=(7, 6))
    plt.plot(cycles_values_1, prob_values_1, label='Leak', color='blue')
    plt.plot(cycles_values_2, prob_values_2, label='Fracture', color='red')
    plt.axhline(y=target_failure_prob, color='green', linestyle='--', label='0.01 probability of failure')
    plt.ylabel('Probability of failure')
    plt.xlabel('Cycles (Inspection Interval)')
    plt.xlim(0, 50000)  # Adjust x-axis limit
    plt.ylim(0, 0.1)  # Adjust y-axis limit
    plt.grid(True)
    plt.show()

# Function to plot KI as a function of crack size for different internal pressures
def plot_ki_vs_crack_size():
    pressures = [40e6, 80e6]
    a_values = np.linspace(0.001, 0.1, 200)  # crack sizes in meters
    plt.figure(figsize=(10, 6))
    for p in pressures:
        SF = [K_IC/delta_k(a, p) for a in a_values]
        plt.plot(a_values * 1e3, SF, label=f'Pressure = {p / 1e6} MPa')

    plt.xlabel('Crack Size (mm)')
    plt.ylabel('Safety factor against K_IC')
    plt.axhline(y=1, color='red', linestyle='--', label='Safety factor of 1')
    plt.axvline(x=t*1e3, color='green', linestyle='--', label='Wall Thickness (t)')
    plt.legend()
    plt.grid(True)
    plt.show()

p = 40e6
print(sigma(p))
print("a_min", a_min)
print("a_max", a_max(p))
print("crack_growth", crack_growth(a_min, a_max(p), p))