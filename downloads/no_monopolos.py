import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LogNorm
from matplotlib.patches import Circle, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D, proj3d


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return min(zs)


# Constantes
mu0 = 4 * np.pi * 1e-7  # Permeabilidad
I = 1.0  # Corriente del bucle (A)
R = 0.1  # Radio del bucle MUY PEQUEÑO (m)
nano = 1e6  # Constante para normalizar (for μT)


def campo_bucle(x, y, z):
    """Calcular campo B para un bucle circular de corriente en el plano XY
    con expansión multipolar hasta octupolo.
    """
    Bx, By, Bz = np.zeros_like(x), np.zeros_like(y), np.zeros_like(z)

    r = np.sqrt(x**2 + y**2 + z**2)
    rho = np.sqrt(x**2 + y**2)
    theta = np.arctan2(rho, z)
    phi = np.arctan2(y, x)

    # Constantes multipolares
    m = I * np.pi * R**2  # Momento dipolar (A·m²)
    Q = I * np.pi * R**4 / 4  # Momento cuadrupolar (A·m³)
    O = I * np.pi * R**6 / 8  # Momento octupolar (A·m⁴)

    prefactor_dip = (mu0 * m) / (4 * np.pi) * nano  # Prefactor dipolar (μT)
    prefactor_quad = (mu0 * Q) / (4 * np.pi) * nano  # Prefactor cuadrupolar (μT·m⁻¹)
    prefactor_oct = (mu0 * O) / (4 * np.pi) * nano  # Prefactor octupolar (μT·m⁻²)

    # Evitar la división por cero
    r_safe = np.where(r > 0, r, 1e-10)

    # === Dipolo (l=1) ===
    Bx_dip = prefactor_dip * 3 * x * z / (r_safe**5)
    By_dip = prefactor_dip * 3 * y * z / (r_safe**5)
    Bz_dip = prefactor_dip * (3 * z**2 - r_safe**2) / (r_safe**5)

    # === Cuadrupolo (l=2) === (simetría axial)
    Bx_quad = prefactor_quad * (15 * x * z**2 - 3 * x * r_safe**2) / (r_safe**7)
    By_quad = prefactor_quad * (15 * y * z**2 - 3 * y * r_safe**2) / (r_safe**7)
    Bz_quad = prefactor_quad * (15 * z**3 - 9 * z * r_safe**2) / (r_safe**7)

    # === Octupolo (l=3) === (simetría axial)
    Bx_oct = prefactor_oct * (105 * x * z**3 - 45 * x * z * r_safe**2) / (r_safe**9)
    By_oct = prefactor_oct * (105 * y * z**3 - 45 * y * z * r_safe**2) / (r_safe**9)
    Bz_oct = prefactor_oct * (105 * z**4 - 90 * z**2 * r_safe**2 + 9 * r_safe**4) / (r_safe**9)

    # Campo total (por ahora solo dipolo)
    Bx = Bx_dip  # + Bx_quad + Bx_oct
    By = By_dip  # + By_quad + By_oct
    Bz = Bz_dip  # + Bz_quad + Bz_oct

    # Magnitud de B
    B_mag = np.sqrt(Bx**2 + By**2 + Bz**2)

    # Normalizar vectores
    norm_vec = np.sqrt(Bx**2 + By**2 + Bz**2 + 1e-10)
    return Bx / norm_vec, By / norm_vec, Bz / norm_vec, B_mag


def campo_bucle2(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    m = I * np.pi * R**2
    prefactor = (mu0 * m) / (4 * np.pi) * nano

    Bx = prefactor * 3 * x * z / (r**5 + 1e-10)
    By = prefactor * 3 * y * z / (r**5 + 1e-10)
    Bz = prefactor * (3 * z**2 - r**2) / (r**5 + 1e-10)

    B_mag = np.sqrt(Bx**2 + By**2 + Bz**2)
    return Bx, By, Bz, B_mag


# Crear figura principal con diseño modificado para una sola barra de color
fig = plt.figure(figsize=(16, 8))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 0.05])

