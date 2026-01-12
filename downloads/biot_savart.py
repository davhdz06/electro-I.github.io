from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D, art3d
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np

# Constantes
I = 1.0  # Corriente cte
mu0 = 4 * np.pi * 1e-7  # Permeabilidad
nano = 1e6  # Constante para normalizar (for μT)

# Crear gráfico
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Ley de Biot-Savart", pad=20, fontsize=14)

# Parámetros del cable de corriente
wire_length = 10
num_segments = 100
dz = wire_length / num_segments

# Dibujarlo
wire_z = np.linspace(-wire_length/2, wire_length/2, num_segments)
wire_x = np.zeros_like(wire_z)
wire_y = np.zeros_like(wire_z)

ax.plot(wire_x, wire_y, wire_z, 'b-', linewidth=3, label='Current-carrying wire')

# Dirección de la corriente
ax.quiver(0, 0, wire_length/2-1, 0, 0, 2, color='blue',
          arrow_length_ratio=0.2, linewidth=2)
ax.text(0, 0, wire_length/2 + 1.5, "I", color='blue', fontsize=14)

# Puntos en cilíndricas alrededor del bucle para dibujar el campo
theta = np.linspace(0, 2*np.pi, 20)
r = np.linspace(0.5, 3, 3)
obs_z = np.linspace(-wire_length/3, wire_length/3, 5)

R, Theta, Z = np.meshgrid(r, theta, obs_z)
obs_x = R * np.cos(Theta)
obs_y = R * np.sin(Theta)
obs_z = Z

# Marcar estos puntos en el gráfico
obs_points = np.vstack([obs_x.ravel(), obs_y.ravel(), obs_z.ravel()]).T

# Parámetros de la aguja
needle_pos = np.array([2.5, 2.5, 0])  # Posición
needle_length = 1.5

# Calcular el campo magnético en cada punto que marcamos
def calculate_B(point, max_segment=None):
    if max_segment is None:
        max_segment = num_segments

    B_total = np.zeros(3)
    for j in range(max_segment):
        segment = np.array([wire_x[j], wire_y[j], wire_z[j]])
        dl = np.array([0, 0, dz])  # Elemento diferencial de corriente

        r_vec = point - segment
        r_mag = np.linalg.norm(r_vec)

        if r_mag < 1e-6:  # Evitar división por 0
            continue

        dB = (mu0 * I / (4 * np.pi)) * np.cross(dl, r_vec) / (r_mag**3)
        B_total += dB

    # Normalizar y usar escala Log
    B_mag = np.linalg.norm(B_total)
    if B_mag > 0:
        B_total = (B_total / nano) * np.log1p(B_mag/nano)
    return B_total

# Calcular campo inicial
B_fields = np.array([calculate_B(p) for p in obs_points])
B_needle = calculate_B(needle_pos)

# Dibujar las líneas de campo
quiv = ax.quiver(obs_points[:,0], obs_points[:,1], obs_points[:,2],
                 B_fields[:,0], B_fields[:,1], B_fields[:,2],
                 length=0.5, normalize=True, color='r', alpha=0.6)

# Orientación de la brújula
if np.linalg.norm(B_needle) > 0:
    B_dir = B_needle/np.linalg.norm(B_needle)
else:
    B_dir = np.array([1, 0, 0])  # Dirección si no hubiera campo

needle_north = needle_pos + needle_length/2 * B_dir
needle_south = needle_pos - needle_length/2 * B_dir

# Dibujar la aguja
#needle_line = ax.quiver(needle_south[0], needle_south[1], needle_south[2],
 #                      B_dir[0], B_dir[1], B_dir[2],
   #                    length=needle_length, arrow_length_ratio=0.3,
    #                   color='g', linewidth=4, label='Magnetic needle')

# Crear base de la brújula
#theta = np.linspace(0, 2*np.pi, 100)
#compass_radius = 0.8
#x_circle = needle_pos[0] + compass_radius * np.cos(theta)
#y_circle = needle_pos[1] + compass_radius * np.sin(theta)
#z_circle = needle_pos[2] * np.ones_like(theta)
#ax.plot(x_circle, y_circle, z_circle, 'k-', linewidth=2, alpha=0.7)

# Formato
ax.set_box_aspect([1, 1, 1])
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-wire_length/2, wire_length/2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend(loc='upper right')

# Añadir leyenda explicativa
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='blue', lw=3, label='Cable conductor (corriente I)'),
    Line2D([0], [0], marker='>', color='blue', lw=0, label='Dirección de la corriente', markersize=10),
    Line2D([0], [0], color='red', lw=2, label='Campo magnético (B)', markersize=10)
]

ax.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
from pathlib import Path
Path("assets/sims/biot-savart").mkdir(parents=True, exist_ok=True)
plt.savefig("assets/sims/biot-savart/bio-savart.png", dpi=200, bbox_inches="tight")
plt.close()
