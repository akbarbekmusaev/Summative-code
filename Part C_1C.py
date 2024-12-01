import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

#equivalent stress total
def plot_tresca_equivalent_stress(sigma_x, sigma_y, theta_deg, sigma_p_max, num_points=100):
    # Convert angle to radians
    theta = theta_deg * (np.pi / 180)

    # Compute cosine and sine of theta
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    # Range of sigma_p values
    sigma_p_values = np.linspace(-sigma_p_max, sigma_p_max, num_points)

    # Arrays to store stress results
    tresca_stresses = []
    Von_Mises_stresses = []

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

        # Calculate Von Mises equivalent stress
        von_mises_equivalent_stress = np.sqrt(sigma_1**2 - sigma_1 * sigma_2 + sigma_2**2)
        Von_Mises_stresses.append(von_mises_equivalent_stress)


    # Plot Tresca equivalent stress as a function of sigma_p
    plt.plot(sigma_p_values, tresca_stresses, label="Tresca Equivalent Stress")
    plt.plot(sigma_p_values, Von_Mises_stresses, label="Von Mises Equivalent Stress")
    plt.xlabel(r"Additional applied stress (MPa)")
    plt.ylabel(r"Resultant stress (MPa)")
    plt.title("Tresca Equivalent Stress as a Function of Applied Stress")
    plt.axhline(y=400, color='k', linestyle='--', label="Yield Stress")
    plt.legend()
    plt.show()

#crack stress tensor
def calculate_matrix_B(sigma_p):
    R = np.array([[np.cos(-np.pi/6), np.sin(-np.pi/6)],
                  [-np.sin(-np.pi/6), np.cos(-np.pi/6)]])

    # Define the matrix B with terms involving sigma_p
    A = np.array([[sigma_p, 0],
                  [0, 0]])

    # Perform the matrix multiplication D = R * B * R^T
    D = np.dot(R, np.dot(A, R.T))

    return D
def calculate_matrix_D(theta_c, sigma_p):
    # Define the rotation matrices A and C
    R = np.array([[np.cos(theta_c), np.sin(theta_c)],
                  [-np.sin(theta_c), np.cos(theta_c)]])

    # Perform the matrix multiplication D = R * B * R^T
    D = np.dot(R, np.dot(calculate_matrix_B(sigma_p), R.T))

    return D

#stress intensity factor
def stress_intensity_factor(D):
    # Third element expression for opening stress
    sigma_crack = D[1,1]
    # Crack size
    a = 0.005 #m
    # Calculate K
    K = sigma_crack * np.sqrt(np.pi * a)
    return K

def calculate_lefm_limit():

    a = (4 / np.pi) * (stress_intensity_factor(D) / sigma_y) ** 2