# =============================================
# GRAFICO IZQUIERDO: Líneas de campo 3D
# =============================================
ax1 = fig.add_subplot(gs[0], projection="3d")
ax1.set_title(
    f"Campo magnético de un bucle (en escala Log μT)\nI = {I} A, R = {R} m",
    pad=20,
)

# Graficar el bucle MUY PEQUEÑO (casi puntual)
theta = np.linspace(0, 2 * np.pi, 100)
ax1.plot(
    R * np.cos(theta),
    R * np.sin(theta),
    np.zeros(100),
    "r-",
    lw=2,
    label="Bucle de corriente",
)

# Parámetros para las líneas de campo
n_lines = 12
max_length = 25
step_size = 0.1
arrow_spacing = 6

# Obtener las magnitudes del campo antes de escalar
all_B_mags = []
phi = np.linspace(0, 2 * np.pi, n_lines, endpoint=False)
seeds = np.array(
    [1.2 * R * np.cos(phi), 1.2 * R * np.sin(phi), 0.15 * np.ones(n_lines)]
).T

# Pre-cálculo para encontrar el rango de datos
for seed in seeds:
    pos = seed.copy()
    for _ in range(max_length):
        _, _, _, B_mag = campo_bucle2(pos[0], pos[1], pos[2])
        all_B_mags.append(B_mag)

        direction = np.array(campo_bucle2(pos[0], pos[1], pos[2])[:3])
        direction = direction / (np.linalg.norm(direction) + 1e-10)
        pos = pos + step_size * direction

# Visualización logarítmica con límites ajustados al valor máximo real
valid_B = np.array(all_B_mags)
valid_B = valid_B[valid_B > 0]  # Solo valores positivos

# AJUSTE CLAVE: Fijar el máximo en ~13 μT para que coincida con el campo cercano
vmin_adjusted = max(valid_B.min() * 0.8, 0.05)
vmax_adjusted = 13.0

# Colormap y normalización
cmap = plt.get_cmap("gist_ncar")
norm = LogNorm(vmin=vmin_adjusted, vmax=vmax_adjusted)

# Gráfico principal
for seed in seeds:
    trajectory = []
    B_mags = []

    # Integración hacia adelante
    pos = seed.copy()
    for _ in range(max_length):
        Bx, By, Bz, B_mag = campo_bucle2(pos[0], pos[1], pos[2])
        trajectory.append(pos.copy())
        B_mags.append(B_mag)

        direction = np.array([Bx, By, Bz])
        direction = direction / (np.linalg.norm(direction) + 1e-10)
        pos = pos + step_size * direction

    # Integración hacia atrás
    pos = seed.copy()
    for _ in range(max_length):
        Bx, By, Bz, B_mag = campo_bucle2(pos[0], pos[1], pos[2])
        trajectory.insert(0, pos.copy())
        B_mags.insert(0, B_mag)

        direction = np.array([Bx, By, Bz])
        direction = direction / (np.linalg.norm(direction) + 1e-10)
        pos = pos - step_size * direction

    trajectory = np.array(trajectory)
    B_mags = np.array(B_mags)

    # Graficar las líneas de campo
    for i in range(len(trajectory) - 1):
        color_val = norm(min(B_mags[i], vmax_adjusted))
        ax1.plot(
            trajectory[i : i + 2, 0],
            trajectory[i : i + 2, 1],
            trajectory[i : i + 2, 2],
            color=cmap(color_val),
            lw=1.5,
            alpha=0.8,
        )

    # Flechas para indicar la dirección
    for i in range(0, len(trajectory) - 1, arrow_spacing):
        if i + 1 < len(trajectory):
            start = trajectory[i]
            end = trajectory[i + 1]
            color_val = norm(min(B_mags[i], vmax_adjusted))

            arrow = Arrow3D(
                [start[0], end[0]],
                [start[1], end[1]],
                [start[2], end[2]],
                mutation_scale=10,
                lw=1,
                arrowstyle="-|>",
                color=cmap(color_val),
                alpha=0.8,
            )
            ax1.add_artist(arrow)

