import matplotlib.pyplot as plt
import numpy as np

# Data extracted
size = [0.011, 0.01, 0.009, 0.008, 0.007, 0.006, 0.005, 0.004, 0.0035, 0.003, 0.0025, 0.002, 0.0017, 0.0015, 0.0012, 0.001]
Hex_elements = [654, 681, 951, 1500, 1864, 3015, 4980, 11096, 16452, 24310, 43968, 84360, 138852, 200380, 392125, 685150]
Hex_lin = [0.0001676, 0.0001678, 0.0001695, 0.0001703, 0.000171, 0.0001733, 0.0001739, 0.0001756, 0.0001763, 0.0001769, 0.0001773, 0.0001777, 0.0001779, 0.0001781, 0.0001782, 0.0001783]
Hex_quad = [0.0001777, 0.0001778, 0.0001779, 0.000178, 0.0001781, 0.0001782, 0.0001783, 0.0001784, 0.0001784, 0.0001784, 0.0001784, 0.0001784, 0.0001784, 0.0001784, 0.0001784, 0.0001784]
Tet_elements = [ 4013, 4638, 6668, 9134, 13118, 18287, 29649, 59971, 81960, 124270, 201341, 359626, 550036, 743740, 1275036, 1947767]
Tet_lin = [0.00016, 0.0001593, 0.0001627, 0.0001648, 0.0001661, 0.000169, 0.0001709, 0.0001736, 0.0001745, 0.0001755, 0.0001762, 0.000177, 0.0001773, 0.0001779, 0.0001779, 0.000178]
Tet_quad = [0.0001777, 0.0001778, 0.0001779, 0.000178, 0.0001781, 0.0001782, 0.0001783, 0.0001784, 0.0001784, 0.0001785, 0.0001785, 0.0001785, 0.0001785, 0.0001785, 0.0001785, 0.0001785]
Wedge_elements = [ 654, 681, 951, 1500, 1864, 3015, 4980, 11096, 16452, 24310, 43968, 84360, 138852, 200380, 392125, 685150]
Wedge_lin =  [0.0001606, 0.0001604, 0.0001637, 0.0001655, 0.0001672, 0.0001697, 0.0001714, 0.0001739, 0.0001748, 0.0001758, 0.0001765, 0.0001772, 0.0001775, 0.0001778, 0.000178, 0.0001782]
Wedge_quad = [ 0.0001778, 0.0001778, 0.0001779, 0.000178, 0.0001781, 0.0001782, 0.0001783, 0.0001784, 0.0001784, 0.0001784, 0.0001784, 0.0001784, 0.0001784, 0.0001784, 0.0001784, 0.0001784]
hex_quad_pin_logN = [3.051538391, 3.24723655, 3.289365952, 3.329601248, 3.381295623, 3.559667278, 3.653598382, 3.779235632, 3.996949248]
hex_quad_pin_disp = [0.0001707, 0.0001709, 0.000171, 0.000171, 0.0001712, 0.0001712, 0.0001713, 0.0001713, 0.0001714]

# Plotting the first set of values
plt.rcParams.update({'font.size': 14})
hex_quad_pin_disp_mm = [disp * 1000 for disp in hex_quad_pin_disp]
coefficients = np.polyfit(hex_quad_pin_logN, hex_quad_pin_disp_mm, 3)
polynomial = np.poly1d(coefficients)
x_fit = np.linspace(min(hex_quad_pin_logN), max(hex_quad_pin_logN), 100)
y_fit = polynomial(x_fit)
plt.figure(figsize=(9, 9))
plt.plot(hex_quad_pin_logN, hex_quad_pin_disp_mm, label='First Set', marker='o')
plt.plot(x_fit, y_fit, label='Best Fit', linestyle='--')
plt.xlabel('Log_10(N)')
plt.ylabel('Displacement (mm)')
plt.xlim(3.0, 4.0)
plt.ylim(0.1705, 0.1715)
plt.legend()
plt.grid(True)
#plt.show()


# Set global font size
plt.rcParams.update({'font.size': 14})

# Plotting Max Displacement for C3D8 and C3D20
plt.figure(figsize=(9, 9))
plt.plot([np.log10(num) for num in Hex_elements], [disp * 1000 for disp in Hex_lin], label='Hex Linear (C3D8R)', marker='s')
plt.plot([np.log10(num) for num in Hex_elements], [disp * 1000 for disp in Hex_quad], label='Hex Quadratic (C3D20R)', marker='s')
plt.plot([np.log10(num) for num in Tet_elements], [disp * 1000 for disp in Tet_lin], label='Tet Linear (C3D4R)', marker='^')
plt.plot([np.log10(num) for num in Tet_elements], [disp * 1000 for disp in Tet_quad], label='Tet Quadratic (C3D10R)', marker='^')
plt.plot([np.log10(num) for num in Wedge_elements], [disp * 1000 for disp in Wedge_lin], label='Wedge Linear (C3D6R)', marker='o')
plt.plot([np.log10(num) for num in Wedge_elements], [disp * 1000 for disp in Wedge_quad], label='Wedge Quadratic (C3D15R)', marker='o')
plt.axhline(y=0.185, color='red', linestyle='--', label='Analytical solution')
plt.xlabel('Log_10(N)')
plt.ylabel('Displacement (mm)')
plt.legend()
plt.grid(True)
plt.show()
