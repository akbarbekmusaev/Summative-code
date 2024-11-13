import numpy as np
import matplotlib.pyplot as plt

# Define constants
a = 0.09  # inner radius
b = 0.1  # outer radius

# Define the range of r from slightly more than a to b
r = np.linspace(a, b, 500)

# Define new values for p_0
p_0_values = [80e6]  # in Pa

# Initialize plot
plt.rcParams.update({'font.size': 14})
plt.figure(figsize=(12, 8))

# Loop over each p_0 value to plot
for p_0 in p_0_values:
    # Recalculate stress functions with the new p_0
    sigma_rr = ((a**2 * p_0) / (b**2 - a**2)) * (1 - (b**2 / r**2))
    sigma_theta_theta = ((a**2 * p_0) / (b**2 - a**2)) * (1 + (b**2 / r**2))
    sigma_zz = (a**2 * p_0) / (b**2 - a**2) * np.ones_like(r)

    # Plot each stress component for the current p_0 value
    plt.plot(r, sigma_rr, label=rf'$\sigma_{{rr}}$ for $p_0 = {p_0*10**-6}$ MPa')
    plt.plot(r, sigma_theta_theta, label=rf'$\sigma_{{\theta\theta}}$ for $p_0 = {p_0*10**-6}$ MPa')
    plt.plot(r, sigma_zz, label=rf'$\sigma_{{zz}}$ for $p_0 = {p_0*10**-6}$ MPa')
    print(f"p_0 = {p_0} Pa")
    print(f"Max stress in sigma_rr: {max(abs(sigma_rr))} Pa")
    print(f"Max stress in sigma_theta_theta: {max(abs(sigma_theta_theta))} Pa")
    print(f"Max stress in sigma_zz: {max(sigma_zz)} Pa")

# Labels and title
plt.xlabel(r'Radius $r$')
plt.ylabel(r'Stress $\sigma$ (MPa)')
plt.legend()
plt.grid(True)
plt.show()

