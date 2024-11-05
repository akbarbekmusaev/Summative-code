import numpy as np

# Constants
E = 70e9  # Elastic modulus in Pascals (Pa)
nu = 0.3  # Poisson's ratio
shearM = E / (2 * (1 + nu))  # Shear modulus in Pa
LameC = E * nu / ((1 + nu) * (1 - 2 * nu))  # Lame's first parameter in Pa

# Given strains and angles
epsilon_1, theta_1 = -0.001177142857142857, np.radians(0)  # Strain from gauge 1
epsilon_2, theta_2 = 0.0017571428571428573, np.radians(90)  # Strain from gauge 2

# Set up the transformation matrix
A = np.array([
[np.cos(theta_1) ** 2, np.sin(theta_1) ** 2],
[np.cos(theta_2) ** 2, np.sin(theta_2) ** 2]])

# Right-hand side vector with measured strains
b = np.array([epsilon_1, epsilon_2])

# Solve for epsilon_x and epsilon_y
epsilon_x_y = np.linalg.solve(A, b)
epsilon_x = epsilon_x_y[0]
epsilon_y = epsilon_x_y[1]
epsilon_z = - LameC/(LameC + 2 * shearM) * (epsilon_x + epsilon_y)

# Calculate stresses from strains using generalized Hooke's law for plain stress
sigma_x = (LameC + 2 * shearM) * epsilon_x + LameC * (epsilon_y+epsilon_z)
sigma_y = (LameC + 2 * shearM) * epsilon_y + LameC * (epsilon_x+epsilon_z)

print(f"Sigma_x: {sigma_x:.2f} Pa")
print(f"Epsilon_x: {epsilon_x:.6f}")
print(f"Sigma_y: {sigma_y:.2f} Pa")
print(f"Epsilon_y: {epsilon_y:.6f}")
print(f"Epsilon_z: {epsilon_z:.6f}")