# Formato
ax1.set_xlim(-0.8, 0.8)
ax1.set_ylim(-0.8, 0.8)
ax1.set_zlim(-0.8, 0.8)
ax1.set_xlabel("X (m)")
ax1.set_ylabel("Y (m)")
ax1.set_zlabel("Z (m)")
ax1.view_init(elev=30, azim=45)
ax1.legend()
ax1.grid(True, alpha=0.2)

# =============================================
# GRAFICO DERECHO: Sección 2D del plano XZ
# =============================================
ax2 = fig.add_subplot(gs[1])
ax2.set_title("Sección del plano XZ (∇·B = 0)\nMagnitud del campo en escala Log", pad=20)

# Mallado para gráfico 2D
x2d = np.linspace(-1.5, 1.5, 30)
z2d = np.linspace(-1.5, 1.5, 30)
X2d, Z2d = np.meshgrid(x2d, z2d)
Y2d = np.zeros_like(X2d)

Bx2d, By2d, Bz2d, B_mag2d = campo_bucle(X2d, Y2d, Z2d)

# Clip para consistencia de escala
B_mag2d_clipped = np.clip(B_mag2d, vmin_adjusted, vmax_adjusted)

# Líneas de campo con mapa de color
ax2.streamplot(
    X2d,
    Z2d,
    Bx2d,
    Bz2d,
    color=B_mag2d_clipped,
    cmap=cmap,
    norm=norm,
    density=2,
    linewidth=1.5,
    arrowsize=1.2,
)

# Sección del bucle
circle = Circle((0, 0), R, color="red", fill=False, lw=2)
ax2.add_patch(circle)

# Texto sobre monopolos
max_field = B_mag2d.max()
min_field = max(B_mag2d[B_mag2d > 0].min(), 0.1)  # evitar log(0)
ax2.text(
    1.5,
    1.8,
    (
        f"La magnitud del campo es de\n{max_field:.1f} μT cerca del bucle\n"
        f"y {min_field:.3f} μT en campo lejano.\n"
        "∇·B = 0 ya que las líneas de campo \n"
        "se cierran en sí mismas (indica que \n"
        "no hay monopolos)"
    ),
    bbox=dict(facecolor="white", alpha=0.9, pad=10),
)

ax2.set_xlabel("X (m)")
ax2.set_ylabel("Z (m)")
ax2.set_xlim(-1.5, 1.5)
ax2.set_ylim(-1.5, 1.5)
ax2.set_aspect("equal")
ax2.grid(True, alpha=0.2)

# =============================================
# BARRA DE COLOR ÚNICA (compartida)
# =============================================
ax_cb = fig.add_subplot(gs[2])
sm = ScalarMappable(norm=norm, cmap=cmap)
cbar = fig.colorbar(sm, cax=ax_cb)
cbar.set_label("Magnitud del campo (μT, escala log)", rotation=270, labelpad=20)

# Rango ajustado
cbar.ax.text(
    0.5,
    -0.01,
    f"Min: {vmin_adjusted:.3f} μT",
    transform=cbar.ax.transAxes,
    ha="center",
    va="top",
    fontsize=8,
)
cbar.ax.text(
    0.5,
    1.01,
    f"Max: {vmax_adjusted:.1f} μT",
    transform=cbar.ax.transAxes,
    ha="center",
    va="bottom",
    fontsize=8,
)

# Marcas específicas
cbar.ax.axhline(y=norm(1.0), color="white", linestyle="--", alpha=0.5, linewidth=0.5)
cbar.ax.axhline(y=norm(5.0), color="white", linestyle="--", alpha=0.5, linewidth=0.5)
cbar.ax.axhline(y=norm(10.0), color="white", linestyle="--", alpha=0.5, linewidth=0.5)

plt.tight_layout()
from pathlib import Path
Path("assets/sims/no-monopolos").mkdir(parents=True, exist_ok=True)
plt.savefig("assets/sims/no-monopolos/no-monopolos.png", dpi=200, bbox_inches="tight")
plt.close()

