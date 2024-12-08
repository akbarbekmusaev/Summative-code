import numpy as np
from scipy.optimize import root_scalar
from scipy.integrate import quad
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# Given constants
D = 0.2  # outer diameter in meters
t = 0.01  # wall thickness in meters
ri = D / 2 - t  # inner radius in meters
ro = D / 2  # outer radius in meters
p_max = 40e6  # max pressure in Pascals (MPa to Pa)
K_IC = 90e6  # fracture toughness in Pa * sqrt(m)
C = 1e-36  # Paris law constant in m/cycle (Pa sqrt(m))^m
m = 4  # Paris' law exponent
a0 = 0.00422  # assumed detection parameter from appendix in meters (example value)
a_initial = 0.001  # initial crack size in meters (example)
nu = 0.3  # Poisson's ratio
target_failure_prob = 0.01 # target probability of failure
sigma_y = 1500e6  # Example value for σ_y

# Pipe axial stress
sigma = (p_max * ri ** 2) / (ro ** 2 - ri ** 2)

# Final crack length from Kic
a_max = (K_IC ** 2) / (np.pi * (sigma ** 2))

# Stress intensity factor range calculation function
def delta_k(a):
    if a <= t:
        Y = 0.728 + 0.373 * (a / t) ** 2 - 0.029 * (a / t) ** 4
    else:
        Y = 1
    return Y * sigma * np.sqrt(np.pi * a)

# Crack growth rate function (da/dN)
def crack_growth_rate(a):
    return C * (delta_k(a) ** m)

# Paris' law integration for a given initial crack size and inspection interval
def crack_growth(a_initial, a_final):
    def integrand(a):
        return (1 / crack_growth_rate(a))
    cycles, _ = quad(integrand, a_initial, a_final)
    return cycles

# Probability of Detection function
def probability_of_detection(a):
    return 1 - np.exp(-(a / a0) ** 4)

#LEFM limit
def LEFM_limit():
    # Define a range of values for `a` from 0 to `t`
    a_values = np.linspace(0, 0.01, 500)

    # Calculate the stress intensity factor
    K_I = np.array([delta_k(a) for a in a_values])

    # Calculate the right side of the inequality
    rhs = (4 / np.pi) * (K_I / sigma_y) ** 2

    # Plotting
    plt.plot(a_values, rhs, label=r'$\frac{4}{\pi} \left( \frac{K_I}{\sigma_y} \right)^2$', color='blue')
    # plt.plot(a_values, a_values, label=r'$a$', color='red')
    # plt.plot(a_values, t - a_values, label=r'$t - a$', color='green')

    # Shading the feasible region
    #plt.fill_between(a_values, rhs, t, where=(a_values >= rhs) & ((t - a_values) >= rhs), color='green', alpha=0.3)

    # Labeling
    plt.xlabel("a")
    plt.ylabel("Value")
    plt.title("Plot of the Inequality")
    plt.legend()
    plt.grid(True)
    plt.show()

ai = 0.00618
af = 0.01
print("crack growth from initial crack size to final crack size: ", crack_growth(ai, af))