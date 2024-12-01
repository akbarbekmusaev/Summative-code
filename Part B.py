import numpy as np
import sympy as sp

# Material and geometry properties
E = 200e9  # Young's modulus in Pascals
nu = 0.28  # Poisson's ratio
t = 1 # Thickness in meters
coords = np.array([[0.29, 0.16], [0.43, 0.26], [0.32, 0.33]])  # Coordinates of triangle nodes (x1, y1), (x2, y2), (x3, y3)
forces = np.array([[540000], [432000], [0], [0], [0], [0]])  # Applied nodal forces (F1x, F1y, F2x, F2y, F3x, F3y)
U2x, U2y, U3x, U3y = 0, 0, 0, 0  # Displacement boundary conditions (U2x, U2y, U3x, U3y)

# Analysis type: 'plane_stress' or 'plane_strain'
analysis_type = 'plane_strain'  # Change this to 'plane_strain' for pla1ne strain analysis

# Step 1: Extract node coordinates
x1, y1 = coords[0]
x2, y2 = coords[1]
x3, y3 = coords[2]

# Step 2: Calculate the area of the triangle using the determinant formula
A = 0.5 * np.abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
#print("Area of the triangle, A:", A)

# Step 3: Define ai, bi, and ci terms for the shape functions
# ai terms (constant terms in shape functions)
a1 = x2 * y3 - x3 * y2
a2 = x3 * y1 - x1 * y3
a3 = x1 * y2 - x2 * y1
#print("Shape function constants (a1, a2, a3):", a1, a2, a3)

# Derivatives of N_i (shape functions) with respect to x and y
# bi and ci terms represent coefficients for x and y in the differentiation of shape functions
b1 = y2 - y3
b2 = y3 - y1
b3 = y1 - y2
c1 = x3 - x2
c2 = x1 - x3
c3 = x2 - x1
print("Shape function x-derivative coefficients (a1, a2, a3):", a1, a2, a3)
print("Shape function x-derivative coefficients (b1, b2, b3):", b1, b2, b3)
print("Shape function y-derivative coefficients (c1, c2, c3):", c1, c2, c3)

# Step 4: Formulate the strain-displacement matrix B using bi and ci terms
B = (1 / (2 * A)) * np.array([
    [b1, 0, b2, 0, b3, 0],
    [0, c1, 0, c2, 0, c3],
    [c1, b1, c2, b2, c3, b3]
])

# Step 5: Define the constitutive matrix D based on the analysis type
if analysis_type == 'plane_stress':
    # For plane stress
    D = (E / (1 - nu**2)) * np.array([
        [1,     nu,  0],
        [nu,    1,   0],
        [0,     0,   (1 - nu) / 2]
    ])
elif analysis_type == 'plane_strain':
    # For plane strain
    D = (E / ((1 + nu) * (1 - 2 * nu))) * np.array([
        [1 - nu,     nu,         0],
        [nu,         1 - nu,     0],
        [0,          0,     (1 - 2 * nu) / 2]
    ])
else:
    raise ValueError("Invalid analysis type. Choose 'plane_stress' or 'plane_strain'.")
print("Constitutive matrix, D:\n", D)

# Step 6: Compute the stiffness matrix K using K = t * A * B.T * D * B
#print("t * A", t * A)
#print("B.T", B.T*2*A)
#print("D", D/(E / ((1 + nu) * (1 - 2 * nu))))
#print("B.T @ D", (B.T@D)/(17072770980000))
KG = t * A * B.T @ D @ B
print("Global stiffness matrix, KG:\n", KG)

# # Step 7: Apply the boundary conditions to the global stiffness matrix
# # node 2 and 3 are fixed
# bc_indices = [2, 3, 4, 5]  # Indices of the fixed displacements
# K1 = KG.copy()
# K1 = np.delete(K1, bc_indices, axis=0)  # Remove rows
# K1 = np.delete(K1, bc_indices, axis=1)  # Remove columns
#
# # Step 8: Solve for the nodal displacements using the equation K * U = F
# F = forces[forces != 0]  # Extract the non-zero forces
# U = np.linalg.solve(K1, F)  # Solve for the nodal displacements
# print("Stiffness matrix, K1:\n", K1)
# print("Forces", F)
# print("Nodal displacements, U:\n", U)

# # step 8 alternative
# penalty_value = 1e30  # A very large number to "fix" the displacement
# for index in bc_indices:
#     KG[index, index] = penalty_value
# print("Stiffness matrix, KG:\n", KG)
# print("Forces", forces)
# print("Nodal displacements, U:\n", np.linalg.solve(KG, forces))

# #Step 9: build the global displacement vector
# U_global = np.array([[U[0]], [U[1]], [U2x], [U2y], [U3x], [U3y]])
# print("Global displacement vector, U_global:\n", U_global)
#
# #Step 10: Calculate the reaction forces
# F_react = KG @ U_global
# print("Reaction force F1x, F1y, F2x, F2y, F3x, F3y:\n", F_react)
#
# #Check the resultant forces
# F_res = np.sum(F_react)
# print("Resultant force:", F_res)

