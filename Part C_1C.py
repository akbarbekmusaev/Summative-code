import numpy as np
import matplotlib.pyplot as plt
def plot_tresca_equivalent_stress(sigma_x, sigma_y, theta_deg, sigma_p_max, num_points=100):
    # Convert angle to radians
    theta = theta_deg * (np.pi / 180)

    # Compute cosine and sine of theta
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    # Range of sigma_p values
    sigma_p_values = np.linspace(-sigma_p_max, sigma_p_max, num_points)

    # Arrays to store Tresca equivalent stress results
    tresca_stresses = []

    # Calculate Tresca stress for each sigma_p
    for sigma_p in sigma_p_values:
        # Compute transformed components due to sigma_p at the given angle
        sigma_px = (3/4) * sigma_p
        sigma_py = (1/4) * sigma_p
        tau_pxy = (np.sqrt(3)/4) * sigma_p

        # Total stress tensor components
        sigma_xx_total = sigma_x + sigma_px
        sigma_yy_total = sigma_y + sigma_py
        tau_xy_total = tau_pxy

        # Compute principal stresses
        avg_normal_stress = (sigma_xx_total + sigma_yy_total) / 2
        radius = np.sqrt(((sigma_xx_total - sigma_yy_total) / 2)**2 + tau_xy_total**2)
        sigma_1 = avg_normal_stress + radius
        sigma_2 = avg_normal_stress - radius

        # Calculate Tresca equivalent stress
        tresca_equivalent_stress = max(abs(sigma_1 - sigma_2), abs(sigma_1), abs(sigma_2))
        tresca_stresses.append(tresca_equivalent_stress)

    # Plot Tresca equivalent stress as a function of sigma_p
    plt.plot(sigma_p_values, tresca_stresses, label="Tresca Equivalent Stress")
    plt.xlabel(r"Additional applied stress (MPa)")
    plt.ylabel(r"Tresca Equivalent Stress (MPa)")
    plt.title("Tresca Equivalent Stress as a Function of Applied Stress")
    plt.axhline(y=400, color='k', linestyle='--', label="Yield Stress")
    plt.legend()
    plt.grid(True)
    plt.show()



# Example usage of the function
plot_tresca_equivalent_stress(sigma_x=-50, sigma_y=108, theta_deg=30, sigma_p_max=400, num_points=1000)
